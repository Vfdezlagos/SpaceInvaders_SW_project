'''Space invader clone game'''

import random
import math
import pygame
from pygame import mixer

# Inicializar pygame
pygame.init()

# crear pantalla
screen = pygame.display.set_mode((800, 600))


# Titulo e icono
pygame.display.set_caption('Invasión espacial (star wars edition)')

icon = pygame.image.load('./assets/nave-imperial-32px.png')
pygame.display.set_icon(icon)

background = pygame.image.load('./assets/background-image.png')


# Agregar musica
mixer.music.load('./assets/main starwars 16 bits.mp3')
mixer.music.set_volume(0.5)
mixer.music.play(-1)


# JUGADOR
# variables del jugador
player_sprite = pygame.image.load('./assets/nave-espacial-64px.png')
PLAYER_POS_X = 368
PLAYER_POS_Y = 520

X_POS_CHANGE = 0
Y_POS_CHANGE = 0

# Funcion jugador
def player(x_pos, y_pos):
    '''player function'''
    screen.blit(player_sprite, (x_pos, y_pos))




#variable puntaje
SCORE = 0
font = pygame.font.Font('./assets/Starjedi.ttf', 26)
TEXT_X_POS = 10
TEXT_Y_POS = 10

#funcion mostrar puntaje
def show_score(text_x, text_y):
    '''Muestra el puntaje en pantalla'''

    text = font.render(f"Score: {SCORE}", True, (255, 232, 0), None)
    screen.blit(text, (text_x, text_y))



#variable game over
final_font = pygame.font.Font('./assets/Starjedi.ttf', 50)
FTEXT_X_POS = 230
FTEXT_Y_POS = 250

#funcion game over
def game_over_text():
    text = final_font.render("game over", True, (255, 232, 0), None)
    screen.blit(text, (FTEXT_X_POS, FTEXT_Y_POS))




#ENEMIGOS
# variables del enemigo

enemy_sprite = []
ENEMY_POS_X = []
ENEMY_POS_Y = []

ENEMY_X_POS_CHANGE = []
ENEMY_Y_POS_CHANGE = []

ENEMY_QNTY = 8
ENEMY_X_VELOCITY = 0.7


for _ in range(ENEMY_QNTY):
    enemy_sprite.append(pygame.image.load('./assets/nave-imperial-64px.png'))
    ENEMY_POS_X.append(random.randint(0, 736))
    ENEMY_POS_Y.append(random.randint(32, 200))
    ENEMY_X_POS_CHANGE.append(ENEMY_X_VELOCITY)
    ENEMY_Y_POS_CHANGE.append(50)

# enemy_sprite = pygame.image.load('./assets/nave-imperial-64px.png')
# ENEMY_POS_X = random.randint(0, 736)
# ENEMY_POS_Y = random.randint(32, 200)

# ENEMY_X_POS_CHANGE = 0.5
# ENEMY_Y_POS_CHANGE = 50

#funcion enemigo
def enemy(ene_x_pos, ene_y_pos, ene):
    '''player function'''
    screen.blit(enemy_sprite[ene], (ene_x_pos, ene_y_pos))


#BALA
# variables de la bala
bullet_sprite = pygame.image.load('./assets/green laser small.png')
bullet_sound = mixer.Sound('./assets/disparo.mp3')
BULLET_POS_X = 0
BULLET_POS_Y = 520

BULLET_Y_POS_CHANGE = 5

BULLET_VISIBLE = False

# funcion bala

def shot_bullet(bul_x_pos, bul_y_pos):
    global BULLET_VISIBLE

    BULLET_VISIBLE = True

    screen.blit(bullet_sprite, (bul_x_pos + 30, bul_y_pos + 10))



#variables colisiones

explosion = pygame.image.load('./assets/explosion.png')
explosion_sound = mixer.Sound('./assets/explosion.mp3')
EXPLOSION_X_POS = 0
EXPLOSION_Y_POS = 0



#funcion detectar colisiones

def hay_colision(x_1, y_1, x_2, y_2):
    '''detecta si hay colision entre 2 objetos'''

    dist = math.sqrt((math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2)))

    if dist < 30:
        return True
    else:
        return False



# Loop del juego
RUNNING = True

while RUNNING:

    # rellenar fondo de la pantalla con rgb y actualizar la pantalla
    #cargar imagen de fondo
    # screen.fill((92, 81, 128))

    screen.blit(background, (0, 0))

    # Iterar eventos
    for event in pygame.event.get():

        # Evento cerrar
        if event.type == pygame.QUIT:
            RUNNING = False

        # Evento presionar TECLAS
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                X_POS_CHANGE = -2

            if event.key == pygame.K_RIGHT:
                X_POS_CHANGE = 2

            if event.key == pygame.K_UP:
                Y_POS_CHANGE = -1

            if event.key == pygame.K_DOWN:
                Y_POS_CHANGE = 1

            if event.key == pygame.K_SPACE:
                if not BULLET_VISIBLE:
                    bullet_sound.play()
                    BULLET_POS_X = PLAYER_POS_X
                    BULLET_POS_Y = PLAYER_POS_Y
                    shot_bullet(BULLET_POS_X, BULLET_POS_Y)


        # Evento soltar flechas
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                X_POS_CHANGE = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                Y_POS_CHANGE = 0


    # Modificar posicion del jugador
    PLAYER_POS_X += X_POS_CHANGE
    PLAYER_POS_Y += Y_POS_CHANGE


    # Mantener dentro de la pantalla al jugador
    if PLAYER_POS_X <= 0:
        PLAYER_POS_X = 0
    elif PLAYER_POS_X >= 736:
        PLAYER_POS_X = 736



    # Modificar posicion enemigos
    for index in range(ENEMY_QNTY):
        ENEMY_POS_X[index] += ENEMY_X_POS_CHANGE[index]



        # Mantener dentro de la pantalla a LOS ENEMIGOS
        if ENEMY_POS_X[index] <= 0:
            ENEMY_X_POS_CHANGE[index] = ENEMY_X_VELOCITY
            ENEMY_POS_Y[index] += ENEMY_Y_POS_CHANGE[index]
        elif ENEMY_POS_X[index] >= 736:
            ENEMY_X_POS_CHANGE[index] = ENEMY_X_VELOCITY * (-1)
            ENEMY_POS_Y[index] += ENEMY_Y_POS_CHANGE[index]

        # colision bala - enemigos
        COLISION_ENEMY_BULLET = hay_colision(ENEMY_POS_X[index], ENEMY_POS_Y[index], BULLET_POS_X, BULLET_POS_Y)

        if COLISION_ENEMY_BULLET:
            explosion_sound.play()
            BULLET_POS_Y = 520
            BULLET_VISIBLE = False
            SCORE += 1
            ENEMY_POS_X[index] = random.randint(0, 736)
            ENEMY_POS_Y[index] = random.randint(32, 200)
            ENEMY_X_VELOCITY += 0.05


        COLISION_ENEMY_USER = hay_colision(ENEMY_POS_X[index], ENEMY_POS_Y[index], PLAYER_POS_X, PLAYER_POS_Y)

        if COLISION_ENEMY_USER or ENEMY_POS_Y[index] >= 520:
            for k in range(ENEMY_QNTY):
                ENEMY_POS_Y[k] = 1000
            game_over_text()
            break

        enemy(ENEMY_POS_X[index], ENEMY_POS_Y[index], index)


    #restringir bala
    if BULLET_POS_Y <= -64:
        BULLET_POS_Y = 520
        BULLET_VISIBLE = False
    #Movimiento bala
    if BULLET_VISIBLE:
        shot_bullet(BULLET_POS_X, BULLET_POS_Y)
        BULLET_POS_Y -= BULLET_Y_POS_CHANGE




    player(PLAYER_POS_X, PLAYER_POS_Y)

    show_score(TEXT_X_POS, TEXT_Y_POS)

    # Actualizar pantalla
    pygame.display.update()
