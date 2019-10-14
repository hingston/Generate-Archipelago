"""Created by William Hingston on 10/10/2019.

See:
    $ python Archipelago.py -h
"""
import argparse
import math
import os
from collections import deque

import noise
from PIL import Image, ImageOps


class Archipelago:
    """Used to generate and count a group of islands.

    Generates an archipelago based on a seed, sea level and weathering with the option to count the number of islands.
    """
    PERSISTENCE = 0.5
    LACUNARITY = 2.0
    BASE = 0

    def __init__(self, n: int = 1000, seed: int = 0, sea_level: float = 0, weathering: int = 5):
        """Inits Archipelago class and checks values are within the acceptable limits."""
        if n <= 0:
            raise ValueError(
                "n must be greater than 0. n = {0}".format(n)
            )
        if not 0 <= seed <= int("0xFFFF", 16):
            raise ValueError("Seed must be between 0 and {0}. seed = {1}".format(int("0xFFFF", 16), seed))
        if not -1 <= sea_level <= 1:
            raise ValueError("Sea level must be between -1 and 1. sea_level = {0}".format(sea_level))
        if not 1 <= weathering <= 5:
            raise ValueError("Weathering must be between 1 and 5. weathering = {0}".format(weathering))
        self.n = n
        self.seed = seed
        self.sea_level = sea_level
        self.weathering = weathering
        self.map = Image.new('1', (self.n, self.n))
        self.pixels = None
        self.num_islands = 0
        self.counted = False
        self.generate()

    def generate(self):
        """Generates islands as an n * n grid of pixels in a binary image representing land and water.

        Loops through every pixel in a grid while using Perlin noise (https://en.wikipedia.org/wiki/Perlin_noise) to
        calculate a value between -1 and 1 based on the seed and weathering. If the value plus sea level is greater than
        0.01 the pixel is land and if is less than 0.01 the pixel is water.
        """
        self.counted = False
        self.pixels = self.map.load()
        # Cache the calculations on constants to save calculations in the loops
        half_n = self.n / 2
        scale = self.n * 0.15
        max_distance = self.n * 0.60
        # Could be sped up with OpenCL https://documen.tician.de/pyopencl/algorithm.html#module-pyopencl.elementwise
        for x in range(self.n):
            for y in range(self.n):
                pixel_value = noise.pnoise2(
                    self.seed + x / scale,
                    self.seed + y / scale,
                    self.weathering,
                    self.PERSISTENCE,
                    self.LACUNARITY,
                    self.n,
                    self.n,
                    self.BASE
                )
                distance_to_center = math.sqrt(
                    math.pow((x - half_n), 2) +
                    math.pow((y - half_n), 2)
                )
                pixel_value -= math.pow(distance_to_center / max_distance, 4)
                self.pixels[x, y] = pixel_value > 0.01 + self.sea_level

    def save_map(self):
        """Saves the n * n grid of pixels as a binary image where black represents land and white represents water."""
        directory = "Output/Seed{0}-{1}x{1}/".format(self.seed, self.n)
        file_name = "w{0}sl{1:+.2f}.png".format(self.weathering, self.sea_level)
        if not os.path.exists(directory):
            os.makedirs(directory)
        ImageOps.invert(self.map.convert('L')).convert('1').save(directory + file_name)

    def append_if(self, queue, x, y):
        """Append to queue if pixel at position x and y is 1 and within the bounds of n * n."""
        if 0 <= x < self.n and 0 <= y < self.n:
            if self.pixels[x, y] == 1:
                queue.append((x, y))

    def bfs(self, x, y):
        """Breadth first search. Mark all the elements within the n * n grid of pixels with 2 if they equal 1."""
        queue = deque()
        queue.append((x, y))
        while queue:
            x, y = queue.pop()
            self.pixels[x, y] = 2
            self.append_if(queue, x - 1, y)
            self.append_if(queue, x, y - 1)
            self.append_if(queue, x + 1, y)
            self.append_if(queue, x, y + 1)

    def count_islands(self):
        """Counts all the islands represented by adjacent 1s in the n * n grid of pixels."""
        if self.counted:
            return
        self.pixels = self.map.load()
        for x in range(self.n):
            for y in range(self.n):
                if self.pixels[x, y] == 1:
                    self.num_islands += 1
                    self.bfs(x, y)
        self.counted = True

    @property
    def get_num_islands(self):
        """Getter method for num_islands. Counts islands if not already counted."""
        if not self.counted:
            self.count_islands()
        return self.num_islands


def test(seed=0, weathering=5, sea_level=0, n=1000):
    """Used to test the Archipelago class.

    Tests by initiating the class which generates the map of islands, counting the number of islands, saves the map as
    a binary image and then prints the details.
    """
    islands = Archipelago(seed=seed, weathering=weathering, sea_level=sea_level, n=n)
    num_islands = islands.get_num_islands
    islands.save_map()
    print("Seed: {0}, Weathering: {1}, Sea level: {2:+.2f}, Number of islands: {3}".format(
        seed,
        weathering,
        sea_level,
        num_islands)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser("$ python Archipelago.py",
                                     description="Generates an archipelago based on a seed, sea level and weathering with the option to count the number of islands.")
    parser.add_argument("--n", default=1000, type=int,
                        help="Used to create an N * N grid of pixels. Must be greater than 0.")
    parser.add_argument("--weathering", default=5, type=int,
                        help="The weathering of the islands. Must be between 1 and 5, where 1 is most weathered (smoother edges) and 5 is least weathered (rougher edges).")
    parser.add_argument("--sea_level", default=0, type=float,
                        help="The sea level. Must be between -1 and 1, where -1 is all land and 1 is all water.")
    parser.add_argument("--seed", default=0, type=int,
                        help="The seed the islands are generated from. Must be between 0 and 65535.")
    args = parser.parse_args()
    test(args.seed, args.weathering, args.sea_level, args.n)
