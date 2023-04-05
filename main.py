import pygame # pygame 모듈의 임포트
import sys # 외장 모듈
import argparse
from pygame.locals import * # QUIT 등의 pygame 상수들을 로드한다.
import Utils

parser = argparse.ArgumentParser(description='2023-AI_huristic-201818779-전민서')
parser.add_argument('--vertical', help='vertical,row')
parser.add_argument('--stripe', help='stripe,col')
args = parser.parse_args()

#initial settings

if len(args.vertical) != 0: #가로칸 개수
    vertical = int(args.vertical)
else:
    vertical = 30
if len(args.stripe) != 0: #세로칸 개수
    stripe = int(args.stripe)
else:
    stripe = 30

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

#game Loop

while True: # 아래의 코드를 무한 반복한다.
    for event in pygame.event.get(): # 발생한 입력 event 목록의 event마다 검사
        if event.type == QUIT: # event의 type이 QUIT에 해당할 경우
            pygame.quit() # pygame을 종료한다
            sys.exit() # 창을 닫는다
    game_world.fill(white) # display를 하얀색으로 채운다
    Utils.draw_grid(vertical,stripe,game_world,width,height)

    pygame.display.update() # 화면을 업데이트한다
    clock.tick(fps) # 화면 표시 회수 설정만큼 루프의 간격을 둔다