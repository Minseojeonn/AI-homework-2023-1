import pygame # pygame 모듈의 임포트
import sys # 외장 모듈
import argparse
import Utils
import pygame_gui
import Algorithm
import modify_pygame
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
game_world = pygame.display.set_mode((width+150, height+60), 0, 32)
clock = pygame.time.Clock() # 시간 설정
manager = pygame_gui.UIManager((width+150, height+60))

#asset
#radio_button
boxes = []
uclid_button = modify_pygame.Checkbox(game_world,610,200,0,caption='uclid')
uclid_button.checked = True
manhaten_button = modify_pygame.Checkbox(game_world,610,250,1,caption='manhaten')
boxes.append(uclid_button)
boxes.append(manhaten_button)
#star
star_image = pygame.image.load('star.png')
star = star_image.get_rect()
star_image = pygame.transform.scale(star_image,(int(height/vertical),int(width/stripe)))
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
grid = [[] for _ in range(stripe)]
for i in range(stripe):
    grid[i] = [[]for _ in range(vertical)]

grid[0][0] = 'star'
grid[stripe-1][vertical-1] = 'door'
selected_func = 'uclid'

#buttons - GUI
Rand_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 600), (170, 50)),
                                            text='Random walls',
                                            manager=manager)
Start_A_Search_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((180, 600), (170, 50)),
                                           text='Start_A*_Search',
                                           manager=manager)
Reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((360, 600), (170, 50)),
                                           text='Reset',
                                           manager=manager)
Exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 600), (170, 50)),
                                           text='EXIT',
                                           manager=manager)
#game Loop
while True: # 아래의 코드를 무한 반복한다.
    time_delta = clock.tick(fps)/1000.0
    #Pygame Event 처리
    for event in pygame.event.get(): #이벤트 처리
        if event.type == pygame.QUIT: #게임종료
            break
        elif event.type == pygame.MOUSEBUTTONDOWN: #마우스클릭
            if event.button == 1:
                column_index = event.pos[0] # CELL_SIZE
                row_index = event.pos[1] # CELL_SIZE
                if column_index<=height and row_index <=width: #Map상의 block 생성 클릭으로.
                    print(int(row_index/int(height/stripe)),int(column_index/int(width/vertical)) )
                    if grid[int(row_index/int(height/stripe))][int(column_index/int(width/vertical))]=='star': #star drag
                        star_dragging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = star.x - mouse_x
                        offset_y = star.y - mouse_y
                    elif grid[int(row_index/int(height/stripe))][int(column_index/int(width/vertical))]=='door': #drag door
                        door_dragging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = door.x - mouse_x
                        offset_y = door.y - mouse_y
                    elif grid[int(row_index/int(height/stripe))][int(column_index/int(width/vertical))]=='block': #block off
                        grid[int(row_index/int(height/stripe))][int(column_index/int(width/vertical))] = []
                    elif grid[int(row_index/int(height/stripe))][int(column_index/int(width/vertical))] == [] : #block on
                        grid[int(row_index/int(height/stripe))][int(column_index/int(width/vertical))]='block'
                for box in boxes:
                    box.update_checkbox(event)
                    if box.checked is True:
                        selected_func = box.caption
                        for b in boxes:
                            if b != box:
                                b.checked = False

        elif event.type == pygame.MOUSEBUTTONUP: ##drag star
            if event.button == 1:
                if star_dragging:
                    star_dragging = False
                if door_dragging:
                    door_dragging = False
        elif event.type == pygame.MOUSEMOTION: ##drag star
            if star_dragging:
                mouse_x, mouse_y = event.pos
                origin_star_x = star.x
                origin_star_y = star.y
                temp_star_x = mouse_x + offset_x
                temp_star_y = mouse_y + offset_y
                #print(int(temp_star_y/int(height/vertical)), int(temp_star_x/int(width/stripe)))
                grid[int(origin_star_y/int(height/stripe))][int(origin_star_x/int(width/vertical))] = []
                grid[int(temp_star_y/int(height/stripe))][int(temp_star_x/int(width/vertical))] = 'star'
                star.x = int(temp_star_x/int(width/vertical)) * int(width/vertical)
                star.y = int(temp_star_y/int(height/stripe)) * int(height/stripe)
            if door_dragging: # drag_door
                mouse_x, mouse_y = event.pos
                origin_door_x = door.x
                origin_door_y = door.y
                temp_door_x = mouse_x + offset_x
                temp_door_y = mouse_y + offset_y
                #print(int(temp_door_y/int(height/vertical)), int(temp_door_x/int(width/stripe)))
                grid[int(origin_door_y/int(height/stripe))][int(origin_door_x/int(width/vertical))] = []
                grid[int(temp_door_y/int(height/stripe))][int(temp_door_x/int(width/vertical))] = 'door'
                door.x = int(temp_door_x/int(width/vertical)) * int(width/vertical)
                door.y = int(temp_door_y/int(height/stripe)) * int(height/stripe)

        #GUI evnet처리
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == Rand_button:
                Utils.make_random_blocks(grid, inc_obstacle_ratio)
            if event.ui_element == Start_A_Search_button:
                print(Algorithm.aStar(grid,selected_func))
            if event.ui_element == Reset_button:
                star.left = 0 #location
                star.top = 0 #location
                door.left = width-int(height/vertical) #location
                door.top = height-int(width/stripe) #location
                for i, gr in enumerate(grid):
                 for j, g in enumerate(gr):
                    grid[i][j] = []
                grid[0][0] = 'star'
                grid[stripe-1][vertical-1] = 'door'
            if event.ui_element == Exit_button:
                exit()

        manager.process_events(event)

    manager.update(time_delta)
    #view
    game_world.fill(white) # display를 하얀색으로 채운다
    Utils.draw_grid(game_world,width,height,vertical,stripe)
    Utils.fill_block(game_world,height,width,stripe,vertical,grid)
    game_world.blit(star_image,star)
    game_world.blit(door_image,door)
    for box in boxes:
        box.render_checkbox()
    print(selected_func)
    clock.tick(fps) # 화면 표시 회수 설정만큼 루프의 간격을 둔다
    manager.update(time_delta)
    manager.draw_ui(game_world)
    pygame.display.update() # 화면을 업데이트한다

exit()