__author__ = 'lukian'


import pygame as pg
from .. import setup
from .. import constants as c


class SpeechStates(pg.sprite.Sprite):
    """Base class for the 3 speech states (standy, listening, processing)"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.sprite_sheet = setup.GFX['speech_recognition']
        self.state = c.STAND_BY
        self.handle_state()
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 545

    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        image = pg.transform.scale(image,
                                   (int(rect.width*0.25),
                                    int(rect.height*0.25)))
        return image

    def handle_state(self):
        """Speech icon determined by state"""
        if self.state == c.STAND_BY:
            self.image = self.get_image(0, 0, 200, 200)
        elif self.state == c.LISTENING:
            self.image = self.get_image(200, 0, 200, 200)
        elif self.state == c.LOADING:
            self.image = self.get_image(400, 0, 200, 200)
        elif self.state == c.RECOGNIZED:
            self.image = self.get_image(600, 0, 200, 200)
        elif self.state == c.FAILED:
            self.image = self.get_image(800, 0, 200, 200)

    def draw(self, surface):
        self.handle_state()
        surface.blit(self.image, self.rect)



















