import binascii
import re
import struct
from urllib.request import urlopen

GAME_ID_RE = re.compile(r'(20[0-9]{8}gm-[0-9a-f]{4}-[0-9]{4,5}-(?:[0-9a-f]{8}|x[0-9a-f]{12}))')

table = [
    22136, 52719, 55146, 42104, 
    59591, 46934, 9248,  28891,
    49597, 52974, 62844, 4015,
    18311, 50730, 43056, 17939,
    64838, 38145, 27008, 39128,
    35652, 63407, 65535, 23473,
    35164, 55230, 27536, 4386,
    64920, 29075, 42617, 17294,
    18868, 2081
]

def tenhouHash(game):
    code_pos = game.rindex("-") + 1
    code = game[code_pos:]
    if code[0] == 'x':
        a,b,c = struct.unpack(">HHH", binascii.a2b_hex(code[1:]))     
        index = 0
        if game[:12] > "2010041111gm":
            x = int("3" + game[4:10])
            y = int(game[9])
            index = x % (33 - y)
        first = (a ^ b ^ table[index]) & 0xFFFF
        second = (b ^ c ^ table[index] ^ table[index + 1]) & 0xFFFF
        return game[:code_pos] + "{:04x}{:04x}".format(first, second)
    else:
        return game

def download_game(game_id, target_fname):
    resp = urlopen('http://e.mjv.jp/0/log/?' + game_id)
    data = resp.read()
    with open(target_fname, 'wb') as f:
        f.write(data)

if __name__ == '__main__':
    import sys
    download_game(sys.argv[1], '/tmp/' + sys.argv[1])
