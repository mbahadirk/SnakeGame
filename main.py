import random
import pygame
import sys
from classes import Box
from classes import Snake

# initalize pygame
pygame.init()

# key initialize
keys = pygame.key.get_pressed()

# font
font = pygame.font.Font(None, 30)

# window size
windowWidth = 1000
windowHeight = 1000
emptySpace = 200
boxLength = 30

# window initialize
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Snake Game")

# matrix
matrixBox = [[None for i in range(20)] for j in range(20)]
matrixSnake = [[None for i in range(20)] for j in range(20)]

# Create a matrix of alternating black and white boxes
for i in range(20):
    for j in range(20):
        if (i + j) % 2 == 0:
            matrixBox[i][j] = Box(i * boxLength + emptySpace, j * boxLength + emptySpace, boxLength, boxLength, (10,10,10), i, j)
        else:
            matrixBox[i][j] = Box(i * boxLength + emptySpace, j * boxLength + emptySpace, boxLength, boxLength, (20,20,20), i, j)

# Create a matrix of alternating black and white boxes
for i in range(20):
    for j in range(20):
        matrixSnake[i][j] = Snake(i * boxLength + emptySpace, j * boxLength + emptySpace, None, None, None)

# snake
snakeSize = 0
snakeColor = "orange"
snakeList = []
snakePositions = [[segment.row, segment.col] for segment in snakeList]
snake = Snake(10, 10, snakeColor, headX=0, headY=0)
snakeList.append(snake)

# apple
eaten = True

# game settings
run = True
alive = True
spacePressed = False
clock = pygame.time.Clock()
ticking = 8     # 8 is default
bestScore = [None for _ in range(3)]
levelIndex = 0   # 0 is default

def gameMode(level):
    global ticking, gameLevel,levelIndex
    _list = ["easy","normal","hard"]
    gameLevel = _list[level]
    levelIndex = level
    ticking = 8 + level*4
gameMode(0)

# # bestScore import
with open("log.txt", "w+") as file:
    try:
        file.seek(0)
        lines = file.readlines()
        for index in range(0,3):
            bestScore[index] = int(lines[index])
    except IndexError:
        file.write("0\n0\n0")
        file.seek(0)
        lines = file.readlines()
        for index in range(0, 3):
            bestScore[index] = int(lines[index])


# random apple locate
def newApple():
    global appleRow, appleCol
    while True:
        appleRow = random.randint(0, 19)
        appleCol = random.randint(0, 19)
        snakePositions = [[segment.row, segment.col] for segment in snakeList]
        # if apple and snake is in same pos change it
        if [appleRow, appleCol] not in snakePositions:
            break

newApple()


def drawScore():
    global snakeSize, bestScore
    scoreText = font.render(f"Score : {snakeSize}", True, (255, 255, 255))
    bestScoreText = font.render(f"Game Mode : {gameLevel}   Best Score : {bestScore[levelIndex]}", True, (255, 255, 255))
    screen.blit(scoreText, ((windowWidth / 2 - 50), 50))
    screen.blit(bestScoreText, ((windowWidth / 2 - 250), 100))

def gameOverText():
    global snakeSize
    text = font.render(f"Game Over", True, (255,255,255))
    resetText = font.render(f"press _space or _enter to restart game", True, (255,255,255))
    screen.blit(text,((windowWidth/2-60),150))
    screen.blit(resetText,((windowWidth/2-60),800))

def resetGame():
    global alive, snakeList, snakePositions, snakeSize, matrixSnake,snake, snakeColor
    alive = True
    snake = None
    snake = Snake(10, 10, snakeColor, headX=0, headY=0)
    snakeList = []
    snakeList.append(snake)
    snakeSize = 0
    snakePositions = [[segment.row, segment.col] for segment in snakeList]
    newApple()

# texts
startText = font.render("Start Game",True,"white")
quitText = font.render("Quit Game",True,"white")
easyText = font.render("easy",True,"white")
normalText = font.render("normal",True,"white")
hardText = font.render("hard",True,"white")

intro = True
level_select = False
# in the beginning its start game
selected_option = 0
selected_level = None
# debounce time
last_space_press_time = 0
debounce_interval = 950
startScreen = True

def draw_menu():
    if startScreen:
        screen.blit(startText, ((windowWidth / 2 - 100), (windowHeight / 2 - 50)))
        screen.blit(quitText, ((windowWidth / 2 - 100), (windowHeight / 2 + 100)))
        pygame.draw.rect(screen, "grey",
                         (windowWidth / 2 - 120, (windowHeight / 2 - 30) + selected_option * 150, 200, 1), 3)
    elif level_select:
        screen.blit(easyText, ((windowWidth / 2 - 60), (windowHeight / 2 - 50)))
        screen.blit(normalText, ((windowWidth / 2 - 70), (windowHeight / 2 + 50)))
        screen.blit(hardText, ((windowWidth / 2 - 60), (windowHeight / 2 + 150)))
        pygame.draw.rect(screen, "grey",
                         (windowWidth / 2 - 90, (windowHeight / 2 - 25) + selected_option * 100, 220, 1), 3)


while intro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if startScreen:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_option = (selected_option + 1) % 2
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_option = (selected_option - 1) % 2
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        startScreen = False
                        level_select = True
                    else:
                        pygame.quit()
                        sys.exit()
            elif level_select:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_option = (selected_option + 1) % 3
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_option = (selected_option - 1) % 3
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        gameMode(0)
                        intro = False
                    elif selected_option == 1:
                        gameMode(1)
                        intro = False
                    else:
                        gameMode(2)
                        intro = False
    screen.fill("black")

    draw_menu()

    pygame.display.update()
    clock.tick(ticking)


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                snake.headY = -1
                snake.headX = 0
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                snake.headY = 1
                snake.headX = 0
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                snake.headX = 1
                snake.headY = 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                snake.headX = -1
                snake.headY = 0
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                spacePressed = True


    screen.fill("black")

    # Draw the matrix of black and white boxes
    for i in range(20):
        for j in range(20):
            matrixBox[i][j].drawBox(screen)

    # snake-apple collision
    if (appleRow == snake.row) and (appleCol == snake.col):
        eaten = True
        newApple()
        snakeSize += 1

    # create a new apple when ate
    if eaten:
        newApple()
        eaten = False
    else:
        if alive == True:
            del snakeList[-1]


    # follow the snake tail you have to change the color here
    for segment in snakeList:
        matrixSnake[segment.row][segment.col].drawBox(screen,snakeColor)

    # check for bite
    for segment in snakeList[1:]:
        if snake.row == segment.row and snake.col == segment.col:
            alive = False

    # check alive situation
    if alive:
        snake.move()
    else:
        if snakeSize > bestScore[levelIndex]:
            bestScore[levelIndex] = snakeSize
            with open("log.txt", "w+") as file:
                file.seek(0)
                file.write(f"{bestScore[0]}\n{bestScore[1]}\n{bestScore[2]}")
        gameOverText()
        if spacePressed:    # press space for reset game
            resetGame()
            spacePressed = False

    # insert the head to the list
    newHead = Snake(snake.row, snake.col, snakeColor, snake.headX, snake.headY)
    snakeList.insert(0, newHead)

    matrixBox[appleRow][appleCol].drawBox(screen, "red")  # draw the apple
    drawScore()

    pygame.display.update()
    clock.tick(ticking)