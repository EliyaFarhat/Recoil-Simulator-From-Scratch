import pygame

class Button:
    def __init__(self, x, y, width, height, label, font, default_color=(50, 50, 50), hover_color=(0, 255, 0), held_color=(255, 0, 0), outline_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.font = font
        self.default_color = default_color
        self.hover_color = hover_color
        self.held_color = held_color
        self.outline_color = outline_color
        self.color = self.default_color
        self.is_hovered = False
        self.is_held = False

    def update(self, mouse_pos, mouse_pressed):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.is_held = self.is_hovered and mouse_pressed[0]

        if self.is_held:
            self.color = self.held_color
        elif self.is_hovered:
            self.color = self.hover_color
        else:
            self.color = self.default_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.outline_color, self.rect, 3)

        text_surface = self.font.render(self.label, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)