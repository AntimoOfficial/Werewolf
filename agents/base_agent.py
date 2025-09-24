from zhipuai import ZhipuAI
from config import API_KEY

class BaseAgent:
    """
    AI 代理的基类，封装了与 LLM 的交互和通用属性。
    """
    def __init__(self, agent_id: int, player_name: str):
        """
        初始化一个 AI 代理。

        :param agent_id: 代理的唯一标识符。
        :param player_name: 玩家名称 (例如, '艾拉')。
        """
        self.agent_id = agent_id
        self.role = self.__class__.__name__.replace('Agent', '').lower()
        self.player_name = player_name
        self.status = 'alive'  # 'alive' or 'dead'
        self.private_knowledge = [] # 用于存储私有信息
        self.client = None
        if API_KEY:
            self.client = ZhipuAI(api_key=API_KEY)
        else:
            print(f"警告: 未找到 API 密钥，代理 {self.player_name} 将无法与 LLM 交互。")

    def receive_info(self, info: str):
        """接收来自 GameMaster 的私有信息并存入记忆。"""
        self.private_knowledge.append(info)

    def get_prompt(self, context: str) -> list:
        """
        根据上下文生成发送给 LLM 的提示信息。
        """
        # 构建包含私有知识的系统提示
        system_prompt = f"你是一个狼人杀游戏中的玩家，你的名字是{self.player_name}，你的角色是{self.role}。"
        if self.private_knowledge:
            system_prompt += "\n你掌握的私有信息如下：\n" + "\n".join(self.private_knowledge)
        system_prompt += f"\n请根据你的角色和当前情况，以 {self.player_name} 的身份进行回应。你的发言应该简短、符合人设。"

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context}
        ]

    def think(self, context: str) -> str:
        """
        调用 LLM 进行思考并返回响应。
        """
        if not self.client:
            return "(由于没有API密钥，无法思考)"

        try:
            response = self.client.chat.completions.create(
                model="glm-4",  # 使用智谱的 glm-4 模型
                messages=self.get_prompt(context),
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"错误: 调用 LLM API 时发生错误: {e}")
            return "(思考时出现错误)"

    def discuss(self, history: list) -> str:
        """
        在白天阶段进行发言。
        """
        context = "现在是白天讨论环节。请根据以下历史发言，并结合你的角色和私有信息，进行你的发言。\n历史发言:\n" + "\n".join(history)
        return self.think(context)

    def vote(self, targets: list) -> str:
        """
        在白天阶段进行投票。
        """
        context = f"现在是投票环节。请从以下玩家中投票选择一人出局: {', '.join(targets)}。请严格按照 '玩家名 | 你的理由' 的格式返回你的选择和理由。"
        choice = self.think(context)
        return choice.strip()

    def night_action(self, **kwargs):
        """
        执行夜晚行动。具体实现由子类定义。
        """
        raise NotImplementedError("子类必须实现 night_action 方法")