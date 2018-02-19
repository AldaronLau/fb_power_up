import pygame, sys, os
from pygame.locals import *

screen = None;
	
# Based on "Python GUI in Linux frame buffer"
# http://www.karoltomala.com/blog/?p=679
disp_no = os.getenv("DISPLAY")
if disp_no:
	print("I'm running under X display = ", disp_no)

# Check which frame buffer drivers are available
# Start with fbcon since directfb hangs with composite output
drivers = ['fbcon', 'directfb', 'svgalib']
found = False
for driver in drivers:
	# Make sure that SDL_VIDEODRIVER is set
	if not os.getenv('SDL_VIDEODRIVER'):
		os.putenv('SDL_VIDEODRIVER', driver)
	try:
		pygame.display.init()
	except pygame.error:
		print('Driver: ' + driver + ' failed.')
		continue
	found = True
	break

if not found:
	raise Exception('No suitable video driver found!')

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print("Framebuffer size: " + str(size[0]) + "x" + str(size[1]))

H = int(480) # int(size[1])
W = int(640) # int((H * int(4)) / int(3))

screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)

# DISPLAYSURF = pygame.display.set_mode((W, H), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
# pygame.display.set_caption('Firebears Power Up')

LARGE_DIV = int(H / int(6))
SMALL_DIV = int(64)

FLOOR = pygame.image.load('floor.png')
SKY = pygame.image.load('sky.png')

TILE_FLOOR = pygame.transform.scale(FLOOR, (LARGE_DIV, LARGE_DIV))
TILE_SKY = pygame.transform.scale(SKY, (LARGE_DIV, LARGE_DIV))

POWER_CUBE = pygame.image.load('powercube.png')
ROBOT = pygame.image.load('robot.png')
YOU = pygame.image.load('you.png')
BASE = pygame.image.load('scale_base.png')
TOWER = pygame.image.load('scale_tower.png')
PLATFORM = pygame.image.load('scale_platform.png')

TILE_POWER_CUBE = pygame.transform.scale(POWER_CUBE, (SMALL_DIV, SMALL_DIV))
TILE_ROBOT = pygame.transform.scale(ROBOT, (SMALL_DIV, SMALL_DIV))
TILE_YOU = pygame.transform.scale(YOU, (SMALL_DIV, SMALL_DIV))
TILE_BASE = pygame.transform.scale(BASE, (SMALL_DIV, SMALL_DIV))
TILE_TOWER = pygame.transform.scale(TOWER, (SMALL_DIV, SMALL_DIV))
TILE_PLATFORM = pygame.transform.scale(PLATFORM, (SMALL_DIV, SMALL_DIV))

PLAYER_X = 0
ROBOT_X = W - SMALL_DIV

L = 0
R = 0

HAS_ROBOT = False
HAS_YOU = False
ROBOT_HAS_POWERCUBE = False
HAS_POWER_CUBE = False
MOVE_NEG = False
MOVE_POS = False

FPS = 30
FPSCLOCK = pygame.time.Clock()

ROBOT_CYCLE = 0
COUNTDOWN = 30

pygame.font.init()
font = pygame.font.Font('SourceCodePro-Bold.ttf', 30)
c = (0, 0, 0)
text = font.render('LEFT/RIGHT=Move, UP=Pick Up, DOWN=Set On Scale', True, c)

STATE = 0

while True: # main game loop
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			elif event.key in (K_UP, K_w) and HAS_YOU == False:
				if abs(PLAYER_X - ROBOT_X) < (SMALL_DIV / 2):
					HAS_ROBOT = True
					ROBOT_CYCLE = 5
				elif PLAYER_X < SMALL_DIV:
					HAS_POWER_CUBE = True
			elif event.key in (K_DOWN, K_s) and HAS_YOU == False:
				if HAS_ROBOT:
					HAS_ROBOT = False
				elif PLAYER_X >= ((W / 2) - (SMALL_DIV / 2)) - (2 * SMALL_DIV) and PLAYER_X < (W / 2) and HAS_POWER_CUBE:
					HAS_POWER_CUBE = False
					L = L + 1
			elif event.key in (K_LEFT, K_a):
				MOVE_NEG = True
			elif event.key in (K_RIGHT, K_d):
				MOVE_POS = True
			elif event.key == K_BACKSPACE:
				L = 0
				R = 0
				ROBOT_CYCLE = 0
				COUNTDOWN = 30
				MOVE_NEG = False
				MOVE_POS = False
				PLAYER_X = 0
				ROBOT_X = W - SMALL_DIV
				text = font.render('LEFT/RIGHT=Move, UP=Pick Up, DOWN=Set On Scale', True, c)
				STATE = 0
				HAS_ROBOT = False
				HAS_YOU = False
				ROBOT_HAS_POWERCUBE = False
				HAS_POWER_CUBE = False
		elif event.type == KEYUP:
			if event.key in (K_LEFT, K_a):
				MOVE_NEG = False
			elif event.key in (K_RIGHT, K_d):
				MOVE_POS = False

	if MOVE_NEG and PLAYER_X > 0 and HAS_YOU == False:
		PLAYER_X -= SMALL_DIV / 8
		if HAS_ROBOT:
			ROBOT_X = PLAYER_X
	if MOVE_POS and PLAYER_X < W and HAS_YOU == False:
		PLAYER_X += SMALL_DIV / 8
		if HAS_ROBOT:
			ROBOT_X = PLAYER_X

	screen.fill((127, 127, 255))

	for i in range(0, 8):
		for j in range(0, 5):
			gRect = pygame.Rect( (
				i * LARGE_DIV,
				j * LARGE_DIV,
				LARGE_DIV,
				LARGE_DIV) )
			screen.blit(TILE_SKY, gRect)

	for i in range(0, 8):
		gRect = pygame.Rect( (
			i * LARGE_DIV,
			5 * LARGE_DIV,
			LARGE_DIV,
			LARGE_DIV) )
		screen.blit(TILE_FLOOR, gRect)

	# Loader Stations
	gRect = pygame.Rect( (
		0,
		H - (SMALL_DIV + LARGE_DIV),
		SMALL_DIV,
		SMALL_DIV) )
	screen.blit(TILE_POWER_CUBE, gRect)

	gRect = pygame.Rect( (
		W - SMALL_DIV,
		H - (SMALL_DIV + LARGE_DIV),
		SMALL_DIV,
		SMALL_DIV) )
	screen.blit(TILE_POWER_CUBE, gRect)

	# scale
	for i in range(-2, 3):
		gRect = pygame.Rect( (
			((W / 2) - (SMALL_DIV / 2)) + (i * SMALL_DIV),
			H - (SMALL_DIV + LARGE_DIV),
			SMALL_DIV,
			SMALL_DIV) )
		screen.blit(TILE_BASE, gRect)

	for i in range(1, 5):
		gRect = pygame.Rect( (
			(W / 2) - (SMALL_DIV / 2),
			(H - (SMALL_DIV + LARGE_DIV)) - (i * SMALL_DIV),
			SMALL_DIV,
			SMALL_DIV) )
		screen.blit(TILE_TOWER, gRect)

	# Players
	if HAS_YOU:
		gRect = pygame.Rect( (
			PLAYER_X,
			H - ((SMALL_DIV * 2) + LARGE_DIV),
			SMALL_DIV,
			SMALL_DIV) )
		screen.blit(TILE_YOU, gRect)
	else:
		gRect = pygame.Rect( (
			PLAYER_X,
			H - (SMALL_DIV + LARGE_DIV),
			SMALL_DIV,
			SMALL_DIV) )
		screen.blit(TILE_YOU, gRect)

	if HAS_POWER_CUBE:
		if HAS_YOU:
			gRect = pygame.Rect( (
				ROBOT_X,
				H - ((SMALL_DIV * 3) + LARGE_DIV),
				SMALL_DIV,
				SMALL_DIV) )
			screen.blit(TILE_POWER_CUBE, gRect)
		else:
			gRect = pygame.Rect( (
				PLAYER_X,
				H - ((SMALL_DIV * 2) + LARGE_DIV),
				SMALL_DIV,
				SMALL_DIV) )
			screen.blit(TILE_POWER_CUBE, gRect)

	if HAS_ROBOT:
		gRect = pygame.Rect( (
			PLAYER_X,
			H - ((SMALL_DIV * 2) + LARGE_DIV),
			SMALL_DIV,
			SMALL_DIV) )
		screen.blit(TILE_ROBOT, gRect)
	else:
		gRect = pygame.Rect( (
			ROBOT_X,
			H - (SMALL_DIV + LARGE_DIV),
			SMALL_DIV,
			SMALL_DIV) )
		screen.blit(TILE_ROBOT, gRect)

	if ROBOT_HAS_POWERCUBE:
		if HAS_ROBOT:
			gRect = pygame.Rect( (
				PLAYER_X,
				H - ((SMALL_DIV * 3) + LARGE_DIV),
				SMALL_DIV,
				SMALL_DIV) )
			screen.blit(TILE_POWER_CUBE, gRect)
		else:
			gRect = pygame.Rect( (
				ROBOT_X,
				H - ((SMALL_DIV * 2) + LARGE_DIV),
				SMALL_DIV,
				SMALL_DIV) )
			screen.blit(TILE_POWER_CUBE, gRect)

	# balancer
	if L > R:
		BALANCER = 1
	elif R > L:
		BALANCER = -1
	else:
		BALANCER = 0

	# left scale
	for i in range(1, 4):
		gRect = pygame.Rect( (
			(W / 2) - (SMALL_DIV / 2) + (i * SMALL_DIV),
			(H - (SMALL_DIV + LARGE_DIV)) - ((3 + BALANCER) * SMALL_DIV),
			SMALL_DIV,
			SMALL_DIV) )
		screen.blit(TILE_PLATFORM, gRect)

	# right scale
	for i in range(1, 4):
		gRect = pygame.Rect( (
			(W / 2) - (SMALL_DIV / 2) - (i * SMALL_DIV),
			(H - (SMALL_DIV + LARGE_DIV)) - ((3 - BALANCER) * SMALL_DIV),
			SMALL_DIV,
			SMALL_DIV) )
		screen.blit(TILE_PLATFORM, gRect)

	# power cubes
	for i in range(0, L):
		gRect = pygame.Rect( (
			(W / 2) - (SMALL_DIV / 2) - (2 * SMALL_DIV),
			(H - (SMALL_DIV + LARGE_DIV)) - ((4 + i - BALANCER) * SMALL_DIV),
			SMALL_DIV,
			SMALL_DIV) )
		screen.blit(TILE_POWER_CUBE, gRect)

	for i in range(0, R):
		gRect = pygame.Rect( (
			(W / 2) - (SMALL_DIV / 2) + (2 * SMALL_DIV),
			(H - (SMALL_DIV + LARGE_DIV)) - ((4 + i + BALANCER) * SMALL_DIV),
			SMALL_DIV,
			SMALL_DIV) )
		screen.blit(TILE_POWER_CUBE, gRect)

	# 
	if STATE == 0:
		if L > 5:
			text = font.render('YOU WIN! BACKSPACE=RESET', True, c)
			STATE = 1
		if R > 5:
			text = font.render('YOU LOSE! BACKSPACE=RESET', True, c)
			STATE = 1

	# TEXT
	screen.blit(text, (0, 0))

	pygame.display.update()

	# AI
	if STATE == 0:
		if ROBOT_CYCLE == 0:
			COUNTDOWN = COUNTDOWN - 1
			if COUNTDOWN < 1:
				ROBOT_HAS_POWERCUBE = True
				ROBOT_CYCLE = 1
		elif ROBOT_CYCLE == 1:
			ROBOT_X -= SMALL_DIV / 8
			if ROBOT_X <= ((W / 2) + (SMALL_DIV / 2)) + (1 * SMALL_DIV):
				COUNTDOWN = 30
				ROBOT_CYCLE = 2
		elif ROBOT_CYCLE == 2:
			COUNTDOWN = COUNTDOWN - 1
			if COUNTDOWN < 1:
				ROBOT_HAS_POWERCUBE = False
				ROBOT_CYCLE = 3
				COUNTDOWN = 30
				R = R + 1
		elif ROBOT_CYCLE == 3:
			COUNTDOWN = COUNTDOWN - 1
			if COUNTDOWN < 1:
				ROBOT_CYCLE = 4
				if L > 2 and R < 3:
					ROBOT_CYCLE = 6
		elif ROBOT_CYCLE == 4:
			ROBOT_X += SMALL_DIV / 8
			if L > 2 and R < 3:
				ROBOT_CYCLE = 6
			if ROBOT_X >= (W - SMALL_DIV):
				COUNTDOWN = 30
				ROBOT_CYCLE = 0
		elif ROBOT_CYCLE == 5:
			if HAS_ROBOT == False:
				ROBOT_X += SMALL_DIV / 8
				if ROBOT_X >= (W - SMALL_DIV):
					COUNTDOWN = 30
					ROBOT_CYCLE = 0
		elif ROBOT_CYCLE == 6:
			ROBOT_X -= SMALL_DIV / 8
			if abs(PLAYER_X - ROBOT_X) < (SMALL_DIV / 2):
				HAS_YOU = True
				ROBOT_CYCLE = 7
			elif ROBOT_X <= 0:
				ROBOT_CYCLE = 5
		elif ROBOT_CYCLE == 7:
			ROBOT_X += SMALL_DIV / 8
			PLAYER_X = ROBOT_X
			if ROBOT_X >= (W - SMALL_DIV):
				COUNTDOWN = 30
				ROBOT_CYCLE = 0
				HAS_YOU = False

	FPSCLOCK.tick(FPS)
