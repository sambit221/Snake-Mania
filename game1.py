import pygame
import random
import os

pygame.mixer.init()

pygame.init()

#colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)
lime = (0, 255, 0)
blue = (0, 0, 255)

#creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#Background image edit section--------------------------
bging = pygame.image.load("snake.jpg")
bging = pygame.transform.scale(bging, (screen_width, screen_height)).convert_alpha()

#game title
pygame.display.set_caption("Snake Mania")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,220,229))
        text_screen("Welcome to Snake mania", black, 200, 220)
        text_screen("Enter Space Bar to Play", black, 200, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #music edit section-----------------------------------
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)


#Game loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    #Check if highScore file exist
    if(not os.path.exists("highScore.txt")):
        with open("highScore.txt", "w") as f:
            f.write("0")

    with open("highScore.txt", "r") as f:
        highScore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 5
    # size of snake can be changed here--------------------
    snake_size = 18
    # Game speed can be controlled over here
    fps = 60
    while not exit_game:
        if game_over:
            with open("highScore.txt", "w") as f:
                f.write(str(highScore))
            gameWindow.fill((233,220,229))
            text_screen("Game over! Press Enter To Continue" , red, 100, 250)
            text_screen("Score: " + str(score) , red, 5, 5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key ==pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key ==pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key ==pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key ==pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
# cheat code to increase score on pressing q--------------------------
                   # if event.key == pygame.K_q:
                    #    score += 5

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) <8 and abs(snake_y - food_y)<8:
                score +=10
                print("score: ",score)

                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                #here the rate of increase in snake length is controlled-----------
                snk_length +=4
                if score> int(highScore):
                    highScore = score

            gameWindow.fill((200,220,229))
            gameWindow.blit(bging, (0, 0))

            text_screen("Score: " + str(score) + "      High Score: "+ str(highScore), red, 5, 5)
            pygame.draw.rect(gameWindow, blue, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

                if head in snk_list[: -1]:
                    game_over = True
                    pygame.mixer.music.load('gameOver.mp3')
                    pygame.mixer.music.play()

                if((snake_x<0) or (snake_x > screen_width) or (snake_y<0) or (snake_y > screen_height)):
                    game_over = True
                    pygame.mixer.music.load('gameOver.mp3')
                    pygame.mixer.music.play()
                    print("Game Over")

            #pygame.draw.rect(gameWindow, red, (food_x, food_y, snake_size, snake_size))
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
gameloop()
