"""Immutable registered bytes. Caller strings are NEVER interpreted as paths."""
import base64
from copy import deepcopy
from collections import OrderedDict
import hashlib
import re
import threading
import uuid

from .profiles import _fields


class ResourceStore:
    def __init__(self, *, max_resource_bytes=2*1024*1024, max_total_bytes=64*1024*1024):
        if not 0 < max_resource_bytes <= 2*1024*1024 or max_total_bytes < max_resource_bytes:
            raise ValueError('Invalid resource budget')
        self.max_resource_bytes = max_resource_bytes
        self.max_total_bytes = max_total_bytes
        self._resources = {}
        self._size = 0
        self._lock = threading.RLock()
        self._captures = OrderedDict()

    def register(self, data, *, modality, profiles, capture_step, metadata=None, resource_id=None):
        resource_id = resource_id or uuid.uuid4().hex
        if (not isinstance(data, bytes) or len(data) > self.max_resource_bytes
                or modality not in ('rgb', 'depth', 'validity') or type(capture_step) is not int or capture_step < 0
                or not isinstance(resource_id, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,128}', resource_id)):
            raise ValueError('Invalid resource')
        profiles = tuple(profiles)
        if not profiles or any(p not in ('rgb', 'rgbd', 'privileged') for p in profiles):
            raise ValueError('Invalid profiles')
        if modality in ('depth', 'validity') and 'rgb' in profiles:
            raise ValueError('RGB profile cannot access depth')
        public = _fields(metadata, ('width','height'), ('content_type', 'units', 'encoding'))
        public.update(resource_id=resource_id, modality=modality, capture_step=capture_step,
                      byte_length=len(data), sha256=hashlib.sha256(data).hexdigest())
        with self._lock:
            if resource_id in self._resources:
                raise ValueError('Resource IDs are immutable')
            if self._size + len(data) > self.max_total_bytes:
                raise ValueError('Resource budget exceeded')
            self._resources[resource_id] = (data, profiles, public)
            self._size += len(data)
        return resource_id

    def get(self, resource_id, profile):
        with self._lock:
            entry = self._resources.get(resource_id) if isinstance(resource_id, str) else None
            if entry is None or profile not in entry[1] or entry[2]['modality'] in ('depth','validity') and profile == 'rgb':
                raise KeyError('Resource unavailable')
            data, _, metadata = entry
            return {**metadata, 'data_base64': base64.b64encode(data).decode('ascii')}

    def discard(self, resource_id):
        """Trusted producer may expire an old standalone frame; clients cannot."""
        with self._lock:
            if any(resource_id in row.values() for row in self._captures.values()):
                raise ValueError('Expire managed captures as a group')
            old = self._resources.pop(resource_id, None)
            if old is not None: self._size -= len(old[0])

    def register_capture(self, *, camera_id, capture_step, rgb, depth, validity, calibration):
        """Atomically retain the latest eight immutable view captures (~20 MiB).

        Older IDs expire together; IDs are never reassigned. The trusted tool
        registry resolves capture_id, never caller-supplied calibration or IDs.
        """
        if type(capture_step) is not int or capture_step<0 or not all(isinstance(v,bytes) for v in (rgb,depth,validity)):
            raise ValueError('Invalid capture')
        if camera_id not in ('front_left','front_right','top','scene'):
            raise ValueError('Unknown camera')
        if (len(rgb),len(depth),len(validity)) != (640*480*3,640*480*4,640*480):
            raise ValueError('Invalid capture dimensions')
        from .profiles import CALIBRATION, numeric
        if not isinstance(calibration,dict) or any(k not in CALIBRATION+('convention',) for k in calibration):
            raise ValueError('Invalid calibration')
        if not all(numeric(v) if k != 'convention' else isinstance(v,str) for k,v in calibration.items()):
            raise ValueError('Invalid calibration')
        if (set(calibration) != {'intrinsics','world_from_camera','convention','near_m','far_m','pixel_center_offset'}
                or calibration['convention'] != 'opencv_x_right_y_down_z_forward'
                or not 0 < calibration['near_m'] < calibration['far_m']
                or not isinstance(calibration['pixel_center_offset'],(list,tuple)) or len(calibration['pixel_center_offset'])!=2
                or len(calibration['intrinsics'])!=3 or any(len(r)!=3 for r in calibration['intrinsics'])
                or len(calibration['world_from_camera'])!=4 or any(len(r)!=4 for r in calibration['world_from_camera'])):
            raise ValueError('Invalid calibration')
        total = len(rgb)+len(depth)+len(validity)
        if total > self.max_total_bytes or max(map(len,(rgb,depth,validity)))>self.max_resource_bytes:
            raise ValueError('Capture exceeds resource budget')
        with self._lock:
            while self._captures and (len(self._captures)>=8 or self._size+total>self.max_total_bytes):
                _, old = self._captures.popitem(last=False)
                for key in ('rgb_resource_id','depth_resource_id','validity_resource_id'):
                    data, _, _ = self._resources.pop(old[key])
                    self._size -= len(data)
            if self._size+total>self.max_total_bytes: raise ValueError('Resource budget exceeded')
            row = dict(capture_id=uuid.uuid4().hex,camera_id=camera_id,capture_step=capture_step,
                width=640,height=480,calibration=deepcopy(calibration),depth_units='m')
            for modality,data,encoding in (('rgb',rgb,'uint8_rgb_hwc'),('depth',depth,'float32_le_hw'),('validity',validity,'uint8_hw')):
                row[modality+'_resource_id'] = self.register(data,modality=modality,
                    profiles=('rgb','rgbd','privileged') if modality=='rgb' else ('rgbd','privileged'),
                    capture_step=capture_step,metadata=dict(width=640,height=480,encoding=encoding,
                    content_type='application/octet-stream',units='m' if modality=='depth' else ''))
            self._captures[row['capture_id']] = deepcopy(row)
            return row

    def resolve_capture(self, capture_id, profile):
        with self._lock:
            if profile not in ('rgb','rgbd','privileged') or capture_id not in self._captures:
                raise KeyError('Capture unavailable')
            row = deepcopy(self._captures[capture_id])
            if profile == 'rgb':
                for key in ('depth_resource_id','validity_resource_id','depth_units'): row.pop(key)
            return row
