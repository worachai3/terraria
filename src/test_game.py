import pytest
import pygame
from pygame.locals import *
from game import Game, Camera
from world import World, BlockType

def test_game_initialization():
    game = Game()
    assert game.WINDOW_SIZE == (800, 600)
    assert game.running == True
    assert game.FPS == 60
    assert game.BLOCK_SIZE == 32
    assert isinstance(game.world, World)
    assert isinstance(game.camera, Camera)

def test_camera_initialization():
    camera = Camera(800, 600)
    assert camera.x == 0
    assert camera.y == 0
    assert camera.width == 800
    assert camera.height == 600
    assert camera.speed == 5

def test_camera_movement():
    camera = Camera(800, 600)
    
    # Test horizontal movement
    camera.move(1, 0)
    assert camera.x == 5
    assert camera.y == 0
    
    # Test vertical movement
    camera.move(0, 1)
    assert camera.x == 5
    assert camera.y == 5
    
    # Test diagonal movement
    camera.move(-1, -1)
    assert camera.x == 0
    assert camera.y == 0

def test_game_quit():
    game = Game()
    # Simulate quit event
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.handle_events()
    assert game.running == False

def test_escape_key():
    game = Game()
    # Simulate escape key press
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE}))
    game.handle_events()
    assert game.running == False

def test_block_colors():
    game = Game()
    # Test that all block types have corresponding colors
    for block_type in BlockType:
        assert block_type in game.BLOCK_COLORS
        assert isinstance(game.BLOCK_COLORS[block_type], tuple)
        assert len(game.BLOCK_COLORS[block_type]) == 3  # RGB values

def test_game_update():
    game = Game()
    
    # Reset player position and place a platform
    player_x = game.world.width * 16  # Center of world
    player_y = game.world.height * 16
    game.player.x = player_x
    game.player.y = player_y
    
    # Create a platform under the player
    for dx in range(-2, 3):  # Platform width of 5 blocks
        block_x = int(player_x / 32) + dx
        block_y = int((player_y + game.player.height + 1) / 32)
        game.world.set_block(block_x, block_y, BlockType.DIRT)
    
    # Update to settle player and camera
    for _ in range(5):  # Multiple updates to stabilize
        game.update()
    
    # Check if camera is centered on player
    player_center_x = game.player.x + game.player.width / 2
    player_center_y = game.player.y + game.player.height / 2
    camera_center_x = game.camera.x + game.camera.width / 2
    camera_center_y = game.camera.y + game.camera.height / 2
    
    # Allow small offset for floating point differences
    assert abs(player_center_x - camera_center_x) <= game.player.width
    assert abs(player_center_y - camera_center_y) <= game.player.height