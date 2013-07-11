import pygame, os, sys
import random
from pygame.locals import *


black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)

pygame.init()

width = 400
height = 400
size = [width, height]
screen = pygame.display.set_mode(size)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)

pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
snake = []

# Vectors
right = [10,0]
left = [-10,0]
up = [0,-10]
down = [0,10]

def load_image(name, colorkey=None):
	fullname = os.path.join('data', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'cannot load image:', name
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
			image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()



class Head(pygame.sprite.Sprite):
	def __init__(self, color = red):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([10,10])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.midtop = [200,200]
		self.follower = None
		self.direction = [10,0]

	def update(self):
		self.follower.pull()
		self.follower.rect.midtop = self.rect.midtop
		self.rect.midtop = self.rect.midtop[0] + self.direction[0], self.rect.midtop[1] + self.direction[1]


class Tail(pygame.sprite.Sprite):
	def __init__(self, leader, position, color = green):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([10,10])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.midtop = position
		self.leader = leader
		self.follower = None
		self.leader.follower = self
		self.direction = [10,0]

	def pull(self):
		if self.follower:
			self.follower.pull()
			self.follower.rect.midtop = self.rect.midtop

	def update(self):
		pass

class Apple(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([10,10])
		self.image.fill(red)
		self.rect = self.image.get_rect()
		self.rect.midtop = [10*random.randint(1,39), 10*random.randint(1,39)]

	def update(self):
		pass

class Block(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('stone.jpg')
		self.rect.midtop = [10*random.randint(1,39), 10*random.randint(1,39)]

	def update(self):
		pass



def on_screen(head):
	return (head.rect.midtop[0] > 0 and head.rect.midtop[0] < width and
		head.rect.midtop[1] > -4 and head.rect.midtop[1] < height)


def game_over():
	font = pygame.font.Font(None, 30)
	text1 = font.render("Game Over",  1, (100,200,100))
	text2 = font.render("Click to play again", 1, (100,200,100))
	text1pos = text1.get_rect()
	text1pos.midtop = size[0]/2, size[1]/2
	text2pos = text1.get_rect()
	text2pos.midtop = size[0]/2-30, size[1]/2 + 30
	screen.blit(text1, text1pos)
	screen.blit(text2, text2pos)
	pygame.display.flip()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
			if event.type == MOUSEBUTTONDOWN:
				main()


def main():
	head = Head()
	t1 = Tail(head, [190,200])
	t2 = Tail(t1,[180,200])
	tail = [t1,t2]
	snake = [head, t1, t2]
	blocks = []
	snake_group = pygame.sprite.Group()
	head_group = pygame.sprite.Group()
	block_group = pygame.sprite.Group()
	head_group.add(head)
	tail_group = pygame.sprite.Group()
	tail_group.add(t1)
	tail_group.add(t2)
	snake_group.add(snake)
	apple = Apple()
	applecount = 1
	allsprites = pygame.sprite.RenderPlain((snake_group, apple))


	def grow(snake):
		leader = snake[-1]
		name = 't%s' % str(len(snake)+1)
		name = Tail(leader, leader.rect.midtop)
		snake.append(name)
		snake_group.add(name)
		allsprites.add(name)
		tail.append(name)
		tail_group.add(name)

	def kill():
		for sprite in allsprites:
			sprite.kill()
			game_over()

	def make_block():
		name = 'block%s' % str(len(blocks))
		name = Block()
		block_group.add(name)
		allsprites.add(name)



	while True:
		clock.tick(18)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
			if event.type == KEYDOWN:
				if event.key == K_DOWN:
					if head.direction == up:
						pass
					else:
						head.direction = down
				elif event.key == K_UP:
					if head.direction == down:
						pass
					else:
						head.direction = up
				elif event.key == K_RIGHT:
					if head.direction == left:
						pass
					else:
						head.direction = right
				elif event.key == K_LEFT:
					if head.direction == right:
						pass
					else:
						head.direction = left


		if not apple in allsprites.sprites():
			apple = Apple()
			allsprites.add(apple)

		if not on_screen(head):
			kill()

		if pygame.sprite.groupcollide(head_group, tail_group,1,1):
			kill()
		if pygame.sprite.groupcollide(head_group, block_group,1,1):
			kill()
		if pygame.sprite.collide_rect(apple, head):
			grow(snake)
			apple.kill()
			applecount += 1
			if applecount %2 == 0:
				make_block()
			apple = Apple()
			allsprites.add(apple)

		allsprites.update()
		screen.blit(background, (0,0))
		allsprites.draw(screen)
		pygame.display.flip()







main()
pygame.quit()