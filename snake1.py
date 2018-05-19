import time
import keyboard
import sys
import os
import random

# prints the FIELD :
def pf():
    time.sleep(sp)
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    print('Snake size:', len(b) + 1)
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, len(b)):
                if i == b[k]['x'] and j == b[k]['y']:
                    f[i][j] = True
            if h['x'] == i and h['y'] == j:
                f[i][j] = True
            print(int(f[i][j]), end='  ')
        print()


sp = 0.1
game = True
struct = {'x': 0,
          'y': 0}
n = 10
f = [[False for i in range(0, n)] for j in range(0, n)]
# sneak AT START :
h = struct.copy()
h['x'] = n // 4
h['y'] = n // 2 - 1
b = []
for i in range(0, n // 2):
    b.append(struct.copy())
    b[i]['x'] = h['x'] + 1 + i
    b[i]['y'] = h['y']
pf()
step = 0
while game:
    keyboard.read_key()
    if keyboard.is_pressed('esc'):
        break
    # MOVE :
    elif keyboard.is_pressed('up') and h['x'] - 1 != b[0]['x'] or\
            keyboard.is_pressed('left') and h['y'] - 1 != b[0]['y'] or\
            keyboard.is_pressed('down') and h['x'] + 1 != b[0]['x'] or\
            keyboard.is_pressed('right') and h['y'] + 1 != b[0]['y']:
        # if step % 5 == 0:

        cx = h['x']
        cy = h['y']
        if keyboard.is_pressed('up'):
            if h['x'] - 1 < 0:
                h['x'] = n - 1
            else:
                h['x'] -= 1
        elif keyboard.is_pressed('left'):
            if h['y'] - 1 < 0:
                h['y'] = n - 1
            else:
                h['y'] -= 1
        elif keyboard.is_pressed('down'):
            if h['x'] + 1 > n-1:
                h['x'] = 0
            else:
                h['x'] += 1
        elif keyboard.is_pressed('right'):
            if h['y'] + 1 > n-1:
                h['y'] = 0
            else:
                h['y'] += 1
        # MOVE body after head (and CLEAR trace) :
        for i in range(0, len(b)):
            f[b[i]['x']][b[i]['y']] = False
            b[i]['x'], cx = cx, b[i]['x']
            b[i]['y'], cy = cy, b[i]['y']
        # LOSS? :
        for i in range(0, len(b)):
            if h == b[i]:
                game = False
        pf()
        step += 1
    else:
        pass
    # ~for being at the bottom(seeing sneak) :
    for i in range(0, 1):
        keyboard.press_and_release(81)
print('The end.')
