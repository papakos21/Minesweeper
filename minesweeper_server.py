"""afsfasf"""
import json
import uuid
from DataBaseManager import DataBaseManager
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler

from DifficultyEnum import Difficulty
from MinesweeperBoard import MinesweeperBoard, MinesweeperBoardDatabaseTracker

games = {}
DATABASEMANAGER = DataBaseManager("minesweeper.db")


class MinesweeperHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        path_components = self.path.split('/')
        response = ""

        if path_components[1] == 'new_game':
            difficulty = path_components[2]
            generated_key = str(uuid.uuid4())
            user_id = self.headers["User_Id"]
            games[generated_key] = MinesweeperBoardDatabaseTracker(MinesweeperBoard(Difficulty.get(difficulty)),
                                                                   game_id=generated_key, user_id=user_id)
            response = json.dumps({'row_size': games[generated_key].get_row_size(),
                                   'column_size': games[generated_key].get_column_size(),
                                   'game_id': generated_key})
        elif path_components[1] == 'human_won':
            response = str(games[path_components[2]].human_won())
        elif path_components[1] == 'high_scores':
            response = json.dumps(DATABASEMANAGER.get_top_times(path_components[2], 10))
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(response, 'UTF-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode("utf-8"))
        game_id = data['game_id']
        games[game_id].reset_changed_tiles()
        games[game_id].players_choice_of_tile_and_action((data['row_index'], data['column_index']), data['action'])
        changed_tiles = games[game_id].get_changed_tiles()
        game_over = False if data['action'] != 'reveal' else games[game_id].game_over()
        game_over_and_changed_tiles = {"game_over": game_over, 'changed_tiles': changed_tiles}
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(game_over_and_changed_tiles), 'UTF-8'))

    def address_string(self):
        host, port = self.client_address[:2]
        # return socket.getfqdn(host)
        return host


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    """Run"""
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run(handler_class=MinesweeperHandler)
