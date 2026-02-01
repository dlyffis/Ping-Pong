from random import random
import pygame

class Sprite:
    def __init__(self, center, image):
        self.image = image
        self.rect = image.get_frect()
        self.rect.center = center

    def render(self, surface):
        surface.blit(self.image, self.rect)
        # на чём         что         где


class Player(Sprite):
    def __init__(self, center, image, speed):
        super().__init__(center, image)
        self.start_center = center
        self.speed = speed
        self.is_move_up = False
        self.is_move_down = False
    
    def reset(self):
        self.rect.center = self.start_center
        self.move_up = False
        self.move_down = False
    
    def update(self):
        if self.is_move_up != self.is_move_down:
            if self.is_move_up:
                self.rect.y -= self.speed 
            else:
                self.rect.y += self.speed

        
        
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600


class Ball(Sprite):
    def __init__(self, center, image, speed):
        super().__init__(center, image)
        self.start_center = center
        self.start_speed = speed
        self.speed = speed
        self.velocity = pygame.Vector2(1, 0)

    def reset(self):
        self.rect.center = self.start_center
        self.speed = self.start_speed 
        self.velocity.update(1, 0)

    def check_x_collision(self, player):
        if self.rect.colliderect(player.rect):
            if self.velocity.x > 0:
                self.rect.right = player.rect.left

            else:
                self.rect.left = player.rect.right
            self.velocity.x =- self.velocity.x
            self.velocity.rotate_ip( (random() - 0.5) * 30 )
            self.speed += 0.8
            
    
    def check_y_collision(self, player):
        if self.rect.colliderect(player.rect):
            if self.velocity.y > 0:
                self.rect.bottom = player.rect.top

            else:
                self.rect.top = player.rect.bottom
            self.velocity.y =- self.velocity.y

    def update(self, left_player, right_player):
        vector = self.velocity * self.speed
        
        self.rect.x += vector.x
        self.check_x_collision(left_player)
        self.check_x_collision(right_player)


        self.rect.y += vector.y
        self.check_y_collision(left_player)
        self.check_y_collision(right_player)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity.y = -self.velocity.y

        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.velocity.y = -self.velocity.y
        



pygame.init()
window = pygame.Window('Ping Pong',(800, 600), pygame.WINDOWPOS_CENTERED)

surface = window.get_surface()
clock = pygame.Clock()
font = pygame.Font(None, 32)

image = pygame.Surface( (40, 100) )
image.fill('blue')
left_player = Player( (40,300), image, 7)
right_player = Player( (800-40,300), image, 7)

image = pygame.Surface( (20,20) )
image.fill('white')
pygame.draw.aacircle(image, 'green', (10,10), 10)
ball = Ball( (400,300), image, 5)

running = True

right_score = 0
left_score = 0

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: 
                left_player.is_move_up = True
            elif event.key == pygame.K_s: 
                left_player.is_move_down = True
            if event.key == pygame.K_UP: 
                right_player.is_move_up = True
            elif event.key == pygame.K_DOWN: 
                right_player.is_move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w: 
                left_player.is_move_up = False
            elif event.key == pygame.K_s: 
                left_player.is_move_down = False
            if event.key == pygame.K_UP: 
                right_player.is_move_up = False
            elif event.key == pygame.K_DOWN: 
                right_player.is_move_down = False
    # Обновление объектов
    left_player.update()
    right_player.update()
    ball.update(left_player,right_player)

    if ball.rect.right >= 800:
        left_score += 1
        left_player.reset()
        right_player.reset()
        ball.reset()
    if ball.rect.left <= 0:
        right_score += 1
        left_player.reset()
        right_player.reset()
        ball.reset()
    #if ball.rect.colliderect(left_player.rect) or ball.rect.colliderect(right_player.rect):
    #    ball.velocity.x -= ball.velocity.x

    # Отрисовка
    # RGB - (0-255, 0-255, 0-255)
    # цвет в кавычках - 'red'
    surface.fill('white')

    left_player.render(surface)
    right_player.render(surface)
    ball.render(surface)

    text = f"{left_score}:{right_score}"
    text_image = font.render(text, True, 'black')
    xy = (400 - text_image.get_width()/2, 10)
    surface.blit(text_image, xy)
    
    window.flip()
    clock.tick(60)
    window.title = 'FPS:' + str(round(clock.get_fps()))
