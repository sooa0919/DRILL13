import os
from pathlib import Path

from pico2d import (draw_line, draw_rectangle, get_canvas_height,
                    get_canvas_width, load_font, load_image)
from sdl2 import SDL_KEYDOWN, SDLK_0, SDLK_1, SDLK_2


class ItemMode:
    """Non-pausing inventory overlay owned by the current play session."""

    CHOICES = {SDLK_0: None, SDLK_1: 21, SDLK_2: 41}

    def __init__(self, boy):
        self.boy = boy
        self.is_open = False
        self.icons = {}
        self.font = None

    def toggle(self):
        self.is_open = not self.is_open

    def handle_event(self, event):
        if (self.is_open and event.type == SDL_KEYDOWN
                and event.key in self.CHOICES):
            self.boy.select_ball(self.CHOICES[event.key])
            return True
        return False

    def position(self):
        # Keep the whole panel visible when the character reaches a screen edge.
        x = max(158, min(get_canvas_width() - 158, self.boy.x))
        y = max(84, min(get_canvas_height() - 84, self.boy.y + 140))
        return x, y

    def draw(self):
        if not self.is_open:
            return
        if self.font is None:
            candidates = [
                Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts/consola.ttf',
                Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'),
                Path('/System/Library/Fonts/Menlo.ttc'),
            ]
            font_path = next((p for p in candidates if p.is_file()), None)
            if font_path is None:
                raise FileNotFoundError('Install Consolas, DejaVu Sans Mono or Menlo')
            self.font = load_font(str(font_path), 14)
        x, y = self.position()
        draw_rectangle(x - 150, y - 76, x + 150, y + 76,
                       23, 31, 45, filled=True)
        accent = (80, 225, 184)
        self.font.draw(x - 136, y + 58, 'ITEMS', accent)
        self.font.draw(x + 66, y + 58, 'E: CLOSE', (210, 220, 235))
        names = ('CLEAR', 'SMALL', 'LARGE')
        selected_name = names[(None, 21, 41).index(self.boy.ball_size)]
        self.font.draw(x - 136, y - 58, f'{selected_name} | SPACE: fire', accent)
        for index, size in enumerate((None, 21, 41)):
            cx = x + (index - 1) * 94
            draw_rectangle(cx - 42, y - 38, cx + 42, y + 42,
                           43, 54, 72, filled=True)
            selected = size == self.boy.ball_size
            border = accent if selected else (95, 112, 135)
            draw_rectangle(cx - 42, y - 38, cx + 42, y + 42, *border)
            if selected:
                draw_rectangle(cx - 40, y - 36, cx + 40, y - 33,
                               *accent, filled=True)
            self.font.draw(cx - 33, y + 29, f'{index} {names[index]}', border)
            label = 'NO BALL' if size is None else f'{size}x{size}'
            self.font.draw(cx - 29, y - 25, label, (220, 230, 245))
            if size is None:
                draw_line(cx - 12, y - 12, cx + 12, y + 12, 190, 200, 215)
                draw_line(cx - 12, y + 12, cx + 12, y - 12, 190, 200, 215)
            else:
                if size not in self.icons:
                    self.icons[size] = load_image(f'ball{size}x{size}.png')
                self.icons[size].draw(cx, y, size, size)
