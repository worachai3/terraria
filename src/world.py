import numpy as np
from enum import Enum

class BlockType(Enum):
    AIR = 0
    DIRT = 1
    STONE = 2
    GRASS = 3

class World:
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.blocks = np.zeros((height, width), dtype=np.int8)
        self.SURFACE_LEVEL = height // 2
        self.generate_terrain()
    
    def generate_terrain(self):
        """Generate basic terrain with surface variations"""
        # Generate surface height variations
        surface_height = np.zeros(self.width, dtype=np.int32)
        for x in range(self.width):
            # Simple sine wave terrain
            surface_height[x] = self.SURFACE_LEVEL + int(np.sin(x * 0.1) * 5)
        
        # Fill terrain
        for x in range(self.width):
            height = surface_height[x]
            # Fill underground with dirt and stone
            for y in range(height, self.height):
                if y < height + 5:  # Top layer is dirt
                    self.blocks[y, x] = BlockType.DIRT.value
                else:  # Below is stone
                    if np.random.random() > 0.5:  # 50% chance of stone
                        self.blocks[y, x] = BlockType.STONE.value
                    else:
                        self.blocks[y, x] = BlockType.DIRT.value
            
            # Add grass on surface
            if height > 0:
                self.blocks[height-1, x] = BlockType.GRASS.value
    
    def get_block(self, x, y):
        """Get block type at given coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return BlockType(self.blocks[y, x])
        return BlockType.AIR
    
    def set_block(self, x, y, block_type):
        """Set block type at given coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.blocks[y, x] = block_type.value
    
    def is_solid(self, x, y):
        """Check if block at coordinates is solid"""
        block = self.get_block(x, y)
        return block != BlockType.AIR