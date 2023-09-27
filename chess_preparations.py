import pygame
import static_values as st
import board
from math import trunc

#todo when all pieces moves correctly
#upgrade the piece class and the rest of the pieces make the inherit it with different if_legal_move and other nessesary funcs


class Image:
	def __init__(self,width,height,img_path,loc):
		self.width = width
		self.height= height
		self.img_path=img_path
		self.loc=loc
		self.image = pygame.image.load(self.img_path)
		self.image = pygame.transform.scale(self.image,(self.width,self.height))
		return 
	def change_size(self,width,height):
		self.width =width
		self.height=height

	def change_location(self,loc):
		self.loc = loc
	
	def draw(self):
		st.screen.blit(self.image,(self.loc))




#creates the set of pieces depending on the team
#note: find a way to center all of the pieces
def create_set(char_team):
	the_set = [None]*16
	
	formating_pawns = board.help_valuey-board.board_size/8
	formating_rest  = board.help_valuey
	if char_team == "b":
		formating_pawns = board.board_size/8
		formating_rest  = 0
	
	for i in range(0,8):
		piece = Image(board.board_size/8,board.board_size/8,"./res/"+char_team+"_pawn.png",(board.help_valuex+(board.board_size/8)*i,formating_pawns))
		the_set[i] = piece
	
	image_names = [char_team+"_rook.png",char_team+"_knight.png",char_team+"_bishop.png",char_team+"_king.png",
	char_team+"_queen.png",char_team+"_bishop.png",char_team+"_knight.png",char_team+"_rook.png"]
	
	
	for i in range(8,16):
		piece = Image(board.board_size/8,board.board_size/8,"./res/"+image_names[i%8],(board.help_valuex+(board.board_size/8)*(i%8),formating_rest))
		the_set[i] = piece
	return the_set

class chess_piece:
	def __init__(self,piece_image,char_team):
		self.piece_image = piece_image
		self.piece_color = char_team
		self.clicked = False
		#imagine a rect. x0 and y0 in pos0 as upper left corner
		#x1 and y1 in pos0 as down right corner
		self.loc0 = (trunc(self.piece_image.loc[0]),trunc(self.piece_image.loc[1]))
		self.loc1 = (trunc(self.piece_image.loc[0]+self.piece_image.width), trunc(self.piece_image.loc[1]+self.piece_image.height))
	
	
	def change_location(self,loc,centered = False):
		if centered:
			self.piece_image.loc = (loc[0]-(self.piece_image.height/2),loc[1]-(self.piece_image.width/2))
		else:
			self.piece_image.loc = loc
		self.loc0 = (trunc(self.piece_image.loc[0]),trunc(self.piece_image.loc[1]))
		self.loc1 = (trunc(self.piece_image.loc[0]+self.piece_image.width), trunc(self.piece_image.loc[1]+self.piece_image.height))
	
	def check_click(self,loc):
		#x0<mouse_x<x1 and y0<mouse_y<y1
		if self.loc0[0]<loc[0] and loc[0]<self.loc1[0] and self.loc0[1]<loc[1] and loc[1]<self.loc1[1]:
			self.clicked = True
			return True
		
		#print(f"{self.loc0[0]}<{loc[0]}<{self.loc1[0]} and {self.loc0[1]}<{loc[1]}<{self.loc1[1]}")
		self.clicked = False
		return False		
	def click_event(self):
		if self.clicked:
			self.change_location(pygame.mouse.get_pos(),True)
			self.clicked = False
		else:
			self.check_click(pygame.mouse.get_pos())
	def clicked_off(self):
		if self.clicked:
			self.clicked = False	
 		

#returns a value that can be converted to the board
#instead of using 1-8 and a-h, just gonna use x and y values
#note: move this two functions in board.py 
def board_location(pos):
	dx = board.board_loc[0]
	dy = board.board_loc[1]
	#print(f"({pos}) : ({board.board_loc})")
	x=y=0
	
	while pos[0] > (dx := dx+board.board_size/8):
		x+=1
	
	while pos[1] > (dy := dy+board.board_size/8):
		y+=1
	#print(f"{x} {y}")
	return (x,y)

def moves_distance(posPiece,posReq):
	x=y=0
	dx = abs(posPiece[0]-posReq[0])
	dy = abs(posPiece[1]-posReq[1])
	#print(f"{dx,dy}")
	
	while (dx := dx - board.board_size/8) > 0:
		
		x +=1
	while (dy := dy - board.board_size/8) > 0:
		
		y +=1	
	#print(f"{x} {y}")
	return (x,y)

def move(the_piece,board_pos):		
		
		old_loc = the_piece.board_loc
		
		new_loc = ((the_piece.board_loc[0]+((-the_piece.move_sign)*the_piece.move_sign*board_pos[0])),
			(the_piece.board_loc[1]+((-the_piece.move_sign)*the_piece.move_sign*board_pos[1])))

		the_piece.change_location(((the_piece.piece_image.loc[0]-(board.board_size/8)*new_loc[0]),
						(the_piece.piece_image.loc[1]-(board.board_size/8)*new_loc[1])))
		the_piece.board_loc = (abs(the_piece.board_loc[0]-new_loc[0]),abs(the_piece.board_loc[1]-new_loc[1])) 
		
		return old_loc

#def bmoves_distance(posPiece,posReq):
#	return (abs(posPiece[0]-posReq[0]),abs(posPiece[1]-posReq[1]))

#checks if the place is used by the set
#if checks the enemy set, set the remove to True
#it will remove the enemy piece
def is_place_empty(test_location,the_set, remove = False):
	for i in range(0,len(the_set)):
		if the_set[i].board_loc == test_location:	
			if remove:
				the_set.pop(i)
			
			return False
	return True
#if the path to the wished place is clean
def is_path_clean(current_location,test_location,the_set, include_last_pos = True):
	#help value
	pos_mover = 1
	steps = 0
	end = 0 
	
	#vertical
	if current_location[0] == test_location[0]:
		#print("vertical")
		#print(f"test_loc[1] {test_location[1]} == current_loc[1] {current_location[1]}")
		steps = current_location[1] - test_location[1]
		if steps < 0:
			pos_mover = -1
			steps = -steps
		if not include_last_pos:
			end = 1
		#print(f"steps left {steps}")
		while steps > end:
			steps = steps -1 
			#print(f"steps left {steps}.  {(test_location[0],test_location[1]+(steps*pos_mover))}")
			if not is_place_empty((test_location[0],test_location[1]+(steps*pos_mover)),the_set):
				return False
		
	#horizontal	
	elif current_location[1] == test_location[1]:
		#print("horizontal")
		#print(f"test_loc[0] {test_location[0]} == current_loc[0] {current_location[0]}")
		steps = current_location[0] - test_location[0]
		if steps < 0:
			pos_mover = -1
			steps = -steps
		
		if not include_last_pos:
			end = 1
		
		#print(f"steps left {steps}")
		while steps > end:
			steps = steps -1 
			#print(f"steps left {steps}")
			if not is_place_empty((test_location[0]+(steps*pos_mover),test_location[1]),the_set):
				return False
		
	#diagonal
	else:	
		pos_mover0 = 1
		pos_mover1 = 1
		#print("diagonal")
		#print(f"delta[0] {test_location[0]-current_location[0]}")
		#print(f"delta[1] {test_location[1]-current_location[1]}")
		steps = current_location[0] - test_location[0]
		if steps < 0:
			#print("0 is minus")
			pos_mover0 = -1
			steps = -steps
		if (current_location[1] - test_location[1]) < 0:
			#print("1 is minus")
			pos_mover1 = -1
		
		if not include_last_pos:
			end = 1
		
		#print(f"steps left {steps}")
		#print(f"testo {(test_location[0]+(steps*pos_mover),test_location[1]-(steps*pos_mover))}")
		while steps > end:
			steps = steps -1 
			#print(f"steps left {steps}")
			#print(f"testo {(test_location[0]+(steps*pos_mover0),test_location[1]-(steps*pos_mover1))}")
			if not is_place_empty(((test_location[0]+(steps*pos_mover0)),(test_location[1]+(steps*pos_mover1))),the_set):
				return False
	
	return True

	
class Pawn(chess_piece):
	
	def __init__(self,piece_image,char_team):
		super().__init__(piece_image,char_team)
		self.f_move = False
		self.board_loc = board_location(self.loc0,self.loc1)
		self.move_sign = 0
		if self.piece_color == "w":
			self.move_sign = -1
		else:
			self.move_sign = 1
		
	def __init__(self, piece):
		super().__init__(piece.piece_image,piece.piece_color)
		self.f_move = True
		self.board_loc = board_location((self.loc1[0]-((self.loc1[0]-self.loc0[0])/2),(self.loc1[1]-((self.loc1[1]-self.loc0[1])/2))))
		self.move_sign = 0
		if self.piece_color == "w":
			self.move_sign = -1
		else:
			self.move_sign = 1
		
	def is_legal_move(self,board_pos,the_set,enemy_set):
		new_loc = (((-self.move_sign)*self.board_loc[0]+(self.move_sign*board_pos[0])),
			((-self.move_sign)*self.board_loc[1]+(self.move_sign*board_pos[1])))
		
		if board_pos[0] < 0 or board_pos[1] < 0 or board_pos[0] > 7 or board_pos[1] > 7:
			return False
		
		
		if not is_place_empty(board_pos,the_set):
			return False
		
		if abs(new_loc[0])==1 and new_loc[1] == 1:
			
			if not is_place_empty(board_pos,enemy_set,True):
				return True
		
		if new_loc[0] < 0 or new_loc[1] < 0:
			return False
		
		
		if new_loc[0] == 0 and new_loc[1] == 0:
			return False
		
		
		if self.f_move and new_loc[0] == 0 and new_loc[1] == 2:
			if not (is_place_empty((board_pos[0],board_pos[1]-self.move_sign),the_set) or 
			is_place_empty((board_pos[0],board_pos[1]-self.move_sign),enemy_set)):
				return False	
			self.f_move = False
			return True
		if new_loc[1] == 1 and new_loc[0] == 0:
			if is_place_empty((board_pos),enemy_set) and is_place_empty((board_pos),enemy_set):
				self.f_move = False
				return True	
		
		return False
	


class Rook(chess_piece):
	
	def __init__(self,piece_image,char_team):
		super().__init__(piece_image,char_team)
		self.f_move = True
		self.board_loc = board_location(self.loc0,self.loc1)
		self.move_sign = 0
		if self.piece_color == "w":
			self.move_sign = -1
		else:
			self.move_sign = 1
		
	
	def __init__(self, piece):
		super().__init__(piece.piece_image,piece.piece_color)
		self.f_move = True
		self.board_loc = board_location((self.loc1[0]-((self.loc1[0]-self.loc0[0])/2),(self.loc1[1]-((self.loc1[1]-self.loc0[1])/2))))
		self.move_sign = 0
		if self.piece_color == "w":
			self.move_sign = -1
		else:
			self.move_sign = 1
		
	def is_legal_move(self,board_pos,the_set,enemy_set):
		new_loc = (((-self.move_sign)*self.board_loc[0]+(self.move_sign*board_pos[0])),
			((-self.move_sign)*self.board_loc[1]+(self.move_sign*board_pos[1])))

		if board_pos[0] < 0 or board_pos[1] < 0 or board_pos[0] > 7 or board_pos[1] > 7:
			#print("out of the board")
			return False
		
		if new_loc[0] == 0 and new_loc[1] == 0:
			return False
		
		#if not is_place_empty(board_pos,the_set):
		if not is_path_clean(self.board_loc,board_pos,the_set):
			return False
		is_place_empty(board_pos,enemy_set,True)
		if new_loc[0] == 0 and new_loc[1] != 0:
			self.f_move = False
			return True
		elif new_loc[1] == 0 and new_loc[0] != 0:
			self.f_move = False
			return True
		
		return False
	
class Bishop(chess_piece):
	
	def __init__(self,piece_image,char_team):
		super().__init__(piece_image,char_team)
		self.board_loc = board_location(self.loc0,self.loc1)
		self.move_sign = 0
		if self.piece_color == "w":
			self.move_sign = -1
		else:
			self.move_sign = 1
		
	
	def __init__(self, piece):
		super().__init__(piece.piece_image,piece.piece_color)
		self.f_move = True
		self.board_loc = board_location((self.loc1[0]-((self.loc1[0]-self.loc0[0])/2),(self.loc1[1]-((self.loc1[1]-self.loc0[1])/2))))
		self.move_sign = 0
		if self.piece_color == "w":
			self.move_sign = -1
		else:
			self.move_sign = 1
		
	def is_legal_move(self,board_pos,the_set,enemy_set):
		new_loc = (((-self.move_sign)*self.board_loc[0]+(self.move_sign*board_pos[0])),
			((-self.move_sign)*self.board_loc[1]+(self.move_sign*board_pos[1])))

		if board_pos[0] < 0 or board_pos[1] < 0 or board_pos[0] > 7 or board_pos[1] > 7:
			#print("out of the board")
			return False
		
		if new_loc[0] == 0 and new_loc[1] == 0:
			return False
		
		if not is_path_clean(self.board_loc,board_pos,the_set):
			return False
		is_place_empty(board_pos,enemy_set,True)
		
		if abs(new_loc[0]) == abs(new_loc[1]) and new_loc[0] != 0:
			return True
		
		return False
	
class Knight(chess_piece):
	
	def __init__(self,piece_image,char_team):
		super().__init__(piece_image,char_team)
		self.board_loc = board_location(self.loc0,self.loc1)
		self.move_sign = 0
		if self.piece_color == "w":
			self.move_sign = -1
		else:
			self.move_sign = 1
		
	
	def __init__(self, piece):
		super().__init__(piece.piece_image,piece.piece_color)
		self.f_move = True
		self.board_loc = board_location((self.loc1[0]-((self.loc1[0]-self.loc0[0])/2),(self.loc1[1]-((self.loc1[1]-self.loc0[1])/2))))
		self.move_sign = 0
		if self.piece_color == "w":
			self.move_sign = -1
		else:
			self.move_sign = 1
		
	def is_legal_move(self,board_pos,the_set,enemy_set):
		new_loc = (((-self.move_sign)*self.board_loc[0]+(self.move_sign*board_pos[0])),
			((-self.move_sign)*self.board_loc[1]+(self.move_sign*board_pos[1])))
		
		if board_pos[0] < 0 or board_pos[1] < 0 or board_pos[0] > 7 or board_pos[1] > 7:
			#print("out of the board")
			return False
		
		if new_loc[0] == 0 and new_loc[1] == 0:
			return False
		
		if not is_place_empty(board_pos,the_set):
			return False

		if (abs(new_loc[0]) == 2 and abs(new_loc[1]) ==1) or (abs(new_loc[1]) == 2 and abs(new_loc[0])==1):
			is_place_empty(board_pos,enemy_set,True)
			return True
		
		
		return False
	
				
class Queen(chess_piece):
	
	def __init__(self,piece_image,char_team):
		super().__init__(piece_image,char_team)
		self.board_loc = board_location(self.loc0,self.loc1)
		self.move_sign = 0
		if self.piece_color == "w":
			self.move_sign = -1
		else:
			self.move_sign = 1
	
	def __init__(self, piece):
		super().__init__(piece.piece_image,piece.piece_color)
		self.board_loc = board_location((self.loc1[0]-((self.loc1[0]-self.loc0[0])/2),(self.loc1[1]-((self.loc1[1]-self.loc0[1])/2))))
		self.move_sign = 0
		if self.piece_color == "w":
			self.move_sign = -1
		else:
			self.move_sign = 1
		
	def is_legal_move(self,board_pos,the_set,enemy_set):
		new_loc = (((-self.move_sign)*self.board_loc[0]+(self.move_sign*board_pos[0])),
			((-self.move_sign)*self.board_loc[1]+(self.move_sign*board_pos[1])))
		
		if board_pos[0] < 0 or board_pos[1] < 0 or board_pos[0] > 7 or board_pos[1] > 7:
			#print("out of the board")
			return False

		if new_loc[0] == 0 and new_loc[1] == 0:
			return False
		
		if not is_place_empty(board_pos,the_set):
			return False
		
		if not ((new_loc[0] == 0 and new_loc[1] != 0) or (new_loc[1] == 0 and new_loc[0] != 0) or (abs(new_loc[0]) == abs(new_loc[1]) and new_loc[0] != 0)):
			return False
		
		if not is_path_clean(self.board_loc,board_pos,the_set):
			return False
		
		if not is_path_clean(self.board_loc,board_pos,enemy_set,False):
			return False
		
		is_place_empty(board_pos,enemy_set,True)
		
		return True
	
		
	
class King(chess_piece):
	
	def __init__(self,piece_image,char_team):
		super().__init__(piece_image,char_team)
		self.f_move = True
		self.board_loc = board_location(self.loc0,self.loc1)
		self.move_sign = 0
		self.checked = False
		if self.piece_color == "w":
			self.move_sign = -1
		else:
			self.move_sign = 1
		
	
	def __init__(self, piece):
		super().__init__(piece.piece_image,piece.piece_color)
		self.f_move = True
		self.board_loc = board_location((self.loc1[0]-((self.loc1[0]-self.loc0[0])/2),(self.loc1[1]-((self.loc1[1]-self.loc0[1])/2))))
		self.move_sign = 0
		self.checked = False
		if self.piece_color == "w":
			self.move_sign = -1
		else:
			self.move_sign = 1
	
	
	def can_castle(self,new_loc,board_pos,the_set):
		rooks = [None]*2
		rook_index = 0
		#note: the first rook will always be on the left
		for i in range(0,len(the_set)):
			if isinstance(the_set[i],Rook):
				rooks[rook_index] = the_set[i]
				rook_index+=1
		
		if not is_path_clean(self.board_loc,board_pos,the_set):
			return False		
		if (not(rooks[0] == None)) and (new_loc[0] == self.move_sign*-2):
			if rooks[0].f_move:
				rooks[0].f_move = False
				print(f"board_pos {board_pos}")
				move(rooks[0],(board_pos[0]+1,board_pos[1]))
				print("Normal Castle")
			
		elif (not(rooks[1] == None)) and (new_loc[0] == self.move_sign*3):
			if rooks[1].f_move:
				rooks[1].f_move = False
				move(rooks[1],(board_pos[0]-1,board_pos[1]))
				print("Grand Castle")
		
		return True
		
	def is_legal_move(self,board_pos,the_set,enemy_set):	
		new_loc = (((-self.move_sign)*self.board_loc[0]+(self.move_sign*board_pos[0])),
			((-self.move_sign)*self.board_loc[1]+(self.move_sign*board_pos[1])))
		
		
		if board_pos[0] < 0 or board_pos[1] < 0 or board_pos[0] > 7 or board_pos[1] > 7:
			#print("out of the board")
			return False
		
		if new_loc[0] == 0 and new_loc[1] == 0:
			return False
		
		if not is_place_empty(board_pos,the_set):
			return False
		
		if self.f_move and (new_loc[0] == self.move_sign*-2 or new_loc[0]== self.move_sign*3):		
			print("Can castle")
			return self.can_castle(new_loc,board_pos,the_set)
		
		
		if abs(new_loc[0]) < 2 and abs(new_loc[1]) < 2:
			is_place_empty(board_pos,enemy_set,True)
			self.f_move = False
			return True
		
		return False
	
	
def is_check(the_piece,king_location,the_set):
	diagonal = False
	linear   = False
	knight   = False
	pawn     = False
	current_location = the_piece.board_loc
	print(f"current obj's class: {type(the_piece)}")
	if isinstance(the_piece,Pawn):
		pawn = True
	elif isinstance(the_piece,Rook):
		linear = True
	elif isinstance(the_piece,Bishop):
		diagonal = True
	elif isinstance((the_piece),Knight):
		knight = True
	elif isinstance(the_piece,Queen):
		print("That is the Queen")
		linear   = True
		diagonal = True
	else:
		return False
	
	if diagonal:
		for i in range(0,7):
			if (king_location == (current_location[0]+i,current_location[1]+i) or king_location == (current_location[0]-i,current_location[1]+i) or
			    king_location == (current_location[0]+i,current_location[1]-i) or king_location == (current_location[0]-i,current_location[1]-i)):
				if is_path_clean(current_location,king_location,the_set, False):
					print("Diagonal check!")
					return True
	#horizontal and vertical
	if linear:
		for i in range(0,7):
			if (king_location == (current_location[0]+i,current_location[1]) or king_location == (current_location[0]-i,current_location[1]) or
			    king_location == (current_location[0],current_location[1]+i) or king_location == (current_location[0],current_location[1]-i)):
				if is_path_clean(current_location,king_location,the_set, False):
					print("Linear check!")
					return True
				
	if knight:
		if (king_location == (current_location[0]+2,current_location[1]+1) or king_location == (current_location[0]+2,current_location[1]-1) or
		    king_location == (current_location[0]-2,current_location[1]+1) or king_location == (current_location[0]-2,current_location[1]-1) or
		    king_location == (current_location[0]+1,current_location[1]+2) or king_location == (current_location[0]+1,current_location[1]-2) or
		    king_location == (current_location[0]-1,current_location[1]+2) or king_location == (current_location[0]-1,current_location[1]-2)):
			print("Knight check!")
			return True
			
	if pawn:
		if (king_location == (current_location[0]+1,current_location[1]-1) or king_location == (current_location[0]-1,current_location[1]-1)):
			print("Pawn check!")
			return True
	return False



