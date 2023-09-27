import pygame
import static_values as st

board = pygame.image.load("./res/board_ultra.png")
board_size = st.less(st.screen_width,st.screen_height)
board_loc = ((st.bigger(st.screen_width,st.screen_height)-board_size)/2,0)
board = pygame.transform.scale(board,(board_size,board_size))
help_valuex = board_loc[0]+5
help_valuey = st.screen_height-board_size/8

def draw():
	st.screen.blit(board,board_loc)




