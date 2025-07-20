from openpylivox.openpylivox import openpylivox
import time

def control_all_lidars():
    # 1. 创建主控制器实例
    main_controller = openpylivox(showMessages=True)
    
    # 2. 发现所有雷达设备
    print("正在发现所有LiDAR设备...")
    main_controller.discover(manualComputerIP="192.168.1.33")
    
    # 3. 搜索所有传感器
    lidarSensorIPs, serialNums, ipRangeCodes, sensorTypes = main_controller._searchForSensors(False)
    
    if not lidarSensorIPs:
        print("未发现任何LiDAR设备！")
        return
    
    print(f"发现 {len(lidarSensorIPs)} 个LiDAR设备:")
    for i, ip in enumerate(lidarSensorIPs):
        print(f"  {i+1}. IP: {ip}, 序列号: {serialNums[i]}, 类型: {sensorTypes[i]}")
    
    # 4. 为每个LiDAR创建独立的控制器
    lidar_controllers = []
    
    for i, sensor_ip in enumerate(lidarSensorIPs):
        print(f"\n正在连接LiDAR {i+1}: {sensor_ip}")
        controller = openpylivox(showMessages=True)
        success = controller.connect("192.168.1.33", sensor_ip, 0, 0, 0)
        if success:
            lidar_controllers.append(controller)
            print(f"成功连接到 {sensor_ip}")
        else:
            print(f"连接失败 {sensor_ip}")
    
    if not lidar_controllers:
        print("没有成功连接任何LiDAR设备！")
        return
    
    print(f"\n成功连接 {len(lidar_controllers)} 个LiDAR设备")
    
    try:
        # 5. 切换所有雷达为"正常模式"
        print("\n切换所有雷达为正常模式...")
        for i, controller in enumerate(lidar_controllers):
            print(f"  切换LiDAR {i+1} ({controller._sensorIP}) 为正常模式...")
            controller.lidarSpinUp()
time.sleep(2)  # 等待生效

        # 6. 切换所有雷达为"省电模式"
        print("\n切换所有雷达为省电模式...")
        for i, controller in enumerate(lidar_controllers):
            print(f"  切换LiDAR {i+1} ({controller._sensorIP}) 为省电模式...")
            controller.lidarSpinDown()
time.sleep(2)  # 等待生效

        # 7. 再切回"正常模式"
        print("\n再次切换所有雷达为正常模式...")
        for i, controller in enumerate(lidar_controllers):
            print(f"  切换LiDAR {i+1} ({controller._sensorIP}) 为正常模式...")
            controller.lidarSpinUp()
time.sleep(2)

    finally:
        # 8. 断开所有连接
        print("\n断开所有连接...")
        for i, controller in enumerate(lidar_controllers):
            print(f"  断开LiDAR {i+1} ({controller._sensorIP})...")
            controller.disconnect()
    
print("全部完成。")

if __name__ == "__main__":
    control_all_lidars()