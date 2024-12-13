from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina()
selected_block = "grass"
player = FirstPersonController(
mouse_sensetivity = Vec2(100,100)
)
block_textures = {
  "grass": load_texture("assets/textures/groundEarth.png"),
  "dirt": load_texture("assets/textures/groundMud.png"),
  "stone": load_texture("assets/textures/wallStone.png"),
  "bedrock": load_texture("assets/textures/stone07.png")
}
hand = Entity(
    parent = camera,
    model = "assets/models/block_model",
    scale = 0.2,
    texture = block_textures.get("grass"),
    position=(0.35, -0.25, 0.5),
    rotation=(-15, -30, -5)
)
class Voxel(Entity):
    def __init__(self, position, block_type):
        super().__init__(
            position = position,
            model="assets/models/block_model",
            scale = 1,
            origin_y = -0.5,
            texture = block_textures.get(block_type),
            collider = "box"
    )
        self.block_type = block_type

for x in range(0,50):
    for y in range(0,50):
        block = Voxel((x,0,y), "grass")

def input(key):
    global selected_block
    if key == "left mouse down":
        hit_info = raycast(camera.world_position, camera.forward, distance=10)
        if hit_info.hit:
            block = Voxel(hit_info.entity.position + hit_info.normal, selected_block)
    elif key == "right mouse down":
        destroy(mouse.hovered_entity)

app.run()