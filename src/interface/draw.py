import pygame

def draw_frame(screen: pygame.Surface):
    
    # Draw to the screen
    screen.fill((255, 255, 255))
    # ...

    # Update the display
    pygame.display.flip()