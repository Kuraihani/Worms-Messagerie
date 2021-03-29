import pygame
import random
import animation 
class Monster(animation.AnimateSprite):
    def __init__(self,game, name,size, offset=0):
        super().__init__(name,size)
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.3
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0,300)
        self.rect.y = 500 - offset
        self.velocity = random.randint(1,2)
        self.start_animation()
        self.loot_amount = 10

    def set_loot_amount(self,amount):
        self.loot_amount = amount

    def set_speed(self, speed):
        self.default_speed = speed
        self.velocity = random.randint(1,3)

    def damage(self,amount):
        #infliger les degats
        self.health -= amount
        #vérifier si le nb de points de vie est inférieur ou égal à 0
        if self.health <= 0:
            self.rect.x = 1000 + random.randint(0,300)
            self.velocity = random.randint(1,self.default_speed)
            self.health = self.max_health
            #incrementer le score
            self.game.add_score(20)

            #si la barre d'event est chargé à son maxi on ne fait pas repop les monstres
            if self.game.comet_event.is_full_loaded():
                #retirer du jeu
                self.game.all_monsters.remove(self)

                #appel de la méthode pour essayer de déclencher la pluie de cometes
                self.game.comet_event.attempt_fall()

    def update_health_bar(self,surface):
        #définir une couleur pour une jauge de vie
        bar_color = (111,210,46)
        #définir une couleur pour l'arriere plan de la jauge (gris foncé)
        back_bar_color = (60, 63, 60)

        #definir la position de notre jauge de vie ainsi que sa largeur et son épaisseur
        bar_position = [self.rect.x + 10, self.rect.y - 20, self.health, 5]

        #definir la position de l'arrière plan de notre jauge de vie 
        back_bar_position = [self.rect.x + 10, self.rect.y - 20, self.max_health, 5]

        # dessiner notre barre de vie
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def update_animation(self):
        self.animate(loop=True)
        
    def forward(self):
        #le deplacement ne se fait que si il ny'a pas de collision avec un groupe de joueur
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        #si le monstre est en collision avec le joueur
        else:
            #infliger des degats
            self.game.player.damage(self.attack)

#définir une class pour les mobs
class BadWorm(Monster):
    def __init__(self,game):
        super().__init__(game,"bad_worms", (130,130))
        self.set_speed(3)
        self.set_loot_amount(20)
#définir une class pour le boss
class Boss(Monster):
    def __init__(self,game):
        super().__init__(game,"boss", (300,300), 130)
        self.health = 250
        self.max_health = 250
        self.attack = 0.8
        self.set_speed(1)
        self.set_loot_amount(50)

