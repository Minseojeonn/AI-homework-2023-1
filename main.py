import pygame # pygame 모듈의 임포트
import sys # 외장 모듈
import argparse
import Utils
import pygame_gui
from pygame.locals import * # QUIT 등의 pygame 상수들을 로드한다.


parser = argparse.ArgumentParser(description='2023-AI_huristic-201818779-전민서')
parser.add_argument('obs_ratio', help='obs_ratio')
parser.add_argument('--vertical', help='vertical,row')
parser.add_argument('--stripe', help='stripe,col')
args = parser.parse_args()

#initial settings

if args.vertical is not None: #가로칸 개수
    vertical = int(args.vertical)
else:
    vertical = 30
if args.stripe is not None: #세로칸 개수
    stripe = int(args.stripe)
else:
    stripe = 30

assert type(float(args.obs_ratio)) == float
inc_obstacle_ratio = float(args.obs_ratio)

width = 600 # 상수 설정
height = 600 # 상수 설정
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
Red = (255, 0, 0)
fps = 10

pygame.init() # 초기화

pygame.display.set_caption('A* Search') # 창 제목 설정
game_world = pygame.display.set_mode((width+100, height+100), 0, 32)
clock = pygame.time.Clock() # 시간 설정

manager = pygame_gui.UIManager((width+100, height+100))

#asset
#star
star_image = pygame.image.load('star.png')
star = star_image.get_rect()
star_image = pygame.transform.scale(star_image,(int(height/vertical),int(width/stripe) ))
star.left = 0 #location
star.top = 0 #location
star_dragging = False

#door - pygame.
door_image = pygame.image.load('door.png')
door = door_image.get_rect()
door_image = pygame.transform.scale(door_image,(int(height/vertical),int(width/stripe) ))
door.left = width-int(height/vertical) #location
door.top = height-int(width/stripe) #location
door_dragging = False

#Map - pygame
grid = [[] for _ in range(vertical)]
for i in range(vertical):
    grid[i] = [[]for _ in range(stripe)]

#buttons - GUI
Rand_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 650), (170, 50)),
                                            text='Random walls',
                                            manager=manager)
Start_A_Search_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 650), (170, 50)),
                                           text='Start_A*_Search',
                                           manager=manager)
Reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 650), (170, 50)),
                                           text='Reset',
                                           manager=manager)

#game Loop
while True: # 아래의 코드를 무한 반복한다.
    time_delta = clock.tick(fps)/1000.0
    #event
    for event in pygame.event.get(): #이벤트 처리
        if event.type == pygame.QUIT: #게임종료
            break
        elif event.type == pygame.MOUSEBUTTONDOWN: #마우스클릭
            column_index = event.pos[0] # CELL_SIZE
            row_index = event.pos[1] # CELL_SIZE
            if column_index<=height and row_index <=width:
                if grid[int(row_index/int(height/stripe))][int(column_index/int(width/vertical))]=='block':
                    grid[int(row_index/int(height/stripe))][int(column_index/int(width/vertical))] = []
                else:
                    grid[int(row_index/int(height/stripe))][int(column_index/int(width/vertical))]='block'
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == Rand_button:
                Utils.make_random_blocks(grid,inc_obstacle_ratio)
            if event.ui_element == Start_A_Search_button:
                pass
            if event.ui_element == Reset_button:
                pass


        manager.process_events(event)

    manager.update(time_delta)
    #view
    game_world.fill(white) # display를 하얀색으로 채운다
    Utils.draw_grid(game_world,width,height,vertical,stripe)
    Utils.fill_block(game_world,width,height,vertical,stripe,grid)
    game_world.blit(star_image,star)
    game_world.blit(door_image,door)
    clock.tick(fps) # 화면 표시 회수 설정만큼 루프의 간격을 둔다
    manager.update(time_delta)
    manager.draw_ui(game_world)
    pygame.display.update() # 화면을 업데이트한다

pygame.quit()