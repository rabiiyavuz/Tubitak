import pygame
import sys
import random

# Pygame başlat
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 800, 600

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)

# Araç boyutları
CAR_WIDTH, CAR_HEIGHT = 50, 30

# Şeritlerin ve çizgilerin boyutları ve konumları
LANE_WIDTH = 200
LANE1_Y = HEIGHT // 4
LANE2_Y = HEIGHT // 4 * 2
LINE_WIDTH = 10

# Aracın başlangıç pozisyonu ve hızı
car_x = WIDTH // 2 - CAR_WIDTH // 2
car_y = LANE1_Y - CAR_HEIGHT // 2
car_speed = 5

# Yeni bir ekran oluştur
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lane Changing Environment")

clock = pygame.time.Clock()

def draw_environment():
    screen.fill(WHITE)

    # Şeritleri ve çizgileri çiz
    pygame.draw.rect(screen, BLACK, (0, LANE1_Y, WIDTH, LANE_WIDTH))
    pygame.draw.rect(screen, BLACK, (0, LANE2_Y, WIDTH, LANE_WIDTH))

    for i in range(0, WIDTH, LINE_WIDTH * 2):
        pygame.draw.rect(screen, GRAY, (i, 0, LINE_WIDTH, HEIGHT))

    # Araçyı çiz
    pygame.draw.rect(screen, RED, (car_x, car_y, CAR_WIDTH, CAR_HEIGHT))

    pygame.display.flip()

# Ana oyun döngüsü
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Şerit değiştirme kontrolü
    if keys[pygame.K_UP] and car_y > LANE1_Y - CAR_HEIGHT // 2:
        car_y -= car_speed
    elif keys[pygame.K_DOWN] and car_y < LANE2_Y + LANE_WIDTH - CAR_HEIGHT // 2:
        car_y += car_speed

    draw_environment()

    clock.tick(30)
