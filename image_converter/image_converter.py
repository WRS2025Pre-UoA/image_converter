import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image,CompressedImage

import cv2
from cv_bridge import CvBridge, CvBridgeError

import numpy as np

class ImageConverter(Node):

    def __init__(self):
        super().__init__('image_converter')
        self.publisher_ = self.create_publisher(Image, 'converted_qr', 10)
        self.subscription = self.create_subscription(
            CompressedImage,
            '/arm_camera/republish_node',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        try:
            np_arr = np.fromstring(msg.data, np.uint8)
            input_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        except CvBridgeError as e:
            print(e)
            return

        try:
            ros_image = self.bridge.cv2_to_imgmsg(input_image, 'rgb8')
            self.publisher_.publish(ros_image)
        except CvBridgeError as e:
            print(e)
            return


def main(args=None):
    rclpy.init(args=args)

    node = ImageConverter()

    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
