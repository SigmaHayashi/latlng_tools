
from os import name
from launch import LaunchDescription
from launch_ros.actions import Node

offset_param_file = '/home/common/ros2_ws/src/latlng_tools/latlng_tools/param/gnss_offset.yaml'

'''
origin_lat = 33.595542
origin_lng = 130.219007
angle_offset = 42.85
scale_offset = 1.0
'''

fix_value = 3
float_value = 2

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='latlng_tools',
            executable='latlng2pos',
            output='screen',
            emulate_tty=True,
            parameters=[
                offset_param_file,
                {
                    'map_frame_name': 'map',
                    'odom_frame_name': 'odom',

                    'visualization_marker': False,
                    'marker_topic_name': 'gnss_position_marker',

                    'fix_value': fix_value,
                    'float_value': float_value,

                    #'origin_lat': origin_lat,
                    #'origin_lng': origin_lng,
                    #'angle_offset': angle_offset,
                    #'scale_offset': scale_offset,

                    'solutions_flag': 'all',
                    
                    'nav_sat_fix_topic_name': 'fix',
                    'odom_topic_name': 'odometry/gnss'
                }
            ]
        ),
        Node(
            package='latlng_tools',
            executable='fix2marker',
            output='screen',
            emulate_tty=True,
            parameters=[{
                'sub_topic_name': 'fix',
                'pub_topic_name': 'fix_marker',

                'marker_keep': 50,
                'marker_color_rgb': [0.2, 1.0, 0.2],
                'marker_scale': [0.3, 0.3, 0.3],

                'log_print': False
            }]
        ),
        Node(
            package='latlng_tools',
            executable='pos2latlng',
            output='screen',
            emulate_tty=True,
            parameters=[
                offset_param_file,
                {
                    #'origin_lat': origin_lat,
                    #'origin_lng': origin_lng,
                    #'angle_offset': angle_offset,
                    #'scale_offset': scale_offset,

                    'pub_topic_name': 'filtered_fix',
                    'sub_topic_name': 'odometry/filtered',
                }
            ]
        ),
        Node(
            package='latlng_tools',
            executable='fix2marker',
            name='filteredfix2marker',
            output='screen',
            emulate_tty=True,
            parameters=[{
                'sub_topic_name': 'filtered_fix',
                'pub_topic_name': 'filtered_fix_marker',

                'marker_keep': 1000,
                'marker_color_rgb': [1.0, 0.0, 1.0],
                'marker_scale': [0.3, 0.3, 0.3],

                'log_print': False
            }]
        )
    ])
