import pygame
from pygame.locals import *
import numpy as np
from world import BlockType

class Player:
    def __init__(self, world, x=0, y=0):
        self.world = world
        self.x = x
        self.y = y
        self.width = 20  # Player width in pixels
        self.height = 40  # Player height in pixels
        
        # Physics properties
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.6  # Slightly increased for more responsive movement
        self.max_speed = 4  # Slightly reduced for better control
        self.jump_strength = -8  # Reduced for better control
        self.gravity = 0.4  # Reduced for smoother falling
        self.friction = 0.8  # Ground friction
        self.air_resistance = 0.95  # Air resistance when jumping
        self.on_ground = False
        
        # Movement flags
        self.moving_left = False
        self.moving_right = False
        
        # Block interaction
        self.interaction_range = 5 * 32  # 5 blocks range
    
    def get_target_block(self, mouse_pos, camera):
        """Get the block coordinates that the player is targeting"""
        # Convert screen coordinates to world coordinates
        world_x = mouse_pos[0] + camera.x
        world_y = mouse_pos[1] + camera.y
        
        # Convert to block coordinates
        block_x = int(world_x / 32)
        block_y = int(world_y / 32)
        
        # Calculate distance from player center to target block center
        player_center = self.center_position
        block_center = (block_x * 32 + 16, block_y * 32 + 16)
        
        distance = np.sqrt((player_center[0] - block_center[0])**2 + 
                         (player_center[1] - block_center[1])**2)
        
        # Check if block is within range
        if distance <= self.interaction_range:
            return block_x, block_y
        return None
    
    def handle_input(self, keys, mouse, camera):
        """Handle keyboard and mouse input for player movement and interaction"""
        # Movement
        self.moving_left = keys[K_a]
        self.moving_right = keys[K_d]
        
        # Jump only if on ground
        if keys[K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False  # Prevent multi-jumps
        
        # Block interaction
        mouse_buttons = mouse.get_pressed()
        mouse_pos = mouse.get_pos()
        target_block = self.get_target_block(mouse_pos, camera)
        
        if target_block:
            if mouse_buttons[0]:  # Left click - Break block
                self.world.set_block(target_block[0], target_block[1], BlockType.AIR)
            elif mouse_buttons[2]:  # Right click - Place block
                # Only place if target block is air and adjacent to a solid block
                if self.world.get_block(target_block[0], target_block[1]) == BlockType.AIR:
                    # Check adjacent blocks
                    adjacent_positions = [
                        (target_block[0]-1, target_block[1]),
                        (target_block[0]+1, target_block[1]),
                        (target_block[0], target_block[1]-1),
                        (target_block[0], target_block[1]+1)
                    ]
                    
                    for adj_x, adj_y in adjacent_positions:
                        if self.world.is_solid(adj_x, adj_y):
                            self.world.set_block(target_block[0], target_block[1], BlockType.DIRT)
                            break
    
    def move(self):
        """Update player position based on physics"""
        # Apply acceleration based on input
        if self.moving_left:
            self.velocity_x = max(self.velocity_x - self.acceleration, -self.max_speed)
        elif self.moving_right:
            self.velocity_x = min(self.velocity_x + self.acceleration, self.max_speed)
        else:
            # Apply friction/air resistance
            if self.on_ground:
                self.velocity_x *= self.friction
            else:
                self.velocity_x *= self.air_resistance
        
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += self.gravity
            # Terminal velocity
            self.velocity_y = min(self.velocity_y, 8)
        
        # Update position and check collisions
        self.update_position()
        
        # Reset extremely small velocities to prevent jittering
        if abs(self.velocity_x) < 0.1:
            self.velocity_x = 0
    
    def update_position(self):
        """Update position and handle collisions"""
        # Move and check horizontally first
        self.x += round(self.velocity_x)  # Round to prevent sub-pixel movement
        self.check_horizontal_collisions()
        
        # Then move and check vertically
        self.y += round(self.velocity_y)  # Round to prevent sub-pixel movement
        self.check_vertical_collisions()
    
    def check_horizontal_collisions(self):
        """Handle horizontal collisions"""
        # Get block coordinates for collision check
        left_block = int(self.x / 32)
        right_block = int((self.x + self.width - 1) / 32)
        top_block = int(self.y / 32)
        bottom_block = int((self.y + self.height - 1) / 32)
        
        # Check each potential collision point
        for y in range(top_block, bottom_block + 1):
            if self.velocity_x > 0:  # Moving right
                if self.world.is_solid(right_block, y):
                    self.x = right_block * 32 - self.width
                    self.velocity_x = 0
                    break
            elif self.velocity_x < 0:  # Moving left
                if self.world.is_solid(left_block, y):
                    self.x = (left_block + 1) * 32
                    self.velocity_x = 0
                    break
    
    def check_vertical_collisions(self):
        """Handle vertical collisions"""
        # Get block coordinates for collision check
        left_block = int(self.x / 32)
        right_block = int((self.x + self.width - 1) / 32)
        top_block = int(self.y / 32)
        bottom_block = int((self.y + self.height - 1) / 32)
        
        self.on_ground = False
        
        # Check each potential collision point
        for x in range(left_block, right_block + 1):
            if self.velocity_y > 0:  # Moving down
                if self.world.is_solid(x, bottom_block):
                    self.y = bottom_block * 32 - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                    break
            elif self.velocity_y < 0:  # Moving up
                if self.world.is_solid(x, top_block):
                    self.y = (top_block + 1) * 32
                    self.velocity_y = 0
                    break
    
    def render(self, screen, camera):
        """Render the player"""
        # Draw player
        pygame.draw.rect(screen, (255, 0, 0),  # Red color for player
                        pygame.Rect(round(self.x - camera.x),  # Round for pixel-perfect rendering
                                  round(self.y - camera.y),
                                  self.width,
                                  self.height))
        
        # Draw interaction range indicator
        mouse_pos = pygame.mouse.get_pos()
        target_block = self.get_target_block(mouse_pos, camera)
        if target_block:
            # Draw highlight on targeted block
            rect = pygame.Rect(
                target_block[0] * 32 - camera.x,
                target_block[1] * 32 - camera.y,
                32, 32
            )
            pygame.draw.rect(screen, (255, 255, 0), rect, 2)  # Yellow outline
    
    @property
    def center_position(self):
        """Get the center position of the player"""
        return (self.x + self.width / 2,
                self.y + self.height / 2)