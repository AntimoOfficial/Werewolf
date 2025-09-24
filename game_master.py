import random
from typing import List
from game_state import GameState
# from agents.base_agent import BaseAgent
# from agents.roles import * # 未来将用于创建不同角色的实例

class GameMaster:
    """
    游戏的主控制器，负责驱动游戏流程、分发信息和执行规则。
    """
    def __init__(self, player_names: List[str]):
        self.game_state = self._initialize_game(player_names)

    def _initialize_game(self, player_names: List[str]) -> GameState:
        """初始化游戏状态，包括创建玩家和分配角色。"""
        game_state = GameState()
        
        # TODO: 实现更复杂的角色分配逻辑
        roles = ['werewolf', 'werewolf', 'seer', 'witch', 'villager', 'villager']
        random.shuffle(roles)

        print("--- 游戏设置 ---")
        # 动态导入所有角色类
        from agents.base_agent import BaseAgent
        from agents.roles import villager, werewolf, seer, witch # noqa

        role_classes = {
            'villager': villager.VillagerAgent,
            'werewolf': werewolf.WerewolfAgent,
            'seer': seer.SeerAgent,
            'witch': witch.WitchAgent,
        }

        for i, name in enumerate(player_names):
            role_name = roles.pop() if roles else 'villager'
            agent_class = role_classes.get(role_name, villager.VillagerAgent)
            agent = agent_class(agent_id=i, player_name=name)
            game_state.players.append(agent)
        
        print(f"创建了 {len(player_names)} 位玩家。角色分配已完成。")
        print("--- 角色揭示 (仅主持人可见) ---")
        for p in game_state.players:
            print(f"{p.player_name}: {p.role}")
        print("---------------------------------")
        
        return game_state

    def wait_for_host(self, message: str = ""):
        """
        暂停游戏，等待主持人（观察者）按键继续。
        """
        prompt = f"{message}\n" if message else ""
        input(f"\n>>> 主持人，{prompt}请按 Enter 键继续... <<<")

    def run_game(self):
        """
        主游戏循环。
        """
        self.game_state.add_history("游戏开始！")
        self.wait_for_host("即将进入第一个夜晚。")

        while not self.is_game_over():
            self.game_state.day_number += 1
            self.game_state.add_history(f"\n{'='*15} 第 {self.game_state.day_number} 天 {'='*15}")

            self.run_night_phase()
            self.run_day_phase()

        self.announce_winner()

    def run_night_phase(self):
        """
        执行夜晚阶段的逻辑。
        """
        self.game_state.game_phase = 'NIGHT'
        self.game_state.add_history("\n--- 夜晚来临，请闭眼 ---")

        # 1. 狼人行动 (TODO)
        # self.game_state.add_history("\n- 狼人请睁眼，商量要击杀的目标。")

        # 2. 预言家行动
        self.game_state.add_history("\n- 预言家请睁眼，选择你要查验的玩家。")
        seers = [p for p in self.game_state.get_living_players() if p.role == 'seer']
        if seers:
            seer = seers[0]
            targets = [p.player_name for p in self.game_state.get_living_players() if p.player_name != seer.player_name]
            
            # 记录输入
            self.game_state.add_history(f"  [输入] 预言家 {seer.player_name} 可查验的玩家列表: {targets}")
            
            # 获取预言家决策
            choice = seer.night_action(targets=targets)

            # 记录输出
            self.game_state.add_history(f"  [输出] 预言家 {seer.player_name} 决定查验: {choice}")

            # 执行查验并告知结果 (TODO: 将结果作为私有信息发给预言家)
            target_player = self.game_state.get_player_by_name(choice)
            if target_player:
                identity = 'werewolf' if target_player.role == 'werewolf' else 'good'
                result_info = f"{target_player.player_name} 的身份是: {identity}。"
                # 告诉主持人结果
                self.game_state.add_history(f"  [结果] {result_info}")
                # 把结果作为私有信息告诉预言家
                seer.receive_info(f"你昨晚查验了 {result_info}")

        # 3. 女巫行动 (TODO)
        # self.game_state.add_history("\n- 女巫请睁眼。")

        self.game_state.add_history("\n--- 天亮了 ---")
        # TODO: 处理夜晚的死亡事件

    def run_day_phase(self):
        """
        执行白天阶段的逻辑。
        """
        living_players = self.game_state.get_living_players()
        if not living_players:
            return

        self.game_state.game_phase = 'DAY_DISCUSSION'
        self.game_state.add_history("\n--- 白天讨论阶段 ---")
        # TODO: 依次调用每个存活玩家的 discuss() 方法

        self.wait_for_host("讨论已结束，即将进入投票阶段。")

        self.game_state.game_phase = 'VOTING'
        self.game_state.add_history("\n--- 投票放逐阶段 ---")
        
        votes = {}
        voter_list = [p.player_name for p in living_players]
        for voter in living_players:
            targets = [p.player_name for p in living_players if p.player_name != voter.player_name]
            raw_choice = voter.vote(targets)
            
            # 解析 AI 的输出
            try:
                target_name = raw_choice.split('|')[0].strip()
                # 确保 AI 的选择是有效的目标
                if target_name not in targets:
                    target_name = random.choice(targets) # 如果无效，则随机选择一个
            except:
                # 如果格式不正确，则随机选择一个目标作为后备
                target_name = random.choice(targets)

            votes[voter.player_name] = target_name

        self.game_state.add_history("\n--- 投票记录 (仅主持人可见) ---")
        vote_counts = {}
        for voter_name, target_name in votes.items():
            self.game_state.add_history(f"  {voter_name} 投给了 {target_name}")
            vote_counts[target_name] = vote_counts.get(target_name, 0) + 1
        
        if not vote_counts:
            self.game_state.add_history("无人投票，无人出局。")
        else:
            # 找到最高票数的玩家
            max_votes = max(vote_counts.values())
            eliminated_players = [p for p, v in vote_counts.items() if v == max_votes]
            # 如果平票，则无人出局 (简化规则)
            if len(eliminated_players) == 1:
                eliminated_player_name = eliminated_players[0]
                self.game_state.add_history(f"\n投票结果: {eliminated_player_name} 被放逐出局。")
                eliminated_player = self.game_state.get_player_by_name(eliminated_player_name)
                if eliminated_player:
                    eliminated_player.status = 'dead'
            else:
                self.game_state.add_history("\n投票结果: 平票，无人出局。")

        self.wait_for_host("投票已结束，即将进入下一个夜晚。")

    def is_game_over(self) -> bool:
        """检查游戏是否结束。"""
        # TODO: 实现游戏结束的判断逻辑 (例如, 狼人数量 >= 好人数量)
        return self.game_state.day_number >= 3 # 暂时以3天作为游戏结束条件

    def announce_winner(self):
        """宣布游戏胜利方。"""
        self.game_state.game_phase = 'ENDED'
        self.game_state.add_history("\n--- 游戏结束 ---")
        # TODO: 实现胜利宣告逻辑
        self.game_state.add_history("（暂未实现胜利宣告逻辑）")
