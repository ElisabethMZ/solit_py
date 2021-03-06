import pygame
import solit_random
import numpy as np
import solit_options
import matplotlib.pyplot as plt
import time
import backtrack
import policy_playing

# settings
fps = 600
wait_time = 200
number_of_games = 1
current_function = "backtrack"
functions = {
    "backtrack": backtrack.play_move_to_victory,
    "lookahead1": solit_options.make_move,
    "lookahead2": solit_options.make_move_2,
    "random": solit_random.make_random_move,
    "policy": policy_playing.policy_move,
    "policy2": policy_playing.policy_move_2
}

print("The current settings are ")
print("fps =  ", fps)
print("wait time = ", wait_time)
print("number of games  = ", number_of_games)
print("current function = ", current_function)

update = input("Change Settings? (y/n)")
if update == "y":
    fps = int(input("Enter fps: "))
    wait_time = int(input("Enter wait time: "))
    number_of_games = int(input("Enter number of games: "))
    current_function = input("Enter current_function: (backtrack, lookahead1, lookahead2, policy, policy2, random)")
# end settings

start_time = time.time()  # fix starting time to calculate elapsed time
x_max, y_max = 350, 350  # horizontal, vertical
WHITE, BLACK, GREY = (255, 255, 255), (0, 0, 0), (122, 122, 122)

pygame.init()  # initialize
screen = pygame.display.set_mode([x_max, y_max])  # screen dimensions
clock = pygame.time.Clock()  # time
done = False

coordinates = []  # center of circles
colors = [0 for i in range(33)]  # colors of circles
for i in range(0, 7):
    coordinates.append((150,100+i*30))
    coordinates.append((180,100+i*30)) 
    coordinates.append((210,100+i*30))
    if (i < 2) or (i > 4):
        continue
    coordinates.append((90,100+i*30))
    coordinates.append((120,100+i*30))
    coordinates.append((240,100+i*30))
    coordinates.append((270,100+i*30))
    
indices = [0, 1, 2, 3, 4, 5, 9, 10, 6, 7, 8, 11,
           12, 16, 17, 13, 14, 15, 18, 19, 23, 24,
           20, 21, 22, 25, 26, 27, 28, 29, 30, 31, 32]  # order of coordinates init vs. canonical init


def transform_colors(board_array):
    counter = 0
    for j in range(0, len(board_array)):
        if board_array[j] != 0:
            colors[indices[counter]] = board_array[j]
            counter += 1


pins_left = []
#  find solution with backtracking
backtrack.solve_solitaer()
solit_random.board = solit_random.start_board.copy()
while not done: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            done = True
                   
    screen.fill(GREY)  # grey background
    transform_colors(solit_random.board.flatten())

    for i in range(0, len(coordinates)):  # draw circles (will be drawn 60 times per second)
        if colors[i] == 2:
            pygame.draw.circle(screen, BLACK, coordinates[i], 11)
        elif colors[i] == 1:
            pygame.draw.circle(screen, WHITE, coordinates[i], 11)

    pygame.display.flip()  # update screen
    pygame.time.wait(wait_time) # delay in ms in case you want to watch the game being played live
    clock.tick(fps)  # fps # increase to decrease runtime(simple solvers), caps eventually

    if functions[current_function]() == 0:  # solver (make_move()) performs a move and returns 1, else returns 0
        pins_left.append((solit_random.board == 2).sum())  # calculate remaining pins
        solit_random.board = np.array(solit_random.start_board)

    if len(pins_left) == number_of_games:   # set the number of games to be played
        break
pygame.quit()  # quits the game

runs = len(pins_left)
mean = np.mean(pins_left)  # now print histogram and time
n, bins, patches = plt.hist(pins_left, 31, (1, 32), density=True, histtype='bar', facecolor='g', alpha=0.75, label = 'mean = ' + str(mean))
plt.xlabel('Number of Pins')
plt.ylabel('Probability')
plt.title('Histogram of remaining pins')
plt.xlim(0, 27)
# plt.ylim(0, 0.28) #zooms in, use when you expect a top probability of < 0.25
plt.grid(True)
elapsed_time = time.time() - start_time
plt.plot([], [], ' ', label="elapsed time = " + "{0:.2f}".format(elapsed_time) + "s")
plt.plot([], [], ' ', label="# of runs = " + str(runs))
plt.legend(handlelength=0)
plt.show()
