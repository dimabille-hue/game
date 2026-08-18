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

    def translucent_rect(self, rect, color, radius=0):
        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, surface.get_rect(), border_radius=radius)
        self.screen.blit(surface, rect.topleft)

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

    def panel(self, rect, radius=16, border=None, fill=None):
        self.translucent_rect(pygame.Rect(rect).move(7, 9), (0, 0, 0, 105), radius)
        self.translucent_rect(rect, fill or (*PALETTE["panel"], 232), radius)
        self.neon_frame(rect, border or PALETTE["grid"], radius, width=1)

    def neon_frame(self, rect, color, radius=14, width=1):
        self.glow(rect.center, color, max(rect.width, rect.height) // 18, 18)
        pygame.draw.rect(self.screen, color, rect, width, border_radius=radius)
        inner = pygame.Rect(rect).inflate(-4, -4)
        pygame.draw.rect(self.screen, (255, 255, 255), inner, 1, border_radius=max(0, radius - 2))

    def progress_bar(self, rect, value, maximum, color, label):
        value = max(0, min(value, maximum))
        ratio = value / maximum if maximum else 0
        pygame.draw.rect(self.screen, (9, 17, 33), rect, border_radius=rect.height // 2)
        fill_rect = pygame.Rect(rect.x, rect.y, int(rect.width * ratio), rect.height)
        if fill_rect.width > 0:
            pygame.draw.rect(self.screen, color, fill_rect, border_radius=rect.height // 2)
        pygame.draw.rect(self.screen, (49, 73, 111), rect, 1, border_radius=rect.height // 2)
        self.centered_text(label, rect.center, "small", PALETTE["white"])

    def button(self, rect, title, color, active=False):
        fill = (28, 48, 78, 235) if active else (18, 30, 52, 220)
        self.translucent_rect(rect, fill, 9)
        pygame.draw.rect(self.screen, color, rect, 1 if not active else 2, border_radius=9)
        self.centered_text(title, rect.center, "small", PALETTE["white"])
