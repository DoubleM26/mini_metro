import pygame


class Station(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.overfilled = False
        self.counter = 0
        self.game_end = False
        self.cur_frame = 0
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.overfilled:
            self.counter += 1
            if self.counter % 45 == 0:
                self.cur_frame = (self.cur_frame + 1) % 2
                self.image = self.frames[self.cur_frame]
            if self.counter >= 900:
                self.game_end = True
        else:
            self.image = self.frames[0]
            self.counter = 0
