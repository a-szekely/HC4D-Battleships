import math
import random

from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from flask_jsonpify import jsonify


app = Flask(__name__)
api = Api(app)

CORS(app)

player1_moves = [[10, 50],
                 [50, 50],
                 [100, 50],
                 [150, 50],
                 [100, 50],
                 ]
player2_moves = []

player1_ships = [
        [[50, 50], [300, 50]],
        [[300, 200], [500, 200]]
    ]
player2_ships = [
        [[50, 50], [300, 50]],
        [[300, 200], [500, 200]]
    ]

current_ai_move = [0]

class Shot(Resource):
    def post(self):
        print('Request sent')
        print(request)
        payload = request.get_json()
        player = payload['player']
        x = payload['x']
        y = payload['y']

        if player == 'ai':
            result = '1'if check_hit(float(x), float(y), player1_ships) else '0'
            print('AI move:', x, y, result)
            return jsonify({
                'result': result,
            })

        else:
            result = '1'if check_hit(float(x), float(y), player2_ships) else '0'
            if current_ai_move[0] < len(player1_moves):
                ai_move = player1_moves[current_ai_move[0]]
            else:
                ai_move = [random.random()*800, random.random()*800]
            current_ai_move[0] += 1

            return jsonify({
                'response': result,
                'ai_move': ai_move
            })

api.add_resource(Shot, '/shot/')


def check_hit(x, y, ships):
    max_dist = 20
    for flags in ships:
        dist = distanceToLineSegment(x, y, flags[0][0], flags[0][1], flags[1][0], flags[1][1])
        if (dist < max_dist):
            return True
    return False


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