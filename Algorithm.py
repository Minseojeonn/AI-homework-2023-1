import Utils
import copy

def loss_func_manhaten(node_cur,node_end):
    return abs(node_cur.position[0] - node_end.position[0]) + abs(node_cur.position[1] - node_end.position[1])

def loss_func_uclid(node_cur,node_end):
    return ((node_cur.position[0] - node_end.position[0]) ** 2) + ((node_cur.position[1] - node_end.position[1]) ** 2)

############
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def aStar(grid_origin, distance):
    visited_node_count = 0
    grid = copy.deepcopy(grid_origin)
    if distance == 'uclid':
        lossfunc = loss_func_uclid
    elif distance == 'manhaten':
        lossfunc = loss_func_manhaten

    Utils.make_bound_block(grid) ## 테두리에 badlock 생성
    start, end = Utils.find_star_and_door(grid)

    # startNode와 endNode 초기화
    startNode = Node(None, start)
    endNode = Node(None, end)

    # openList, closedList 초기화
    openList = []
    closedList = []

    # openList에 시작 노드 추가
    openList.append(startNode)

    # endNode를 찾을 때까지 실행
    while openList:
        visited_node_count = visited_node_count + 1

        # 현재 노드 지정
        currentNode = openList[0]
        currentIdx = 0

        # 이미 같은 노드가 openList에 있고, f 값이 더 크면
        # currentNode를 openList안에 있는 값으로 교체
        for index, item in enumerate(openList):
            if item.f < currentNode.f:
                currentNode = item
                currentIdx = index

        # openList에서 제거하고 closedList에 추가
        openList.pop(currentIdx)
        closedList.append(currentNode)

        # 현재 노드가 목적지면 current.position 추가하고
        # current의 부모로 이동
        if currentNode == endNode:
            path = []
            current = currentNode
            while current is not None:
                # maze 길을 표시하려면 주석 해제
                # x, y = current.position
                # maze[x][y] = 7
                path.append(current.position)
                current = current.parent
            print("방문횟수 출력 : ", visited_node_count) #방문횟수 출력
            return path[::-1]  # reverse


        children = []
        # 인접한 xy좌표 전부
        for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

            # 노드 위치 업데이트
            nodePosition = (
                currentNode.position[0] + newPosition[0],  # X
                currentNode.position[1] + newPosition[1])  # Y

            # 장애물이 있으면 다른 위치 불러오기
            print(nodePosition[0],nodePosition[1])
            if grid[nodePosition[0]][nodePosition[1]] == 'block':
                continue

            new_node = Node(currentNode, nodePosition)
            children.append(new_node)

        # 자식들 모두 loop
        for child in children:

            # 자식이 closedList에 있으면 continue
            if child in closedList:
                continue

            # f, g, h값 업데이트
            child.g = currentNode.g + 1
            child.h = lossfunc(child,endNode)

            # print("position:", child.position) 거리 추정 값 보기
            # print("from child to goal:", child.h)

            child.f = child.g + child.h

            # 자식이 openList에 있으고, g값이 더 크면 continue
            if len([openNode for openNode in openList
                    if child == openNode and child.g > openNode.g]) > 0:
                continue

            openList.append(child)