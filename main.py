from re import template
import pygame
from sys import exit, set_coroutine_origin_tracking_depth
from pygame.mixer_music import play
import time

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

pygame.init()
screen = pygame.display.set_mode((900, 500))
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

start_time = 0
game_run = False
score = 0

while running:
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

	keys = pygame.key.get_pressed()
	if keys[pygame.K_w]:
		fou_rect.top -= int(300 * dt)
	if keys[pygame.K_s]:
		fou_rect.top += int(300 * dt) 
	if keys[pygame.K_a]:	
		fou_rect.left -= int(300 * dt) 
	if keys[pygame.K_d]:
		fou_rect.left += int(300 * dt) 

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

		soul_rect.left -= 3
		if soul_rect.left < 0:
			score += 1
			soul_rect.right = screen.get_width()
		
		screen.blit(soul_surf, soul_rect)
		screen.blit(fou_surf, fou_rect)
		timer = get_time(time.time() - start_time)
		time_surf = dete_font.render(f"Timer = {timer}", False, "White")
		time_rect = time_surf.get_rect(topleft = (15, 8))
		screen.blit(time_surf, time_rect)

		score_surf = dete_font.render(f"Score = {score}", False, "White")
		score_rect = score_surf.get_rect(topright = (screen.get_width() - 15, 8))
		screen.blit(score_surf, score_rect)

		if(fou_rect.colliderect(soul_rect)):
			screen.blit(game_over, (320, 100))
			pygame.display.flip()
			time.sleep(1)
			break
		screen.blit(opening_text, (314,95))
		
	pygame.display.flip()
	dt = clock.tick(60) / 1000

pygame.quit()