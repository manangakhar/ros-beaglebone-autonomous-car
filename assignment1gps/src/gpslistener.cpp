#include "ros/ros.h"
#include <visualization_msgs/Marker.h>
#include "std_msgs/String.h"

float count2;
void chatterCallback(const std_msgs::String::ConstPtr& msg)
{
  ROS_INFO("I heard: [%s] %f", msg->data.c_str(),count2);
  ros::NodeHandle n;
  ros::Publisher marker_pub = n.advertise<visualization_msgs::Marker>("visualization_marker", 1);
  uint32_t shape = visualization_msgs::Marker::CUBE;
  
  visualization_msgs::Marker marker;
  marker.header.frame_id = "/my_frame";
  marker.header.stamp = ros::Time::now();

  marker.ns = "gps_cube";
  marker.id = count2*20;//0;

  marker.type = shape;

  marker.action = visualization_msgs::Marker::ADD;

	//relative
  marker.pose.position.x = count2;//0;
  marker.pose.position.y = 0;
  marker.pose.position.z = 0;
  marker.pose.orientation.x = 0.0;
  marker.pose.orientation.y = 0.0;
  marker.pose.orientation.z = 0.0;
  marker.pose.orientation.w = 1.0;

  marker.scale.x = .1; //1 m
  marker.scale.y = .1;
  marker.scale.z = .1;

  marker.color.r = 0.0f;
  marker.color.g = 1.0f;
  marker.color.b = 0.0f;
  marker.color.a = 1.0; //should be non zero (obvio)

  marker.lifetime = ros::Duration();

  // Publish the marker
  marker_pub.publish(marker);
  count2+=0.05;
}

int main(int argc, char **argv)
{
	//ros::Rate loop_rate(20);
	count2=0;
  ros::init(argc, argv, "gpslistener");
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("MyGPSData", 1000, chatterCallback);
  
  ros::Publisher marker_pub = n.advertise<visualization_msgs::Marker>("visualization_marker", 1);
  while (marker_pub.getNumSubscribers() < 1)
  {
    if (!ros::ok())
      return 0;
    ROS_WARN_ONCE("Please create a subscriber to the marker");
    sleep(0.1);
  }
	ROS_INFO("subscriber created");
  ros::spin();

  return 0;
}
