cmake_minimum_required(VERSION 3.8)
project(wall_eb_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}

  "action/Speak.action"

  # plus tard :
  # "action/Navigate.action"
  # "srv/GenerateMessage.srv"
  # "msg/Person.msg"

)

ament_export_dependencies(rosidl_default_runtime)

ament_package()
