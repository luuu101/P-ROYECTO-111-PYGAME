import pygame, random
import unittest




from unittest.mock import MagicMock, patch

# Constantes
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGHT
    border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100

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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, -100)
            self.speedy = random.randrange(1, 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def show_go_screen():
    screen.blit(background, [0,0])
    draw_text(screen, "SHOOTER", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Instruciones van aquí", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "jugar", 20, WIDTH // 2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
                "assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
                "assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())


explosion_anim = []
for i in range(9):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70,70))
    explosion_anim.append(img_scale)

background = pygame.image.load("assets/background.png").convert()

laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)

game_over = True
running = True
while running:
    if game_over:

        show_go_screen()

        game_over = False
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)
        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)

        score = 0


    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()


    all_sprites.update()

    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        player.shield -= 25
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield <= 0:
            game_over = True

    screen.blit(background, [0, 0])

    all_sprites.draw(screen)

    draw_text(screen, str(score), 25, WIDTH // 2, 10)

    draw_shield_bar(screen, 5, 5, player.shield)

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

    def test_shield_initial(self):
        """Verifica que el escudo del jugador esté al 100% al inicio"""
        self.assertEqual(self.player.shield, 100)

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

    def test_shoot_bullet(self):
        """Verifica que el jugador dispare correctamente una bala"""
        self.player.shoot()
        self.assertEqual(len(bullets), 1)  # Debería haber una bala en el grupo de balas

class TestMeteor(unittest.TestCase):
    def setUp(self):
        """Configuramos el entorno de prueba para el meteorito"""
        pygame.init()
        self.meteor = Meteor()

    def test_initial_position(self):
        """Verifica que el meteorito tenga una posición inicial aleatoria dentro del área visible"""
        self.assertGreater(self.meteor.rect.x, 0)
        self.assertLess(self.meteor.rect.x, WIDTH - self.meteor.rect.width)
        self.assertGreater(self.meteor.rect.y, -140)

    def test_meteor_update(self):
        """Verifica que el meteorito se mueva hacia abajo correctamente"""
        initial_y = self.meteor.rect.y
        self.meteor.update()
        self.assertGreater(self.meteor.rect.y, initial_y)

    def test_meteor_reset_position(self):
        """Verifica que el meteorito se reinicie cuando sale de la pantalla"""
        self.meteor.rect.y = HEIGHT + 10
        self.meteor.update()
        self.assertLess(self.meteor.rect.y, HEIGHT)

class TestBullet(unittest.TestCase):
    def setUp(self):
        """Configuramos el entorno de prueba para la bala"""
        pygame.init()
        self.bullet = Bullet(400, 300)

    def test_bullet_initial_position(self):
        """Verifica que la bala se cree en la posición correcta"""
        self.assertEqual(self.bullet.rect.centerx, 400)
        self.assertEqual(self.bullet.rect.top, 300)

    def test_bullet_move(self):
        """Verifica que la bala se mueva hacia arriba"""
        initial_y = self.bullet.rect.y
        self.bullet.update()
        self.assertLess(self.bullet.rect.y, initial_y)

    def test_bullet_off_screen(self):
        """Verifica que la bala sea destruida al salir de la pantalla"""
        self.bullet.rect.top = 0  # Colocamos la bala en la parte superior de la pantalla
        self.bullet.update()
        self.assertTrue(self.bullet.rect.bottom < 0)


if __name__ == '__main__':
    unittest.main()
