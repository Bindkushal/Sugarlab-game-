import pygame, random  

# Game setup 

pygame.init()  
SIZE, TILE, FONT = 400, 100, pygame.font.Font(None, 60)  
screen = pygame.display.set_mode((SIZE, SIZE))  
pygame.display.set_caption("Fifteen Puzzle")  

# creat Gride to 15 

def create_grid():  
    grid = [i for i in range(1, 16)] + [0]  
    random.shuffle(grid)  
    return [grid[i:i+4] for i in range(0, 16, 4)]  

# Draws the grid on the screen

def draw_grid(grid):  
    screen.fill((255, 255, 255))  
    for i, row in enumerate(grid):  
        for j, tile in enumerate(row):  
            if tile:  
                rect = pygame.Rect(j*TILE, i*TILE, TILE-2, TILE-2)  
                pygame.draw.rect(screen, (0, 0, 255), rect)  
                screen.blit(FONT.render(str(tile), True, (255, 255, 255)), rect.center) 

#Finds the blank tile

def find_blank(grid):  
    for i, row in enumerate(grid):  
        if 0 in row: return i, row.index(0)  
        

def move_tile(grid, row, col):  
    br, bc = find_blank(grid)  
    if abs(br-row) + abs(bc-col) == 1:  
        grid[br][bc], grid[row][col] = grid[row][col], grid[br][bc]  

def main():  
    grid, running = create_grid(), True  
    while running:  
        for e in pygame.event.get():  
            if e.type == pygame.QUIT: running = False  
            if e.type == pygame.MOUSEBUTTONDOWN: move_tile(grid, *divmod(e.pos[1]//TILE*4 + e.pos[0]//TILE, 4))  
        draw_grid(grid)  
        pygame.display.update()  

    pygame.quit()  

if __name__ == "__main__":  
    main()  