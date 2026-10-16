"""Small rigid botanical proxies for the two protected plants, with convex leaf collisions."""
import os
import numpy as np,sapien,trimesh
from scipy.spatial.transform import Rotation
from .paths import CACHE_ROOT as ROOT

def add(e,b,vertices,name):
 if name not in ['seedling_pot','established_plant_pot']:return
 rim=np.concatenate(vertices)[:,2].max();scale=1.0 if name=='seedling_pot' else 1.5;items=[]
 stem=trimesh.creation.cylinder(radius=.0025*scale,height=.14*scale,sections=10);stem.apply_translation([0,0,rim+.065*scale]);items.append((stem,[.26,.34,.14]))
 for i in range(9):
  theta=i*2.399;leaf=trimesh.creation.icosphere(subdivisions=2);leaf.vertices*=np.array([.032,.012,.0035])*scale;R=Rotation.from_euler('xyz',[.05,-.45,theta]).as_matrix();leaf.vertices=leaf.vertices@R.T+np.array([np.cos(theta)*.027,np.sin(theta)*.027,.025+i*.012])*scale+[0,0,rim];items.append((leaf,[.16+(i%3)*.035,.36+(i%3)*.025,.13]))
 out=ROOT/'assets/foliage';out.mkdir(exist_ok=True,parents=True)
 for i,(mesh,color) in enumerate(items):
  path=out/f'{name}_{i}.obj'
  if not path.exists():
   tmp=out/f'{name}_{i}_{os.getpid()}.obj';mesh.export(tmp);os.replace(tmp,path)
  b.add_convex_collision_from_file(str(path),material=e.material,density=30)
  if e.scene.can_render():b.add_visual_from_file(str(path),material=sapien.render.RenderMaterial(base_color=[*color,1],roughness=.8))
  vertices.append(np.array(mesh.vertices))
