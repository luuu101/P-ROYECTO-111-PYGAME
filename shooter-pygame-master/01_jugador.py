import pygame, random
import unittest
from unittest.mock import patch

# Constantes
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

all_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)


# Game Loop
running = True
while running:
    # Keep loop running at the right speed
    clock.tick(60)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    #Draw / Render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display.
    pygame.display.flip()

pygame.quit()


# Pruebas unitarias

class TestPlayer(unittest.TestCase):
    def setUp(self):
        """Configuramos el entorno de prueba"""
        pygame.init()
        self.player = Player()
        self.screen = pygame.Surface((WIDTH, HEIGHT))  # Superficie para pruebas

    def test_initial_position(self):
        """Verifica que el jugador esté en la posición inicial correcta"""
        self.assertEqual(self.player.rect.centerx, WIDTH // 2)
        self.assertEqual(self.player.rect.bottom, HEIGHT - 10)

    def test_player_move_left(self):
        """Verifica que el jugador se mueva correctamente a la izquierda"""
        self.player.rect.centerx = WIDTH // 2
        self.player.speed_x = -5
        self.player.update()
        self.assertEqual(self.player.rect.x, WIDTH // 2 - 5)

    def test_player_move_right(self):
        """Verifica que el jugador se mueva correctamente a la derecha"""
        self.player.rect.centerx = WIDTH // 2
        self.player.speed_x = 5
        self.player.update()
        self.assertEqual(self.player.rect.x, WIDTH // 2 + 5)

    @patch('pygame.key.get_pressed')
    def test_player_left_key_pressed(self, mock_get_pressed):
        """Verifica que el jugador se mueva a la izquierda cuando la tecla izquierda es presionada"""
        mock_get_pressed.return_value = {pygame.K_LEFT: True, pygame.K_RIGHT: False}
        self.player.update()
        self.assertEqual(self.player.rect.x, WIDTH // 2 - 5)

    @patch('pygame.key.get_pressed')
    def test_player_right_key_pressed(self, mock_get_pressed):
        """Verifica que el jugador se mueva a la derecha cuando la tecla derecha es presionada"""
        mock_get_pressed.return_value = {pygame.K_LEFT: False, pygame.K_RIGHT: True}
        self.player.update()
        self.assertEqual(self.player.rect.x, WIDTH // 2 + 5)

if __name__ == '__main__':
    unittest.main()

