import pytest
import numpy as np
from world import World, BlockType

def test_world_initialization():
    world = World(width=100, height=100)
    assert world.width == 100
    assert world.height == 100
    assert world.blocks.shape == (100, 100)

def test_block_setting_and_getting():
    world = World(width=10, height=10)
    
    # Test setting and getting a block
    world.set_block(5, 5, BlockType.DIRT)
    assert world.get_block(5, 5) == BlockType.DIRT
    
    # Test getting block outside bounds returns AIR
    assert world.get_block(-1, -1) == BlockType.AIR
    assert world.get_block(100, 100) == BlockType.AIR

def test_terrain_generation():
    world = World(width=50, height=50)
    
    # Test that surface level has some grass blocks
    grass_count = np.sum(world.blocks == BlockType.GRASS.value)
    assert grass_count > 0
    
    # Test that there are both dirt and stone blocks
    dirt_count = np.sum(world.blocks == BlockType.DIRT.value)
    stone_count = np.sum(world.blocks == BlockType.STONE.value)
    assert dirt_count > 0
    assert stone_count > 0
    
    # Test that top portion is mostly air
    top_portion = world.blocks[:world.SURFACE_LEVEL-10]
    air_count = np.sum(top_portion == BlockType.AIR.value)
    assert air_count == top_portion.size

def test_solid_blocks():
    world = World(width=10, height=10)
    
    # Air is not solid
    world.set_block(0, 0, BlockType.AIR)
    assert not world.is_solid(0, 0)
    
    # Dirt is solid
    world.set_block(1, 1, BlockType.DIRT)
    assert world.is_solid(1, 1)
    
    # Stone is solid
    world.set_block(2, 2, BlockType.STONE)
    assert world.is_solid(2, 2)
    
    # Grass is solid
    world.set_block(3, 3, BlockType.GRASS)
    assert world.is_solid(3, 3)