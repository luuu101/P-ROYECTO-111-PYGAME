import pygame, random

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
        self._speed_x = 0  # Atributo privado para la velocidad horizontal

    # Getter para speed_x
    def get_speed_x(self):
        return self._speed_x

    # Setter para speed_x
    def set_speed_x(self, value):
        # Validación simple: no dejar que la velocidad sea mayor a 5 o menor a -5
        if -5 <= value <= 5:
            self._speed_x = value
        else:
            print("Valor de velocidad no válido. Debe estar entre -5 y 5.")

    def update(self):
        self.set_speed_x(0)  # Resetear la velocidad en cada actualización
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.set_speed_x(-5)
        if keystate[pygame.K_RIGHT]:
            self.set_speed_x(5)
        self.rect.x += self.get_speed_x()
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/meteorGrey_med1.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self._speedy = random.randrange(1, 10)
        self._speedx = random.randrange(-5, 5)

    # Getter para speedx
    def get_speedx(self):
        return self._speedx

    # Setter para speedx
    def set_speedx(self, value):
        if -5 <= value <= 5:
            self._speedx = value
        else:
            print("Valor de velocidad horizontal no válido. Debe estar entre -5 y 5.")

    # Getter para speedy
    def get_speedy(self):
        return self._speedy

    # Setter para speedy
    def set_speedy(self, value):
        if 1 <= value <= 10:
            self._speedy = value
        else:
            print("Valor de velocidad vertical no válido. Debe estar entre 1 y 10.")

    def update(self):
        self.rect.x += self.get_speedx()  # Usamos el getter para obtener la velocidad en x
        self.rect.y += self.get_speedy()  # Usamos el getter para obtener la velocidad en y

        # Si el meteorito se sale de la pantalla, lo reposicionamos aleatoriamente
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 22:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.set_speedy(random.randrange(1, 8))  # Cambiar la velocidad vertical al reposicionar

# Cargar fondo
background = pygame.image.load("assets/background.png").convert()

# Crear grupo de sprites
all_sprites = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()

# Crear instancia del jugador
player = Player()
all_sprites.add(player)

# Crear meteoritos
for i in range(8):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)

# Bucle principal del juego
running = True
while running:
    # Mantener el juego a 60 fps
    clock.tick(60)

    # Procesar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar todos los sprites
    all_sprites.update()

    # Dibujar / Renderizar
    screen.blit(background, [0, 0])  # Dibujar fondo
    all_sprites.draw(screen)  # Dibujar todos los sprites
    pygame.display.flip()  # Actualizar la pantalla

# Cerrar Pygame
pygame.quit()
