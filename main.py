from game_master import GameMaster

def main():
    """项目主入口"""
    # 定义参与本局游戏的玩家列表
    player_names = ['Ella', 'Bane', 'Chris', 'Diana', 'Eric', 'Fiona'] # 创建6名玩家

    # 初始化游戏控制器
    game_master = GameMaster(player_names)

    # 开始游戏
    try:
        game_master.run_game()
    except KeyboardInterrupt:
        print("\n游戏被主持人手动中断。")
    except Exception as e:
        print(f"\n游戏因未知错误而中断: {e}")

if __name__ == "__main__":
    main()
