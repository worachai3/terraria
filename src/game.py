import pygame
import sys
from pygame.locals import *
from world import World, BlockType
from player import Player

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.speed = 5

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
    
    def follow(self, target_x, target_y):
        """Make camera follow a target position"""
        # Center the camera on the target
        self.x = target_x - self.width // 2
        self.y = target_y - self.height // 2

class Game:
    def __init__(self):
        pygame.init()
        
        # Initialize display
        self.WINDOW_SIZE = (800, 600)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Terraria Clone")
        
        # Initialize game objects
        self.clock = pygame.time.Clock()
        self.world = World(100, 100)
        self.camera = Camera(*self.WINDOW_SIZE)
        
        # Create player at middle of world
        spawn_x = (self.world.width * 32) // 2
        spawn_y = 0
        self.player = Player(self.world, spawn_x, spawn_y)
        
        # Game settings
        self.FPS = 60
        self.BLOCK_SIZE = 32
        self.running = True
        
        # Block colors
        self.BLOCK_COLORS = {
            BlockType.AIR: (135, 206, 235),    # Sky blue
            BlockType.DIRT: (139, 69, 19),     # Brown
            BlockType.STONE: (128, 128, 128),  # Gray
            BlockType.GRASS: (34, 139, 34)     # Green
        }
        
        # Enable key repeat for smooth movement
        pygame.key.set_repeat(1, 10)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
    
    def handle_input(self):
        """Handle continuous keyboard and mouse input"""
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse
        self.player.handle_input(keys, mouse, self.camera)
    
    def update(self):
        """Update game state"""
        self.handle_input()
        self.player.move()
        
        # Make camera follow player
        self.camera.follow(*self.player.center_position)
    
    def render(self):
        """Render the game state"""
        # Fill screen with background color
        self.screen.fill(self.BLOCK_COLORS[BlockType.AIR])
        
        # Calculate visible range
        start_x = max(0, int(self.camera.x // self.BLOCK_SIZE))
        end_x = min(self.world.width, int((self.camera.x + self.WINDOW_SIZE[0]) // self.BLOCK_SIZE + 1))
        start_y = max(0, int(self.camera.y // self.BLOCK_SIZE))
        end_y = min(self.world.height, int((self.camera.y + self.WINDOW_SIZE[1]) // self.BLOCK_SIZE + 1))
        
        # Render visible blocks
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                block_type = self.world.get_block(x, y)
                if block_type != BlockType.AIR:
                    rect = pygame.Rect(
                        x * self.BLOCK_SIZE - int(self.camera.x),
                        y * self.BLOCK_SIZE - int(self.camera.y),
                        self.BLOCK_SIZE,
                        self.BLOCK_SIZE
                    )
                    pygame.draw.rect(self.screen, self.BLOCK_COLORS[block_type], rect)
                    # Add block outline
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
        
        # Render player
        self.player.render(self.screen, self.camera)
        
        # Draw crosshair at mouse position
        mouse_pos = pygame.mouse.get_pos()
        crosshair_size = 10
        pygame.draw.line(self.screen, (255, 255, 255),
                        (mouse_pos[0] - crosshair_size, mouse_pos[1]),
                        (mouse_pos[0] + crosshair_size, mouse_pos[1]))
        pygame.draw.line(self.screen, (255, 255, 255),
                        (mouse_pos[0], mouse_pos[1] - crosshair_size),
                        (mouse_pos[0], mouse_pos[1] + crosshair_size))
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()