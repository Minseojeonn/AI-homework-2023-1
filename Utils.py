import pygame # pygame 모듈의 임포트
import sys # 외장 모듈
import argparse
from pygame.locals import * # QUIT 등의 pygame 상수들을 로드한다.

def draw_grid(game_world, WIDTH, HEIGHT, vertical, stripe):
    col_CELL_SIZE=int(WIDTH/vertical)
    row_CELL_SIZE=int(HEIGHT/stripe)
    for column_index in range(vertical):
        for row_index in range(stripe):
            pygame.draw.rect(game_world, (0,0,0,0), pygame.Rect(column_index * col_CELL_SIZE, row_index * row_CELL_SIZE, row_CELL_SIZE, row_CELL_SIZE), 1)


#colum = 세로
#row = 가로

def fill_block(game_world,width,height,vertical,stripe,grid):
    col_CELL_SIZE=int(width/vertical)
    row_CELL_SIZE=int(height/stripe)
    font1 = pygame.font.SysFont(None,30)
    for column_index in range(vertical):
        for row_index in range(stripe):
            mark = grid[int(row_index/int(height/stripe))][int(column_index/int(width/vertical))
            if mark == 'block':
                x_image = font1.render('X', True, (255, 0, 0))
                game_world.blit(x_image, (column_index * col_CELL_SIZE, row_index * row_CELL_SIZE))