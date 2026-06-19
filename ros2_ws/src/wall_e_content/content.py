import rclpy
from rclpy.node import Node
Class Content(Node):
    def __init__(self):
        super().__init__('Content')

        self.askllm = self.create_service(
            askllm,
            'askllm',
            self.askllm
        )
        
        
