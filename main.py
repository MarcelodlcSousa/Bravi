import random
from itertools import product
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

chess = []

def knight_moves(position):
    x, y = position
    moves = list(product([x - 1, x + 1], [y - 2, y + 2])) + list(
        product([x - 2, x + 2], [y - 1, y + 1]))
    moves = [(x, y) for x, y in moves if x >= 0 and y >= 0 and x < 8 and y < 8]
    return moves

class PostXadrez(Resource):

    def post(self, piece_type, color, line_index, column_index):
        ids = [id['id'] for id in chess if 'id' in id]
        lines = [line['line_index'] for line in chess if 'line_index' in line]
        columns = [column['column_index'] for column in chess if 'column_index' in column]
        if len(ids) == 17:
            return 'Maximum chess pieces limit reached!', 404
        if len(lines) != 0 and len(columns) != 0:
            for line in lines:
                if line_index == line:
                    return 'Location is already occupied by another piece!', 404
                for column in columns:
                    if column_index == column:
                        return 'Location is already occupied by another piece!', 404
        if line_index not in range(1, 8) and column_index not in range(1, 8):
            return 'Out of chessboard boundaries', 404
        id = random.randint(0, 16)
        if len(ids) != 0:
            for id in ids:
                while id in ids:
                    id = random.randint(0, 16)
                piece = {'id': id,
                        'piece_type': piece_type,
                        'color': color,
                        'line_index': line_index,
                        'column_index': column_index}
        else:
            piece = {'id': random.randint(0, 16),
                    'piece_type': piece_type,
                    'color': color,
                    'line_index': line_index,
                    'column_index': column_index}

        chess.append(piece)

        return chess


class GetKnight(Resource):

    def get(self, id, piece_type, color, line_index, column_index):
        d = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
        possible_moves = []
        corrected_coords = []
        for piece in chess:
            if piece['piece_type'] == piece_type:
                if piece_type == 'knight':
                    moves = knight_moves((line_index, column_index))
                    for location in moves:
                        new_moves = knight_moves(location)
                    for coords in new_moves:
                        a, b = coords
                        alg_column = d[b]
                        corrected_coords.append((a, alg_column))
                    return corrected_coords
        return {'id': None}, 404

class GetAny(Resource):

    def get(self, piece_type, color):
        for piece in chess:
            if piece['piece_type'] == piece_type:
                    return piece['id']
        return {'id': None}, 404

api.add_resource(PostXadrez,'/addpiece/<string:piece_type>-<string:color>-<int:line_index>-<int:column_index>')
api.add_resource(GetKnight,'/getknight/<int:id>-<string:piece_type>-<string:color>-<int:line_index>-<int:column_index>')
api.add_resource(GetAny,'/getany/<string:piece_type>-<string:color>')

if __name__ == "__main__":
    app.run(debug=False)