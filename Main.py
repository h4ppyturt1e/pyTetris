import pygame as pg
from classes.Mino import Playfield, Tetromino
from classes.Constants import *


def main():
    # initialize the board
    playfield = Playfield()

    # initialize pygame window
    pg.init()
    pg.font.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("Tetris")
    clock = pg.time.Clock()
    runtime = 0
    
    run = True
    while run:
        
        # event loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            
            # keypresses
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    playfield.movePiece("left")
                elif event.key == pg.K_RIGHT:
                    playfield.movePiece("right")
                elif event.key == pg.K_DOWN:
                    playfield.movePiece("down")
                elif event.key == pg.K_UP:
                    playfield.rotatePiece("CW")
                elif event.key == pg.K_z:
                    playfield.rotatePiece("CCW")
                elif event.key == pg.K_SPACE:
                    playfield.hardDrop()
                elif event.key == pg.K_ESCAPE:
                    run = False
                
        # clear the display
        screen.fill("black")
        
        
        
        
        # draw the board
        draw(playfield, screen, runtime)
        
        # update the screen according to fps
        pg.display.flip()

        pg.time.delay(REPEAT_RATE)
        clock.tick(FRAME_RATE)
        runtime += clock.get_time()

def draw(playfield, screen, runtime):
    # clear the screen
    screen.fill("black")
    
    # draws the grid with lines
    for x in range(0, WIDTH + 1):
        pg.draw.line(screen, "white", (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT * BLOCK_SIZE))
    for y in range(0, HEIGHT + 1):
        pg.draw.line(screen, "white", (0, y * BLOCK_SIZE), (WIDTH * BLOCK_SIZE, y * BLOCK_SIZE))
    
    # draws the blocks
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if playfield.board[y][x] != 0:
                pg.draw.rect(screen, COLOR_DICT[playfield.board[y][x]], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # draw the game runtime on the topright of the screen
    font = pg.font.SysFont("Arial", 30)
    textSurface = font.render(str(runtime), False, "white")
    screen.blit(textSurface, (WIDTH * BLOCK_SIZE + 10, 10))
    # display fps under it
    textSurface = font.render(str(int(1000 / pg.time.get_ticks())), False, "white")
    screen.blit(textSurface, (WIDTH * BLOCK_SIZE + 10, 40))

if __name__ == '__main__':
    # get user prefs
    
    
    main()
