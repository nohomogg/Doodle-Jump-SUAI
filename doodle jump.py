import random
import pygame
import sprites


class Game:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Doodle Jump by Gavinek Gleb')
        self.big_font = pygame.freetype.Font('Font.ttf', 75)
        self.middle_font = pygame.freetype.Font('Font.ttf', 40)
        self.small_font = pygame.freetype.Font('Font.ttf', 25)

        self.highscore = 0
        self.speed = 0
        self.player = None
        self.on_ground = False

        self.menu()

    def draw_overlay(self):
        pygame.draw.rect(self.screen, (2, 94, 115), (0, 0, 150, 800), 0)
        pygame.draw.rect(self.screen, (2, 94, 115), (650, 0, 150, 800), 0)
        pygame.draw.rect(self.screen, (1, 31, 38), (0, 0, 150, 800), 10)
        pygame.draw.rect(self.screen, (1, 31, 38), (650, 0, 150, 800), 10)

    def draw_menu_header(self):
        text_surf, _ = self.big_font.render('Doodle Jump', (0, 0, 0))
        self.screen.blit(text_surf, (170, 200))

        text_surf, text_rect = self.small_font.render(f'Highscore: {self.highscore}', (0, 0, 0))
        self.screen.blit(
            text_surf,
            (
                (self.screen.get_rect().w - text_rect.w) / 2,
                300,
            ),
        )

    def menu(self):
        play_button = sprites.Button(400, 540, 'Play', self.middle_font)

        menu_run = True
        while menu_run:

            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.be_inside(mouse_pos[0], mouse_pos[1]):
                        menu_run = self.game()

            play_button.update(mouse_pos[0], mouse_pos[1])

            self.screen.fill((165, 166, 146))
            self.draw_overlay()
            self.draw_menu_header()
            self.screen.blit(play_button.image, play_button.rect)
            pygame.display.flip()

            self.clock.tick(60)

    def boundaries(self, platforms):
        for platform in platforms.sprites():
            if (
                self.player.rect.right >= platform.rect.left and
                self.player.rect.left <= platform.rect.right and
                platform.rect.bottom >= self.player.rect.bottom >= platform.rect.top
            ):
                if self.speed >= 0:
                    self.speed = 0
                    self.on_ground = True

    def draw_result(self, score):
        text_surf, _ = self.small_font.render(f'Score: {score}', (0, 0, 0))
        self.screen.blit(text_surf, (20, 50))

    def game(self):

        self.player = sprites.Sprite(400, 500, 50, 50, 'player.png')
        power = 13
        platforms = pygame.sprite.Group(
            [sprites.Sprite(random.randint(230, 550), (i * 100) + 100, 200, 20, 'platform.png') for i in range(10)]
        )

        upper_platform = platforms.sprites()[0]

        self.speed = 0
        score = 0
        game_run = True
        fail = False

        while game_run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.rect.x -= 5
            if keys[pygame.K_d]:
                self.player.rect.x += 5

            self.player.rect.y += self.speed

            if not self.on_ground:
                self.speed += 1
            else:
                self.speed = -power
                self.on_ground = False

            for platform in platforms.sprites():
                if self.speed < 0:
                    platform.rect.y -= self.speed
                if platform.rect.y > 820:
                    platform.kill()
                    score += 1

            if upper_platform.rect.y > 100:
                upper_platform = sprites.Sprite(random.randint(230, 550), 0, 200, 20, 'platform.png')
                platforms.add(upper_platform)

            if self.player.rect.y > 820:
                game_run = False
                fail = True

            self.boundaries(platforms)

            self.screen.fill((165, 166, 146))
            self.draw_overlay()
            self.draw_result(score)
            platforms.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            pygame.display.flip()
            self.clock.tick(60)

        if score > self.highscore:
            self.highscore = score

        return fail

Game()