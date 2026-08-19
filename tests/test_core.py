import random
import time
import unittest

from board import Board
from combat import attack, steal
from game import Game
from loot import LOOT_TABLE
from tile import Tile


class CoreGameTests(unittest.TestCase):
    def setUp(self):
        random.seed(12345)
        self.game = Game()

    def test_board_has_required_special_sectors_and_size(self):
        board = Board()

        self.assertEqual(board.SIZE, 7)
        self.assertEqual(board.get(0, 0).kind, "player_base")
        self.assertEqual(board.get(6, 6).kind, "bot_base")
        self.assertEqual(board.get(3, 3).kind, "center")
        self.assertIsNone(board.get(-1, 0))
        self.assertIsNone(board.get(7, 0))

    def test_reveal_opens_area_within_bounds(self):
        board = Board()
        board.reveal(0, 0, 1)

        self.assertTrue(board.get(0, 0).revealed)
        self.assertTrue(board.get(1, 0).revealed)
        self.assertTrue(board.get(0, 1).revealed)
        self.assertTrue(board.get(1, 1).revealed)
        self.assertFalse(board.get(2, 2).revealed)

    def test_player_moves_one_tile_and_spends_resources(self):
        self.game.board.tiles[0][1] = Tile("empty")
        self.game.board.reveal(1, 0, 0)

        self.game.move_player(1, 0)

        self.assertEqual((self.game.player.x, self.game.player.y), (1, 0))
        self.assertEqual(self.game.player.moves, 2)
        self.assertEqual(self.game.player.fuel, 9)

    def test_asteroid_costs_two_movement_but_one_fuel(self):
        self.game.board.tiles[0][1] = Tile("asteroid")
        self.game.board.reveal(1, 0, 0)

        self.game.move_player(1, 0)

        self.assertEqual((self.game.player.x, self.game.player.y), (1, 0))
        self.assertEqual(self.game.player.moves, 1)
        self.assertEqual(self.game.player.fuel, 9)

    def test_delivery_converts_cargo_to_score_and_clears_hold(self):
        self.game.player.cargo.append(LOOT_TABLE["mineral"])

        self.game.check_delivery()

        self.assertEqual(self.game.player.score, 1500)
        self.assertEqual(self.game.player.cargo, [])
        self.assertEqual(self.game.messages[-1], ("Груз доставлен! +1500", "good"))

    def test_scan_reveals_radius_once(self):
        self.game.scan()

        self.assertFalse(self.game.player.scan_available)
        self.assertTrue(self.game.board.get(2, 0).revealed)
        previous_messages = len(self.game.messages)

        self.game.scan()

        self.assertEqual(len(self.game.messages), previous_messages + 1)
        self.assertEqual(self.game.messages[-1][1], "warning")

    def test_attack_requires_adjacency_and_consumes_action(self):
        self.game.player.x = 5
        self.game.player.y = 6
        self.game.bot.x = 6
        self.game.bot.y = 6

        result = attack(self.game, self.game.player, self.game.bot)

        self.assertTrue(result)
        self.assertEqual(self.game.player.moves, 2)
        self.assertEqual(self.game.bot.shield, 0)

    def test_steal_transfers_cargo_when_adjacent(self):
        self.game.player.x = 5
        self.game.player.y = 6
        self.game.bot.x = 6
        self.game.bot.y = 6
        item = LOOT_TABLE["scrap"]
        self.game.bot.cargo.append(item)

        result = steal(self.game, self.game.player, self.game.bot)

        self.assertTrue(result)
        self.assertIn(item, self.game.player.cargo)
        self.assertNotIn(item, self.game.bot.cargo)
        self.assertEqual(self.game.player.moves, 2)

    def test_destroyed_ship_drops_cargo_and_respawns(self):
        item = LOOT_TABLE["technology"]
        self.game.player.x = 2
        self.game.player.y = 2
        self.game.player.hp = 0
        self.game.player.cargo.append(item)

        self.game.check_destroyed(self.game.player)

        self.assertEqual((self.game.player.x, self.game.player.y), (0, 0))
        self.assertEqual(self.game.player.hp, 3)
        self.assertEqual(self.game.player.cargo, [])
        self.assertIn(item, self.game.board.get(2, 2).dropped_loot)

    def test_timer_ends_game(self):
        self.game.started_at = time.time() - 901

        self.game.check_time()

        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.messages[-1], ("Время вышло!", "danger"))


if __name__ == "__main__":
    unittest.main()
