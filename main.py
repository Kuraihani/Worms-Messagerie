import pygame, sys
from game import Game
import math
import json

pygame.init()

#définir une clock 
clock = pygame.time.Clock()
FPS = 60

#générer la fenetre du jeu
pygame.display.set_caption("World War Worms")
screen = pygame.display.set_mode((1080,720))

#Charger l'arrière plan
background = pygame.image.load('assets/background.jpg')

#importer charger notre bannière
banner = pygame.image.load('assets/banner.png')
banner = pygame.transform.scale(banner,(400,400))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 3.33)

#importer les inputs
#PSEUDO INPUT
pseudo_placeholder = 'Pseudo'
pseudo_text = ''
pseudo_input_rect = pygame.Rect(screen.get_width()/2.5,350,200,32)
pseudo_active = False

#SERVEUR INPUT
server_placeholder = 'Serveur'
server_text = 'localhost'
server_input_rect = pygame.Rect(screen.get_width()/2.5,420,200,32)
server_active = False

#PORT INPUT
port_placeholder = 'Port'
port_text = '59001'
port_input_rect = pygame.Rect(screen.get_width()/2.5,500,200,32)
port_active = False


base_font = pygame.font.Font("assets/font.ttf",20)
color_active = pygame.Color('orange')
color_passive = pygame.Color('gray15')
color = color_passive



#importer charger notre bouton pour lancer la partie
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400,150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 1.3)


game = Game()

#boucle tant que cette condition est vrai
running = True
while running:
    #tant que le jeu est actif

    #arrière plan
    screen.blit(background,(0,0))

    #verifier si notre jeu a commencé
    if game.is_playing:
        #declencher les instructions de la partie
        game.update(screen)
    else:
        #ajouté mon écran de bienvenue
        
        #bouton Jouer
        screen.blit(play_button, play_button_rect)

        #form
        if pseudo_active or server_active or port_active:
            color = color_active
        else:
            color = color_passive
        #PSEUDO
        pygame.draw.rect(screen,color,pseudo_input_rect)
        pseudo_placeholder_surface = base_font.render(pseudo_placeholder,True,(0,0,0))
        pseudo_text_surface = base_font.render(pseudo_text,True,(255,255,255))
        pseudo_input_rect.w = max(200,pseudo_text_surface.get_width() + 10)
        screen.blit(pseudo_text_surface,(pseudo_input_rect.x + 5,pseudo_input_rect.y + 5))
        screen.blit(pseudo_placeholder_surface,(pseudo_input_rect.x + 5,pseudo_input_rect.y - 30))

        #SERVER
        pygame.draw.rect(screen,color,server_input_rect)
        server_placeholder_surface = base_font.render(server_placeholder,True,(0,0,0))
        server_text_surface = base_font.render(server_text,True,(255,255,255))
        server_input_rect.w = max(200,server_text_surface.get_width() + 10)
        screen.blit(server_text_surface,(server_input_rect.x + 5,server_input_rect.y + 5))
        screen.blit(server_placeholder_surface,(server_input_rect.x + 5,server_input_rect.y - 30))

        #PORT
        pygame.draw.rect(screen,color,port_input_rect)
        port_placeholder_surface = base_font.render(port_placeholder,True,(0,0,0))
        port_text_surface = base_font.render(port_text,True,(255,255,255))
        port_input_rect.w = max(200,port_text_surface.get_width() + 10)
        screen.blit(port_text_surface,(port_input_rect.x + 5,port_input_rect.y + 5))
        screen.blit(port_placeholder_surface,(port_input_rect.x + 5,port_input_rect.y - 30))

        #MESSAGE

        
        #banner
        screen.blit(banner,banner_rect)
        
    #mettre à jour l'ecran
    pygame.display.flip()

    #si le joueur ferme la fenetre
    for event in pygame.event.get():
        #si l'event est fermeture de fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

            #RESET MESSAGERIE
            data_message = {}
            data_message['message'] = []
            data_message['message'].append({
                'isGame':False,
                'text_message': "Bienvenue sur worms"
            })
            with open('message.txt', 'w') as outfile:
                json.dump(data_message, outfile)

        #détecter si un joueur lache une touche du clavier
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True        
            if event.key == pygame.K_SPACE:
                if game.is_playing:
                    game.player.launch_projectile()
                else:
                    #mettre le jeu en mode lancé
                    game.start()
                    game.sound_manager.play('click')             
            if pseudo_active == True:
                if event.key == pygame.K_BACKSPACE:
                        pseudo_text = pseudo_text[:-1]
                else:
                    pseudo_text += event.unicode
            if server_active == True:
                if event.key == pygame.K_BACKSPACE:
                        server_text = server_text[:-1]
                else:
                    server_text += event.unicode
            if port_active == True:
                if event.key == pygame.K_BACKSPACE:
                        port_text = port_text[:-1]
                else:
                    port_text += event.unicode
                    
        elif event.type == pygame.KEYUP: #si la touche n'est plus utilisé
            game.pressed[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #verification poru savoir si la souris est en collision avec le button jouer
            if play_button_rect.collidepoint(event.pos):
                #mettre le jeu en mode lancé
                if pseudo_text and server_text and port_text != '':
                    game.start()
                    game.sound_manager.play('click')
                    if game.is_playing:
                        pygame.MOUSEBUTTONDOWN = False
            if pseudo_input_rect.collidepoint(event.pos):
                pseudo_active = True
            else:
                pseudo_active = False
            if server_input_rect.collidepoint(event.pos):
                server_active = True
            else:
                server_active = False
            if port_input_rect.collidepoint(event.pos):
                port_active = True
            else:
                port_active = False
            
                    
        
    #fixer le nombre de fps
    clock.tick(FPS)


 