import pygame, random

pygame.init()

#Display Variables
window_width = 700
window_height = 300
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Chrome Dinosaur Game')
game_font = pygame.font.SysFont('04B_19.ttf',22)
jump_sound = pygame.mixer.Sound('sound/upbeat.wav')

#Map and player movement
player_frame = [pygame.image.load('images/dino.png').convert_alpha(), pygame.image.load('images/dino2.png').convert_alpha(), 
                pygame.image.load('images/dino3.png').convert_alpha()]
player_duck = [pygame.image.load('images/dino_duck.png').convert_alpha(), pygame.image.load('images/dino_duck2.png').convert_alpha()]
map_surface = pygame.image.load('images/floor.png').convert_alpha()
map_x_pos = 0
incrementer = 4.25
player_index=0
player_index_duck=0

#enemy movement and other map items
bird_frame = [pygame.image.load('images/bird.png').convert_alpha(), pygame.image.load('images/bird2.png').convert_alpha()]
bird_index=0
cactus_surface = pygame.image.load('images/cactus.png').convert_alpha()
enemy_list =[]
SPAWNENEMY = pygame.USEREVENT
pygame.time.set_timer(SPAWNENEMY,700)
DINORUN = pygame.USEREVENT+1
pygame.time.set_timer(DINORUN,200)
birdy = [172, 180, 210]
BIRDFLAP = pygame.USEREVENT+2
pygame.time.set_timer(BIRDFLAP, 300)

#Jumping Variables
isJump = False
jumpCount = 10
run = True

#Game Over Screen
game_over_surface = pygame.image.load('images/game_over.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center =(350,90))
gameActive = True
score = 0
high_score =0

def create_cactus():
    new_cactus = cactus_surface.get_rect(center =  (710, 234))
    return new_cactus

def create_bird():
    random_bird_pos = random.choice(birdy)
    new_bird = bird_surface.get_rect(midbottom = (710, random_bird_pos))
    return new_bird
    
def move_enemy(enemys, incrementer):
    for enemy in enemys:
        enemy.centerx -= 2 + incrementer
    return enemys

def draw_enemy(Enemys):
    for enemy in Enemys:
        if enemy[2] == 56:
            window.blit(bird_surface, enemy)
        else:
            window.blit(cactus_surface, enemy)

def background_loop():
    white = 0,0,0
    window.fill(white)
    window.blit(map_surface, (int(map_x_pos),75))
    window.blit(map_surface, (int(map_x_pos + 2000),75))
    window.blit(player_surface, player_rect)

def checkCollision(Enemys):
    for enemy in Enemys:
        if player_rect.colliderect(enemy):
            return True
    return False

def score_display(game_state):
    if game_state=="main_game":
        score_surface = game_font.render(f'Score '+ str(int(score)), True,(105,105,105))
        score_rect = score_surface.get_rect(center = (658,40))
        window.blit(score_surface, score_rect)
    if game_state =="game_over":
        high_score_surface = game_font.render(f'High Score '+ str(int(high_score)), True,(105,105,105))
        high_score_rect = high_score_surface.get_rect(center = (640,20))
        window.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score >= high_score:
        high_score = score
    return high_score

#Main loop that runs during the game
while run:
    pygame.time.delay(10)
    jump_sound.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == SPAWNENEMY:
            r = random.randrange(0,2)
            if r ==0: enemy_list.append(create_bird())
            else: enemy_list.append(create_cactus())
        if event.type ==DINORUN and keys[pygame.K_DOWN]==False:
            player_index+=1
            if player_index >2:
                player_index=0
        if event.type==DINORUN and keys[pygame.K_DOWN]:
            player_index_duck +=1
            if player_index_duck>1:
                player_index_duck=0
        if event.type==BIRDFLAP:
            bird_index+= 1
            if bird_index>1:
                bird_index=0
    keys = pygame.key.get_pressed() #Checks for keys being pressed
    if not(isJump):
        if keys[pygame.K_UP]:
            isJump = True
        if keys[pygame.K_DOWN]:
            player_surface = player_duck[player_index_duck]
            player_rect = player_surface.get_rect(center = (140, 235))
            bird_surface = bird_frame[bird_index]
        if not keys[pygame.K_DOWN]:
            player_surface = player_frame[player_index]
            bird_surface = bird_frame[bird_index]
            player_rect = player_surface.get_rect(center = (140, 227))
        if gameActive == False and keys[pygame.K_SPACE]:
            gameActive= True
            enemy_list.clear()
            player_rect.center = (140, 235)
            incrementer = 4.25
            score = 0

    else:
        if jumpCount >= -10:
            negative = 1
            if jumpCount <0:
                negative = -1
            player_rect.centery -= int(jumpCount **2 *0.25 * negative)
            jumpCount -=1
            
        else:
            isJump = False
            player_rect.centery = 227
            jumpCount = 10
    if gameActive:
        map_x_pos -= incrementer
        background_loop()
        if map_x_pos <= -2000: #Checks for map being scrolled off on the side
            map_x_pos = 0
            incrementer = incrementer + 0.01
        if checkCollision(enemy_list):
            gameActive= False
            window.blit(game_over_surface, game_over_rect)
            high_score = update_score(score, high_score)
            score_display('game_over')
        enemy_list = move_enemy(enemy_list, incrementer)
        score += 0.1
        checkCollision(enemy_list)
        draw_enemy(enemy_list)
        score_display('main_game')
        pygame.display.update()
print("Game Over")