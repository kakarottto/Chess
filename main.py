import sys
import pygame

import static_values as st
import board
import chess_preparations as chess

white_set = chess.create_set("w")
black_set = chess.create_set("b")

white_pieces = [None]*16
black_pieces = [None]*16


for i in range(0,16):
	white_pieces[i] = chess.chess_piece(white_set[i],"w")
	black_pieces[i] = chess.chess_piece(black_set[i],"b")

for i in range(0,8):
	white_pieces[i] = chess.Pawn(white_pieces[i])
	black_pieces[i] = chess.Pawn(black_pieces[i])

white_pieces[8] = chess.Rook(white_pieces[8])
black_pieces[8] = chess.Rook(black_pieces[8])

white_pieces[9] = chess.Knight(white_pieces[9])
black_pieces[9] = chess.Knight(black_pieces[9])

white_pieces[10] = chess.Bishop(white_pieces[10])
black_pieces[10] = chess.Bishop(black_pieces[10])

w_king = white_pieces[11] = chess.King(white_pieces[11])
b_king = black_pieces[11] = chess.King(black_pieces[11])

white_pieces[12] = chess.Queen(white_pieces[12])
black_pieces[12] = chess.Queen(black_pieces[12])

white_pieces[15] = chess.Rook(white_pieces[15])
black_pieces[15] = chess.Rook(black_pieces[15])

white_pieces[14] = chess.Knight(white_pieces[14])
black_pieces[14] = chess.Knight(black_pieces[14])

white_pieces[13] = chess.Bishop(white_pieces[13])
black_pieces[13] = chess.Bishop(black_pieces[13])


#kurva   = [chess.Queen(chess.chess_piece(white_set[12],"w")),chess.Pawn(chess.chess_piece(white_set[0],"w"))]

#tarikat = [chess.King(chess.chess_piece(black_set[11],"b")),chess.Pawn(chess.chess_piece(black_set[0],"b"))]

def event_handler():
	global testy
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			return False
		elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:#left mouse click
			#white
			if st.turn_to_move:
				for i_w in range(0,len(white_pieces)):
					if white_pieces[i_w].clicked:
						b_loc = chess.board_location(pygame.mouse.get_pos())
				
						if white_pieces[i_w].is_legal_move(b_loc,white_pieces,black_pieces):
							white_pieces[i_w].clicked = False
							old_loc = chess.move(white_pieces[i_w],b_loc)
							
							if w_king.checked:
								bool_checked = False
								for j_b in range(0,len(black_pieces)):
									#if i am being checked by smb, go the old loc and dont finish the move 
									if chess.is_check(black_pieces[j_b],w_king.board_loc,white_pieces):
										print("you are still being checked. cannot continue")
										chess.move(white_pieces[i_w],old_loc)
										print("moved to the old pos")
										bool_checked = True
										break
								w_king.checked = bool_checked
							
							if w_king.checked:
								break
							
							if chess.is_check(white_pieces[i_w],b_king.board_loc,black_pieces):
								b_king.checked = True
							
							print("end white move")
							st.turn_to_move = False
							break
						else:
							print("Naah")
						white_pieces[i_w].clicked = False
			
					else:
						white_pieces[i_w].check_click(pygame.mouse.get_pos())		
						
						
			
			
			#black
			else:
				for i_b in range(0,len(black_pieces)):
					if black_pieces[i_b].clicked:
						b_loc = chess.board_location(pygame.mouse.get_pos())
				
						if black_pieces[i_b].is_legal_move(b_loc,black_pieces,white_pieces):
							black_pieces[i_b].clicked = False
							
							old_loc = chess.move(black_pieces[i_b],b_loc)
							
							if b_king.checked: 
								bool_checked = False
								for j_w in range(0,len(white_pieces)):
								#if i am being checked by smb, go the old loc and dont finish the move 
									if chess.is_check(white_pieces[j_w],b_king.board_loc,black_pieces):
										print("you are still being checked. cannot continue")
										chess.move(black_pieces[i_b],old_loc)
										print("moved to the old pos")
										bool_checked = True
										break
								
								b_king.checked = bool_checked
								
								
							if b_king.checked:
								break
									
							if chess.is_check(black_pieces[i_b],w_king.board_loc,black_pieces):
								w_king.checked = True
							
							print("end black move")
							st.turn_to_move = True
							break
						else:
							print("Naah")
						black_pieces[i_b].clicked = False
			
					else:
						black_pieces[i_b].check_click(pygame.mouse.get_pos())
					
					
			print(pygame.mouse.get_pos())
			
		elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:#right mouse click
			#testy.clicked_off()
			for i in range(0,16):
				white_pieces[i].clicked_off()
				black_pieces[i].clicked_off()	
	
	return True



def main():
	#global st.run
	st.init_pygame()
	logo = pygame.image.load("./res/w_rook.png")
	pygame.display.set_icon(logo)
	pygame.display.set_caption("chessy")
	
	
	
	
	
	while st.run:
		st.screen.fill((0,0,0))
		st.run = event_handler()
		board.draw()
		
		for i_w in range(0,len(white_pieces)):
			white_pieces[i_w].piece_image.draw()
		for i_b in range(0,len(black_pieces)):
			black_pieces[i_b].piece_image.draw()
		
		pygame.display.update()
		pygame.time.Clock().tick(60)
	
	
	
if __name__ == "__main__":
	main()
