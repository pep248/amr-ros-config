from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
from xacro import process_file

def generate_launch_description():
    # Define valid robot models
    
    model = 'pioneer3dx'
    
    VALID_ROBOT_MODELS = [
        'pioneer-lx',
        'pioneer3at',
        'pioneer3dx',
        'powerbot',
        'seekurjr',
        'terabot-arm'
    ]

    # Function to get the xacro file path based on robot model
        
    xacro_path = os.path.join(
            get_package_share_directory('amr-ros-config'),
            'urdf',
            f'{model}.urdf.xacro'
        )

    robot_description_content = process_file(xacro_path).toxml()
    
    # Declare the robot description argument, using dynamic substitution
    declare_robot_description = DeclareLaunchArgument(
        'robot_description',
        default_value=robot_description_content,
        description='Robot description in URDF format',
    )

    return LaunchDescription([
        declare_robot_description,

        # Load and visualize the robot URDF in RViz
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': LaunchConfiguration('robot_description')}],
        ),

        # Launch RViz with a pre-configured config file if available
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', os.path.join(
                get_package_share_directory('amr-ros-config'),
                'rviz',  # Folder containing RViz config (optional)
                'view_robot.rviz')]  # Optional pre-saved RViz config file
        ),

        # Joint State Publisher GUI to add sliders for joint movement
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen',
        ),
    ])
