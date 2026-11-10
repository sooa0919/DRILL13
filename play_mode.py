from pico2d import *
import game_framework
import game_world
import title_mode
import pause_mode
from boy import Boy
from grass import Grass
from item_mode import ItemMode

boy = None
items = None
paused_at = 0.0

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if not getattr(event, 'repeat', False):
                game_framework.push_mode(pause_mode)
                return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_e:
            if not getattr(event, 'repeat', False):
                items.toggle()
        elif not items.handle_event(event):
            boy.handle_event(event)



def init():
    global boy, items
    boy = Boy()
    items = ItemMode(boy)
    game_world.add_object(boy)

    grass = Grass()
    game_world.add_object(grass, 0)


def update():
    game_world.update()


def pause():
    global paused_at
    paused_at = get_time()


def resume():
    boy.idle_started_at += get_time() - paused_at
    boy.pressed_keys.clear()
    if boy.state == 'RUN':
        boy.stop_run()

def render_world():
    game_world.render()
    items.draw()


def render():
    clear_canvas()
    render_world()
    update_canvas()


def finish():
    global boy, items
    game_world.clear()
    boy = None
    items = None
