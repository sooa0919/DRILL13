from pico2d import *
import game_framework
import game_world


def init():
    pass


def finish():
    pass


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if not getattr(event, 'repeat', False):
                game_framework.pop_mode()
                return


def update():
    pass


def render():
    clear_canvas()
    game_world.render()
    x, y = get_canvas_width() // 2, get_canvas_height() // 2
    draw_rectangle(x - 64, y - 64, x + 64, y + 64,
                   30, 30, 30, filled=True)
    draw_rectangle(x - 64, y - 64, x + 64, y + 64,
                   255, 255, 255)
    draw_rectangle(x - 32, y - 40, x - 12, y + 40,
                   255, 255, 255, filled=True)
    draw_rectangle(x + 12, y - 40, x + 32, y + 40,
                   255, 255, 255, filled=True)
    update_canvas()
