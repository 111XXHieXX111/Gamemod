from OpenGameEngine import *
import glob
import json
import os
import builtins


if not os.path.exists("mods"):
    os.mkdir("mods")

if not os.path.exists("descriptors"):
    os.mkdir("descriptors")


mods = glob.glob("mods/*.json")
descriptors = glob.glob("descriptors/*.dscr")
descriptors2 = []


for descriptor in descriptors:
    descriptors2.append(os.path.basename(descriptor))


descriptors.clear()
descriptors = descriptors2.copy()
del descriptors2


game_objects = {}
game_descriptors = []
game_updates = []
game_functions = {}


def load_mod(mod_path: str):
    try:
        with open(mod_path, "r") as raw_mod:
            data = json.load(raw_mod)

        mod_name = data.get("mod_name", "nameless")
        mod_version = data.get("mod_version", "???")
        mod_objects = data.get("objects", [])
        mod_descriptor = data.get("descriptor", False)

        descriptor_found = True
        
        if mod_name != "nameless" and mod_descriptor:
            mod_name_we = os.path.basename(mod_path).split(".")[0]
            if mod_name_we + ".dscr" in descriptors:
                with open("descriptors/" + mod_name_we + ".dscr", "r") as raw_descriptor:
                    game_descriptors.append(raw_descriptor.read())
            else:
                descriptor_found = False

        print(f"Loading: {mod_name} mod ({mod_version})")

        if not descriptor_found:
            print("Descriptor not found!")

        for obj in mod_objects:
            obj_m = obj.get("model", "rectangle")
            obj_px = obj.get("x", 0)
            obj_py = obj.get("y", 0)
            obj_sx = obj.get("width", 0)
            obj_sy = obj.get("height", 0)
            obj_c = obj.get("color", [0, 0, 0, 0])
            obj_r = obj.get("render", True)
            obj_n = obj.get("name", "nameless")

            print(f"Loading object {obj_n}")

            if obj_m == "rectangle":
                gfx_obj = gfx.Rectangle()
            elif obj_m == "circle":
                gfx_obj = gfx.Circle()
            else:
                print(f"Unknown model! {obj_m}")
                gfx_obj = gfx.Rectangle()

            Transform.SetPosition(gfx_obj, Vec2(obj_px, obj_py))
            Transform.SetSize(gfx_obj, Vec2(obj_sx, obj_sy))
            Color.Set(gfx_obj, Color4(obj_c[0], obj_c[1], obj_c[2], obj_c[3]))

            game_objects.update({obj_n: (gfx_obj, obj_r)})

    except Exception as ex:
        print(f"Error loading mod:{ex}")


def add_another_object(gfx_obj, name: str, render: bool):
    game_objects.update({name: (gfx_obj, render)})

def remove_another_object(name: str):
    game_objects.pop(name)


def add_global_function(func, name: str):
    game_functions.update({name: func})

def remove_global_function(name: str):
    game_functions.pop(name)


window = Renderer.Window()


camera = Renderer.Camera2D()
window.SetCamera(camera)


mod_namespace = {
    "game_objects": game_objects,
    "Transform": Transform,
    "Color": Color,
    "Color3": Color3,
    "Color4": Color4,
    "c256": c256,
    "Vec1": Vec1,
    "Vec2": Vec2,
    "Vec3": Vec3,
    "gfx": gfx,
    "__builtins__": vars(builtins),
    "window": window,
    "Input": Input,
    "ImGUI": ImGUI,
    "ImGUIf": ImGUIf,
    "ImGUIo": ImGUIo,
    "TextureFilter": TextureFilter,
    "Renderer": Renderer,
    "Texture": Texture,
    "Layers": Layers,
    "Math": Math,
    "Random": Random,
    "Misc": Misc,
    "Physics": Physics,
    "sfx": sfx,
    "Keys": Keys,
    "MouseButton": MouseButton,
    "camera": camera,
    "add_another_object": add_another_object,
    "remove_another_object": remove_another_object,
    "add_global_function": add_global_function,
    "remove_global_function": remove_global_function,
    "game_functions": game_functions
}


@window.UpdateFunction
def update():
    for upd in game_updates:
        try:
            upd()
        except:...

    for name, (gfx_obj, should_render) in game_objects.items():
        if should_render:
            gfx_obj.Draw()


for mod_path in mods:
    load_mod(mod_path)


for game_descriptor in game_descriptors:
    current_mod_namespace = mod_namespace.copy()
    exec(game_descriptor, current_mod_namespace)
    if "update" in current_mod_namespace:
        game_updates.append(current_mod_namespace["update"])

window.Run()
