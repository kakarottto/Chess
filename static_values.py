import pygame

#static values and inits here


run = True

#if true white's turn, if false black's turn
turn_to_move = True

screen_width = 1024
screen_height= 720
screen = pygame.display.set_mode((screen_width,screen_height))

default_color = (0,0,0)
white_color   = (255,255,255)
orange_color  = (240,100,20)

chess_turn = "w"

def less(a,b):
	if a>b:
		return b
	return a

def bigger(a,b):
	if a>b:
		return a
	return b

def init_pygame():
	pygame.init()
	pygame.font.init()

#locate index using value from array
def locate_index_arr(array, value):
	length = len(array)
	for i in range(0,length):
		if array[i] == value:
			return i
	
	return -1
