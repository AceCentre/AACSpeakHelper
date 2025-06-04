#!/usr/bin/env python3
"""
Test script to verify that multiple server instances are prevented.

This script helps test the single instance mechanism by:
1. Starting the first server instance
2. Attempting to start a second server instance
3. Verifying that the second instance is rejected

Usage:
    python test_multiple_servers.py
"""

import subprocess
import time
import sys
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_single_instance():
    """Test that only one server instance can run at a time."""
    
    print("=" * 60)
    print("Testing AACSpeakHelper Server Single Instance Mechanism")
    print("=" * 60)
    
    # Path to the server script
    server_script = "AACSpeakHelperServer.py"
    
    if not os.path.exists(server_script):
        print(f"❌ Error: {server_script} not found in current directory")
        return False
    
    print(f"✅ Found server script: {server_script}")
    
    # Start the first server instance
    print("\n1. Starting first server instance...")
    try:
        # Use uv run to start the server
        process1 = subprocess.Popen(
            ["uv", "run", "python", server_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"✅ First server started with PID: {process1.pid}")
        
        # Give it time to initialize
        time.sleep(3)
        
        # Check if the first process is still running
        if process1.poll() is not None:
            stdout, stderr = process1.communicate()
            print(f"❌ First server exited unexpectedly!")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
        
        print("✅ First server is running")
        
    except Exception as e:
        print(f"❌ Failed to start first server: {e}")
        return False
    
    # Try to start a second server instance
    print("\n2. Attempting to start second server instance...")
    try:
        process2 = subprocess.Popen(
            ["uv", "run", "python", server_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"✅ Second server process started with PID: {process2.pid}")
        
        # Wait for the second process to complete (it should exit quickly)
        stdout, stderr = process2.communicate(timeout=10)
        
        if process2.returncode == 1:
            print("✅ Second server correctly rejected (exit code 1)")
            print("✅ Single instance mechanism is working!")
            success = True
        else:
            print(f"❌ Second server exited with unexpected code: {process2.returncode}")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            success = False
            
    except subprocess.TimeoutExpired:
        print("❌ Second server did not exit within timeout - this suggests the single instance check failed")
        process2.kill()
        success = False
    except Exception as e:
        print(f"❌ Error starting second server: {e}")
        success = False
    
    # Clean up the first server
    print("\n3. Cleaning up...")
    try:
        process1.terminate()
        process1.wait(timeout=5)
        print("✅ First server terminated successfully")
    except subprocess.TimeoutExpired:
        print("⚠️  First server did not terminate gracefully, killing it")
        process1.kill()
    except Exception as e:
        print(f"⚠️  Error terminating first server: {e}")
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST PASSED: Single instance mechanism is working correctly!")
        print("   Only one server instance can run at a time.")
    else:
        print("❌ TEST FAILED: Single instance mechanism is not working properly!")
        print("   Multiple server instances may be able to run simultaneously.")
    print("=" * 60)
    
    return success

def test_client_communication():
    """Test that the client can still communicate with the server."""
    
    print("\n" + "=" * 60)
    print("Testing Client-Server Communication")
    print("=" * 60)
    
    # Start the server
    print("1. Starting server...")
    try:
        server_process = subprocess.Popen(
            ["uv", "run", "python", "AACSpeakHelperServer.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"✅ Server started with PID: {server_process.pid}")
        
        # Give it time to initialize
        time.sleep(3)
        
        # Check if the server is still running
        if server_process.poll() is not None:
            stdout, stderr = server_process.communicate()
            print(f"❌ Server exited unexpectedly!")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
        
        print("✅ Server is running")
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    # Test client communication
    print("\n2. Testing client communication...")
    try:
        client_process = subprocess.run(
            ["uv", "run", "python", "client.py", "-t", "test message", "-v"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if client_process.returncode == 0:
            print("✅ Client communication successful")
            print(f"Client output: {client_process.stdout}")
            success = True
        else:
            print(f"❌ Client communication failed (exit code: {client_process.returncode})")
            print(f"STDOUT: {client_process.stdout}")
            print(f"STDERR: {client_process.stderr}")
            success = False
            
    except subprocess.TimeoutExpired:
        print("❌ Client communication timed out")
        success = False
    except Exception as e:
        print(f"❌ Error testing client communication: {e}")
        success = False
    
    # Clean up the server
    print("\n3. Cleaning up...")
    try:
        server_process.terminate()
        server_process.wait(timeout=5)
        print("✅ Server terminated successfully")
    except subprocess.TimeoutExpired:
        print("⚠️  Server did not terminate gracefully, killing it")
        server_process.kill()
    except Exception as e:
        print(f"⚠️  Error terminating server: {e}")
    
    return success

if __name__ == "__main__":
    print("AACSpeakHelper Server Testing Script")
    print("This script tests the single instance mechanism and basic functionality")
    
    # Test single instance mechanism
    single_instance_ok = test_single_instance()
    
    # Test client communication
    communication_ok = test_client_communication()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print(f"Single Instance Test: {'✅ PASS' if single_instance_ok else '❌ FAIL'}")
    print(f"Communication Test: {'✅ PASS' if communication_ok else '❌ FAIL'}")
    
    if single_instance_ok and communication_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("The double speech issue should now be resolved.")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("The double speech issue may still occur.")
        sys.exit(1)
