"""Original 10m prototype sloop. Run with Blender --background --python.
Exports one visual mesh and a separate deck-only UCX collision mesh.
"""
import bpy
import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'Assets' / 'Sloop'
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
verts, faces, indices = [], [], []
colors = [('Hull', (0.16, .065, .025, 1)), ('Deck', (.43, .23, .085, 1)),
          ('Trim', (.07, .17, .20, 1)), ('Canvas', (.82, .74, .48, 1)),
          ('Iron', (.045, .05, .055, 1)), ('Brass', (.62, .37, .07, 1))]

def part(v, f, mat):
    start = len(verts)
    verts.extend(v)
    faces.extend(tuple(start + i for i in face) for face in f)
    indices.extend([mat] * len(f))

def box(center, size, mat):
    x, y, z = center
    a, b, c = [s / 2 for s in size]
    v = [(x+dx*a, y+dy*b, z+dz*c) for dx,dy,dz in
         [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),
          (-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
    part(v, [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)], mat)

def beam(a, b, radius, mat, sides=8):
    from mathutils import Vector
    av, bv = Vector(a), Vector(b)
    direction = (bv-av).normalized()
    u = direction.cross(Vector((0,0,1)))
    if u.length < .01:
        u = direction.cross(Vector((0,1,0)))
    u.normalize()
    w = direction.cross(u).normalized()
    v = []
    for p in [av,bv]:
        for j in range(sides):
            t = j*math.tau/sides
            v.append(tuple(p + radius*(math.cos(t)*u+math.sin(t)*w)))
    f = [tuple(reversed(range(sides))),tuple(range(sides,2*sides))]
    f.extend((j,(j+1)%sides,(j+1)%sides+sides,j+sides) for j in range(sides))
    part(v,f,mat)

# Tapered, fully closed hull; pointed bow faces +X.
outline = [(-4.6,-1.45),(-2.6,-2),(.8,-2),(3.4,-1.3),(5,0),
           (3.4,1.3),(.8,2),(-2.6,2),(-4.6,1.45)]
N = len(outline)
v = [(x*.85,y*.45,-1.15) for x,y in outline] + [(x,y,1.6) for x,y in outline]
f = [tuple(reversed(range(N))),tuple(range(N,2*N))]
f.extend((j,(j+1)%N,(j+1)%N+N,j+N) for j in range(N))
part(v,f,0)
# Deck planking gives the silhouette readable wood bands.
for j in range(17):
    x = -4.35 + j*.5
    width = 3.7 if x<1 else max(.5,3.7-(x-1)*.8)
    box((x,0,1.64),(.47,width,.08),1)
for side in [-1,1]:
    for j in range(N-1):
        if outline[j][1]*side>0 and outline[j+1][1]*side>=0:
            x,y=outline[j]; xx,yy=outline[j+1]
            beam((x,y,1.9),(xx,yy,1.9),.10,2)
            beam((x,y,2.22),(xx,yy,2.22),.07,2)
            beam((x,y,1.65),(x,y,2.22),.06,0)
beam((-4.6,-1.45,1.9),(-4.6,1.45,1.9),.10,2)
box((-3.1,0,2.05),(2.4,2.6,.7),0)
box((-3.1,0,2.43),(2.6,2.8,.12),1)
beam((.15,0,1.65),(.15,0,8.7),.15,0)
beam((.15,-2.5,7.9),(.15,2.5,7.9),.10,0)
beam((.15,-2.25,4.45),(.15,2.25,4.45),.08,0)
# Curved square sail with thin thickness, both faces visible.
rows, cols = 5, 7
sv = []
for layer in [-.025,.025]:
    for r in range(rows):
        z=4.5+r*.83
        for c in range(cols):
            y=(c/(cols-1)-.5)*(4.4+r*.12)
            bulge=.60*math.sin(c/(cols-1)*math.pi)*math.sin((r+.5)/rows*math.pi)
            sv.append((.15+bulge+layer,y,z))
sf=[]
for l in range(2):
    for r in range(rows-1):
        for c in range(cols-1):
            p=l*rows*cols+r*cols+c
            q=(p,p+1,p+cols+1,p+cols)
            sf.append(q if l else tuple(reversed(q)))
part(sv,sf,3)
for x,y in [(-3.3,-1.6),(-3.3,1.6),(2.7,-1.5),(2.7,1.5)]:
    beam((x,y,1.8),(.15,0,8.2),.022,4,6)
beam((3.8,0,1.65),(6.3,0,2.4),.11,0)
# Helm and two deck cannons are visual placeholders.
beam((-3,0,2.4),(-3,0,3.25),.07,0)
for j in range(8):
    t=j*math.tau/8
    tt=(j+1)*math.tau/8
    beam((-3,0,3.3),(-3,.43*math.cos(t),3.3+.43*math.sin(t)),.025,5)
    beam((-3,.38*math.cos(t),3.3+.38*math.sin(t)),
         (-3,.38*math.cos(tt),3.3+.38*math.sin(tt)),.035,0)
for side in [-1,1]:
    box((-1,side*1.4,1.9),(1,.6,.45),0)
    beam((-1,side*.95,2.12),(-1,side*2.1,2.3),.16,4,12)

mesh=bpy.data.meshes.new('SM_FNSOT_Sloop')
mesh.from_pydata(verts,[],faces)
mesh.update()
obj=bpy.data.objects.new(mesh.name,mesh)
bpy.context.collection.objects.link(obj)
for name,color in colors:
    m=bpy.data.materials.new('M_FNSOT_'+name)
    m.diffuse_color=color
    m.use_nodes=True
    bsdf=m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value=color
    bsdf.inputs['Roughness'].default_value=.8
    obj.data.materials.append(m)
for p,i in zip(mesh.polygons,indices):
    p.material_index=i
bpy.context.view_layer.objects.active=obj
obj.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(island_margin=.02)
bpy.ops.object.mode_set(mode='OBJECT')
# Separate convex deck collision, so the sail/rigging don't become one blocking hull.
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,1.48))
collision=bpy.context.object
collision.name='UCX_SM_FNSOT_Sloop_00'
collision.dimensions=(8,3.4,.25)
bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
obj.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'FNSOT_Sloop.blend'))
bpy.ops.export_scene.fbx(filepath=str(OUT/'SM_FNSOT_Sloop.fbx'),use_selection=True,
                        global_scale=1,apply_unit_scale=False,
                        object_types={'MESH'},axis_forward='X',axis_up='Z',
                        bake_anim=False)
print('FNSOT_EXPORT_DONE',len(verts),len(faces))
