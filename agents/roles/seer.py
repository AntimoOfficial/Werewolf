from ..base_agent import BaseAgent

class SeerAgent(BaseAgent):
    """
    预言家角色的代理。
    """
    def __init__(self, agent_id: int, player_name: str):
        super().__init__(agent_id, player_name)

    def night_action(self, targets: list, **kwargs) -> str:
        """
        预言家选择一名玩家进行查验。
        :param targets: 可查验的玩家列表。
        :return: 选择查验的玩家名字。
        """
        context = f"现在是你的行动回合，你可以查验一名玩家的身份。请从以下玩家中选择一位进行查验：{', '.join(targets)}。请直接返回你选择的玩家名字。"
        choice = self.think(context)
        # TODO: 需要增加从LLM返回的自然语言中解析出玩家名字的逻辑
        return choice.strip()
