

class Pos:
    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def __str__(self):
        return "%f:%f" % (self.x, self.y)

    def __repr__(self):
        return "%f:%f" % (self.x, self.y)


class Ball:
    def __init__(self, pos=None):
        if pos is None:
            pos = Pos(0, 0)
        self.__pos = pos

    @property
    def pos(self):
        return self.__pos

    def getPosition(self):
        return self.pos


class Field:
    def __init__(self, ball=None):
        self.ball = ball


class Player:

    __NEXT_ID = 0

    def __init__(self, name='', first_pos=Pos(0, 0)):
        self.__id = self.__get_next_id()
        self.__name = name
        assert isinstance(first_pos, Pos)
        self.__first_pos = first_pos
        self.__pos = first_pos

    def __get_next_id(self):
        id_ = self.__NEXT_ID
        self.__NEXT_ID += 1
        return id_

    @property
    def id(self):
        return self.__id

    def getId(self):
        return self.id

    @property
    def name(self):
        return self.__name

    def getName(self):
        return self.name

    @property
    def first_pos(self):
        return self.__first_pos

    def getFirstPosition(self):
        return self.first_pos

    @property
    def pos(self):
        return self.__pos

    def getPosition(self):
        return self.pos

    def __str__(self):
        return "%s:%s" % (self.name, self.pos)

    def __repr__(self):
        return "%s:%s" % (self.name, self.pos)


class Team:

    def __init__(self):
        self.__players = [None for i in range(5)]
        self.__score = 0

    @property
    def score(self):
        return self.__score

    def getScore(self):
        return self.score

    def ___set_players(self, players):
        assert isinstance(players, (list, tuple)), "players must be a list of client.Player instances"
        for each in players:
            assert isinstance(each, Player), "each instance in players list must be a client.Player instance"
        self.__players = players

    def ___add_player(self, player):
        if len(self.__players) > 5:
            raise Exception('Team can not have more than 5 players')
        else:
            assert isinstance(player, Player), 'player must be a client.Player instance'
            self.__players.append(player)

    def getPlayer(self, id):
        assert id < 5
        return self.__players[id]

    def __iter__(self):
        for each in self.__players:
            yield each


class Triple:

    def __init__(self):
        self.player_id = 0
        self.angle = 0
        self.power = 100

    def setPlayerID(self, playerID):
        self.player_id = playerID

    def setAngle(self, angle):
        self.angle = angle

    def setPower(self, power):
        self.power = power
