import random
import sys
import pandas as pd
import numpy as np
from player import Player
from ranking import rank_of_seven_card

class OneGame:
    def __init__(self,players,db_player,sb_amount,min_raise):
        self.players = players
        self.db_player = db_player
        self.sb_amount = sb_amount
        self.min_raise = min_raise
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
        players_length = len(self.players)
        for i in range(1,players_length):
            next_index = (current_index + i) % players_length
            if self.players[next_index].battle_flag:
                return next_index
        return None
    
    def _betting_round(self):
        ### レイズだのフォールドなどを一周する関数
        print("betting start")
        while True:
            player = self.players[self.current_index]
            action = player.take_action(self.field_max_bet_amount,self.min_raise)
            if action == "r":
                self.field_max_bet_amount = player.bet_amount
            
            active_players = [p for p in self.players if p.battle_flag]
            if len(active_players) <= 1 or all(p.bet_amount for p in active_players):
                break

            self.current_index = self._get_next_player_index(self.current_index)

    def start(self):
        ###デッキのシャッフル
        random.shuffle(self.deck)

        ### sbプレイヤー、bbプレイヤーからmoneyを徴収する
        self.players[self._get_next_player_index(self.db_player)].bet(self.sb_amount)
        self.players[self._get_next_player_index(self._get_next_player_index(self.db_player))].bet(self.sb_amount * 2)
        self.field_money = self.sb_amount * 3
        self.field_max_bet_amount = self.sb_amount * 2

        ### 各プレイヤーに二枚ずつデッキからカードを配る
        for player in self.players:
            player.recieve_card(self.deck.pop(0))
            player.recieve_card(self.deck.pop(0))
        
        self.current_index = self._get_next_player_index(self.db_player)
        self.first_index = self.current_index
    
        ### bbプレイヤーの一個次から、ゲーム開始
        self._betting_round()

        ### フィールドに三枚表示する
        self.field_card.append(self.deck.pop(0))
        self.field_card.append(self.deck.pop(0))
        self.field_card.append(self.deck.pop(0))

        ### もう一回プレイヤーを一周する
        self._betting_round()

        # フィールドに一枚追加する（これで4枚）
        self.field_card.append(self.deck.pop(0))

        ### もう一回プレイヤーを一周する
        self._betting_round()

        ### フィールドに一枚追加する（これで5枚）
        self.field_card.append(self.deck.pop(0))

        ### 各プレイヤーの手札を見て、勝敗を決定する
        best_player_score = 0
        for player in self.players:
            if player.battle_flag:
                player.recieve_card(self.field_card)
                player_five_card, player_rank_text, player_rank_num = rank_of_seven_card(player.card)
                if best_player_score < player_rank_num:
                    best_player_score = player_rank_num
                    best_player_num = player.num
        
        self.players[best_player_num].get(self.field_money)
        for player in self.players:
            player.reset()