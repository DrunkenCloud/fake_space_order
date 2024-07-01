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
        self.rect.y -= 3

    def destroy(self):
        if not game_run or self.rect.y < 0:
            self.kill()

    def update(self):
        self.attack_movement()
        self.destroy()

class Trial_Attack(pygame.sprite.Sprite):
    def __init__(self, type, pos):
        super().__init__()

        if type == "ball":
            self.image = pygame.image.load("images/shadow_ball.png").convert_alpha()
            self.rect = self.image.get_rect(midbottom = (pos[0], pos[1]))

    def attack_movement(self):
        self.rect.y -= 3

    def destroy(self):
        if self.rect.y < 0 or game_run:
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
reloader = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

enemies_group = pygame.sprite.Group()
attacks_group = pygame.sprite.Group()
trial_attacks_group = pygame.sprite.Group()

sora_surface = pygame.image.load("images/bg.jpg").convert()
wasd_surface = pygame.image.load("images/wasd.jpeg").convert_alpha()
shadow_ball_surf = pygame.image.load("images/shadow_ball.png").convert_alpha()
soul_surf = pygame.image.load("images/enemy_1.png").convert_alpha()

opening_text = entry_font.render("Fake Space Order", False, "Gold")
tostart_text = entry_font.render("Press ENTER to Enter/Exit (2s Cooldown)", False, "Green")
toexit_text = entry_font.render("Press ESCAPE to Exit the Game", False, "LightBlue")
movement = dete_font.render("Move Fou via WASD", False, "Black")
how_to_attack1 = dete_font.render("Attack using SPACE", False, "Pink")
how_to_attack2 = dete_font.render("Reload time is 2 seconds", False, "Pink")
enemies_kill1 = dete_font.render("These are the Enemies", False, "Violet")
enemies_kill2 = dete_font.render("If You Touch Them", False, "Violet")
enemies_kill3 = dete_font.render("You Loose", False, "Violet")
enemies_kill4 = dete_font.render("Kill Them", False, "Violet")
enemies_kill5 = dete_font.render("To Increase your Score", False, "Violet")
game_over = exit_font.render("GAME OVER!!", False, "Red")

game_run = False
start_time = time.time()
score = 0
high_score = 0
timer = ""
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)
reload_timer = time.time()

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
        if music != 1:
            play_music(music1)
            music = 1
        screen.fill("Purple")
        screen.blit(wasd_surface, (65, 350))
        screen.blit(tostart_text, (120, 150))
        screen.blit(toexit_text, (200, 200))
        highscore_text = dete_font.render(f"High Score: {high_score}", False, "Orange")
        screen.blit(highscore_text, (360, 300))
        screen.blit(movement, (40, 300))
        screen.blit(how_to_attack1, (320, 350))
        screen.blit(how_to_attack2, (295, 380))
        screen.blit(shadow_ball_surf, (310, 440))
        screen.blit(enemies_kill1, (600, 300))
        screen.blit(enemies_kill2, (600, 330))
        screen.blit(enemies_kill3, (600, 360))
        screen.blit(enemies_kill4, (600, 390))
        screen.blit(enemies_kill5, (600, 420))
        screen.blit(soul_surf, (775, 365))
        if (time.time() - reload_timer > 2):
            reload_rect = pygame.rect.Rect(360,430,200,50)
        else:
            reload_rect = pygame.rect.Rect(360, 430, 200*((time.time() - reload_timer) / 2), 50)    
        pygame.draw.rect(screen, "Pink", reload_rect)
        pygame.draw.rect(screen, "Black", pygame.rect.Rect(360,430,200,50), 7)
        if keys[pygame.K_SPACE]:
            if (time.time() - reload_timer) > 2:
                trial_attacks_group.add(Trial_Attack("ball", [player.sprite.rect.x, player.sprite.rect.y]))
                reload_timer = time.time()
        if keys[pygame.K_RETURN] and (time.time() - start_time) > 2:
            start_time = time.time()
            game_run = True
            reload_timer = time.time()
        if keys[pygame.K_ESCAPE]:
            running = False
            continue
        player.update()
        player.draw(screen)
        trial_attacks_group.update()
        trial_attacks_group.draw(screen)
    else:
        if keys[pygame.K_ESCAPE]:
            running = False
            continue
        if keys[pygame.K_RETURN] and (time.time() - start_time) > 2:
            start_time = time.time()
            game_run = False
            pygame.display.flip()
            if score > high_score:
                high_score = score
            score = 0
            enemies_group.update()
            attacks_group.update()
            continue
        if music != 2:
            play_music(music2)
            music = 2
        screen.blit(sora_surface, (0,0))
        player.update()
        player.draw(screen)
        enemies_group.update()
        enemies_group.draw(screen)
        if keys[pygame.K_SPACE]:
            if (time.time() - reload_timer) > 2:
                attacks_group.add(Attack("ball", [player.sprite.rect.x, player.sprite.rect.y]))
                reload_timer = time.time()
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

        if (time.time() - reload_timer > 2):
            reload_rect = pygame.rect.Rect(600,400,200,50)
        else:
            reload_rect = pygame.rect.Rect(600, 400, 200*((time.time() - reload_timer) / 2), 50)    
        pygame.draw.rect(screen, "Purple", reload_rect)
        pygame.draw.rect(screen, "Black", pygame.rect.Rect(600,400,200,50), 7)

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

    screen.blit(opening_text, (310,100))
    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit()