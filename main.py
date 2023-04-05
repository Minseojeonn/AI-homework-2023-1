import pygame # pygame 모듈의 임포트
import sys # 외장 모듈
import argparse
import Utils
from pygame.locals import * # QUIT 등의 pygame 상수들을 로드한다.


parser = argparse.ArgumentParser(description='2023-AI_huristic-201818779-전민서')
parser.add_argument('--vertical', help='vertical,row')
parser.add_argument('--stripe', help='stripe,col')
args = parser.parse_args()

#initial settings

if args.vertical is not None: #가로칸 개수
    vertical = int(args.vertical)
else:
    vertical = 5
if args.stripe is not None: #세로칸 개수
    stripe = int(args.stripe)
else:
    stripe = 5

width = 600 # 상수 설정
height = 600 # 상수 설정
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
Red = (255, 0, 0)
fps = 10

pygame.init() # 초기화

pygame.display.set_caption('A* Search') # 창 제목 설정
game_world = pygame.display.set_mode((width, height), 0, 32) # 메인 디스플레이를 설정한다
clock = pygame.time.Clock() # 시간 설정

#asset
#star
star_image = pygame.image.load('star.png')
star = star_image.get_rect()
star_image = pygame.transform.scale(star_image,(int(height/vertical),int(width/stripe) ))
star.left = 0 #location
star.top = 0 #location

#door
door_image = pygame.image.load('door.png')
door = door_image.get_rect()
door_image = pygame.transform.scale(door_image,(int(height/vertical),int(width/stripe) ))
door.left = width-int(height/vertical) #location
door.top = height-int(width/stripe) #location

#Map
grid = [[] for _ in range(vertical)]
for i in range(vertical):
    grid[i] = [[]for _ in range(stripe)]

grid[2][2]='block'

#game Loop
while True: # 아래의 코드를 무한 반복한다.
    event = pygame.event.poll() #이벤트 처리
    if event.type == pygame.QUIT: #게임종료
        break
    elif event.type == pygame.MOUSEBUTTONDOWN: #마우스클릭
        column_index = event.pos[0] # CELL_SIZE
        row_index = event.pos[1] # CELL_SIZE
        grid[int(row_index/int(height/stripe))][int(column_index/int(width/vertical))]='block'
        print(grid)
    game_world.fill(white) # display를 하얀색으로 채운다
    Utils.draw_grid(game_world,width,height,vertical,stripe)
    Utils.fill_block(game_world,width,height,vertical,stripe,grid)
    game_world.blit(star_image,star)
    game_world.blit(door_image,door)
    pygame.display.update() # 화면을 업데이트한다
    clock.tick(fps) # 화면 표시 회수 설정만큼 루프의 간격을 둔다


pygame.quit()