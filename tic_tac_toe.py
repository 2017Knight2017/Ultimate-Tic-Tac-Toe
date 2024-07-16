import pygame
from math import tau
from itertools import chain

def is_win(arr):
	a = arr[1][1]
	b = arr[0][2]
	c = arr[2][0]
	if a == b == c == 0:
		return 0
	if not a == 0 and (
		a == arr[0][0] == arr[2][2] or
	 	a == arr[2][0] == arr[0][2] or
		a == arr[0][1] == arr[2][1] or
		a == arr[1][0] == arr[1][2]):
		return a
	elif not b == 0 and (
		b == arr[1][2] == arr[2][2] or
		b == arr[0][1] == arr[0][0]):
		return b
	elif not c == 0 and (
		c == arr[1][0] == arr[0][0] or
		c == arr[2][1] == arr[2][2]):
		return c


pygame.init()
width, height = 800, 600

board_width, board_height = 600, 500
w3_big, h3_big = board_width/3, board_height/3
margin_w_big, margin_h_big = (width-board_width)/2, (height-board_height)/2

slot_width, slot_height = w3_big-50, h3_big-30
w3_small, h3_small = slot_width/3, slot_height/3
margin_w_small, margin_h_small = (w3_big-slot_width)/2, (h3_big-slot_height)/2

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
current_phase = "init"
drawing_progress = 0.0
BLACK = (0, 0, 0)
GREEN = (0, 204, 0)
screen.fill((255,255,255))

big_column = big_line = small_column = small_line = 0

turn = 0
board_data = [[[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]],
			  [[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]],
			  [[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]]
big_board_data = [[0,0,0],[0,0,0],[0,0,0]]

selected = [-1, -1]

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()

	match current_phase:
		case "init":
			if drawing_progress <= 1:
				pygame.draw.line(screen, BLACK, 
					 (margin_w_big+w3_big, margin_h_big),
					 (margin_w_big+w3_big, margin_h_big + board_height*drawing_progress), 5)
				pygame.draw.line(screen, BLACK,
					 (margin_w_big+w3_big*2, height-margin_h_big),
					 (margin_w_big+w3_big*2, height-margin_h_big - board_height*drawing_progress), 5)
				pygame.draw.line(screen, BLACK,
					 (margin_w_big, margin_h_big+h3_big),
					 (margin_w_big + board_width*drawing_progress, margin_h_big+h3_big), 5)
				pygame.draw.line(screen, BLACK,
					 (width-margin_w_big, margin_h_big+h3_big*2),
					 (width-margin_w_big - board_width*drawing_progress, margin_h_big+h3_big*2), 5)

				for i in range(3):
					for j in range(3):
						pygame.draw.line(screen, BLACK, 
						 	(margin_w_big + margin_w_small + w3_big*i + w3_small, margin_h_big + margin_h_small + h3_big*j),
						 	(margin_w_big + margin_w_small + w3_big*i + w3_small, margin_h_big + margin_h_small + h3_big*j + slot_height*drawing_progress), 2)
						pygame.draw.line(screen, BLACK,
						 	(margin_w_big + margin_w_small + w3_big*i + w3_small*2, height-(margin_h_big + margin_h_small + h3_big*j)),
						 	(margin_w_big + margin_w_small + w3_big*i + w3_small*2, height-(margin_h_big + margin_h_small + h3_big*j) - slot_height*drawing_progress), 2)
						pygame.draw.line(screen, BLACK,
						 	(margin_w_big + margin_w_small + w3_big*j, margin_h_big + margin_h_small + h3_big*i + h3_small),
						 	(margin_w_big + margin_w_small + w3_big*j + slot_width*drawing_progress, margin_h_big + margin_h_small + h3_big*i + h3_small), 2)
						pygame.draw.line(screen, BLACK,
						 	(width-(margin_w_big + margin_w_small + w3_big*j), margin_h_big + margin_h_small + h3_big*i + h3_small*2),
						 	(width-(margin_w_big + margin_w_small + w3_big*j) - slot_width*drawing_progress, margin_h_big + margin_h_small + h3_big*i + h3_small*2), 2)
				drawing_progress += 0.01
			else:
				drawing_progress = 0.0
				current_phase = "game"

		case "game":
			pressed = pygame.mouse.get_pressed()
			pos = pygame.mouse.get_pos()
			if pressed[0]:
				big_column = int((pos[0] - margin_w_big) // w3_big)
				big_line = int((pos[1] - margin_h_big) // h3_big)
				small_column = int((pos[0] - margin_w_small*(2*big_column+1) - margin_w_big) // w3_small)
				small_line = int((pos[1] - margin_h_small*(2*big_line+1) - margin_h_big) // h3_small)

				# If the user clicks out of bounds of the slot.
				match (big_column, small_column):
					case (0, 3): small_column = 2
					case (1, 6): small_column = 5
					case (2, 9): small_column = 8
					case (1, 2): small_column = 3
					case (2, 5): small_column = 6
					case (0, -1): small_column = 0

				match (big_line, small_line):
					case (0, 3): small_line = 2
					case (1, 6): small_line = 5
					case (2, 9): small_line = 8
					case (1, 2): small_line = 3
					case (2, 5): small_line = 6
					case (0, -1): small_line = 0

				small_column %= 3
				small_line %= 3
				if all([0 <= big_line <= 2,
		   			   	0 <= big_column <= 2,
					   	not board_data[big_line][big_column][small_line][small_column],
						selected == [big_line, big_column] or selected == [-1, -1]]):
					board_data[big_line][big_column][small_line][small_column] = turn + 1
					current_phase = "drawing " + "ccirrocslse"[turn::2]

					if all(chain(board_data[small_line][small_column][0],
							   	 board_data[small_line][small_column][1],
							   	 board_data[small_line][small_column][2])):
						selected = [-1, -1]
					else:
						selected = [small_line, small_column]

					for i in range(3):
							for j in range(3):
								pygame.draw.line(screen, BLACK, 
								 	(margin_w_big + margin_w_small + w3_big*i + w3_small, margin_h_big + margin_h_small + h3_big*j),
								 	(margin_w_big + margin_w_small + w3_big*i + w3_small, margin_h_big + margin_h_small + h3_big*j + slot_height), 2)
								pygame.draw.line(screen, BLACK, 
								 	(margin_w_big + margin_w_small + w3_big*i + 2*w3_small, margin_h_big + margin_h_small + h3_big*j),
								 	(margin_w_big + margin_w_small + w3_big*i + 2*w3_small, margin_h_big + margin_h_small + h3_big*j + slot_height), 2)
								pygame.draw.line(screen, BLACK,
								 	(margin_w_big + margin_w_small + w3_big*i, margin_h_big + margin_h_small + h3_big*j + h3_small),
								 	(margin_w_big + margin_w_small + w3_big*i + slot_width, margin_h_big + margin_h_small + h3_big*j + h3_small), 2)
								pygame.draw.line(screen, BLACK,
								 	(margin_w_big + margin_w_small + w3_big*i, margin_h_big + margin_h_small + h3_big*j + 2*h3_small),
								 	(margin_w_big + margin_w_small + w3_big*i + slot_width, margin_h_big + margin_h_small + h3_big*j + 2*h3_small), 2)

					if selected == [-1, -1]:
						for i in range(3):
							for j in range(3):
								if not all(chain(board_data[j][i][0],
							   			   		 board_data[j][i][1],
							   			   		 board_data[j][i][2])):
									pygame.draw.line(screen, GREEN, 
									 	(margin_w_big + margin_w_small + w3_big*i + w3_small, margin_h_big + margin_h_small + h3_big*j),
									 	(margin_w_big + margin_w_small + w3_big*i + w3_small, margin_h_big + margin_h_small + h3_big*j + slot_height), 2)
									pygame.draw.line(screen, GREEN, 
									 	(margin_w_big + margin_w_small + w3_big*i + 2*w3_small, margin_h_big + margin_h_small + h3_big*j),
									 	(margin_w_big + margin_w_small + w3_big*i + 2*w3_small, margin_h_big + margin_h_small + h3_big*j + slot_height), 2)
									pygame.draw.line(screen, GREEN,
									 	(margin_w_big + margin_w_small + w3_big*i, margin_h_big + margin_h_small + h3_big*j + h3_small),
									 	(margin_w_big + margin_w_small + w3_big*i + slot_width, margin_h_big + margin_h_small + h3_big*j + h3_small), 2)
									pygame.draw.line(screen, GREEN,
									 	(margin_w_big + margin_w_small + w3_big*i, margin_h_big + margin_h_small + h3_big*j + 2*h3_small),
									 	(margin_w_big + margin_w_small + w3_big*i + slot_width, margin_h_big + margin_h_small + h3_big*j + 2*h3_small), 2)
					else:
						pygame.draw.line(screen, GREEN, 
						 	(margin_w_big + margin_w_small + w3_big*selected[1] + w3_small, margin_h_big + margin_h_small + h3_big*selected[0]),
						 	(margin_w_big + margin_w_small + w3_big*selected[1] + w3_small, margin_h_big + margin_h_small + h3_big*selected[0] + slot_height), 2)
						pygame.draw.line(screen, GREEN, 
						 	(margin_w_big + margin_w_small + w3_big*selected[1] + 2*w3_small, margin_h_big + margin_h_small + h3_big*selected[0]),
						 	(margin_w_big + margin_w_small + w3_big*selected[1] + 2*w3_small, margin_h_big + margin_h_small + h3_big*selected[0] + slot_height), 2)
						pygame.draw.line(screen, GREEN,
						 	(margin_w_big + margin_w_small + w3_big*selected[1], margin_h_big + margin_h_small + h3_big*selected[0] + h3_small),
						 	(margin_w_big + margin_w_small + w3_big*selected[1] + slot_width, margin_h_big + margin_h_small + h3_big*selected[0] + h3_small), 2)
						pygame.draw.line(screen, GREEN,
						 	(margin_w_big + margin_w_small + w3_big*selected[1], margin_h_big + margin_h_small + h3_big*selected[0] + 2*h3_small),
						 	(margin_w_big + margin_w_small + w3_big*selected[1] + slot_width, margin_h_big + margin_h_small + h3_big*selected[0] + 2*h3_small), 2)

		case "drawing cross":
			if drawing_progress <= 1:
				x1 = margin_w_big + big_column*w3_big + margin_w_small*(2*big_column+1) + (small_column - big_column)*w3_small
				y1 = margin_h_big + big_line*h3_big + margin_h_small*(2*big_line+1) + margin_h_small*big_line + (small_line - big_line)*h3_small
				pygame.draw.line(screen, BLACK, (x1,y1), (x1 + w3_small*drawing_progress, y1 + h3_small*drawing_progress), 4)
				pygame.draw.line(screen, BLACK, (x1+w3_small,y1), (x1+w3_small - w3_small*drawing_progress, y1 + h3_small*drawing_progress), 4)
				drawing_progress += 0.04
			else: 
				drawing_progress = 0
				if is_win(board_data[big_line][big_column]) and not big_board_data[big_line][big_column]:
					current_phase = "drawing big cross"
				else:
					turn = 0
					current_phase = "game"

		case "drawing circle":
			rect = pygame.Rect(margin_w_big + big_column*w3_big + margin_w_small*(2*big_column+1) + (small_column - big_column)*w3_small + 2,
					   		   margin_h_big + big_line*h3_big + margin_h_small*(2*big_line+1) + margin_h_small*big_line + (small_line - big_line)*h3_small + 2,
							   min(h3_small, w3_small),
							   min(h3_small, w3_small))
			if drawing_progress <= 1:
				# It's more convenient to me to use tau instead of pi*2.
				pygame.draw.arc(screen, BLACK, rect, 0, drawing_progress*tau, 4)
				drawing_progress += 0.03
			else: 
				drawing_progress = 0
				if is_win(board_data[big_line][big_column]) and not big_board_data[big_line][big_column]:
					current_phase = "drawing big circle"
				else:
					turn = 1
					current_phase = "game"

		case "drawing big circle":
			if drawing_progress <= 1:
				rect = pygame.Rect(margin_w_big + big_column*w3_big + margin_w_small + 2,
						   		   margin_h_big + big_line*h3_big + margin_h_small + 2,
								   min(slot_height, slot_width),
								   min(slot_height, slot_width))
				pygame.draw.arc(screen, BLACK, rect, 0, drawing_progress*tau, 5)
				drawing_progress += 0.02
			else:
				drawing_progress = 0
				big_board_data[big_line][big_column] = turn + 1
				if is_win(big_board_data):
					current_phase = "end"
				else:
					turn = 1
					current_phase = "game"

		case "drawing big cross":
			if drawing_progress <= 1:
				x1 = margin_w_big + big_column*w3_big + margin_w_small
				y1 = margin_h_big + big_line*h3_big  # The big cross is actually shifted a bit up in order to avoid an overlap with the smaller ones.
				pygame.draw.line(screen, BLACK, (x1,y1), (x1 + slot_width*drawing_progress, y1 + slot_height*drawing_progress), 6)
				pygame.draw.line(screen, BLACK, (x1+slot_width,y1), (x1+slot_width - slot_width*drawing_progress, y1 + slot_height*drawing_progress), 6)
				drawing_progress += 0.03
			else:
				drawing_progress = 0
				big_board_data[big_line][big_column] = turn + 1
				if is_win(big_board_data):
					current_phase = "end"
				else:
					turn = 0
					current_phase = "game"

		case "end":
			a = big_board_data
			if a[0][0] == a[0][1] == a[0][2] == turn + 1:
				if drawing_progress <= 1:
					pygame.draw.line(screen, BLACK,
									(margin_w_big, margin_h_big + h3_big/2),
									(margin_w_big + (width-2*margin_w_big)*drawing_progress, margin_h_big + h3_big/2), 8)
					drawing_progress += 0.01

			elif a[1][0] == a[1][1] == a[1][2] == turn + 1:
				if drawing_progress <= 1:
					pygame.draw.line(screen, BLACK,
									(margin_w_big, margin_h_big + h3_big/2 + h3_big),
									(margin_w_big + (width-2*margin_w_big)*drawing_progress, margin_h_big + h3_big/2 + h3_big), 8)
					drawing_progress += 0.01

			elif a[2][0] == a[2][1] == a[2][2] == turn + 1:
				if drawing_progress <= 1:
					pygame.draw.line(screen, BLACK,
									(margin_w_big, margin_h_big + h3_big/2 + 2*h3_big),
									(margin_w_big + (width-2*margin_w_big)*drawing_progress, margin_h_big + h3_big/2 + 2*h3_big), 8)
					drawing_progress += 0.01

			elif a[0][0] == a[1][0] == a[2][0] == turn + 1:
				if drawing_progress <= 1:
					pygame.draw.line(screen, BLACK,
									(margin_w_big + w3_big/2, margin_h_big),
									(margin_w_big + w3_big/2, margin_h_big + (height-2*margin_h_big)*drawing_progress), 8)
					drawing_progress += 0.01

			elif a[0][1] == a[1][1] == a[2][1] == turn + 1:
				if drawing_progress <= 1:
					pygame.draw.line(screen, BLACK,
									(margin_w_big + w3_big/2 + w3_big, margin_h_big),
									(margin_w_big + w3_big/2 + w3_big, margin_h_big + (height-2*margin_h_big)*drawing_progress), 8)
					drawing_progress += 0.01

			elif a[0][2] == a[1][2] == a[2][2] == turn + 1:
				if drawing_progress <= 1:
					pygame.draw.line(screen, BLACK,
									(margin_w_big + w3_big/2 + 2*w3_big, margin_h_big),
									(margin_w_big + w3_big/2 + 2*w3_big, margin_h_big + (height-2*margin_h_big)*drawing_progress), 8)
					drawing_progress += 0.01

			elif a[0][0] == a[1][1] == a[2][2] == turn + 1:
				if drawing_progress <= 1:
					pygame.draw.line(screen, BLACK,
									(margin_w_big, margin_h_big),
									(margin_w_big + (width-2*margin_w_big)*drawing_progress, margin_h_big + (height-2*margin_h_big)*drawing_progress), 8)
					drawing_progress += 0.01

			elif a[0][2] == a[1][1] == a[2][0] == turn + 1:
				if drawing_progress <= 1:
					pygame.draw.line(screen, BLACK,
									(margin_w_big + (width-2*margin_w_big), margin_h_big),
									(margin_w_big + (width-2*margin_w_big)*(1-drawing_progress), margin_h_big+(height-2*margin_h_big)*drawing_progress), 8)
					drawing_progress += 0.01

	pygame.display.flip()
	clock.tick(60)
