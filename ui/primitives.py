import pygame

from ui.theme import PALETTE


class DrawPrimitives:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts

    def text(self, text, x, y, font_name="normal", color=None):
        font = self.fonts[font_name]
        self.screen.blit(font.render(str(text), True, color or PALETTE["text"]), (x, y))

    def centered_text(self, text, center, font_name="normal", color=None):
        font = self.fonts[font_name]
        surface = font.render(str(text), True, color or PALETTE["text"])
        self.screen.blit(surface, surface.get_rect(center=center))

    def glow(self, center, color, radius, alpha=70):
        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        for step in range(5, 0, -1):
            pygame.draw.circle(
                surface,
                (*color, alpha // step),
                (radius, radius),
                radius * step // 5,
            )
        self.screen.blit(
            surface,
            (center[0] - radius, center[1] - radius),
            special_flags=pygame.BLEND_PREMULTIPLIED,
        )

    def panel(self, rect, radius=14, border=None):
        shadow = pygame.Rect(rect).move(6, 7)
        pygame.draw.rect(self.screen, (0, 0, 0, 95), shadow, border_radius=radius)
        pygame.draw.rect(self.screen, PALETTE["panel"], rect, border_radius=radius)
        pygame.draw.rect(self.screen, border or PALETTE["grid"], rect, 1, border_radius=radius)
