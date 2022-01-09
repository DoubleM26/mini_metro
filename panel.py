import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image):
        super().__init__(group)
        self.image = image
        self.default_image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.triggered = False

    def trigger(self):
        if not self.triggered:
            self.image = pygame.transform.scale(self.image, (48, 48))
            self.rect.x -= 6
            self.rect.y -= 6
            self.triggered = True


class Panel:
    def __init__(self, group):
        self.buttons = [
                        Button(group, 490, 665, pygame.image.load("data/yellow_button.png")),
                        Button(group, 550, 665, pygame.image.load("data/brown_button.png")),
                        Button(group, 610, 665, pygame.image.load("data/green_button.png")),
                        ]
        self.bridges = Button(group, 670, 665, pygame.image.load("data/yellow_button.png"))

    def trigger(self, i):
        for button in self.buttons:
            if button.triggered:
                button.image = button.default_image
                button.rect.x += 6
                button.rect.y += 6
                button.triggered = False
        self.buttons[i].trigger()
