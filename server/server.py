import math
import random
import json

from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from flask_jsonpify import jsonify


app = Flask(__name__)
api = Api(app)

CORS(app)


def get_flags(ships):
    flags = []
    flags_hit = []
    for ship in ships:
        num = (ship[1][0] - ship[0][0] + 20) // 50
        start = ship[0]
        f = []
        f_hit = []
        for i in range(num):
            f.append([start[0] + i * 50 + 25, start[1]])
            f_hit.append(False)
        flags.append(f)
        flags_hit.append(f_hit)

    print(flags)
    return flags, flags_hit

player1_moves = [[10, 50],
                 [50, 50],
                 [100, 50],
                 [150, 50],
                 [100, 50],
                 ]
player2_moves = []

ships = [
    [
        [[50, 50], [80, 50]],
        [[450, 50], [530, 50]],
        [[50, 100], [130, 100]],
        [[100, 150], [280, 150]],
        [[200, 200], [580, 200]],
        [[50, 300], [230, 300]],
        [[70, 350], [100, 350]],
        [[450, 350], [480, 350]],
        [[210, 400], [290, 400]],
        [[350, 450], [530, 450]],
        [[30, 550], [410, 550]],
    ],
    [
        [[50, 50], [80, 50]],
        [[450, 50], [530, 50]],
        [[50, 100], [130, 100]],
        [[100, 150], [280, 150]],
        [[200, 200], [580, 200]],
        [[50, 300], [230, 300]],
        [[70, 350], [100, 350]],
        [[450, 350], [480, 350]],
        [[210, 400], [290, 400]],
        [[350, 450], [530, 450]],
        [[30, 550], [410, 550]],
    ]
]

flags = [get_flags(ships[0])[0], get_flags(ships[1])[0]]
flags_hit = [get_flags(ships[0])[1], get_flags(ships[1])[1]]

print(flags, flags_hit)


current_ai_move = [0]

class Shot(Resource):
    def post(self):
        print('Request sent')
        print(request)
        print(request.data)
        payload = json.loads(request.data.decode())
        print('Payload', payload)
        player = payload['player']
        x = payload['x']
        y = payload['y']

        if player == 'ai':
            result = '1'if check_hit(float(x), float(y), ships[0]) else '0'
            print('AI move:', x, y, result)
            sunk = '1' if check_sunk(float(x), float(y), 0) else '0'
            #return jsonify({
            #    'result': result,
            #})
            return result + sunk

        else:
            result = '1'if check_hit(float(x), float(y), ships[1]) else '0'
            sunk, ship = check_sunk(float(x), float(y), 0)
            if current_ai_move[0] < len(player1_moves):
                ai_move = player1_moves[current_ai_move[0]]
            else:
                ai_move = [random.random()*600, random.random()*600]
            current_ai_move[0] += 1

            return jsonify({
                'hit': result,
                'sunk': sunk,
                'ai_move': ai_move,
                'ship': ship
            })

api.add_resource(Shot, '/shot/')


def check_hit(x, y, ships):
    max_dist = 30
    for ends in ships:
        dist = distanceToLineSegment(x, y, ends[0][0], ends[0][1], ends[1][0], ends[1][1])
        if (dist < max_dist):
            return True
    return False

def check_sunk(x, y, player):
    for i, f in enumerate(flags[player]):
        for j, flag in enumerate(f):
            dx = flag[0]-x
            dy = flag[1]-y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < 20:
                flags_hit[player][i][j] = True
                for b in flags_hit[player][i]:
                    if not b:
                        return '0', []
                return '1', ships[player][i]
    return '0', []


def distanceToLineSegment(x, y, x1, y1, x2, y2):

  A = x - x1
  B = y - y1
  C = x2 - x1
  D = y2 - y1

  dot = A * C + B * D
  len_sq = C * C + D * D
  param = -1
  if len_sq != 0:
      param = dot / len_sq

  if (param < 0):
    xx = x1
    yy = y1
  
  elif (param > 1) :
    xx = x2
    yy = y2
  
  else:
    xx = x1 + param * C
    yy = y1 + param * D

  dx = x - xx
  dy = y - yy
  return math.sqrt(dx * dx + dy * dy)




if __name__ == '__main__':
    app.run(port=5002)