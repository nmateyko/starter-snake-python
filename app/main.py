import json
import os
import random
import bottle
from board import Board

from api import ping_response, start_response, move_response, end_response


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print("start data: " + json.dumps(data))

    color = "#00FFFF"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json
    b = Board(data)
    directions = ['up', 'down', 'left', 'right']
    random.shuffle(directions)
    good_directions = []
    for d in directions:
        if (not b.wall_in_direction(d)
                and not b.snake_in_direction(d)):
            good_directions.append(d)
    if len(good_directions) > 0 and b.health < 20:
        direction = good_directions[b.towards_food(good_directions)]
    elif len(good_directions) > 0:
        direction = random.choice(good_directions)
    else:
        direction = 'up'

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
