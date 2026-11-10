from pico2d import *
import game_framework
import title_mode

image = None
running = True
logo_start_time = 0.0

def init():
    global image, running, logo_start_time

    image = load_image('tuk_credit.png')
    running = True
    logo_start_time = get_time()

def finish():
    global image
    del image

def update():
    global running, logo_start_time

    if get_time() - logo_start_time >= 2.0:
        game_framework.change_mode(title_mode)
        running = False

def render():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

def handle_events():
    events = get_events()
