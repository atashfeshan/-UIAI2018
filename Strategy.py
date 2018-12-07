import math
import random
import pandas as pd
import numpy as np
from MyFunc import *
from client import *
from sklearn import svm
from scipy.spatial import distance
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
b = 0
diff = 0


def init_players():
    players = [Player(name="tomato", first_pos=Pos(-6.45, 1.6)),
               Player(name="banana", first_pos=Pos(-6, 0.55)),
               Player(name="Melon", first_pos=Pos(-6, -0.55)),
               Player(name="Eggplant", first_pos=Pos(-6.45, -1.6)),
               Player(name="Cucumber", first_pos=Pos(-1, 0))]
    return players


def do_turn(game):
    global b
    global diff
    t = 0
    my = game.getMyTeam().getScore()
    them = game.getOppTeam().getScore()
    f = my-them
    if f < diff:
        b += 1
    if b == 3:
        diff = 0
        t = random.randrange(-15, 15)
    diff = f
    ###########################################
    # read data and classification
    data = pd.read_csv('ee.csv')
    data = np.array(data)
    train_data = data[..., :137]
    train_label = data[..., 137:140]
    clf = svm.SVC(kernel='linear', C=1.0)
    gnb = GaussianNB()
    k = KMeans(n_clusters=1)
    clf.fit(train_data, range(len(train_data)))
    gnb.fit(train_data, range(len(train_data)))
    act = Triple()
    #########################################
    # set the position
    mine = []
    yours = []
    for i in range(5):
        x = game.getOppTeam().getPlayer(i).getPosition().getX()
        y = game.getOppTeam().getPlayer(i).getPosition().getY()
        x1 = game.getMyTeam().getPlayer(i).getPosition().getX()
        y1 = game.getMyTeam().getPlayer(i).getPosition().getY()
        mine.append([x1, y1])
        yours.append([x, y])

    x2 = game.getBall().getPosition().getX()
    y2 = game.getBall().getPosition().getY()
    ##########################################
    # make test data
    obj = mine.copy()
    obj.extend(yours)
    board = list(make_board(obj))
    board.extend([x2, y2])
    ##########################################
    # predict test label
    m1 = train_label[clf.predict([board])][0]
    m2 = train_label[gnb.predict([board])][0]
    k.fit([m1, m2])
    m = k.cluster_centers_[0]
    k = [m[0], m[1]]
    ##########################################
    # find best player
    ma = 1000
    near = 0
    for i in range(5):
        dst = distance.euclidean(k, mine[i])
        if dst < ma:
            ma = dst
            near = i
    ##########################################
    # get the position
    x1 = game.getMyTeam().getPlayer(near).getPosition().getX()
    y1 = game.getMyTeam().getPlayer(near).getPosition().getY()
    x2 = game.getBall().getPosition().getX()
    y2 = game.getBall().getPosition().getY()
    ##########################################
    # calculate angle
    angle = math.fabs(math.degrees(math.atan((y2 - y1) / (x2 - x1))))
    if x2 > x1:
        if y2 < y1:
            angle = 360 - angle
    else:
        if y2 < y1:
            angle += 180
        else:
            angle = 180 - angle
    ##########################################
    # make sure about power
    power = 100
    if (angle < 270) and (angle > 90):
        power = 50
    #########################################
    player_id = near

    if (angle < 93) and (angle > 87):
        angle += 10
    elif (angle < 273) and (angle > 267):
        angle -= 10
    if (x2 < -5) and (x1 > x2) and (angle < 50) and (angle > -50):
        if angle > 0:
            angle += 45
        else:
            angle -= 45
    #########################################
    # Out put
    ##########################################
    act.setPlayerID(player_id)   #
    act.setAngle(angle+t)        #
    act.setPower(power)          #
    return act                   #
    ##########################################
