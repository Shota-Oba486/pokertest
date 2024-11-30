import random
import numpy as np
from player import Player
from ranking import rank_of_seven_card

class OneRound:
    def __init__(self,players,btn_player,sb_amount,min_raise):
        self.players = players
        self.btn_player = btn_player
        self.sb_amount = sb_amount
        self.min_raise = min_raise
        self.round = True
        self.battle_user_list = [player.stack >= 0 for player in  players]
        self.players_length = len(players)
        self.field_card = []
        self.deck = [
            "As", "Ad", "Ac", "Ah",
            "Ks", "Kd", "Kc", "Kh",
            "Qs", "Qd", "Qc", "Qh",
            "Js", "Jd", "Jc", "Jh",
            "Ts", "Td", "Tc", "Th",
            "9s", "9d", "9c", "9h",
            "8s", "8d", "8c", "8h",
            "7s", "7d", "7c", "7h",
            "6s", "6d", "6c", "6h",
            "5s", "5d", "5c", "5h",
            "4s", "4d", "4c", "4h",
            "3s", "3d", "3c", "3h",
            "2s", "2d", "2c", "2h"
        ]

    def _get_next_player_index(self,current_index):
        ### 現在のindexから次のactiveプレイヤーのインデックスを把握する関数
        for i in range(1,self.players_length):
            next_index = (current_index + i) % self.players_length
            if self.battle_user_list[next_index]:
                return next_index
        return None
    
    def _betting_round(self):
        ### レイズだのフォールドなどが終わるまでプレイヤーを周回する関数
        act_done_list = [False] * self.players_length
        print(self.battle_user_list)

        while True:
            if act_done_list[self.current_index] == True:
                break

            player = self.players[self.current_index]
            print(player.name,end = "")

            action = player.take_action(self.field_max_bet_amount,self.min_raise)
            print("action:",action," bet_amount:",player.bet_amount)

            if action == "r":
                self.field_max_bet_amount = player.bet_amount
                act_done_list = [False] * self.players_length
                act_done_list[self.current_index] = True
            if action == "c":
                act_done_list[self.current_index] = True
            if action == "f":
                act_done_list[self.current_index] = True
                self.battle_user_list[self.current_index] = False

            self.current_index = self._get_next_player_index(self.current_index)

            if sum(self.battle_user_list) <= 1:
                break

    def start(self):
        ###デッキのシャッフル
        random.shuffle(self.deck)
        sb_player = self._get_next_player_index(self.btn_player)
        bb_player = self._get_next_player_index(sb_player)

        ### sbプレイヤー、bbプレイヤーからmoneyを徴収する
        self.players[sb_player].bet(self.sb_amount)
        self.players[bb_player].bet(self.sb_amount * 2)
        self.field_max_bet_amount = self.sb_amount * 2

        ### 各プレイヤーに二枚ずつデッキからカードを配る
        print("二枚ずつカードを配布")
        for player in self.players:
            player.recieve_card(self.deck.pop(0))
            player.recieve_card(self.deck.pop(0))
        
        self.current_index = self._get_next_player_index(bb_player)
        self.first_index = self.current_index
    
        ### bbプレイヤーの一個次から、ゲーム開始
        print("first round start!!")
        self._betting_round()

        ### フィールドに三枚表示する
        self.field_card.append(self.deck.pop(0))
        self.field_card.append(self.deck.pop(0))
        self.field_card.append(self.deck.pop(0))
        print("field card :" ,{self.field_card[0]},{self.field_card[1]},{self.field_card[2]})

        ### もう一回プレイヤーを一周する
        print("second round start!!(3cards)")
        self._betting_round()

        # フィールドに一枚追加する（これで4枚）
        self.field_card.append(self.deck.pop(0))
        print("field card :" ,{self.field_card[0]},{self.field_card[1]},{self.field_card[2]},{self.field_card[3]})

        ### もう一回プレイヤーを一周する
        print("second round start!!(4cards)")
        self._betting_round()

        ### フィールドに一枚追加する（これで5枚）
        self.field_card.append(self.deck.pop(0))
        print("field card :" ,{self.field_card[0]},{self.field_card[1]},{self.field_card[2]},{self.field_card[3]},{self.field_card[4]})

        ### 最後にもう一回プレイヤーを一周する
        print("second round start!!(5cards)")
        self._betting_round()        

        ### 各プレイヤーの手札を見て、勝敗を決定する
        print("judgment start!!")
        best_player_score = 0
        for player in self.players:
            if self.battle_user_list[player.num]:
                player.card = player.card + self.field_card
                player_five_card, player_rank_text, player_hand_score = rank_of_seven_card(player.card)
                print(player.name,player_five_card[0],player_five_card[1],player_five_card[2],player_five_card[3],player_five_card[4])
                if best_player_score < player_hand_score:
                    best_player_score = player_hand_score
                    best_player_num = player.num
            else:
                print(player.name,"fold")

        self.field_money = sum(player.bet_amount for player in self.players)
        self.players[best_player_num].get(self.field_money)
        for player in self.players:
            player.reset()
        print(best_player_num)