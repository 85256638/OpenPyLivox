#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Livox Lidar Power Mode Test Script

This script tests the ability to switch all connected Livox lidars between:
- Normal mode (spinning)
- Power-saving mode (stopped)

Author: Assistant
Date: 2024
"""

import openpylivox as opl
import time
import sys

def test_lidar_power_modes():
    """
    Test switching all connected Livox lidars between normal and power-saving modes
    """
    print("=" * 60)
    print("Livox Lidar Power Mode Test")
    print("=" * 60)
    
    # List to store all connected sensors
    sensors = []
    connected_count = 0
    
    print("\nStep 1: Discovering and connecting to all Livox sensors...")
    print("-" * 50)
    
    # Connect to all available sensors
    while connected_count < 4:  # Try to connect to up to 4 sensors
        try:
            # Create a new sensor object
            sensor = opl.openpylivox(True)  # Show messages
            
            # Try to auto-connect with specified computer IP
            connected = sensor.auto_connect("192.168.1.33")
            
            if connected:
                sensors.append(sensor)
                connected_count += 1
                print(f"✓ Connected to sensor {connected_count}: {sensor.serialNumber()} at {sensor.connectionParameters()[1]}")
            else:
                print(f"✗ Failed to connect to sensor {connected_count + 1}")
                break
                
        except Exception as e:
            print(f"✗ Error connecting to sensor {connected_count + 1}: {str(e)}")
            break
    
    if not sensors:
        print("❌ No sensors connected. Exiting...")
        return False
    
    print(f"\nSuccessfully connected to {len(sensors)} sensor(s)")
    
    # Test sequence for each sensor
    test_sequence = [
        ("Normal Mode (Spin Up)", "spin_up"),
        ("Power-Saving Mode (Spin Down)", "spin_down"),
        ("Normal Mode (Spin Up)", "spin_up"),
        ("Power-Saving Mode (Spin Down)", "spin_down"),
        ("Normal Mode (Spin Up)", "spin_up"),
    ]
    
    print(f"\nStep 2: Testing power mode transitions for {len(sensors)} sensor(s)...")
    print("-" * 50)
    
    for test_num, (test_name, test_action) in enumerate(test_sequence, 1):
        print(f"\nTest {test_num}: {test_name}")
        print("-" * 30)
        
        success_count = 0
        error_count = 0
        
        for i, sensor in enumerate(sensors):
            try:
                sensor_ip = sensor.connectionParameters()[1]
                serial = sensor.serialNumber()
                
                print(f"  Sensor {i+1} ({serial} at {sensor_ip}): ", end="")
                
                if test_action == "spin_up":
                    sensor.lidarSpinUp()
                    print("✓ Spun up successfully")
                    success_count += 1
                    
                elif test_action == "spin_down":
                    sensor.lidarSpinDown()
                    print("✓ Spun down successfully")
                    success_count += 1
                    
                # Add a small delay between operations
                time.sleep(0.5)
                
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                error_count += 1
        
        print(f"  Summary: {success_count} success, {error_count} errors")
        
        # Add delay between test sequences
        if test_num < len(test_sequence):
            print("  Waiting 2 seconds before next test...")
            time.sleep(2)
    
    print(f"\nStep 3: Final status check...")
    print("-" * 50)
    
    # Final status check
    for i, sensor in enumerate(sensors):
        try:
            sensor_ip = sensor.connectionParameters()[1]
            serial = sensor.serialNumber()
            
            # Get lidar status codes
            status_codes = sensor.lidarStatusCodes()
            system_status = status_codes[0] if status_codes else -1
            
            status_text = "Unknown"
            if system_status == 0:
                status_text = "OK"
            elif system_status == 1:
                status_text = "Warning"
            elif system_status == 2:
                status_text = "Error"
            
            print(f"  Sensor {i+1} ({serial} at {sensor_ip}): {status_text}")
            
        except Exception as e:
            print(f"  Sensor {i+1}: Error getting status - {str(e)}")
    
    print(f"\nStep 4: Disconnecting all sensors...")
    print("-" * 50)
    
    # Disconnect all sensors
    for i, sensor in enumerate(sensors):
        try:
            sensor_ip = sensor.connectionParameters()[1]
            serial = sensor.serialNumber()
            sensor.disconnect()
            print(f"✓ Disconnected sensor {i+1} ({serial} at {sensor_ip})")
        except Exception as e:
            print(f"✗ Error disconnecting sensor {i+1}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Power Mode Test Completed!")
    print("=" * 60)
    
    return True

def main():
    """
    Main function to run the power mode test
    """
    try:
        success = test_lidar_power_modes()
        if success:
            print("✅ Test completed successfully!")
        else:
            print("❌ Test failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 