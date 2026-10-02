import pygame
import random

# ============================================================
# CONFIGURAÇÕES
# ============================================================

WIDTH = 800
HEIGHT = 600

FPS = 60

BACKGROUND_COLOR = (30, 30, 30)


# ============================================================
# PLAYER
# ============================================================

class Player:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Limites da tela
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (0, 200, 255),
            self.rect
        )


# ============================================================
# ENEMY
# ============================================================

class Enemy:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 2

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (220, 50, 50),
            self.rect
        )


# ============================================================
# BULLET
# ============================================================

class Bullet:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 15)
        self.speed = 8

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (255, 255, 0),
            self.rect
        )


# ============================================================
# GAME
# ============================================================

class Game:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption("Space Shooter")

        self.clock = pygame.time.Clock()

        self.running = True

        # Objetos do jogo
        self.player = Player(375, 500)

        self.enemies = [
            Enemy(100, 50),
            Enemy(300, 100),
            Enemy(600, 20),
            Enemy(500, 150),
            Enemy(200, 200)
        ]

        self.bullets = []

        # Pontuação
        self.score = 0

        # Fonte para mostrar o score
        self.font = pygame.font.Font(None, 36)

    # --------------------------------------------------------
    # EVENTOS
    # --------------------------------------------------------

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                # ESC fecha o jogo
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                # Espaço dispara
                if event.key == pygame.K_SPACE:

                    bullet_x = (
                        self.player.rect.centerx - 2
                    )

                    bullet_y = self.player.rect.top

                    bullet = Bullet(
                        bullet_x,
                        bullet_y
                    )

                    self.bullets.append(bullet)

    # --------------------------------------------------------
    # ATUALIZAÇÃO
    # --------------------------------------------------------

    def update(self):

        # Atualiza jogador
        self.player.update()

        # Atualiza inimigos
        for enemy in self.enemies:
            enemy.update()

        # Atualiza tiros
        for bullet in self.bullets:
            bullet.update()

        # Remove tiros que saíram da tela
        self.bullets = [
            bullet
            for bullet in self.bullets
            if bullet.rect.bottom > 0
        ]

        # Verifica colisões
        self.check_collisions()

        # Remove inimigos que saíram da tela
        self.enemies = [
            enemy
            for enemy in self.enemies
            if enemy.rect.top < HEIGHT
        ]

    # --------------------------------------------------------
    # COLISÕES
    # --------------------------------------------------------

    def check_collisions(self):

        # Percorremos uma cópia da lista
        # porque podemos remover objetos durante o loop.
        for bullet in self.bullets[:]:

            for enemy in self.enemies[:]:

                if bullet.rect.colliderect(enemy.rect):

                    print("ACERTOU!")

                    # Remove o tiro
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    # Remove o inimigo
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)

                    # Aumenta a pontuação
                    self.score += 1

                    # Um tiro só pode acertar
                    # um inimigo
                    break

    # --------------------------------------------------------
    # DESENHO
    # --------------------------------------------------------

    def draw(self):

        # Fundo
        self.screen.fill(BACKGROUND_COLOR)

        # Jogador
        self.player.draw(self.screen)

        # Inimigos
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Tiros
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # Score
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            score_text,
            (10, 10)
        )

        # Atualiza a tela
        pygame.display.flip()

    # --------------------------------------------------------
    # LOOP PRINCIPAL
    # --------------------------------------------------------

    def run(self):

        while self.running:

            # 1. Eventos
            self.handle_events()

            # 2. Atualização
            self.update()

            # 3. Desenho
            self.draw()

            # Controla FPS
            self.clock.tick(FPS)

        pygame.quit()


# ============================================================
# INÍCIO DO PROGRAMA
# ============================================================

if __name__ == "__main__":

    game = Game()

    game.run()
