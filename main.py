from re import template
import pygame
from sys import exit, set_coroutine_origin_tracking_depth
from pygame.mixer_music import play
import time
from random import randint

pygame.init()
screen = pygame.display.set_mode((900, 500))

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

def enemy_movement(enemy_list, score):
	if enemy_list:
		for enemy_rect in enemy_list:
			choice = randint(1, 4)
			if choice == 1:
				enemy_rect.x -= 5
			elif choice == 2:
				enemy_rect.x += 5

			if enemy_rect.left < 0:
				enemy_rect.x += (screen.get_width() - 50)
			elif enemy_rect.right > screen.get_width():
				enemy_rect.x -= (screen.get_width() - 50)

			enemy_rect.y += 1

			if enemy_rect.y == screen.get_height():
				enemy_rect.y = 0
				score += 1

			screen.blit(soul_surf, enemy_rect)
		return enemy_list,score
	else: return [],score

pygame.display.set_caption("IDK Something")
entry_font = pygame.font.Font('fonts/linux_biolinum/LinBiolinum_RB.otf ', 35)
exit_font = pygame.font.Font('fonts/linux_biolinum/LinBiolinum_RB.otf ', 40)
dete_font = pygame.font.Font('fonts/linux_biolinum/LinBiolinum_RI.otf ', 30)

clock = pygame.time.Clock()
running = True
dt = 0

sora_surface = pygame.image.load('images/bg.jpg').convert()

opening_text = entry_font.render("Fate Space Order", False, "Gold")
tostart_text = entry_font.render("Press SPACE to Begin!", False, "Gold")
game_over = exit_font.render("GAME OVER!!", False, "Red")

soul_surf = pygame.image.load('images/enemy_1.png').convert_alpha()
soul_rect = soul_surf.get_rect(topleft = (300, 200))

fou_surf = pygame.image.load('images/fou.png').convert_alpha()
fou_rect = fou_surf.get_rect(center = (screen.get_width() // 2 ,screen.get_height() // 2))

shield_surf = pygame.image.load('images/shield.png')
shield_rect = shield_surf.get_rect(topleft = (80, 150))

enemies_rect_list = []

start_time = 0
game_run = False
score = 0
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2000)

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if game_run:
			if event.type == enemy_timer:
				enemies_rect_list.append(soul_surf.get_rect(topleft = (randint(50, screen.get_width() - 50), randint(0, screen.get_height() // 4))))

	keys_pressed = ""
	keys = pygame.key.get_pressed()
	if keys[pygame.K_w]:
		fou_rect.top -= int(300 * dt)
		keys_pressed += "W" + " "
	if keys[pygame.K_s]:
		fou_rect.top += int(300 * dt)
		keys_pressed += "S" + " "
	if keys[pygame.K_a]:	
		fou_rect.left -= int(300 * dt) 
		keys_pressed += "A" + " "
	if keys[pygame.K_d]:
		fou_rect.left += int(300 * dt)
		keys_pressed += "D" + " "

	if fou_rect.left < 0:
		fou_rect.x += (screen.get_width() - 50)
	elif fou_rect.right > screen.get_width():
		fou_rect.x -= (screen.get_width() - 50)

	if fou_rect.y >= (screen.get_height() - 50):
		fou_rect.y = 0
	elif fou_rect.y <= 0:
		fou_rect.y = (screen.get_height() - 50)

	if game_run == False:
		screen.fill("Purple")
		screen.blit(opening_text, (314,95))
		screen.blit(fou_surf, fou_rect)
		screen.blit(tostart_text, (275, 150))
		if keys[pygame.K_SPACE]:
			start_time = time.time()
			game_run = True
	else:
		screen.blit(sora_surface, (0,0))

		enemies_rect_list, score = enemy_movement(enemies_rect_list, score)
		
		screen.blit(fou_surf, fou_rect)
		timer = get_time(time.time() - start_time)
		time_surf = dete_font.render(f"Timer = {timer}", False, "White")
		time_rect = time_surf.get_rect(topleft = (15, 8))
		screen.blit(time_surf, time_rect)

		score_surf = dete_font.render(f"Score = {score}", False, "White")
		score_rect = score_surf.get_rect(topright = (screen.get_width() - 15, 8))
		screen.blit(score_surf, score_rect)

		if enemies_rect_list:
			for enemy_rect in enemies_rect_list:
				if(fou_rect.colliderect(enemy_rect)):
					screen.blit(game_over, (320, 100))
					pygame.display.flip()
					time.sleep(1)
					running = False
					break
			else:		
				screen.blit(opening_text, (314,95))
		
	pygame.display.flip()
	dt = clock.tick(60) / 1000
pygame.quit()