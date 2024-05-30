import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Frame rate
FPS = 60

class Game:
    def __init__(self):
        self.levels = [Level(1, 5), Level(2, 8), Level(3, 10)]
        self.current_level_index = 0
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.score = Score()
        self.hud = HUD(self.score)
        self.running = True
    
    def run(self):
        while self.running and self.current_level_index < len(self.levels):
            current_level = self.levels[self.current_level_index]
            current_level.play(self.player, self.score, self.hud)
            if self.player.is_alive:
                self.current_level_index += 1
                self.player.reset_position()
            else:
                self.running = False
        
        if self.player.is_alive:
            print("Congratulations! You've completed all levels!")
        else:
            print("Game Over!")
        pygame.quit()
    
    def quit(self):
        self.running = False

class Level:
    def __init__(self, level_number, num_enemies):
        self.level_number = level_number
        self.enemies = [
            Enemy(
                random.randint(0, SCREEN_WIDTH - 40),
                random.randint(0, SCREEN_HEIGHT // 2),
                40,
                40,
                level_number
            ) for _ in range(num_enemies)
        ]
    
    def play(self, player, score, hud):
        input_handler = InputHandler()
        clock = pygame.time.Clock()
        level_completed = False
        
        while player.is_alive and not level_completed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    player.is_alive = False
            
            input_handler.handle_input(player)
            player.move()
            player.update_projectiles(self.enemies, score)
            
            for enemy in self.enemies:
                enemy.move()
                if enemy.y > SCREEN_HEIGHT:
                    player.is_alive = False
                enemy.update_projectiles(player)
            
            self.enemies = [enemy for enemy in self.enemies if enemy.is_alive]
            if not self.enemies:
                level_completed = True
            
            SCREEN.fill(BLACK)
            hud.display()
            player.draw()
            for enemy in self.enemies:
                enemy.draw()
            pygame.display.flip()
            clock.tick(FPS)
        
        if level_completed and player.is_alive:
            print(f"Level {self.level_number} completed!")

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 5
        self.is_alive = True
        self.projectiles = []
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x - self.speed > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.speed < SCREEN_WIDTH - self.width:
            self.x += self.speed
    
    def shoot(self):
        self.projectiles.append(Projectile(self.x + self.width // 2, self.y, -5, GREEN))
    
    def update_projectiles(self, enemies, score):
        for projectile in self.projectiles:
            projectile.move()
            if projectile.y < 0:
                self.projectiles.remove(projectile)
            else:
                for enemy in enemies:
                    if projectile.collides_with(enemy):
                        self.projectiles.remove(projectile)
                        enemy.is_alive = False
                        score.add_points(10)
                        break
    
    def draw(self):
        pygame.draw.rect(SCREEN, GREEN, (self.x, self.y, self.width, self.height))
        for projectile in self.projectiles:
            projectile.draw()
    
    def reset_position(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50

class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.is_alive = True
        self.projectiles = []
    
    def move(self):
        self.y += self.speed
    
    def shoot(self):
        if random.random() < 0.02:
            self.projectiles.append(Projectile(self.x + self.width // 2, self.y + self.height, 5, RED))
    
    def update_projectiles(self, player):
        for projectile in self.projectiles:
            projectile.move()
            if projectile.y > SCREEN_HEIGHT:
                self.projectiles.remove(projectile)
            elif projectile.collides_with(player):
                self.projectiles.remove(projectile)
                player.is_alive = False
    
    def draw(self):
        pygame.draw.rect(SCREEN, RED, (self.x, self.y, self.width, self.height))
        for projectile in self.projectiles:
            projectile.draw()

class Projectile:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.radius = 5
        self.speed = speed
        self.color = color
    
    def move(self):
        self.y += self.speed
    
    def collides_with(self, entity):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2).colliderect(pygame.Rect(entity.x, entity.y, entity.width, entity.height))
    
    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.radius)

class Score:
    def __init__(self):
        self.points = 0
    
    def add_points(self, points):
        self.points += points

class HUD:
    def __init__(self, score):
        self.score = score
        self.font = pygame.font.SysFont(None, 36)
    
    def display(self):
        score_text = self.font.render(f"Score: {self.score.points}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))

class InputHandler:
    def handle_input(self, player):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.shoot()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run() 