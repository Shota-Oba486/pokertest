from player import Player
from one_round import OneRound

class RunGame:
    def __init__(self,player_num,stack,play_num,min_raise,sb_amount):
        self.player_num = player_num
        self.players = []
        for i in range(player_num):
            self.players.append(Player(stack,"player" + str(i),i))
        self.play_num = play_num
        self.current_play_num = 0
        self.min_raise = min_raise
        self.btn_player = 0
        self.sb_amount = sb_amount
        self.result = []

    def start(self):
        for i in range(self.play_num):
            print("round",i+1,":start!!!")
            self.current_play_num += 1
            one_round = OneRound(self.players,self.btn_player,self.sb_amount,self.min_raise)
            one_round.start()

            for i in range(1, self.player_num):
                potential_btn_player = (self.btn_player + i) % self.play_num
                if self.players[potential_btn_player].stack >= 0:
                    self.btn_player = potential_btn_player
                    break
        
        for player in self.players:
            self.result.append(player.stack)
        self.rank_list = sorted(range(len(self.result)), key=lambda i: self.result[i], reverse=True)
        
        print(self.result)