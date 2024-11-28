class Player:
    def __init__(self,stack,name,num):
        self.stack = stack
        self.name = name
        self.card = []
        self.num = num
        self.battle_flag = True
    
    def get(self,get_amount):
        self.stack += get_amount
    
    def receive_card(self, card):
        self.card.append(card)
    
    def reset(self):
        self.bet_amount = 0
        self.card = []
        self.battle_flag = True

    def take_action(self,field_max_bet,min_raise):
        while True:
            action = input("choose your action, f(fold) or c(call) or r(raise)")
            if action == "f":
                self.battle_flag == False
                return "f"
            elif action == "c":
                call_amount = field_max_bet - self.bet_amount
                if self.stack >= call_amount:
                    self.stack -= call_amount
                    self.bet_amount += call_amount
                    return "c"
                else:
                    print("not enough money to call")
            elif action == "r":
                raise_amount = int(input(f"raise amount min:{min_raise}"))

                total_bet_amount = field_max_bet + raise_amount
                if raise_amount >= min_raise and self.stack >= (total_bet_amount - self.bet_amount):
                    self.stack -= (total_bet_amount - self.bet_amount)
                    self.bet_amount  = total_bet_amount
                    print(f"raise to {total_bet_amount} chips")
                    return "r"
                else:
                    print("Invalid raise amount")
            else:
                print("try again")