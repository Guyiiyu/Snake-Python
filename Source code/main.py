import sys
import pygame
import random

WindowSize = ( 720, 480 )
fontSize = 20
cellSize = 16
mpSize = int(WindowSize[0]/cellSize), int(WindowSize[1]/cellSize)
#蛇的速度
snakeSpeed = 10

#颜色定义
colorBlack = ( 0, 0, 0)
colorRed = ( 255, 0, 0)
colorGreen = ( 0, 255, 0)
colorBlue = ( 0, 0, 255)
colorDarkBlue = ( 0, 0, 120)

#方向定义
left = 0
down = 1
up = 2
right = 3

#入口函数
def main():
    pygame.init()
    screen = pygame.display.set_mode(WindowSize)
    pygame.display.set_caption("贪吃蛇小游戏~~")
    snakeClock = pygame.time.Clock()
    imgGameStart = pygame.image.load('./img/gameStart.jpg')

    while 1:
        showGameStartInfo(screen, imgGameStart)
        gameRunning(screen, snakeClock)
        
#展示游戏开始信息
def showGameStartInfo(screen, imgGameStart):
    font = pygame.font.Font("./font/msyh.ttc", fontSize)
    screen.blit(imgGameStart, (0,0))
    fontBuffer = font.render("按任意键开始游戏", True, colorRed)
    screen.blit(fontBuffer, (250, 300))
    fontBuffer = font.render("按q或ESC结束游戏", True, colorRed)
    screen.blit(fontBuffer, (250, 300 + fontSize))       
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            justiceGameOver(event)
            if event.type == pygame.KEYDOWN:
                return
       
#退出游戏
def terminate():
    pygame.quit()
    sys.exit()   

#展示游戏结束信息
def showGameOverInfo(screen, imgGameEnd, score):
    font = pygame.font.Font("./font/msyh.ttc", fontSize)
    screen.blit(imgGameEnd, (0,0))
    fontBuffer = font.render("你的得分是%s" % score, True, colorRed)
    screen.blit(fontBuffer, (250, 300 - fontSize))
    fontBuffer = font.render("按r重新开始游戏", True, colorRed)
    screen.blit(fontBuffer, (250, 300))
    fontBuffer = font.render("按q或ESC结束游戏", True, colorRed)
    screen.blit(fontBuffer, (250, 300 + fontSize))       
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            justiceGameOver(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return

#游戏运行主体
def gameRunning(screen, snakeClock):
    startxy = [random.randint(5, mpSize[0]-5), random.randint(5, mpSize[1]-5)]
    snake = [
        {'x':startxy[0], 'y':startxy[1]},
        {'x':startxy[0]-1, 'y':startxy[1]},
        {'x':startxy[0]-2, 'y':startxy[1]}
    ]
    direction = right
    score = 0
    food = CreateFood(screen)

    while True:
        if food not in snake:
            del snake[-1]
        else:
            score += 1
            food = CreateFood(screen)
        for event in pygame.event.get():
            justiceGameOver(event)
            direction = justiceSnakeTurn(event, direction)
        snakeMove(direction, snake)
        if not isSnakeAlive(snake):
            imgGameEnd = pygame.image.load('./img/gameEnd.jpg')
            showGameOverInfo(screen, imgGameEnd, score)
            return
        screen.fill(colorBlack)
        DrawFood(screen, food)
        DrawSnake(screen, snake)
        DrawScore(screen, score)
        pygame.display.update()
        
        snakeClock.tick(snakeSpeed)

#判断蛇是否活着 超出边界 吃到自己就是死
def isSnakeAlive(snake):
    if snake[0]['x'] == -1 or snake[0]['x'] == mpSize[0] or snake[0]['y'] == -1 or snake[0]['y'] == mpSize[1]:
        return False
    elif snake[0] in snake[1:]:
        return False
    return True

#蛇移动
def snakeMove(direction, snake):
    if direction == left:
        tmp = {'x':snake[0]['x']-1, 'y':snake[0]['y']}
    elif direction == down:
        tmp = {'x':snake[0]['x'], 'y':snake[0]['y']+1}
    elif direction == up:
        tmp = {'x':snake[0]['x'], 'y':snake[0]['y']-1}
    elif direction == right:
        tmp = {'x':snake[0]['x']+1, 'y':snake[0]['y']}

    snake = snake.insert(0, tmp)
#画出蛇
def DrawSnake(screen, snake):
    for i in snake:
        x = i['x'] * cellSize
        y = i['y'] * cellSize
        tmp = (x, y, cellSize, cellSize)
        pygame.draw.rect(screen, colorDarkBlue, tmp)
        tmp = (x+3, y+3, cellSize-6, cellSize-6)
        pygame.draw.rect(screen, colorBlue, tmp)


#创造食物
def CreateFood(screen):
    xy = {'x':random.randint(0, mpSize[0]-1), 'y':random.randint(0, mpSize[1]-1)}
    return xy
#画出食物
def DrawFood(screen, xy):
    x = xy['x'] * cellSize
    y = xy['y'] * cellSize
    appleRect = (x, y, cellSize, cellSize)
    pygame.draw.rect(screen, colorGreen, appleRect)
#画出分数
def DrawScore(screen, score):
    font = pygame.font.Font("./font/msyh.ttc", fontSize)
    fontBuffer = font.render("得分:%s" % score, True, colorRed)
    screen.blit(fontBuffer, (600 ,0))

#判断蛇转弯的方向
def justiceSnakeTurn(event, direction):
    if event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_LEFT, pygame.K_a) and direction != right:
            direction = left
        elif event.key in  (pygame.K_RIGHT, pygame.K_d) and direction != left:
            direction = right
        elif event.key in (pygame.K_UP, pygame.K_w) and direction != down:
            direction = up
        elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != up:
            direction = down

    return direction

#判断游戏是否应该结束
def justiceGameOver(event):
    if event.type == pygame.QUIT:
        terminate()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            terminate()
        

main()