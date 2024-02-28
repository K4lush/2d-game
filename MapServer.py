import pygame

from AnimatedSprite import AnimatedSprite
from PlatformObjects import StillObjects

class MapServer:
    def __init__(self):
        self.map = [
            [-1, -1, -1, -1, -1, -1, -1, ],
            [-1, -1, -1, -1, -1, -1, -1, ],
            [-1, -1, -1, -1, -1, 1, -1, ],
            [-1, -1, -1, -1, 1, 1, -1, ],
            [1, 1, 1, 1, 1, 1, 1, ],
            [-1, -1, -1, -1, -1, -1, -1, ]
        ]
#
        self.platforms = []
        self.terrain = []
#
        self.create_blocks_from_map()

    def create_blocks_from_map(self):
        """Creates block objects based on the map data."""
        tile_size = 120  # Size of each tile
        # Assuming self.settings.map is a 2D list indicating the type of tile at each position
        for row_index, row in enumerate(self.map):
            for col_index, tile_type in enumerate(row):
                print("PLATFORMS: ",tile_type)
                x = col_index * tile_size
                y = row_index * tile_size
                block = StillObjects(tile_type, x, y, tile_size, tile_size, sprite=None)
                self.platforms.append(block)

                if tile_type == 1:
                    self.terrain.append(block)
