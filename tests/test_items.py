import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from sdl2 import (SDL_KEYDOWN, SDL_KEYUP, SDL_QUIT, SDLK_0, SDLK_1,
                 SDLK_2, SDLK_e, SDLK_p, SDLK_RIGHT, SDLK_SPACE,
                 SDLK_ESCAPE)
import ball
import boy
import game_framework
import game_world
import item_mode
import pause_mode
import play_mode


def key(value, event_type=SDL_KEYDOWN, repeat=False):
    return SimpleNamespace(type=event_type, key=value, repeat=repeat)


class ItemTests(unittest.TestCase):
    def setUp(self):
        game_world.clear()
        self.addCleanup(game_world.clear)
        for target in ('boy.load_image', 'ball.load_image', 'item_mode.load_image'):
            mock = patch(target, return_value=MagicMock())
            mock.start()
            self.addCleanup(mock.stop)
        self.hero = boy.Boy()
        self.items = item_mode.ItemMode(self.hero)
        ball.Ball.images = {}

    def test_default_small_ball(self):
        self.hero.fire_ball()
        self.assertEqual(game_world.world[1][0].size, 21)

    def test_select_sizes_and_clear(self):
        self.items.toggle()
        for shortcut, size in ((SDLK_0, None), (SDLK_1, 21), (SDLK_2, 41)):
            self.assertTrue(self.items.handle_event(key(shortcut)))
            self.assertEqual(self.hero.ball_size, size)

    def test_closed_inventory_ignores_numbers(self):
        self.assertFalse(self.items.handle_event(key(SDLK_2)))
        self.assertEqual(self.hero.ball_size, 21)

    def test_key_up_does_not_select(self):
        self.items.toggle()
        self.assertFalse(self.items.handle_event(key(SDLK_2, SDL_KEYUP)))

    def test_clear_stops_new_shots_and_preserves_existing_balls(self):
        self.hero.fire_ball()
        existing = game_world.world[1][0]
        self.hero.select_ball(None)
        self.hero.fire_ball()
        self.assertEqual(game_world.world[1], [existing])

    def test_new_shots_keep_their_selected_size(self):
        self.hero.fire_ball()
        self.hero.select_ball(41)
        self.hero.fire_ball()
        self.assertEqual([o.size for o in game_world.world[1]], [21, 41])

    def test_ball_draw_uses_exact_dimensions(self):
        for size in (21, 41):
            shot = ball.Ball(100, 90, 10, size)
            shot.draw()
            shot.image.draw.assert_called_with(100, 90, size, size)

    def test_invalid_size_is_rejected(self):
        with self.assertRaises(ValueError):
            self.hero.select_ball(42)
        with self.assertRaises(ValueError):
            ball.Ball(0, 0, 10, 42)

    def events(self, *events):
        with patch.object(play_mode, 'boy', self.hero), \
                patch.object(play_mode, 'items', self.items), \
                patch.object(play_mode, 'get_events', return_value=events):
            play_mode.handle_events()

    def test_toggle_ignores_key_repeat_and_keeps_selection(self):
        self.events(key(SDLK_e), key(SDLK_e, repeat=True), key(SDLK_2))
        self.assertTrue(self.items.is_open)
        self.events(key(SDLK_e))
        self.assertFalse(self.items.is_open)
        self.assertEqual(self.hero.ball_size, 41)

    def test_movement_firing_and_world_continue_while_open(self):
        game_world.add_object(self.hero)
        with patch('boy.get_canvas_width', return_value=800), \
                patch('ball.get_canvas_width', return_value=800):
            self.events(key(SDLK_e), key(SDLK_RIGHT), key(SDLK_SPACE))
            play_mode.update()
        self.assertEqual(self.hero.x, 405)
        self.assertEqual(game_world.world[1][1].x, 410)
        self.events(key(SDLK_RIGHT, SDL_KEYUP))
        self.assertEqual(self.hero.state, 'IDLE')

    def test_sleep_still_wakes_with_space(self):
        self.hero.fall_asleep()
        self.events(key(SDLK_e), key(SDLK_SPACE))
        self.assertEqual(self.hero.state, 'IDLE')
        self.assertEqual(game_world.world[1], [])

    def test_pause_remains_frozen_and_preserves_inventory(self):
        self.items.toggle()
        with patch('game_framework.push_mode') as push:
            self.events(key(SDLK_p))
            push.assert_called_once_with(pause_mode)
        with patch('game_world.update') as update:
            pause_mode.update()
            update.assert_not_called()
        self.assertTrue(self.items.is_open)

    def test_inventory_does_not_change_idle_timer(self):
        started_at = self.hero.idle_started_at
        self.events(key(SDLK_e), key(SDLK_e))
        self.assertEqual(self.hero.idle_started_at, started_at)

    def test_panel_stays_above_character_and_inside_edges(self):
        with patch('item_mode.get_canvas_width', return_value=800), \
                patch('item_mode.get_canvas_height', return_value=600):
            for hero_x in (25, 400, 775):
                self.hero.x = hero_x
                x, y = self.items.position()
                self.assertGreaterEqual(x - 150, 8)
                self.assertLessEqual(x + 150, 792)
                self.assertGreater(y - 76, self.hero.y + 50)

    def test_escape_and_quit_are_available_while_open(self):
        self.items.toggle()
        with patch('game_framework.change_mode') as change:
            self.events(key(SDLK_ESCAPE))
            change.assert_called_once_with(play_mode.title_mode)
        with patch('game_framework.quit') as quit_game:
            self.events(SimpleNamespace(type=SDL_QUIT))
            quit_game.assert_called_once()

    def test_finish_clears_overlay_and_world(self):
        play_mode.boy, play_mode.items = self.hero, self.items
        game_world.add_object(self.hero)
        play_mode.finish()
        self.assertIsNone(play_mode.boy)
        self.assertIsNone(play_mode.items)
        self.assertFalse(any(game_world.world))


if __name__ == '__main__':
    unittest.main()
