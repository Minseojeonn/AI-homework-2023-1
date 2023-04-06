import Utils

def A_star_manhaten(grid):
    #배열의 4방향에 block을 추가해준다
    Utils.make_bound_block(grid)
    for gr in grid:
        print(gr)
    exit()