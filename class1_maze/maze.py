import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 迷宫参数
CELL_SIZE = 20
GRID_SIZE = 25  # 正方形迷宫的尺寸
WIDTH = CELL_SIZE * GRID_SIZE
HEIGHT = CELL_SIZE * GRID_SIZE

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 创建屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("随机迷宫生成器")

# 创建迷宫数据结构
def create_maze(size):
    # 初始化迷宫，所有墙都存在
    maze = [[{"right": True, "bottom": True} for _ in range(size)] for _ in range(size)]
    
    # 深度优先搜索生成迷宫
    def carve_passages(x, y, visited):
        visited.add((x, y))
        directions = [(0, 1, "right", "left"), (1, 0, "bottom", "top"), 
                     (0, -1, "left", "right"), (-1, 0, "top", "bottom")]
        random.shuffle(directions)
        
        for dx, dy, wall, opposite_wall in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and (nx, ny) not in visited:
                # 移除相邻单元格之间的墙
                if wall == "right":
                    maze[y][x]["right"] = False
                elif wall == "bottom":
                    maze[y][x]["bottom"] = False
                elif wall == "left" and nx >= 0:
                    maze[ny][nx]["right"] = False
                elif wall == "top" and ny >= 0:
                    maze[ny][nx]["bottom"] = False
                
                carve_passages(nx, ny, visited)
    
    # 从随机点开始生成
    start_x, start_y = random.randint(0, size-1), random.randint(0, size-1)
    carve_passages(start_x, start_y, set())
    
    return maze

# 绘制迷宫
def draw_maze(maze):
    screen.fill(WHITE)
    
    # 绘制外边框
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 2)
    
    # 绘制内部的墙
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell_x = x * CELL_SIZE
            cell_y = y * CELL_SIZE
            
            # 绘制右侧的墙
            if maze[y][x]["right"]:
                pygame.draw.line(screen, BLACK, 
                                (cell_x + CELL_SIZE, cell_y),
                                (cell_x + CELL_SIZE, cell_y + CELL_SIZE), 2)
            
            # 绘制底部的墙
            if maze[y][x]["bottom"]:
                pygame.draw.line(screen, BLACK,
                                (cell_x, cell_y + CELL_SIZE),
                                (cell_x + CELL_SIZE, cell_y + CELL_SIZE), 2)

# 主循环
def main():
    maze = create_maze(GRID_SIZE)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 按空格键生成新迷宫
                    maze = create_maze(GRID_SIZE)
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        draw_maze(maze)
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()