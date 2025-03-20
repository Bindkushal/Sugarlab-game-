import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 400
TILE_SIZE = WINDOW_SIZE // 4

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)

# Set up display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Fifteen Puzzle")

font = pygame.font.Font(None, 60)

def create_grid():
    """Create the initial solved grid."""
    grid = []
    count = 1
    for i in range(4):
        row = []
        for j in range(4):
            if i == 3 and j == 3:
                row.append(0)
            else:
                row.append(count)
                count += 1
        grid.append(row)
    return grid

def shuffle_grid(grid, moves=1000):
    """Shuffle the grid by making random valid moves."""
    blank_row, blank_col = 3, 3  # Initial position of the blank
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
    for _ in range(moves):
        possible = []
        for dr, dc in directions:
            nr, nc = blank_row + dr, blank_col + dc
            if 0 <= nr < 4 and 0 <= nc < 4:
                possible.append((dr, dc))
        if possible:
            dr, dc = random.choice(possible)
            # Swap the blank with the adjacent tile
            grid[blank_row][blank_col], grid[blank_row + dr][blank_col + dc] = grid[blank_row + dr][blank_col + dc], grid[blank_row][blank_col]
            blank_row += dr
            blank_col += dc

def draw_grid(grid):
    """Draw the grid on the screen."""
    screen.fill(WHITE)
    for i in range(4):
        for j in range(4):
            tile = grid[i][j]
            if tile == 0:
                continue  # Skip drawing the blank tile
            else:
                # Draw the tile
                rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                pygame.draw.rect(screen, BLUE, rect)
                text = font.render(str(tile), True, WHITE)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def get_clicked_pos(mouse_pos):
    """Convert mouse position to grid coordinates."""
    x, y = mouse_pos
    row = y // TILE_SIZE
    col = x // TILE_SIZE
    return row, col

def is_adjacent(blank_pos, tile_pos):
    """Check if the tile is adjacent to the blank."""
    br, bc = blank_pos
    tr, tc = tile_pos
    return (abs(br - tr) == 1 and bc == tc) or (abs(bc - tc) == 1 and br == tr)

def move_tile(grid, tile_pos):
    """Move the tile to the blank position if adjacent."""
    blank_pos = find_blank(grid)
    if is_adjacent(blank_pos, tile_pos):
        # Swap the tile with the blank
        grid[blank_pos[0]][blank_pos[1]], grid[tile_pos[0]][tile_pos[1]] = grid[tile_pos[0]][tile_pos[1]], grid[blank_pos[0]][blank_pos[1]]
        return True
    return False

def find_blank(grid):
    """Find the position of the blank tile (0)."""
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                return (i, j)
    return (3, 3)  # Fallback, though grid should always have a blank

def is_solved(grid):
    """Check if the grid is in the solved state."""
    solved = create_grid()
    return grid == solved

def main():
    grid = create_grid()
    shuffle_grid(grid)
    running = True
    solved = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not solved:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(mouse_pos)
                    if 0 <= row < 4 and 0 <= col < 4 and grid[row][col] != 0:
                        if move_tile(grid, (row, col)):
                            solved = is_solved(grid)
            elif event.type == pygame.KEYDOWN and not solved:
                blank_row, blank_col = find_blank(grid)
                moved = False
                if event.key == pygame.K_UP:
                    if blank_row > 0:
                        grid[blank_row][blank_col], grid[blank_row - 1][blank_col] = grid[blank_row - 1][blank_col], grid[blank_row][blank_col]
                        moved = True
                elif event.key == pygame.K_DOWN:
                    if blank_row < 3:
                        grid[blank_row][blank_col], grid[blank_row + 1][blank_col] = grid[blank_row + 1][blank_col], grid[blank_row][blank_col]
                        moved = True
                elif event.key == pygame.K_LEFT:
                    if blank_col > 0:
                        grid[blank_row][blank_col], grid[blank_row][blank_col - 1] = grid[blank_row][blank_col - 1], grid[blank_row][blank_col]
                        moved = True
                elif event.key == pygame.K_RIGHT:
                    if blank_col < 3:
                        grid[blank_row][blank_col], grid[blank_row][blank_col + 1] = grid[blank_row][blank_col + 1], grid[blank_row][blank_col]
                        moved = True
                if moved:
                    solved = is_solved(grid)

        draw_grid(grid)
        if solved:
            # Display victory message
            text = font.render("Solved!", True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            screen.blit(text, text_rect)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()