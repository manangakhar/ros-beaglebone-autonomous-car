#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/classification.hpp>

using namespace std;

//message sending
int main(int argc, char **argv)
{
  ros::init(argc, argv, "gpstalker");
  ros::NodeHandle n;

  ros::Publisher chatter_pub = n.advertise<std_msgs::String>("MyGPSData", 1000);
  ros::Rate loop_rate(20);

	ROS_INFO("%s", "reading starts");
	//READING FROM FILE
	ifstream fin("/home/manan/ros_ws/src/assignment1gps/src/GPS_data.txt"); //input file
	string line;
	std::vector<std::string> tokens;
	std::vector<std::vector<std::string> > dataset;
	ROS_INFO("%s", "file starts");
	while(!fin.eof())
	{
		getline(fin,line); //getline(file,str_to_put_into)
		//ROS_INFO("%s", line.c_str());
		boost::algorithm::split(tokens, line, boost::is_any_of(",")); //split into,split what,delimeter
		dataset.push_back(tokens); //add to vector(arraylist in java)
	}
	fin.close();
	ROS_INFO("%s", "file closed");
	std::vector<string> coordinates;
	for(int i=0;i<dataset.size();i++)
	{
		if(strcmp(dataset[i][0].c_str(),"$GPGGA")) //if not GPGGA, ignore
			continue;
		if(atoi(dataset[i][6].c_str())!=1) //if fix!=1, ignore
			continue;
		//assuming GPGGA and GPS fix
		coordinates.push_back(dataset[i][2]+","+dataset[i][4]);
	}
	//READNIG FROM FILE ENDS
	ROS_INFO("%s", "reading ends");

  int count = 0;
  while (ros::ok())
  {
    std_msgs::String msg;
    std::stringstream ss;
    if(count<coordinates.size())
	    ss<<coordinates[count].c_str();//ss << "hello world " << count;
    msg.data = ss.str();

    ROS_INFO("%s   %d", msg.data.c_str(),count);
    //ROS_INFO("%d", count);
		
		if(count<coordinates.size())
	    chatter_pub.publish(msg);
	   else
	   	loop_rate=2;

    ros::spinOnce();

    loop_rate.sleep();

    ++count;
  }

  return 0;
}
