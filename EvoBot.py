import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import optparse

def get_options():
    parser = optparse.OptionParser()

    parser.add_option('-p', '--production_mult',
        action="store", dest="production_mult", 
        help="When a bot's strength reaches production * mult, it moves", default=5.)
    
    parser.add_option('-d', '--default_direction',
        action="store", dest="default_direction", 
        help="Default direction to move 0 to 3 for N, E, S, W", default=1)

    options, args = parser.parse_args()
    return options


myID, game_map = hlt.get_init()
hlt.send_init("EvoBot")

options = get_options()
production_mult = float(options.production_mult)
default_direction = [NORTH, EAST, SOUTH, WEST][max(0,min(3,int(float(options.default_direction))))]

def find_nearest_enemy_direction(square):
    direction = NORTH
    max_distance = min(game_map.width, game_map.height) / 2
    for d in (NORTH, EAST, SOUTH, WEST):
        distance = 0
        current = square
        while current.owner == myID and distance < max_distance:
            distance += 1
            current = game_map.get_target(current, d)
        if distance < max_distance:
            direction = d
            max_distance = distance
    return direction

def get_move(square):
    target, direction = max(((neighbor, direction) for direction, neighbor in enumerate(game_map.neighbors(square))
                                if neighbor.owner != myID),
                                default = (None, None),
                                key = lambda t: t[0].production)
    if target is not None and target.strength < square.strength:
        return Move(square, direction)
    elif square.strength < square.production * production_mult:
        return Move(square, STILL)

    border = any(neighbor.owner != myID for neighbor in game_map.neighbors(square))
    if not border:
        return Move(square, find_nearest_enemy_direction(square))
    else:
        #wait until we are strong enough to attack
        return Move(square, STILL)

    
while True:
    
    game_map.get_frame()
    moves = [get_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)

