import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 800
FPS = 60
GRAVITY = 0.08

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Most Beautiful Fireworks Show")
clock = pygame.time.Clock()

# Define colors
COLORS = [
    (255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0),
    (0, 255, 255), (0, 128, 255), (128, 0, 255), (255, 0, 255),
    (255, 255, 255), (255, 105, 180)
]

# Glow helper
def draw_glow(surface, x, y, color, radius):
    for i in range(4, 0, -1):
        alpha = max(10, int(255 * (i / 4) * 0.3))
        glow = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*color, alpha), (radius, radius), int(radius * i / 4))
        surface.blit(glow, (x - radius, y - radius), special_flags=pygame.BLEND_RGBA_ADD)

# Particle class
class Particle:
    def __init__(self, x, y, color, angle, speed, size):
        self.x = x
        self.y = y
        self.color = color
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.size = size
        self.life = 100
        self.trail = []

    def update(self):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size *= 0.97
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)

    def draw(self, surface):
        for i, (tx, ty) in enumerate(self.trail):
            fade = int(255 * (i / len(self.trail)))
            pygame.draw.circle(surface, (*self.color, fade), (int(tx), int(ty)), max(1, int(self.size / 2)))
        draw_glow(surface, int(self.x), int(self.y), self.color, int(self.size + 2))

    def is_alive(self):
        return self.life > 0

# Firework class
class Firework:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.vy = random.uniform(-12, -16)
        self.color = random.choice(COLORS)
        self.exploded = False
        self.particles = []
        self.shape = random.choice(["circle", "star", "love"])

    def update(self):
        if not self.exploded:
            self.y += self.vy
            self.vy += GRAVITY * 1.5
            if self.vy >= 0:
                self.explode()
        else:
            for p in self.particles:
                p.update()
            self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 4)
        else:
            for p in self.particles:
                p.draw(surface)

    def explode(self):
        self.exploded = True
        if self.shape == "circle":
            for i in range(120):
                angle = 2 * math.pi * i / 120
                speed = random.uniform(2, 6)
                self.particles.append(Particle(self.x, self.y, self.color, angle, speed, 4))
        elif self.shape == "star":
            for i in range(5):
                angle = 2 * math.pi * i / 5
                for j in range(20):
                    offset = (j - 10) / 10.0
                    a = angle + offset * 0.2
                    speed = 4 + abs(offset) * 3
                    self.particles.append(Particle(self.x, self.y, self.color, a, speed, 4))
        elif self.shape == "love":
            for t in range(0, 360, 4):
                rad = math.radians(t)
                x = 16 * math.sin(rad) ** 3
                y = 13 * math.cos(rad) - 5 * math.cos(2 * rad) - 2 * math.cos(3 * rad) - math.cos(4 * rad)
                angle = math.atan2(-y, x)
                dist = math.hypot(x, y) * 0.7
                self.particles.append(Particle(self.x, self.y, self.color, angle, dist, 4))

    def is_done(self):
        return self.exploded and not self.particles

# Main loop
fireworks = []
running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 15))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if random.random() < 0.04:
        fireworks.append(Firework())

    for fw in fireworks:
        fw.update()
        fw.draw(screen)

    fireworks = [fw for fw in fireworks if not fw.is_done()]
    pygame.display.flip()

pygame.quit()
sys.exit()
