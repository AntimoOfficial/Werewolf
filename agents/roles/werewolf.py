from ..base_agent import BaseAgent

class WerewolfAgent(BaseAgent):
    """
    狼人角色的代理。
    """
    def __init__(self, agent_id: int, player_name: str):
        super().__init__(agent_id, player_name)

    def night_action(self, **kwargs):
        # TODO: 实现狼人夜间讨论和投票杀人的逻辑
        # print(f"{self.player_name} (狼人) 正在选择目标...")
        return None
