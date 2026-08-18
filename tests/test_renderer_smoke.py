import importlib.util
import os
import unittest

pygame_available = importlib.util.find_spec("pygame") is not None


@unittest.skipUnless(pygame_available, "pygame is not installed")
class RendererSmokeTests(unittest.TestCase):
    def test_renderer_draws_one_frame_without_invalid_colors(self):
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

        import pygame
        from config import SCREEN_HEIGHT, SCREEN_WIDTH
        from game import Game
        from ui.renderer import SpaceRenderer

        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        fonts = {
            "small": pygame.font.Font(None, 18),
            "normal": pygame.font.Font(None, 24),
            "big": pygame.font.Font(None, 34),
            "title": pygame.font.Font(None, 42),
        }

        renderer = SpaceRenderer(screen, fonts)
        renderer.render(Game(), 0.25)
        pygame.quit()


if __name__ == "__main__":
    unittest.main()
