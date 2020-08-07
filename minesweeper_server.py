"""afsfasf"""
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler

from MinesweeperBoard import MinesweeperBoard


class MinesweeperHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        potential_coordinates = self.path.split('/')
        row_index = int(potential_coordinates[1])
        column_index = int(potential_coordinates[2])
        game.players_choice_of_tile_and_action((row_index, column_index), 'reveal')
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(str(game.board[row_index][column_index].number_of_neighbour_bombs), 'UTF-8'))



game = MinesweeperBoard()


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    """Run"""
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run(handler_class=MinesweeperHandler)


