from abc import *
from typing import Dict, Tuple

import json
import rospy
from std_msgs.msg import String
from .helpers import timestamp


# Base Node of ROS
class NodeBase:
    __node_name: str = None
    __publishers: Dict[str, rospy.Publisher] = {}
    __subscribers: Dict[str, rospy.Subscriber] = {}

    def __init__(self, node_name: str):
        self.__node_name = node_name
        rospy.init_node(self.node_name)

    @property
    def node_name(self) -> str:
        return self.__node_name

    def add_publisher(self,
                      topic_name: str,
                      *args, **kwargs) -> rospy.Publisher:

        # Initialize publisher
        publisher = rospy.Publisher(topic_name, *args, **kwargs)

        # Delete exist publisher
        if topic_name in self.__publishers:
            del self.__publishers[topic_name]

        # Add publisher to list
        self.__publishers[topic_name] = publisher

        return publisher

    def add_subscriber(self,
                       topic_name: str,
                       *args, **kwargs) -> rospy.Subscriber:

        # Initialize publisher
        subscriber = rospy.Subscriber(topic_name, *args, **kwargs)

        # Delete exist publisher
        if topic_name in self.__subscribers:
            del self.__subscribers[topic_name]

        # Add publisher to list
        self.__subscribers[topic_name] = subscriber

        return subscriber

    def publish(self,
                topic_name: str,
                *args, **kwargs):

        publisher = self.__publishers[topic_name]
        publisher.publish(*args, **kwargs)

    @classmethod
    def spin(cls):
        rospy.spin()


# Node of DeepTask
class DTNode(NodeBase, metaclass=ABCMeta):
    def __init__(self,
                 publish_message: str,
                 subscribe_message: str,
                 queue_size: int = 10,
                 *args, **kwargs):

        super(DTNode, self).__init__(*args, **kwargs)
        self.source_name = None
        self.publish_message = publish_message
        self.subscribe_message = subscribe_message
        self.add_publisher(publish_message, String, queue_size=queue_size)
        self.add_subscriber(subscribe_message, String, self.subscribe)

    def subscribe(self, message):
        received_message = json.loads(message.data)

        # Check message format
        if not isinstance(received_message, dict):
            return

        header = received_message['header']

        if not isinstance(header, dict) or 'target' not in header:
            return

        # Check receiver
        source = header['source']
        targets = header['target']

        if not targets:
            return

        if isinstance(targets, str):
            targets = [targets]
            header['target'] = targets

        if not self.source_name or self.source_name not in targets:
            return

        # Process received message
        rospy.loginfo(f'Received message: {received_message}')
        content_names = header['content']

        if not content_names:
            return

        if isinstance(content_names, str):
            content_names = [content_names]

        if not isinstance(content_names, list):
            return

        contents = {content_name: received_message[content_name] for content_name in content_names}
        targets, generated_content_names, generated_contents = self.generate_content(source, content_names, contents)

        # Publish message
        if targets:
            generated_message = self.generate_message(targets, generated_content_names, generated_contents)
            self.publish(self.publish_message, json.dumps(generated_message, ensure_ascii=False))
            rospy.loginfo(f'Published message: {generated_message}')

    # Generate DeepTask ROS module output message
    def generate_message(self,
                         targets: list,
                         content_names: list,
                         contents: Dict[str, dict]) -> dict:

        message = {
            'header': {
                'timestamp': timestamp(),
                'source': self.source_name,
                'target': targets,
                'content': content_names,
            }
        }

        message.update(contents)

        return message

    # Generate specific ROS module output content
    @abstractmethod
    def generate_content(self,
                         source: str,
                         content_names: list,
                         content: Dict[str, dict]) -> Tuple[list, list, Dict[str, dict]]:

        pass
