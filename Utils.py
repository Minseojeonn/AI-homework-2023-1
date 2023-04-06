import pygame  # pygame 모듈의 임포트
import sys  # 외장 모듈
import argparse
import random
from pygame.locals import *  # QUIT 등의 pygame 상수들을 로드한다.


def draw_grid(game_world, WIDTH, HEIGHT, vertical, stripe):
    col_CELL_SIZE = int(HEIGHT / stripe)
    row_CELL_SIZE = int(WIDTH / vertical)
    for column_index in range(vertical):
        for row_index in range(stripe):
            pygame.draw.rect(game_world, (0, 0, 0, 0),
                             pygame.Rect(column_index * row_CELL_SIZE, row_index * col_CELL_SIZE, row_CELL_SIZE,
                                         col_CELL_SIZE), 1)


# colum = 세로
# row = 가로





def fill_block(game_world, width, height, vertical, stripe, grid):
    col_CELL_SIZE = int(width / vertical)
    row_CELL_SIZE = int(height / stripe)
    font1 = pygame.font.SysFont(None, 30)
    for column_index in range(stripe):
        for row_index in range(vertical):
            mark = grid[row_index][column_index]
            if mark == 'block':
                x_image = pygame.image.load('Rock.png')
                x_image = pygame.transform.scale(x_image, (row_CELL_SIZE,col_CELL_SIZE))
                game_world.blit(x_image, (column_index * row_CELL_SIZE , row_index * col_CELL_SIZE))
            if mark == 'load':
                x_image = pygame.image.load('path.png')
                x_image = pygame.transform.scale(x_image, (row_CELL_SIZE,col_CELL_SIZE))
                game_world.blit(x_image, (column_index * row_CELL_SIZE , row_index * col_CELL_SIZE))


def make_random_blocks(grid, inc_obstacle_ratio):
    block_vertical = len(grid)
    block_stripe = len(grid[0])
    block_count = block_vertical * block_stripe
    huddle_num = int(block_count * inc_obstacle_ratio)
    for i, gr in enumerate(grid):
        for j, g in enumerate(gr):
            if grid[i][j] == 'block':
                grid[i][j] = []

    while huddle_num > 0:
        randomint_stripe = random.randrange(0, block_stripe)
        randomint_vertical = random.randrange(0, block_vertical)
        if grid[randomint_vertical][randomint_stripe] == []:
            grid[randomint_vertical][randomint_stripe] = 'block'
            huddle_num = huddle_num - 1


def make_bound_block(grid):
    for i, gr in enumerate(grid):
        grid[i].append('block')
        grid[i].insert(0, 'block')
    upper_down_block = ['block' for _ in range(len(grid[i]))]
    grid.insert(0, upper_down_block)
    grid.append(upper_down_block)


def find_star_and_door(grid):
    door = None
    star = None

    for gr in grid:
        #print(gr)
        pass

    for i, gr in enumerate(grid):
        for j, g in enumerate(gr):
            if grid[i][j] == 'door':
                door = (i, j)
            if grid[i][j] == 'star':
                star = (i, j)

    if door is None or star is None:
        print("there is no door or Star!")
        exit()
    else:
        return star, door


def fill_path(grid,loads):
    for load in loads[1:-1]:
        grid[load[0]-1][load[1]-1] = 'load'