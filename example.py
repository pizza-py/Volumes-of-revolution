import pygame
import sys
import math

pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graphing Calculator")

def draw_axes():
    pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)  # Y-axis
    pygame.draw.line(screen, BLACK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)  # X-axis

def graph_function(f, color=BLACK):
    for x in range(-WIDTH // 2, WIDTH // 2):
        screen_x = WIDTH // 2 + x
        try:
            y = f(x)
            screen_y = HEIGHT // 2 - y
            pygame.draw.circle(screen, color, (screen_x, screen_y), 1)
        except:
            continue

def get_user_function():
    user_input = input("Enter a function in terms of x (e.g., '0.01 * (x ** 2)'): ")
    def user_function(x):
        return eval(user_input)
    return user_function

def main():
    user_function = get_user_function()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(WHITE)
        draw_axes()
        graph_function(user_function)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
