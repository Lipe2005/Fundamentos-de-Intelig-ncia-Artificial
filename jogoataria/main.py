# pyrefly: ignore [missing-import]
import pygame
import sys
from settings import *
from sprites import Player, Asteroid

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("arial", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def main():
    # Inicializando o Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo Atari - Defesa Espacial")
    clock = pygame.time.Clock()

    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    # Criando o jogador
    player = Player()
    all_sprites.add(player)

    score = 0
    running = True
    game_over = False

    # Dificuldade progressiva
    difficulty_level = 0   # Sobe a cada 50 pontos
    spawn_interval = SPAWN_INTERVAL_INITIAL
    asteroid_speed = ASTEROID_SPEED_INITIAL

    # Evento para gerar asteroides de tempo em tempo
    SPAWN_ASTEROID = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_ASTEROID, spawn_interval)

    while running:
        # Manter a taxa de frames correta
        clock.tick(FPS)

        # Processamento de Eventos (entradas do teclado/janela)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    projectile = player.shoot()
                    all_sprites.add(projectile)
                    projectiles.add(projectile)
            
            if event.type == SPAWN_ASTEROID and not game_over:
                asteroid = Asteroid()
                all_sprites.add(asteroid)
                asteroids.add(asteroid)

        # Atualização do estado do jogo
        if not game_over:
            all_sprites.update()

            # Checar colisão entre projétil e asteroide
            # O groupcollide retorna um dicionário se baterem. Os "True" fazem com que ambos sumam.
            hits = pygame.sprite.groupcollide(asteroids, projectiles, True, True)
            for hit in hits:
                score += 10 # Aumenta 10 pontos a cada acerto

            # Checar se o asteroide chegou no fundo
            for asteroid in asteroids:
                if asteroid.rect.top > HEIGHT:
                    game_over = True
            
            # Checar colisão entre jogador (nave) e asteroide
            if pygame.sprite.spritecollide(player, asteroids, False):
                game_over = True

        # Desenho
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        # Exibição de pontuação
        draw_text(screen, f"Pontos: {score}", 30, 10, 10)

        # Exibição de game over
        if game_over:
            draw_text(screen, "FIM DE JOGO", 64, WIDTH // 2 - 150, HEIGHT // 2 - 50)
            draw_text(screen, "Feche a janela para sair", 22, WIDTH // 2 - 100, HEIGHT // 2 + 30)

        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
