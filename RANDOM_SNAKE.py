import pygame
from random import randint
SIZE_BLOCK = 20
PALE_GREEN = (152,251,152)

size = [360,350]
COUNT_BLOCKS = 16
MARGIN=1
def getR_COLOR():
    d=(randint(0,255),randint(0,255),randint(0,255))
    return(d)
SNAKE_COLOR,FRAME_COLOR,R_COLOR1,R_COLOR2=getR_COLOR(),getR_COLOR(),getR_COLOR(),getR_COLOR()
     

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')
timer = pygame.time.Clock()


class SnakeBlock:
    def __init__(self,x,y):
        self.x=x
        self.y=y
snake_blocks = [SnakeBlock(9,9), SnakeBlock(9,10)]
d_row=0
d_col=1
              
def draw_block(color,row,column):
    pygame.draw.rect(screen,color,[10+column*SIZE_BLOCK+MARGIN*(column+1),5+row*SIZE_BLOCK+MARGIN*(row+1),SIZE_BLOCK,SIZE_BLOCK])        
while True:
    for event in pygame.event.get():
        print (pygame.event.event_name(event.type))
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and d_col !=0:
                d_row = -1
                d_col = 0
            elif event.key == pygame.K_DOWN and d_col !=0:
                d_row = 1
                d_col = 0
            elif event.key == pygame.K_LEFT and d_row !=0:
                d_row = 0
                d_col = -1
            elif event.key == pygame.K_RIGHT and d_row !=0:
                d_row = 0
                d_col = 1

    screen.fill(FRAME_COLOR)

    for row in range(COUNT_BLOCKS):
        
        for column in range(COUNT_BLOCKS):
            
            if column%2==0 and row%2!=0:
                color=R_COLOR1
            elif column%2!=0 and row%2==0:
                color=R_COLOR1
    
            else:
                color=R_COLOR2
          

            
        
            draw_block(color,row,column)

    for block in snake_blocks:
        draw_block(SNAKE_COLOR,block.x,block.y)
    head = snake_blocks[-1]
    new_head = SnakeBlock(head.x + d_row, head.y + d_col)
    snake_blocks.append(new_head)
    snake_blocks.pop(0)

    pygame.display.flip()
    timer.tick(7)
