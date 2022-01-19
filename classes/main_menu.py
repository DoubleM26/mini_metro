from constants import *


class MiniMap(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image, db, ind):
        super().__init__(group)
        self.db = db
        self.image = pygame.transform.scale(image, (270, 180))
        self.default_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.triggered = False

        self.record = self.db.records[ind]
        self.record_text = SMALL_MENU_FONT.render(str(self.record), False, (234, 194, 53))
        self.record_text_rect = self.record_text.get_rect()
        self.record_text_rect.x, self.record_text_rect.y = RECORDS_POSITIONS[ind]

    def trigger(self):
        if not self.triggered:
            self.rect.x -= 8
            self.rect.y -= 6
            self.image = pygame.transform.scale(self.image, (297, 198))
            self.triggered = True
            self.record_text_rect.x += 18
            self.record_text_rect.y -= 6

    def un_trigger(self):
        if self.triggered:
            self.triggered = False
            self.image = self.default_image
            self.rect.x += 8
            self.rect.y += 6
            self.record_text_rect.x -= 18
            self.record_text_rect.y += 6
















