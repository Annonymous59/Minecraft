
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from math import floor
from random import randint

app = Ursina()

player = FirstPersonController(
    sensitivity = Vec2(100,100)
)
counts = {"l":0, "t":0}
selected_block = "grass"
model = "assets/models/block_model"
normal_speed = player.speed
block_textures = {
  "grass": load_texture("assets/textures/groundEarth.png"),
  "dirt": load_texture("assets/textures/groundMud.png"),
  "stone": load_texture("assets/textures/wallStone.png"),
  "bedrock": load_texture("assets/textures/stone07.png"),
  "brick": load_texture("assets/textures/wallBrick01.png"),
  "ice": load_texture("assets/textures/ice01.png"),
  "trunk": load_texture("assets/textures/Tree.png"),
  "leafs": load_texture("assets/textures/leaves.png"),
  "water": load_texture("assets/textures/water.png"),
  "sand": load_texture("assets/textures/sand.png")


}
class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = model,
            position = Vec3(0.5, -0.4, 2),
            rotation = Vec3(-15,-35,0),
            scale = 0.2
        )


    def animation(self):
        self.animate("rotation", Vec3(0, -35, 0), duration=0.25)
        self.animate("position", Vec3(0.25, -0.25, 2.5), duration=0.25)
        invoke(
            self.animate,
            "rotation", Vec3(-15, -35, 0), duration=0.25, curve=curve.linear, delay=0.25
        )
        invoke(
            self.animate,
            "position", Vec3(0.5, -0.4, 2), duration=0.25, curve=curve.linear, delay=0.5
        )
hand = Hand()


class Block(Entity):
    global model
    def __init__(self, pos, block_type = "grass", color = color.white, col = "box"):
        super().__init__(
            position = pos,
            model = model,
            scale = 1,
            origin_y = -0.5,
            color = color,
            texture = block_textures.get(block_type),
            collider = col

        )
        self.block_type = block_type




heights = {}
min_height = 0
water_level = 0
terrain_width = randint(0, 60)

def generarte_map():
    global terrain_width
    freq = 24
    amp = 5
    land_noise = PerlinNoise(octaves=3, seed=1000)
    for i in range(terrain_width * terrain_width):
        x = floor(i / terrain_width)
        z = floor(i % terrain_width)
        y = floor(land_noise([x / freq, z / freq]) * amp)
        heights[(x, z)] = y
        Block(pos=(x, -1, z), block_type="sand")
        Block(pos=(x, -2, z), block_type="bedrock")

        if y >= water_level:
            Block(pos=(x,y,z), block_type="grass")

        for gap in range(water_level, y):
            Block(pos=(x, gap, z), block_type="water", col=None)

        if y < water_level:
            for gap in range(y, water_level + 1):
                Block(pos=(x,gap,z), block_type="water", col=None)





def input(key):
    global selected_block
    global counts

    speed_change()
    if key == "left mouse down":
            hit_info = raycast(camera.world_position, camera.forward, distance=10)
            hand.animation()

            if hit_info.hit:
                Block(hit_info.entity.position + hit_info.normal, selected_block)
                hand.animation()

    elif key == "right mouse down" and mouse.hovered_entity.block_type != "bedrock":
            destroy(mouse.hovered_entity)
            hand.animation()
            try:
                if mouse.hovered_entity.block_type == "trunk":
                    counts["t"] += 1
                elif mouse.hovered_entity.block_type == "leafs":
                    counts["l"] += 1
            except AttributeError:
                pass
    match key:
        case "1":
            selected_block = "grass"
        case "2":
            selected_block = "brick"
        case "3":
            selected_block = "dirt"
        case "4":
            selected_block = "ice"
        case "5":
            selected_block = "bedrock"
    if key == "6" and counts.get("l") > 0:
            selected_block = "leafs"
    if key == "7" and counts.get("t") > 0:
            selected_block = "trunk"


def update():
    hand.texture = block_textures.get(selected_block)
def generate_tree(x,z, heights,min_height):
    terrain_height = heights.get((x,z), min_height)
    trunk_height = randint(3,5)
    for y in range(terrain_height,terrain_height + trunk_height):
        Block(pos = (x,y,z), block_type="trunk")

    leaf_radius = 2

    for lx in range(-leaf_radius, leaf_radius + 1):
        for lz in range(-leaf_radius, leaf_radius + 1):
            for ly in range(-leaf_radius//2, leaf_radius//2 + 1):
                if abs(lx) + abs(lz) + abs(ly) <= leaf_radius:
                    leaf_pos = (lx + x, ly + terrain_height + trunk_height, lz + z)
                    Block(pos=leaf_pos, block_type="leafs")

def speed_change():
    global normal_speed
    if held_keys["shift"]:
        player.speed = normal_speed + 2
        print(player.speed)

    else:
        player.speed = normal_speed - 2
        print(player.speed)






def start():
    global heights, min_height
    num_trees = randint(2, 10)
    for _ in range(num_trees):
        generate_tree(randint(0, terrain_width - 1), randint(0, terrain_width - 1), heights, min_height)
        generarte_map()
        print(num_trees)
        app.run()


start()