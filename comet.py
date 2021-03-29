import pygame
import random

#creer une class pour gerer cette comete
class Comet(pygame.sprite.Sprite):

    def __init__(self,comet_event):
        super().__init__()
        #définir l'image associé à la comette
        self.image = pygame.image.load('assets/bombe.png')
        self.image = pygame.transform.scale(self.image,(100,100))
        self.rect = self.image.get_rect()
        self.velocity = random.randint(1,8)
        self.rect.x = random.randint(20,800)
        self.rect.y = - random.randint(0,800)
        self.comet_event = comet_event

    def remove(self):
        self.comet_event.all_comets.remove(self) 
        self.comet_event.game.sound_manager.play('meteorite')
        #si il n'y a plus de boule de feu sur le jeu
        if len(self.comet_event.all_comets) == 0:
            #remettre la jauge au depart
            self.comet_event.reset_percent()
            #apparaitre les deux premiers monstre
            self.comet_event.game.start()
                
    def fall(self):
        self.rect.y += self.velocity
        #ne tombe pas sur le sol
        if self.rect.y >= 500:
            self.remove()

        #verifier si la boule de feu touche le joueur
        if self.comet_event.game.check_collision(self, self.comet_event.game.all_players):
            #retirer la boule de feu
            self.remove()
            self.comet_event.game.player.damage(20)
            