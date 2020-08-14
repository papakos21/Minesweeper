"""afsfasf"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler

from DifficultyEnum import Difficulty
from MinesweeperBoard import MinesweeperBoard
game = MinesweeperBoard()

class MinesweeperHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        path_components = self.path.split('/')
        response = ""
        if path_components[1] == 'get_column_size':
            response = str(game.get_column_size())
        elif path_components[1] == 'get_row_size':
            response = str(game.get_row_size())
        elif path_components[1] == 'get_tile' and path_components[2].isdigit() and path_components[3].isdigit():
            row_index = int(path_components[2])
            column_index = int(path_components[3])
            # game.players_choice_of_tile_and_action((row_index, column_index), 'reveal')
            tile = game.get_tile(row_index, column_index)
            response = json.dumps(tile.__dict__)
        elif path_components[1] == 'new_game':
            difficulty = path_components[2]
            game = MinesweeperBoard(Difficulty.get(difficulty))
            response = json.dumps({'row_size':game.get_row_size(), 'column_size':game.get_column_size()})


        elif path_components[1] == 'human_won':
            response = str(game.human_won())
        elif path_components[1] == 'game_over':
            response = str(game.game_over())
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(response, 'UTF-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode("utf-8") )
        game.reset_changed_tiles()
        game.players_choice_of_tile_and_action((data['row_index'], data['column_index']), data['action'])
        changed_tiles = game.get_changed_tiles()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(changed_tiles), 'UTF-8'))





def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    """Run"""
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run(handler_class=MinesweeperHandler)
