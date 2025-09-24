from ..base_agent import BaseAgent

class VillagerAgent(BaseAgent):
    """
    村民角色的代理。
    """
    def __init__(self, agent_id: int, player_name: str):
        super().__init__(agent_id, player_name)

    def night_action(self, **kwargs):
        # 村民在夜晚没有行动
        return None
