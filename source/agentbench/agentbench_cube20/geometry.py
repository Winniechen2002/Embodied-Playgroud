"""Independent integer-rotation oracle; no discrete move tables are used."""
import numpy as np
from .catalog import State, moves, rules

NORMALS = {'R': (1,0,0),'L':(-1,0,0),'F':(0,1,0),'B':(0,-1,0),'U':(0,0,1),'D':(0,0,-1)}
ORDER = ('URF','UFL','ULB','UBR','DFR','DLF','DBL','DRB')
CENTERS = np.array([sum((np.array(NORMALS[f]) for f in name), np.zeros(3,dtype=int)) for name in ORDER])

def configuration(sequence):
    positions = CENTERS.copy()
    rotations = np.tile(np.eye(3,dtype=int), (8,1,1))
    for face, count in sequence:
        axis = -np.array(NORMALS[face])
        cross = np.array([[0,-axis[2],axis[1]],[axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
        matrix = np.outer(axis,axis)+cross
        for _ in range(count % 4):
            selected = positions @ np.array(NORMALS[face]) > 0
            positions[selected] = positions[selected] @ matrix.T
            rotations[selected] = matrix @ rotations[selected]
    return positions, rotations

def decode(positions, rotations):
    permutation=[]; orientation=[]
    for index, center in enumerate(CENTERS):
        found=np.flatnonzero(np.all(positions == center,axis=1))
        if len(found)!=1: raise ValueError('Missing or overlapping cubie')
        cubie=int(found[0]); permutation.append(cubie)
        ud=rotations[cubie] @ np.array(NORMALS[ORDER[cubie][0]])
        orientation.append(next(i for i,f in enumerate(ORDER[index]) if np.array_equal(ud,NORMALS[f])))
    return State(tuple(permutation),tuple(orientation))

def quaternion(matrix):
    from scipy.spatial.transform import Rotation
    q=Rotation.from_matrix(matrix).as_quat()
    return tuple(float(v) for v in q[[3,0,1,2]])
