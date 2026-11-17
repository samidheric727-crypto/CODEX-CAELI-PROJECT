"""CODEX CAELI: real MPFB2-skinned Selena / 15 seconds.
No primitive figure substitutes. Requires original CC0 MakeHuman assets.
"""
import bpy, sys, os, math, importlib, random
from mathutils import Vector
random.seed(2008)
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,"output"); os.makedirs(OUT,exist_ok=True)
ASSETS=os.path.join(ROOT,"assets")
def svc(suffix,name):
    for item in list(sys.modules):
        if item.endswith(suffix):
            x=getattr(importlib.import_module(item),name,None)
            if x:return x
    raise RuntimeError("Missing MPFB service "+suffix)
try:
    bpy.ops.preferences.addon_enable(module="bl_ext.user_default.mpfb")
except Exception as e: print("MPFB enable warning:",e)
HumanService=svc("mpfb.services.humanservice","HumanService")
files={}
for root,_,names in os.walk(ASSETS):
    for name in names: files.setdefault(name,os.path.join(root,name))
required=["young_caucasian_female.mhmat","low-poly.mhclo","eyebrow001.mhclo","eyelashes01.mhclo","long01.mhclo","female_casualsuit01.mhclo"]
missing=[n for n in required if n not in files]
if missing: raise RuntimeError("Original MakeHuman CC0 assets missing: "+", ".join(missing))
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene; sc.render.engine="CYCLES"; sc.cycles.device="CPU"; sc.cycles.samples=12
sc.render.resolution_x=360; sc.render.resolution_y=640
sc.render.resolution_percentage=100;sc.render.fps=12
sc.frame_start=1;sc.frame_end=180
sc.render.image_settings.file_format="PNG";sc.render.filepath=OUT+"/frame_"
sc.world.color=(.026,.030,.043)
def material(name,rgb,metal=0):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*rgb,1)
    b=m.node_tree.nodes.get("Principled BSDF");b.inputs["Base Color"].default_value=(*rgb,1)
    b.inputs["Metallic"].default_value=metal;b.inputs["Roughness"].default_value=.67
    return m
wall=material("midnight charcoal",(.046,.058,.075));wood=material("walnut",(.17,.085,.039))
red=material("blood-red classification seal",(.46,.026,.031))
paper=material("aged archival paper",(.7,.63,.49))
ink=material("ink",(.02,.023,.028))
bronze=material("bronze",(.4,.22,.11),.65)
stone=material("stone",(.10,.12,.15))
def cub(name,loc,dims,mt):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name
    o.dimensions=dims;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mt)
    b=o.modifiers.new("soft handmade edges","BEVEL");b.width=.012;b.segments=2
    return o
def text_obj(msg,loc,size,mt):
    c=bpy.data.curves.new(msg,"FONT");c.body=msg;c.size=size;c.extrude=.001
    o=bpy.data.objects.new(msg,c);sc.collection.objects.link(o);o.location=loc;c.materials.append(mt)
def aim(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler()
def light(name,loc,target,color,power,sz):
    d=bpy.data.lights.new(name,"AREA");d.energy=power;d.color=color;d.size=sz
    o=bpy.data.objects.new(name,d);sc.collection.objects.link(o);o.location=loc;aim(o,target)
cub("stone floor",(0,0,-.13),(15,15,.2),stone)
cub("archive back wall",(0,3.5,2.7),(14,.20,5.6),wall)
cub("archive side wall",(-5,0,2.6),(.2,13,5.6),wall)
cub("walnut desk",(0,-.2,1.06),(3.5,1.35,.14),wood)
for x in (-1.4,1.4):
    for y in (-.6,.3):cub("desk leg",(x,y,.51),(.15,.15,.97),wood)
for side in (-3.5,3.5):
    for lvl in range(4):
        cub("archive shelf",(side,2.0,.55+lvl*.72),(.68,1.2,.065),wood)
        for j in range(6):
            cub("classified archive book",(side,1.58+j*.15,.81+lvl*.72),(.32,.08,.42),(ink,red,wood)[j%3])
cub("red file folder",(.20,-.19,1.145),(.87,.60,.035),red)
for j in range(3):cub("document sheet",(.20,-.19,1.165+j*.003),(.73,.48,.002),paper)
text_obj("CODEX CAELI",(-.12,-.30,1.178),.096,ink)
text_obj("CLASSIFIED / 2008",(-.12,-.42,1.179),.040,ink)

# Actual skinned MPFB human, not a collection of geometric body parts.
human=HumanService.create_human();human.name="Selena | actual MPFB character mesh"
rig=HumanService.add_builtin_rig(human,"mixamo")
if not rig or rig.type!="ARMATURE":raise RuntimeError("MPFB character has no valid skeletal armature")
rig.name="Selena | Mixamo-compatible skeleton"
HumanService.set_character_skin(files["young_caucasian_female.mhmat"],human,skin_type="GAMEENGINE")
for fn,kind in (("low-poly.mhclo","Eyes"),("eyebrow001.mhclo","Eyebrows"),
                ("eyelashes01.mhclo","Eyelashes"),("long01.mhclo","Hair"),
                ("female_casualsuit01.mhclo","Clothes")):
    asset=HumanService.add_mhclo_asset(files[fn],human,asset_type=kind,material_type="GAMEENGINE")
    if asset is None: raise RuntimeError("MPFB failed to attach "+kind)
bpy.context.view_layer.update()
scale=1.70/max(human.dimensions.z,.01);rig.scale=(scale,)*3;rig.location=(-.1,1.15,0)
def bone(suffix,angles,f):
    p=next((x for x in rig.pose.bones if x.name.lower().endswith(suffix.lower())),None)
    if p:
        p.rotation_mode="XYZ";p.rotation_euler=[math.radians(v) for v in angles]
        p.keyframe_insert(data_path="rotation_euler",frame=f,group="Selena character performance")
    else: print("WARN missing bone",suffix)
for f in (1,15,30,45,60,75,90,105,120,135,150,165,180):
    t=f/12
    bone("Spine",(1*math.sin(t*.75),0,2*math.sin(t*.7)),f)
    bone("Spine1",(2*math.sin(t*.8),0,1*math.sin(t*.9)),f)
    bone("Neck",(2*math.sin(t*.6),0,-4 if f<110 else 5),f)
    bone("Head",(4 if f<100 else -3,0,-8 if f<120 else 12),f)
    bone("RightArm",(-18 if f<70 else -35,0,17),f)
    bone("RightForeArm",(0,0,-25 if f<70 else -45),f)
    bone("LeftArm",(-15,0,-13),f)
    bone("LeftForeArm",(0,0,-27 if f<95 else -19),f)
# MPFB may purge materials with zero users; recreate the lamp material after adding character assets.
bronze=material("bronze | retained after MPFB import",(.4,.22,.11),.65)
cub("desk lamp base",(-1.1,-.5,1.14),(.22,.22,.06),bronze)
cub("desk lamp stem",(-1.1,-.5,1.44),(.06,.06,.55),bronze)
cub("desk lamp shade",(-1.1,-.5,1.76),(.43,.35,.17),bronze)
light("warm key",(-1.4,-2.2,3.8),(0,.7,1.5),(1,.67,.42),520,3)
light("blue window fill",(3,-2.6,3.2),(0,1,1.5),(.39,.57,1),540,3)
light("dramatic backlight",(-1.2,2.3,3.6),(0,1,1.6),(1,.74,.5),550,2.5)
d=bpy.data.cameras.new("cinema 37mm");d.lens=37
cam=bpy.data.objects.new("camera dolly",d);sc.collection.objects.link(cam);sc.camera=cam
for f,loc,target in (
 (1,(2.2,-5.4,2.3),(-.1,.6,1.45)),
 (55,(1.5,-4.3,2.1),(-.1,.9,1.44)),
 (110,(.55,-3.2,1.9),(-.1,1.1,1.5)),
 (180,(-.25,-2.2,1.75),(-.1,1.1,1.57))):
    cam.location=loc;aim(cam,target)
    cam.keyframe_insert(data_path="location",frame=f);cam.keyframe_insert(data_path="rotation_euler",frame=f)
sc.frame_set(1)
path=OUT+"/CODEX_CAELI_SELENA_MPFBRIG.blend"
bpy.ops.wm.save_as_mainfile(filepath=path)
print("SUCCESS - actual skinned MPFB human, archive set, 15 seconds",path)
