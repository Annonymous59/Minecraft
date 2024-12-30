from random import randint

from perlin_noise import PerlinNoise
from ursina import *

app = Ursina()
class TerrainMesh(Entity):
    def __init__(self, size=10, amplitude=2, frequency=5, **kwargs):
        super().__init__()
        self.model = Mesh()

        noise = PerlinNoise(octaves=4, seed=randint(0, 1000))
        self.model.vertices = []

        # Створення вершин ландшафту
        for z in range(size):
            for x in range(size):
                y = noise([x / frequency, z / frequency]) * amplitude
                self.model.vertices.append(Vec3(x, y, z))

        # Створення трикутників
        self.model.triangles = []
        for z in range(size - 1):
            for x in range(size - 1):
                i = x + z * size - 1
                self.model.triangles.append((i, i + 1, i + size))
                self.model.triangles.append((i + 1, i + size + 1, i + size))

        # Генерація нормалей та текстури
        self.model.generate_normals()
        self.model.generate()

        self.texture = "grass"
        self.color = color.green

# Створення об'єкта ландшафту
terrain = TerrainMesh(size=20)

app.run()