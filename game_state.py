from typing import List
# 在未来的实现中，我们将从 agents.base_agent 导入 BaseAgent
# from agents.base_agent import BaseAgent

class GameState:
    """
    存储和管理游戏的所有当前状态。
    这是一个纯粹的数据容器，不包含游戏逻辑。
    """
    def __init__(self):
        self.players: List = [] # 未来将是 List[BaseAgent]
        self.day_number: int = 0
        self.game_phase: str = 'STARTING'  # 例如: 'NIGHT', 'DAY_DISCUSSION', 'VOTING', 'ENDED'
        self.game_history: List[str] = []
        self.nightly_deaths: List = [] # 未来将是 List[BaseAgent]

    def get_player_by_name(self, name: str):
        """根据玩家名称查找玩家对象。"""
        for player in self.players:
            if player.player_name == name:
                return player
        return None

    def get_living_players(self) -> List:
        """获取所有存活的玩家。"""
        return [p for p in self.players if p.status == 'alive']

    def add_history(self, event: str):
        """记录游戏事件并实时打印到控制台。"""
        print(event)
        self.game_history.append(f"[Day {self.day_number} | {self.game_phase}] {event}")
