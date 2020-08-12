import requests
import json

from Tile import Tile

SERVER_URL = 'http://localhost:8000'
r = requests.get('http://localhost:8000/get_row_size')
print(r.status_code)
print(r.text)

data = json.dumps({'row_index': 0,'column_index': 0,'action': 'reveal'})
response = requests.post(SERVER_URL +'/play', data )

# response = requests.get(SERVER_URL+'/get_tile/'+ str(0)+'/' + str(0))
# tile_data = json.loads(response.text)
# tile = Tile()
# tile.flag = tile_data['flag']