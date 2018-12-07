import socket

from client import *

import Strategy


class Game:

    def __init__(self, inet_address, port):
        self.field = Field()
        self.__ball = Ball()
        self.__my_team = Team()
        self.__opp_team = Team()
        self.__cycle_no = 0
        self.__server_address = (inet_address, port)
        self.__input = None
        self.__output = None

    def connect_to_server(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.setblocking(True)
            self.__socket.connect(self.__server_address)
            self.__input = self.__socket.makefile(encoding='utf-8', mode='r')
            self.__output = self.__socket.makefile(encoding='utf-8', mode='w')
        except Exception as e:
            print(e)
            return False
        return True

    def start(self, team_name):
        lines = []
        lines.append("register %s" % team_name)

        self.my_team._Team___set_players(Strategy.init_players())
        x = ",".join(str(player) for player in self.my_team)
        formation = "formation %s" % x
        lines.append(formation)

        try:
            for each in lines:
                print(each, end='\n', flush=True, file=self.__output)
        except Exception as e:
            print(e)

        self.opp_team._Team___set_players(Strategy.init_players())
        while True:
            try:
                lines = []
                lines.append(self.__input.readline())
                if str(lines[0]).strip('\n') == 'END':
                    print("Finished")
                    break
                lines.append(self.__input.readline())
                lines.append(self.__input.readline())
                lines.append(self.__input.readline())

            except Exception as e:
                print("problem in getting response from server:")
                print('\t', e)
                return
            self.play_round(lines)

    def play_round(self, lines):
        self_team = lines[0].split(',')
        opp_team = lines[1].split(',')
        for each, each_pos in zip(self.my_team, self_team):
            each.pos._Pos__x, each.pos._Pos__y = map(float, each_pos.split(":"))

        for each, each_pos in zip(self.opp_team, opp_team):
            each.pos._Pos__x, each.pos._Pos__y = map(float, each_pos.split(":"))

        self.ball.pos._Pos__x, self.ball.pos._Pos__y = map(float, lines[2].split(":"))

        self.my_team._Team__score, self.opp_team._Team__score, self.__cycle_no = map(int, lines[3].split(','))

        self.kick(Strategy.do_turn(self))

    def kick(self, triple):
        res = '%s,%s,%s' % (triple.player_id, triple.angle, triple.power)
        print(res, end='\n', flush=True, file=self.__output)

    @property
    def my_team(self):
        return self.__my_team

    def getMyTeam(self):
        return self.my_team

    @property
    def opp_team(self):
        return self.__opp_team

    def getOppTeam(self):
        return self.opp_team

    @property
    def cycle_no(self):
        return self.__cycle_no

    @property
    def ball(self):
        return self.__ball

    def getBall(self):
        return self.ball

if __name__ == "__main__":
    game = Game('127.0.0.1', 9595)
    game.connect_to_server()
    game.start('Cats') #Write your team name here

