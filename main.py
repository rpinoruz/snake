import pygame
import random
import math

pygame.init()
W, H = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("SNAKE")
clock = pygame.time.Clock()
running = True

class Snake(object):
    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.body = [
            {"x": 1, "y": 7},
            {"x": 2, "y": 7},
            {"x": 3, "y": 7}
        ]
        self.head = self.body[-1]
        self.scale = 40
        self.direction = "right"
        self.controls = {
            "up": [pygame.K_w, pygame.K_UP],
            "down": [pygame.K_s, pygame.K_DOWN],
            "left": [pygame.K_a, pygame.K_LEFT],
            "right": [pygame.K_d, pygame.K_RIGHT],
        }
        self.alive = True

    def draw(self):
        if not self.alive:
            return
        for block in self.body:
            pygame.draw.rect(
                self.screen, WHITE, (block["x"]*self.scale, block["y"]*self.scale, self.scale, self.scale))

    def move(self):
        new_head = self.head.copy()
        match self.direction:
            case "right":
                new_head["x"] += 1
            case "left":
                new_head["x"] -= 1
            case "up":
                new_head["y"] -= 1
            case "down":
                new_head["y"] += 1
        self.head = new_head.copy()
        self.body.append(new_head)
        self.body.pop(0)
        self.check_collision()

    def controller(self, key):
        if key in self.controls["up"]:
            self.direction = "up"
        if key in self.controls["down"]:
            self.direction = "down"
        if key in self.controls["left"]:
            self.direction = "left"
        if key in self.controls["right"]:
            self.direction = "right"

    def grow(self, food):
        new_head = {
            "x": food.x,
            "y": food.y
        }
        self.head = new_head.copy()
        self.body.append(new_head)

    def die(self):
        self.alive = False

    def check_collision(self):
        if (
            self.head["x"] < 0
            or self.head["x"] >= self.w // self.scale
            or self.head["y"] < 0
            or self.head["y"] >= self.h // self.scale
        ):
            self.die()

        for block in self.body[:-1]:
            if block["x"] == self.head["x"] and block["y"] == self.head["y"]:
                self.die()

    def update(self):
        self.move()
        self.draw()


class Food(object):
    def __init__(self, screen, snake):
        self.screen = screen
        self.snake = snake
        self.w, self.h = screen.get_size()
        self.eaten = True
        self.scale = 30
        self.offset = 5
        self.x, self.y = self.get_position().values()

    def is_inside_snake(self, x, y):
        for block in self.snake.body:
            if block["x"] == x and block["y"] == y:
                return True
        return False

    def get_position(self):
        max_x = self.w // self.snake.scale
        max_y = self.h // self.snake.scale
        x = random.randint(1, max_x - 1)
        y = random.randint(1, max_y - 1)
        while self.is_inside_snake(x, y):
            x = random.randint(1, max_x - 1)
            y = random.randint(1, max_y - 1)

        return {"x": x, "y": y}

    def get_eaten(self):
        if self.is_inside_snake(self.x, self.y):
            self.eaten = True
            self.snake.grow(self)
            self.x, self.y = self.get_position().values()
        self.eaten = False

    def draw(self):
        pygame.draw.rect(self.screen, RED, ((self.x * self.snake.scale) + self.offset,
                         (self.y * self.snake.scale) + self.offset, self.scale, self.scale))

    def update(self):
        self.get_eaten()
        self.draw()


snake = Snake(screen)
food = Food(screen, snake)

def reset_game():
    snake.__init__(screen)
    food.__init__(screen, snake)

game_over = False  # Variable to track the game over state
reset_pressed = False  # Variable to track if "R" key is pressed for reset

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if not snake.alive and game_over:
                    reset_game()
                    game_over = False
                    reset_pressed = True
            else:
                snake.controller(event.key)

    if not snake.alive:
        if not game_over and not reset_pressed:
            game_over = True
    else:
        reset_pressed = False

    screen.fill("black")
    snake.update()
    food.update()
    pygame.display.flip()
    clock.tick(5)

pygame.quit()
