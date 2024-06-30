from typing import Self
import pygame
from pygame.mixer_music import play
import time
from random import randint
from sys import exit


class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('images/fou.png').convert_alpha()
		self.rect = self.image.get_rect(center = (screen.get_width()//2, screen.get_height()//2))

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.rect.top -= int(300 * dt)
		if keys[pygame.K_s]:
			self.rect.top += int(300 * dt)
		if keys[pygame.K_a]:	
			self.rect.left -= int(300 * dt) 
		if keys[pygame.K_d]:
			self.rect.left += int(300 * dt)

		if self.rect.left < 0:
			self.rect.x += (screen.get_width() - 50)
		elif self.rect.right > screen.get_width():
			self.rect.x -= (screen.get_width() - 50)

		if self.rect.y >= (screen.get_height() - 50):
			self.rect.y = 0
		elif self.rect.y <= 0:
			self.rect.y = (screen.get_height() - 50)

	def update(self):
		self.player_input()

class Enemy(pygame.sprite.Sprite):
	def __init__(self, type):
		super().__init__()

		if type == "soul":
			self.image = pygame.image.load('images/enemy_1.png').convert_alpha()
			self.rect = self.image.get_rect(topleft = (randint(50, screen.get_width() - 50), randint(0, screen.get_height() // 4)))

	def enemy_movement(self):
		choice = randint(1, 4)
		if choice == 1:
			self.rect.x -= 5
		elif choice == 2:
			self.rect.x += 5

		if self.rect.left < 0:
			self.rect.x += (screen.get_width() - 50)
		elif self.rect.right > screen.get_width():
			self.rect.x -= (screen.get_width() - 50)

		self.rect.y += 1

		if self.rect.y > screen.get_height():
			self.rect.y = 0

	def update(self):
		self.enemy_movement()

def get_time(timer):
	secs = int((timer % 60) // 1)
	mins = int(((timer % 3600) - secs) // 60)
	hours = int((timer - (mins * 60) - secs) // 3600)
	result = str(hours) + " : "
	if (mins < 10):
		result = result + "0"
	result += str(mins) + " : "
	if (secs < 10):
		result = result + "0"
	result += str(secs)
	return result

def has_collision():
	if pygame.sprite.spritecollide(player.sprite, enemies_group, False):
		return False
	return True

pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("IDK Something")
entry_font = pygame.font.Font('fonts/linux_biolinum/LinBiolinum_RB.otf', 35)
exit_font = pygame.font.Font('fonts/linux_biolinum/LinBiolinum_RB.otf', 40)
dete_font = pygame.font.Font('fonts/linux_biolinum/LinBiolinum_RI.otf', 30)

clock = pygame.time.Clock()
running = True
dt = 0

player = pygame.sprite.GroupSingle()
player.add(Player())
enemies_group = pygame.sprite.Group()

sora_surface = pygame.image.load('images/bg.jpg').convert()

opening_text = entry_font.render("Fate Space Order", False, "Gold")
tostart_text = entry_font.render("Press SPACE to Begin!", False, "Gold")
game_over = exit_font.render("GAME OVER!!", False, "Red")

soul_surf = pygame.image.load('images/enemy_1.png').convert_alpha()
soul_rect = soul_surf.get_rect(topleft = (300, 200))

shield_surf = pygame.image.load('images/shield.png')
shield_rect = shield_surf.get_rect(topleft = (80, 150))

enemies_rect_list = []
game_run = False
start_time = 0
score = 0
timer = ""
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2000)

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if game_run:
			if event.type == enemy_timer:
				enemies_group.add(Enemy("soul"))

	keys_pressed = ""
	keys = pygame.key.get_pressed()

	if game_run == False:
		screen.fill("Purple")
		screen.blit(opening_text, (314,95))
		player.update()
		player.draw(screen)
		screen.blit(tostart_text, (275, 150))
		if keys[pygame.K_SPACE]:
			start_time = time.time()
			game_run = True
	else:
		screen.blit(sora_surface, (0,0))
		
		player.update()
		player.draw(screen)
		enemies_group.update()
		for enemy in enemies_group:
			if enemy.rect.y == screen.get_height():
				enemy.rect.y = 0
				score += 1
		enemies_group.draw(screen)

		timer = get_time(time.time() - start_time)
		time_surf = dete_font.render(f"Timer = {timer}", False, "White")
		time_rect = time_surf.get_rect(topleft = (15, 8))
		screen.blit(time_surf, time_rect)

		score_surf = dete_font.render(f"Score = {score}", False, "White")
		score_rect = score_surf.get_rect(topright = (screen.get_width() - 15, 8))
		screen.blit(score_surf, score_rect)

		game_run = has_collision()
		if not game_run:
			screen.blit(game_over, (320, 100))
			pygame.display.flip()
			time.sleep(2)
			break

	screen.blit(opening_text, (314,95))
	pygame.display.flip()
	dt = clock.tick(60) / 1000
pygame.quit()