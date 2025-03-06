import pytest
import pygame
from pygame.locals import *
from player import Player
from world import World, BlockType

@pytest.fixture
def world():
    return World(100, 100)

@pytest.fixture
def player(world):
    return Player(world, 50, 50)

@pytest.fixture
def camera():
    class MockCamera:
        def __init__(self):
            self.x = 0
            self.y = 0
    return MockCamera()

def test_player_initialization(player):
    assert player.x == 50
    assert player.y == 50
    assert player.width == 20
    assert player.height == 40
    assert player.velocity_x == 0
    assert player.velocity_y == 0
    assert not player.moving_left
    assert not player.moving_right
    assert not player.on_ground

def test_player_movement(player, camera):
    # Test horizontal movement
    keys = {K_a: False, K_d: True, K_SPACE: False}
    class MockMouse:
        def get_pressed(self):
            return [0, 0, 0]
        def get_pos(self):
            return (0, 0)
    
    mock_mouse = MockMouse()
    player.handle_input(keys, mock_mouse, camera)
    assert player.moving_right
    assert not player.moving_left
    
    player.move()
    assert player.velocity_x > 0
    
    # Test left movement
    keys = {K_a: True, K_d: False, K_SPACE: False}
    player.handle_input(keys, mock_mouse, camera)
    assert player.moving_left
    assert not player.moving_right

def test_player_jumping(player, camera):
    # Put player on ground
    player.on_ground = True
    initial_y = player.y
    
    # Test jump
    keys = {K_a: False, K_d: False, K_SPACE: True}
    class MockMouse:
        def get_pressed(self):
            return [0, 0, 0]
        def get_pos(self):
            return (0, 0)
    
    mock_mouse = MockMouse()
    player.handle_input(keys, mock_mouse, camera)
    player.move()
    
    assert player.velocity_y < 0  # Moving upward
    assert player.y < initial_y  # Position changed

def test_player_gravity(player):
    initial_velocity = player.velocity_y
    player.move()
    assert player.velocity_y > initial_velocity  # Gravity increased velocity

def test_player_collision(world, player):
    # Place a block below player
    block_x = int(player.x / 32)
    block_y = int((player.y + player.height + 1) / 32)
    world.set_block(block_x, block_y, BlockType.DIRT)
    
    # Move player down
    player.velocity_y = 5
    player.move()
    
    assert player.on_ground
    assert player.velocity_y == 0

def test_player_center_position(player):
    center_x, center_y = player.center_position
    assert center_x == player.x + player.width / 2
    assert center_y == player.y + player.height / 2

def test_block_interaction_range(player, world, camera):
    # Test block within range
    mouse_pos = (100, 100)  # Screen coordinates
    target = player.get_target_block(mouse_pos, camera)
    assert target is not None
    
    # Test block outside range
    far_mouse_pos = (1000, 1000)  # Far away coordinates
    far_target = player.get_target_block(far_mouse_pos, camera)
    assert far_target is None

def test_block_breaking(player, world, camera):
    # Place a block
    test_x, test_y = 3, 3
    world.set_block(test_x, test_y, BlockType.DIRT)
    
    # Simulate clicking on the block within range
    class MockMouse:
        def get_pressed(self):
            return [1, 0, 0]  # Left click
        def get_pos(self):
            return (test_x * 32, test_y * 32)
    
    mock_mouse = MockMouse()
    keys = {K_a: False, K_d: False, K_SPACE: False}
    
    # Move player close to block
    player.x = test_x * 32
    player.y = test_y * 32
    
    # Break block
    player.handle_input(keys, mock_mouse, camera)
    assert world.get_block(test_x, test_y) == BlockType.AIR

def test_block_placing(player, world, camera):
    # Clear a block and have a solid block adjacent
    test_x, test_y = 3, 3
    world.set_block(test_x, test_y, BlockType.AIR)
    world.set_block(test_x, test_y + 1, BlockType.DIRT)  # Adjacent block
    
    # Simulate right clicking on the empty block
    class MockMouse:
        def get_pressed(self):
            return [0, 0, 1]  # Right click
        def get_pos(self):
            return (test_x * 32, test_y * 32)
    
    mock_mouse = MockMouse()
    keys = {K_a: False, K_d: False, K_SPACE: False}
    
    # Move player close to block
    player.x = test_x * 32
    player.y = test_y * 32
    
    # Place block
    player.handle_input(keys, mock_mouse, camera)
    assert world.get_block(test_x, test_y) == BlockType.DIRT

def test_player_friction(player, camera):
    # Give player initial velocity
    player.velocity_x = player.max_speed
    
    # No movement keys pressed
    keys = {K_a: False, K_d: False, K_SPACE: False}
    class MockMouse:
        def get_pressed(self):
            return [0, 0, 0]
        def get_pos(self):
            return (0, 0)
    
    mock_mouse = MockMouse()
    player.handle_input(keys, mock_mouse, camera)
    player.move()
    
    # Velocity should decrease due to friction
    assert abs(player.velocity_x) < player.max_speed