from openpylivox.openpylivox import openpylivox
import time

def set_all_lidars_normal():
    """设置所有LiDAR设备为正常模式"""
    
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
        # 5. 设置所有雷达为"正常模式"
        print("\n正在设置所有雷达为正常模式...")
        for i, controller in enumerate(lidar_controllers):
            print(f"  设置LiDAR {i+1} ({controller._sensorIP}) 为正常模式...")
            controller.lidarSpinUp()
            time.sleep(0.5)  # 每个设备之间稍作延迟
        
        print("等待模式切换生效...")
        time.sleep(3)  # 等待所有设备模式切换完成
        
        print("所有LiDAR设备已成功设置为正常模式！")
        
    finally:
        # 6. 断开所有连接
        print("\n断开所有连接...")
        for i, controller in enumerate(lidar_controllers):
            print(f"  断开LiDAR {i+1} ({controller._sensorIP})...")
            controller.disconnect()
    
    print("操作完成。")

if __name__ == "__main__":
    set_all_lidars_normal() 