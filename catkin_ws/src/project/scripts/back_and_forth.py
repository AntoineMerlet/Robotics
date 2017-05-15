#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from math import pi

class BackAndForth():
    def __init__(self):
        # Init the node. Not anonymous cbecause only one 
        rospy.init_node('back_and_forth', anonymous=False)

        # When shutdown, perfoms launch the shutdown function below      
        rospy.on_shutdown(self.shutdown)
        
        # This is the publisher to the cmd_vel
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        
        # Frequency
        rate = 50
        r = rospy.Rate(rate)
        
        # Set our variables in meters and radians
        linear_speed = 0.2
        goal_distance = 1.0
        angular_speed = 1.0
        goal_angle = pi*2
        
        # Travel time estimations
        linear_duration = goal_distance / linear_speed
        angular_duration = goal_angle / angular_speed
        
        #Perfomed twice to have a back and forth
        for i in range(2):
            # Init the Twist message
            move_cmd = Twist()
            
            # Init the linear speed
            move_cmd.linear.x = linear_speed
            
            # Normalizing the travel duration according to the frequency
            ticks = int(linear_duration * rate)
            
            # Perform movement
            for t in range(ticks):
                self.cmd_vel.publish(move_cmd)
                r.sleep()
            
            # Stop the robot before the rotation
            move_cmd = Twist()
            self.cmd_vel.publish(move_cmd)
            rospy.sleep(1)
            
            
            # Init the angular speed
            move_cmd.angular.z = angular_speed

            # Normalizing the rotate duration according to the frequency
            ticks = int(goal_angle * rate)
            
            # Perform Rotation
            for t in range(ticks):           
                self.cmd_vel.publish(move_cmd)
                r.sleep()
                
            # Publish an empty message to stop the robot for a few moments before going back
            move_cmd = Twist()
            self.cmd_vel.publish(move_cmd)
            rospy.sleep(1)    
            
        # Back and forth finish, publishing empty message to stop the robot
        self.cmd_vel.publish(Twist())
        
    def shutdown(self):
        # Always stop the robot when shutting down the node.
        rospy.loginfo("Stopping the robot...")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
        BackAndForth()
    except:
        rospy.loginfo("Back-and-Forth node terminated.")

