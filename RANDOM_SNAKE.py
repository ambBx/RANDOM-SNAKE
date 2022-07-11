import pygame
import sys
from random import randint
import pygame_menu
from time import sleep

pygame.init()
courier = pygame.font.SysFont("Courier", 20)  # выбераем размер шрифта

font = pygame.font.SysFont("Open Sans", 25)

SIZE_BLOCK = 20
PALE_GREEN = (152, 251, 152)

size = [350, 450]
COUNT_BLOCKS = 16
MARGIN = 1
snake_blocks = []
scores = []


def getR_COLOR():
    d = (randint(0, 255), randint(0, 255), randint(0, 255))
    return(d)


def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [5 + column * SIZE_BLOCK + MARGIN * (
        column + 1), 5 + row * SIZE_BLOCK + MARGIN * (
        row + 1), SIZE_BLOCK, SIZE_BLOCK])


screen = pygame.display.set_mode(size)
pygame.display.set_caption('Zмейка')
timer = pygame.time.Clock()




class SnakeBlock:
    length = None
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(
            other, SnakeBlock) and self.x == other.x and self.y == other.y


def getRandomEmptyBlock():
    x = randint(0, COUNT_BLOCKS - 1)
    y = randint(0, COUNT_BLOCKS - 1)
    empty_block = SnakeBlock(x, y)
    while empty_block in snake_blocks:
        empty_block.x = randint(0, COUNT_BLOCKS - 1)
        empty_block.y = randint(0, COUNT_BLOCKS - 1)
    return empty_block


def showMenu():
    menuTheme = pygame_menu.Theme(background_color=getR_COLOR(),
                                  title_background_color=getR_COLOR(),
                                  title_font_shadow=True,
                                  widget_padding=25)
    menu = pygame_menu.Menu('Zzzмейка', 350, 450,
                            theme=menuTheme)

    name_box = menu.add.text_input(
        'Имя :', default='Борис', onchange=getPlayerName)

    #menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)

    menu.add.button('Играть', start_the_game, name_box)
    menu.add.button('Выход', pygame_menu.events.EXIT)
    menu.mainloop(screen)


def getPlayerName(value):
    player_name = value

def write_scores(name, score, filename='high_scores.txt'):
    with open(filename, 'a+') as fh:
        line = '%s %d\n' % (str(name), int(score))
        fh.write(line)

def read_scores(filename='high_scores.txt'):
    with open(filename, 'rU') as fh:
        scores = []
    
        for line in fh:
            name , _, score = line.partition(' ')
            name = name.strip()
            score = int(score.strip())
            scores.append((name, score))
    
        return scores

def gameOver(PLAYER_NAME, total):
    screen.fill(getR_COLOR())


    text_player_name = font.render(f"Игрок: {PLAYER_NAME}", 0, (255, 255, 255))
    screen.blit(text_player_name, (SIZE_BLOCK * 5, SIZE_BLOCK * 7))

    text_total = font.render(f"Очки: {total}", 0, (255, 255, 255))
    screen.blit(text_total, (SIZE_BLOCK * 5, SIZE_BLOCK * 9))

    write_scores(PLAYER_NAME,total)

    pygame.display.flip()
    sleep(3)
    showHighScores()
    sleep(3)
    showMenu()

def showHighScores():
    screen.fill(getR_COLOR())
    scores=read_scores()
    for name, score in enumerate(scores):
        i=SIZE_BLOCK
        text_line = font.render(f"{name}   {score} ", True, (255, 255, 255))
        screen.blit(text_line, (SIZE_BLOCK*2, SIZE_BLOCK*5+i))
        pygame.display.flip()
        i=i+i
    #screen.blit(text_line, (SIZE_BLOCK*2, SIZE_BLOCK*5+i))
    pygame.display.flip()


def start_the_game(namebox):
    PLAYER_NAME = namebox.get_value()
    SnakeBlock.length = 3
    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    food = getRandomEmptyBlock()
    d_row = 0
    d_col = 1
    speed = 1
    total = 0  
    SNAKE_COLOR, FRAME_COLOR, R_COLOR1, R_COLOR2 = getR_COLOR(
    ), getR_COLOR(), getR_COLOR(), getR_COLOR()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    d_row = -1
                    d_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    d_row = 1
                    d_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    d_row = 0
                    d_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    d_row = 0
                    d_col = 1

        screen.fill(FRAME_COLOR)

        text_total = courier.render(
            f"Очки: {total}", 0, (255, 255, 255))
        screen.blit(text_total, (SIZE_BLOCK, 20 * SIZE_BLOCK))

        text_speed = courier.render(
            f"Уровень: {speed}", 0, (255, 255, 255))
        screen.blit(text_speed, (10 * SIZE_BLOCK, 20 * SIZE_BLOCK))

        text_player_name = courier.render(
            f"Игрок: {PLAYER_NAME}", 0, (255, 255, 255))
        screen.blit(text_player_name, (SIZE_BLOCK, 18 * SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                # шашечки
                if column % 2 == 0 and row % 2 != 0:
                    color = R_COLOR1
                elif column % 2 != 0 and row % 2 == 0:
                    color = R_COLOR1

                else:
                    color = R_COLOR2

                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            gameOver(PLAYER_NAME, total)

        FOOD_RCOLOR = getR_COLOR()
        draw_block(FOOD_RCOLOR, food.x, food.y)

        if food == head:
            speed = total // 2 + 1
            total += 1  
            SnakeBlock.length += 10
            #snake_blocks.append(food)
            food = getRandomEmptyBlock()

        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        new_head = SnakeBlock(head.x + d_row, head.y + d_col)
        if new_head in snake_blocks:
            gameOver(PLAYER_NAME, total)
        snake_blocks.append(new_head)

        if SnakeBlock.length < len(snake_blocks):
            snake_blocks.pop(0)
        

        pygame.display.flip()
        timer.tick(5 + speed)


showMenu()
