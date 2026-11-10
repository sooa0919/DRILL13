from pico2d import draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_0, SDLK_1, SDLK_2


class ItemMode:
    """Non-pausing inventory overlay owned by the current play session."""

    CHOICES = {SDLK_0: None, SDLK_1: 21, SDLK_2: 41}

    def __init__(self, boy):
        self.boy = boy
        self.is_open = False

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
