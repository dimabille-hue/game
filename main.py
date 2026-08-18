import pygame

from config import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from game import Game
from ui.geometry import mouse_to_tile
from ui.renderer import SpaceRenderer
from ui.theme import BOARD_X

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Последний сектор")
clock = pygame.time.Clock()

fonts = {
    "small": pygame.font.Font(None, 18),
    "normal": pygame.font.Font(None, 24),
    "big": pygame.font.Font(None, 34),
    "title": pygame.font.Font(None, 42),
}

renderer = SpaceRenderer(screen, fonts)
game = Game()
selected_tile = None
action_menu = None


def get_actions(x, y):
    tile = game.board.get(x, y)
    actions = []
    distance = abs(game.player.x - x) + abs(game.player.y - y)

    if distance == 1:
        actions.append(("Двигаться", lambda: game.move_player(x - game.player.x, y - game.player.y)))

    if tile.revealed:
        if tile.kind == "planet":
            actions.append(("Исследовать", game.scan))
        if tile.kind == "station":
            actions.append(("Ремонт", game.repair))
        if tile.kind == "pirate":
            actions.extend((("Атаковать", game.player_attack), ("Ограбить", game.player_steal)))

    return actions


def open_action_menu(x, y):
    global action_menu, selected_tile

    selected_tile = (x, y)
    actions = get_actions(x, y)
    if not actions:
        action_menu = None
        game.log("Для этой клетки нет доступных действий.", "warning")
        return

    width = 190
    row_height = 42
    height = len(actions) * row_height + 12
    px = BOARD_X + x * TILE_SIZE + TILE_SIZE
    py = 80 + y * TILE_SIZE

    if px + width > SCREEN_WIDTH:
        px = BOARD_X + x * TILE_SIZE - width
    if py + height > SCREEN_HEIGHT:
        py = SCREEN_HEIGHT - height - 10

    action_menu = {
        "x": px,
        "y": py,
        "width": width,
        "height": height,
        "actions": actions,
    }


def handle_left_click(position):
    global action_menu

    if action_menu is not None:
        x = action_menu["x"]
        y = action_menu["y"]
        width = action_menu["width"]
        for i, (_title, callback) in enumerate(action_menu["actions"]):
            button = pygame.Rect(x + 6, y + 6 + i * 42, width - 12, 36)
            if button.collidepoint(position):
                action_menu = None
                callback()
                return
        action_menu = None
        return

    target = mouse_to_tile(position)
    if target is None:
        return

    x, y = target
    if abs(game.player.x - x) + abs(game.player.y - y) == 1:
        game.move_player(x - game.player.x, y - game.player.y)
    else:
        game.log("ЛКМ: выбери соседнюю клетку.", "warning")


def handle_right_click(position):
    target = mouse_to_tile(position)
    if target is not None:
        open_action_menu(*target)


def handle_key(event):
    global action_menu, game

    char = event.unicode.lower()
    if event.key == pygame.K_n or char == "т":
        game = Game()
        action_menu = None
        return

    log_actions = {
        pygame.K_PAGEUP: lambda: game.scroll_log(3),
        pygame.K_PAGEDOWN: lambda: game.scroll_log(-3),
        pygame.K_HOME: game.log_to_top,
        pygame.K_END: game.log_to_bottom,
    }
    if event.key in log_actions:
        log_actions[event.key]()
        return

    if event.key == pygame.K_ESCAPE:
        action_menu = None
        return

    if game.game_over:
        return

    moves = [
        ((pygame.K_UP, pygame.K_w), "ц", (0, -1)),
        ((pygame.K_DOWN, pygame.K_s), "ы", (0, 1)),
        ((pygame.K_LEFT, pygame.K_a), "ф", (-1, 0)),
        ((pygame.K_RIGHT, pygame.K_d), "в", (1, 0)),
    ]
    for keys, ru_key, delta in moves:
        if event.key in keys or char == ru_key:
            game.move_player(*delta)
            return

    key_actions = {
        pygame.K_SPACE: game.end_turn,
        pygame.K_e: game.scan,
        pygame.K_r: game.repair,
        pygame.K_f: game.player_attack,
        pygame.K_g: game.player_steal,
    }
    ru_actions = {
        "у": game.scan,
        "к": game.repair,
        "а": game.player_attack,
        "п": game.player_steal,
    }
    if event.key in key_actions:
        key_actions[event.key]()
    elif char in ru_actions:
        ru_actions[char]()


def main():
    running = True
    while running:
        now = pygame.time.get_ticks() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                game.scroll_log(1 if event.y > 0 else -1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    handle_left_click(event.pos)
                elif event.button == 3:
                    handle_right_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                handle_key(event)

        game.check_time()
        renderer.render(game, now, selected_tile, action_menu)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
