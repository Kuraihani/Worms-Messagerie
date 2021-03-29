import pygame
from player import Player
from monster import Monster, BadWorm, Boss
from comet_event import CometFallEvent
from sound import SoundManager

from message import Message
import json

class Game: 
    def __init__(self):
        #definir si le jeu a commencé
        self.is_playing = False
        #générer le joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)

        #APPEL MESSAGERIE
        self.message = Message(self)


        #gérer l'event
        self.comet_event = CometFallEvent(self)
        #groupe de monstre
        self.all_monsters = pygame.sprite.Group()
        self.score = 0
        self.pressed = {}
        self.font = pygame.font.Font("assets/font.ttf", 25)
        self.sound_manager = SoundManager()

    def start(self):
        self.is_playing = True
        #self.spawn_monster(BadWorm)
        #self.spawn_monster(BadWorm)
        #self.spawn_monster(Boss)


    def game_over(self):
        #remettre le jeu à neuf, retirer les monstres, remettre le joeueur à 100 vie, jeu en attente
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.comet_event.reset_percent()
        self.is_playing = False
        self.score = 0
        self.sound_manager.play('game_over')

    def add_score(self,points=10):
        self.score += points

    def update(self,screen):
        #afficher le score sur l'ecran
        score_text = self.font.render(f"Score: {self.score}", 1, (0,0,0))
        screen.blit(score_text,(20,20))

        #AFFICHAGE MESSAGERIE
        self.message.init_messagerie(screen)

        #appliquer image du joueur
        screen.blit(self.player.image,self.player.rect)

        #actualiser la barre de vie du joueur
        self.player.update_health_bar(screen)

        #actualiser la barre d'event
        self.comet_event.update_bar(screen)

        #actualiser l'animation du joueur
        self.player.update_animation()

        #recup les projectiles du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()

        #recup les monstres du jeu
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()

        #recup les comets
        for comet in self.comet_event.all_comets:
            comet.fall()

        #appliquer les projectiles
        self.player.all_projectiles.draw(screen)

        #appliquer l'ensemble des images de mon groupe de monstre
        self.all_monsters.draw(screen)

        #appliquer l'ensemble des images de mon groupe de comettes
        self.comet_event.all_comets.draw(screen)

        #verfier si le joueur souhaite aller à gauche ou à droite ou sauter
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        if self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()

        #CODE JUMP
        if self.pressed.get(pygame.K_UP):
            self.player.jump()

            
            
    def check_collision(self,sprite,group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self,monster_class_name):
        self.all_monsters.add(monster_class_name.__call__(self))

