class Player:
    def __init__(self,stack,name,num):
        self.stack = stack
        self.name = name
        self.card = []
        self.num = num
        self.bet_amount = 0
    
    def get(self,get_amount):
        self.stack += get_amount
    
    def recieve_card(self, card):
        self.card.append(card)
    
    def reset(self):
        self.bet_amount = 0
        self.card = []
    
    def bet(self,bet_amount):
        self.bet_amount += bet_amount
        self.stack -= bet_amount

    def take_action(self,field_max_bet,min_raise):
        while True:
            print({self.name},"'s hand :",{self.card[0]},{self.card[1]})
            print("current stack",{self.stack},"current_bet",self.bet_amount)
            action = input(f"{self.name}:choose your action, f(fold) or c(call) or r(raise)")
            if action == "f":
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