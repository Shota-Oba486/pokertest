from game import RunGame

def main():
    # プレイヤー4人、持ち点10,000、3Round、min_raise=100、sb_amount=100
    run_game = RunGame(4,10000,3,100,100)
    run_game.start()

if __name__ == "main":
    main()