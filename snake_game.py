from tokenize import PlainToken
import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
# font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25)

RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4
    
class Point:
    
    def __init__(self, x, y, color):
        self.x = x
        self.y =y
        self.color = color
        self.outercolor = (color[0] + 20, color[1] + 20, color[2] + 20)
    

# rgb colors

WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

GREEN = (0,200,0)
PINK = (200,0,200)
PURPLE = (100,0,100)
BLUE = (0,0,200)
YELLOW = (200,200,0)
LIGHT_BLUE = (0,200,200)
ORANGE = (200,100,0)
DARK_RED = (100,0,0)


colors = [PINK,PURPLE,GREEN,BLUE,YELLOW,LIGHT_BLUE,ORANGE,DARK_RED]

BLOCK_SIZE = 20
SPEED = 20

class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = RIGHT
        
        self.head = Point(self.w/2, self.h/2, random.choice(colors))
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y, random.choice(colors)),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y,random.choice(colors))]
        self.snakepos = [(self.head.x,self.head.y),(self.head.x-BLOCK_SIZE, self.head.y), (self.head.x-(2*BLOCK_SIZE),self.head.y )]
        self.score = 0
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y, RED)
        if (x,y) in self.snakepos:
            self._place_food()
        
    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = UP
                elif event.key == pygame.K_DOWN:
                    self.direction = DOWN
        
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)
        self.snakepos.insert(0,(self.head.x, self.head.y))
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head.x == self.food.x and self.head.y == self.food.y:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
            self.snakepos.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score
    
    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if (self.head.x, self.head.y) in self.snakepos[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, pt.color, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display,pt.outercolor, pygame.Rect(pt.x+4, pt.y+4, 10, 10))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        
        if direction == RIGHT:
            x += BLOCK_SIZE
        elif direction == LEFT:
            x -= BLOCK_SIZE
        elif direction == DOWN:
            y += BLOCK_SIZE
        elif direction == UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y, random.choice(colors))
            

if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
        
        
    pygame.quit()