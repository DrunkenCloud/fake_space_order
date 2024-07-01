import pygame
import time
from random import randint


class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("images/fou.png").convert_alpha()
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
			self.image = pygame.image.load("images/enemy_1.png").convert_alpha()
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

	def destroy(self):
		if not game_run:
			self.kill()

	def update(self):
		self.enemy_movement()
		self.destroy()

class Attack(pygame.sprite.Sprite):
	def __init__(self, type, pos):
		super().__init__()

		if type == "ball":
			self.image = pygame.image.load("images/shadow_ball.png").convert_alpha()
			self.rect = self.image.get_rect(midbottom = (pos[0], pos[1]))

	def attack_movement(self):
		self.rect.y -= 2

	def destroy(self):
		if not game_run:
			self.kill()

	def update(self):
		self.attack_movement()
		self.destroy()

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

def enemy_kill():
	collisions = pygame.sprite.groupcollide(attacks_group, enemies_group, True, True)
	return sum(len(collided_enemies) for collided_enemies in collisions.values())

def play_music(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(-1)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("Dont sue me for Copyright pls")
entry_font = pygame.font.Font("fonts/linux_biolinum/LinBiolinum_RB.otf", 35)
exit_font = pygame.font.Font("fonts/linux_biolinum/LinBiolinum_RB.otf", 40)
dete_font = pygame.font.Font("fonts/linux_biolinum/LinBiolinum_RI.otf", 30)
music1 = "songs/holo.mp3"
music2 = "songs/Zoltraak.mp3"

clock = pygame.time.Clock()
running = True
dt = 0
music = 2

player = pygame.sprite.GroupSingle()
player.add(Player())

enemies_group = pygame.sprite.Group()
attacks_group = pygame.sprite.Group()

sora_surface = pygame.image.load("images/bg.jpg").convert()

opening_text = entry_font.render("Fake Space Order", False, "Gold")
tostart_text = entry_font.render("Press SPACE to Begin!", False, "Green")
toexit_text = entry_font.render("Press ENTER to Exit the Game", False, "LightBlue")
game_over = exit_font.render("GAME OVER!!", False, "Red")

game_run = False
start_time = 0
score = 0
high_score = 0
timer = ""
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2000)
attack_timer = pygame.USEREVENT + 2
pygame.time.set_timer(attack_timer, 2000)

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if game_run:
			if event.type == enemy_timer:
				enemies_group.add(Enemy("soul"))

			if event.type == attack_timer:
				for players in player:
					attacks_group.add(Attack("ball", [players.rect.x, players.rect.y]))

	keys_pressed = ""
	keys = pygame.key.get_pressed()

	if game_run == False:
		if music != 1:
			play_music(music1)
			music = 1
		screen.fill("Purple")
		screen.blit(opening_text, (314,100))
		player.update()
		player.draw(screen)
		screen.blit(tostart_text, (275, 150))
		screen.blit(toexit_text, (210, 200))
		highscore_text = dete_font.render(f"High Score: {high_score}", False, "Orange")
		screen.blit(highscore_text, (360, 300))
		if keys[pygame.K_SPACE]:
			start_time = time.time()
			game_run = True
		if keys[pygame.K_RETURN]:
			running = False
			continue
	else:
		if music != 2:
			play_music(music2)
			music = 2
		screen.blit(sora_surface, (0,0))
		player.update()
		player.draw(screen)
		enemies_group.update()
		enemies_group.draw(screen)
		attacks_group.update()
		attacks_group.draw(screen)
		
		timer = get_time(time.time() - start_time)
		time_surf = dete_font.render(f"Timer = {timer}", False, "White")
		time_rect = time_surf.get_rect(topleft = (15, 8))
		screen.blit(time_surf, time_rect)

		score += enemy_kill()
		score_surf = dete_font.render(f"Score = {score}", False, "White")
		score_rect = score_surf.get_rect(topright = (screen.get_width() - 15, 8))
		screen.blit(score_surf, score_rect)

		game_run = has_collision()
		if not game_run:
			screen.blit(game_over, (320, 100))
			pygame.display.flip()
			time.sleep(1.5)
			if score > high_score:
				high_score = score
			score = 0
			enemies_group.update()
			attacks_group.update()
			continue

	screen.blit(opening_text, (314,100))
	pygame.display.flip()
	dt = clock.tick(60) / 1000
pygame.quit()