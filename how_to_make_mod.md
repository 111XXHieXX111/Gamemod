# How to make mod?

## First step

Create json file in folder mods

## Mod Cover

Mod template:
```json
{
    "mod_name": your_mod_name,
    "mod_version": your_mod_version,
    "descriptor": mod_has_descriptor,
    "objects": your_mod_objects
}
```

Example:
```json
{
    "mod_name": "Example mod",
    "mod_version": "1.0.0",
    "descriptor": false,
    "objects": []
}
```

Default values:
+ mod_name : nameless
+ mod_version : ???
+ descriptor : false
+ objects : []

## Mod Objects

Objects template:
```json
[
    {
        "name": your_object_name,
        "x": your_object_x,
        "y": your_object_y,
        "width": your_object_width,
        "height": your_object_height,
        "model": your_object_model,
        "color": your_object_color,
        "render": render_object
    }
]
```

Example:
```json
[
    {
        "name": "Example rectangle",
        "x": 20,
        "y": 20,
        "width": 60,
        "height": 60,
        "model": "rectangle",
        "color": [0, 0, 0, 1],
        "render": true
    }
]
```

Default values:
+ name : nameless
+ x : 0
+ y : 0
+ width : 0
+ height : 0
+ model : rectangle
+ color : [0, 0, 0, 0]
+ render : true

## Mod descriptor

See engine documentation for use descriptor! You can use values such as:
+ game_objects
+ Transform
+ Color
+ Color3
+ Color4
+ c256
+ Vec1
+ Vec2
+ Vec3
+ gfx
+ window (Window)
+ Input
+ ImGUI
+ ImGUIf
+ ImGUIo
+ TextureFilter
+ Renderer
+ Texture
+ Layers
+ Math
+ Random
+ Misc
+ Physics
+ sfx
+ builtins
+ Keys
+ MouseButton
+ camera (Camera2D)
+ game_functions

Descriptor example:
```python
r_color = 0

rect = game_objects["Example rectangle"][0]

def update():
    global r_color
    Transform.SetPosition(rect, Vec2(80, 80))
    Color.Set(rect, Color3(r_color, 1, 1))
    r_color += 0.01
    if r_color >= 1.01:
        r_color = 0
```

## game_objects format

value in game_objects = (
    gfx_obj,
    render (bool)
)

## Structure

game_folder
+ mods
+ + your_mod_name.json

+ descriptors
+ + your_mod_name.dscr

If a mod does not have a descriptor, you do not need to add a descriptor file.

## API Methods

### Another objects

+ adding to game_objects
+ removing from game_objects

#### add_another_object

> def add_another_object(gfx_obj, name: str, render: bool)

If you need to add an external graphical object.

Example:
```python
rect = gfx.Rectangle()

add_another_object(rect, "rect", True)
```

#### remove_another_object

> def remove_another_object(name: str)

If you need to remove an external graphical object.

Example:
```python
remove_another_object("rect")
```

### Global functions

+ adding to game_functions
+ removing from game_functions

format:
+ name: func

#### add_global_function

> def add_global_function(func, name: str)

If you want to add a function that is accessible from other mods.

Example:
```python
def hello():
    print("Hello, World!")

add_global_function(hello, "helloworld")
```

#### remove_global_function

> def remove_global_function(name: str)

If you want to remove a feature that is available from other mods.

Example:
```python
remove_global_function("helloworld")
```
