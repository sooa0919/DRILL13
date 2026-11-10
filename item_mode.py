from pico2d import draw_line, draw_rectangle, load_image
from sdl2 import SDL_KEYDOWN, SDLK_0, SDLK_1, SDLK_2


class ItemMode:
    """Non-pausing inventory overlay owned by the current play session."""

    CHOICES = {SDLK_0: None, SDLK_1: 21, SDLK_2: 41}

    def __init__(self, boy):
        self.boy = boy
        self.is_open = False
        self.icons = {}

    def toggle(self):
        self.is_open = not self.is_open

    def handle_event(self, event):
        if (self.is_open and event.type == SDL_KEYDOWN
                and event.key in self.CHOICES):
            self.boy.select_ball(self.CHOICES[event.key])
            return True
        return False

    def draw(self):
        if not self.is_open:
            return
        x, y = self.boy.x, self.boy.y + 140
        draw_rectangle(x - 150, y - 76, x + 150, y + 76,
                       23, 31, 45, filled=True)
        for index, size in enumerate((None, 21, 41)):
            cx = x + (index - 1) * 94
            draw_rectangle(cx - 42, y - 38, cx + 42, y + 42,
                           43, 54, 72, filled=True)
            if size is None:
                draw_line(cx - 12, y - 12, cx + 12, y + 12, 190, 200, 215)
                draw_line(cx - 12, y + 12, cx + 12, y - 12, 190, 200, 215)
            else:
                if size not in self.icons:
                    self.icons[size] = load_image(f'ball{size}x{size}.png')
                self.icons[size].draw(cx, y, size, size)
