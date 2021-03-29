import pygame
import json

class Message:
    def __init__(self, game):
        self.game = game

    def init_messagerie(self, screen):
        #MESSAGERIE
        message_text = self.game.font.render("", 1, (0,0,0))
        message_text1 = self.game.font.render("", 1, (0,0,0))
        message_text2 = self.game.font.render("", 1, (0,0,0))
        message_text3 = self.game.font.render("", 1, (0,0,0))
        message_text4 = self.game.font.render("", 1, (0,0,0))
        message_text5 = self.game.font.render("", 1, (0,0,0))
        message_text6 = self.game.font.render("", 1, (0,0,0))
        with open('message.txt') as json_file:
            self.text_message = json.load(json_file)
        i = 0
        for m in self.text_message['message']:
            if(i == 0):
                message_text = self.game.font.render(m['text_message'], 1, (0,0,0))
            if(i == 1):
                message_text1 = self.game.font.render(m['text_message'], 1, (0,0,0))
            if(i == 2):
                message_text2 = self.game.font.render(m['text_message'], 1, (0,0,0))
            if(i == 3):
                message_text3 = self.game.font.render(m['text_message'], 1, (0,0,0))
            if(i == 4):
                message_text4 = self.game.font.render(m['text_message'], 1, (0,0,0))
            if(i == 5):
                message_text5 = self.game.font.render(m['text_message'], 1, (0,0,0))
            if(i == 6):
                message_text6 = self.game.font.render(m['text_message'], 1, (0,0,0))
            i += 1

        screen.blit(message_text, (20, 40))
        screen.blit(message_text1, (20, 70))
        screen.blit(message_text2, (20, 100))
        screen.blit(message_text3, (20, 130))
        screen.blit(message_text4, (20, 160))
        screen.blit(message_text5, (20, 190))
        screen.blit(message_text6, (20, 220))

