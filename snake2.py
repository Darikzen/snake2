import re
from keyboard import *
import time
import sys
import os
import random
import numpy as np

# clear screen:
def cls():
    time.sleep(sp)
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


# print the field:
def pf():
    cls()
    print('\nsnake size:', s, '\n')
    for i in range(0, n):
        print(end = '  ')
        for j in range(0, n):
            if f[i][j]:
                pr = trobj
            else:
                pr = flobj
            print(pr, end=' '*btwnc)
        print('\n'*btwnr)
    # chek out print:
    if chkot_trgr:
        print('\n# step: {0}\n# sp: {1:.4}\n# nowp: {2}'.format(st, sp, nowp))

# moves:
def up(a):
    if a['x'] == 0:
        a['x'] = n - 1
    else:
        a['x'] -= 1

def left(a):
    if a['y'] == 0:
        a['y'] = n - 1
    else:
        a['y'] -= 1

def down(a):
    if a['x'] + 1 > n - 1:
        a['x'] = 0
    else:
        a['x'] += 1

def right(a):
    if a['y'] + 1 > n - 1:
        a['y'] = 0
    else:
        a['y'] += 1


# check out:
chkot_btn = 61
chkot_trgr = False
optns = ''
f = open('snake2_options.txt')
for line in f:
    optns += line
f.close()
# graphics:
btwnc = int(re.search('space_between_cols.*:\s*(\d*)', optns).group(1))
btwnr = int(re.search('space_between_rows.*:\s*(\d*)', optns).group(1))
trobj = re.search('true_object.*:\s*\'(.*)\'', optns).group(1)
flobj = re.search('false_object.*:\s*\'(.*)\'', optns).group(1)
# gameplay:
sp = float(re.search('speed.*:\s*(\d*\.?\d*)', optns).group(1))
startsp = sp
spup = float(re.search('speed-up.*:\s*(\d*\.?\d*)', optns).group(1))
n = int(re.search('field_size.*:\s*(\d*)', optns).group(1))
maxp = int(re.search('max_points_together.*:\s*(\d*)', optns).group(1))
# controls:
kup = int(re.search('key_up.*:\s*(\d*)', optns).group(1))
kleft = int(re.search('key_left.*:\s*(\d*)', optns).group(1))
kdown = int(re.search('key_down.*:\s*(\d*)', optns).group(1))
kright = int(re.search('key_right.*:\s*(\d*)', optns).group(1))
del optns
# how many "points" now exist:
nowp = 0
# snake size:
s = 5
f = np.array([[False for i in range(0, n)] for j in range(0, n)])
# direct.-s:
d = np.array([['' for i in range(0, n)] for j in range(0, n)])
# body at start:
for i in range(0, s):
    f[i+n//2-s//2][n//2] = True
    d[i+n//2-s//2+1][n//2] = 'u'
# prev. head direct.:
dhw = 'u'
# head:
h = {'x': n//2-s//2,
     'y': n//2}
# tail:
t = {'x': n//2-s//2+s-1,
     'y': n//2}
pf()
# steps counter:
st = 0
now = ''
while True:
    if is_pressed(kup) and dhw != 'd' \
            or is_pressed(kleft) and dhw != 'r' \
            or is_pressed(kdown) and dhw != 'u' \
            or is_pressed(kright) and dhw != 'l':
        break
while True:
    if is_pressed(chkot_btn):
        if not chkot_trgr:
            chkot_trgr = True
        else:
            chkot_trgr = False
    if is_pressed(kup) and dhw != 'd':
        now = 'u'
    elif is_pressed(kleft) and dhw != 'r':
        now = 'l'
    elif is_pressed(kdown) and dhw != 'u':
        now = 'd'
    elif is_pressed(kright) and dhw != 'l':
        now = 'r'
    # move head:
    if now == 'u':
        d[h['x']][h['y']] = dhw = 'u'
        up(h)
    elif now == 'l':
        d[h['x']][h['y']] = dhw = 'l'
        left(h)
    elif now == 'd':
        d[h['x']][h['y']] = dhw = 'd'
        down(h)
    elif now == 'r':
        d[h['x']][h['y']] = dhw = 'r'
        right(h)
    f[t['x']][t['y']] = False
    # game over?:
    if f[h['x']][h['y']]:
        # point?:
        if d[h['x']][h['y']] == 'p':
            s += 1
            sp *= 1 - spup
            nowp -= 1
            d[h['x']][h['y']] = ''
            f[t['x']][t['y']] = True
        else:
            otcm = 'GAME OVER'
            break
    # move tail?:
    if not f[t['x']][t['y']]:
        # prev. tail direct.:
        d[t['x']][t['y']], dtw = '', d[t['x']][t['y']]
        if dtw == 'u':
            up(t)
        elif dtw == 'l':
            left(t)
        elif dtw == 'd':
            down(t)
        elif dtw == 'r':
            right(t)
    f[h['x']][h['y']] = True
    # add "points":
    if nowp < maxp and s != n*n and nowp + s != n*n:
        while True:
            x = random.randint(0, n-1)
            y = random.randint(0, n-1)
            if not f[x][y]:
                f[x][y] = True
                d[x][y] = 'p'
                break
        nowp += 1
    pf()
    st += 1
    # victory?:
    if s == n * n:
        otcm = 'VICTORY'
        break
name = input('{0:_^{1}}\n\nEnter your name or just press "Enter":\n'.format(otcm, n*len(flobj) + btwnc*(n-1)+2))
if name != '':
    f = open('snake2_records.txt', 'a')
    f.write('\n* {0} *\n(speed: {1}\nspeed-up: {2}\nfield_size: {3}\nmax_points_together: {4})\nsnake SIZE: {5}\n'\
            .format(name.upper().replace(' ', '_'), startsp, spup, n, maxp, s))
    f.close()
