import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from std_msgs.msg import Bool

class Rgoap(Node):
    def __init__(self):
        super().__init__('Rgoap')
        self.ttsready = self.create_subscription(
            Bool,
            "/ttsready",
            self.setttsready,
            1,
        )
        self.Play_client = ActionClient(
            self,
            Play.action,
            "play",
        )
        self.Play_client.wait_for_server()
        self.runner = Runner()
        #init state
        Condition.add(MemoryCondition(self.runner.memory, 'robot.ReadyToPlay', False))
        Condition.add(MemoryCondition(self.runner.memory, 'robot.AudioPlayed', 0))

class Playaudio(Action):
    def __init__(self):
        self.audioid = RgoapNode.memory.get_value('robot.audioid')
        Action.__init__(
            self,
            [Precondition(Condition.get('robot.ReadyToPlay'), True)],
            [Effect(Condition.get('robot.ReadyToPlay'), False),
             Effect(Condition.get("robot.AudioPlayed"), memory.get_value('robot.AudioPlayed') + 1)]
        )
        
    def run(self, next_worldstate):
        goal = Play.goal()
        goal.audio = audioid
        future = RgoapNode.speak_client.send_goal_async(goal)
        goal_handle = future
        result = goal_handle.get_result_async()

class WaitForPlaying(Action):
    def __init__(self):
        self.audioid = RgoapNode.runner.memory.get_value('robot.audioid')
        Action.__init__(
            self,
            [Precondition(Condition.get('robot.ReadyToPlay'), False)],
            [Effect(Condition.get('robot.ReadyToPlay'), True)]
        )

    def run(self, next_worldstate):
        while not RgoapNode.memory.get_value('robot.contentrequest').done():
            rclpy.spin_once(RgoapNode, timeout_sec=0.1)
        return
def main():
    global RgoapNode = rgoap() 
