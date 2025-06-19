#!/usr/bin/env python3
import sys
import math
import os
import rosnode
import rospy

#from SafetyHandler import CheckSafety
from control_msgs.msg import FollowJointTrajectoryActionGoal
from pan_tilt_msgs.msg import PanTiltCmdDeg

class HeadControl:
    def __init__(self):
        self.head_control_cmd_publisher = rospy.Publisher('pan_tilt_cmd_deg',PanTiltCmdDeg,queue_size=0)

    def data_callback(self,msg):
        positions = msg.goal.trajectory.points[0].positions
        ## Positions Contains the Joint Values for the joints in order
        ##  joint_names:
        ##    - head_pan     joint[0]
        ##    - head_tilt    joint[1]

        # Creating Head Control Command Message
        panTiltCmd = PanTiltCmdDeg()
        panTiltCmd.yaw = (float)((int)((positions[0] * 180) / math.pi))
        panTiltCmd.pitch = (float)((int)((positions[1] * 180) / math.pi))
        panTiltCmd.speed = 30   ## In degrees/s need to be between 1-30 Degrees /sec
        self.head_control_cmd_publisher.publish(panTiltCmd)


if __name__ == '__main__':
    #Creating the ros node and service client
    rospy.init_node("head_controller")

    # Initialize the Class
    head_control = HeadControl()
    rospy.Subscriber("head/follow_joint_trajectory/goal", FollowJointTrajectoryActionGoal, head_control.data_callback, queue_size=1)
    rospy.spin()
