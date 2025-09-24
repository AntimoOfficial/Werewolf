from ..base_agent import BaseAgent

class WitchAgent(BaseAgent):
    """
    女巫角色的代理。
    """
    def __init__(self, agent_id: int, player_name: str):
        super().__init__(agent_id, player_name)
        self.has_antidote = True
        self.has_poison = True

    def night_action(self, **kwargs):
        # TODO: 实现女巫用药逻辑
        return None
