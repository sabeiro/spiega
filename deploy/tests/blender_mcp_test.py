#!/usr/bin/env python3
"""Simple Blender MCP Test"""

import socket
import json

CONFIG = {
    'host': '127.0.0.1',
    'port': 9876,
    'timeout': 5
}

def test_connection():
    """Test connection to server"""
    print("=" * 60)
    print("Blender MCP Server Test")
    print("=" * 60)
    print()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((CONFIG['host'], CONFIG['port']))
        print("[PASS] Connection successful!")
        sock.close()
        return True
    except Exception as e:
        print(f"[FAIL] {e}")
        return False

def test_get_scene_info():
    """Test get_scene_info command"""
    print()
    print("Test: Get Scene Info")
    print("-" * 40)
    
    test = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_scene_info"
    }
    
    try:
        conn = socket.create_connection((CONFIG['host'], CONFIG['port']))
        msg = json.dumps(test).encode('utf-8')
        conn.send(len(msg).to_bytes(4, 'big'))
        conn.send(msg)
        conn.close()
        print("[PASS] Scene info requested")
        return True
    except Exception as e:
        print(f"[FAIL] {e}")
        return False

def test_create_object():
    """Test create_object command"""
    print()
    print("Test: Create Object")
    print("-" * 40)
    
    test = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "create_object",
        "params": {
            "obj_type": "cube",
            "name": "test_cube",
            "position": [0, 0, 0]
        }
    }
    
    try:
        conn = socket.create_connection((CONFIG['host'], CONFIG['port']))
        msg = json.dumps(test).encode('utf-8')
        conn.send(len(msg).to_bytes(4, 'big'))
        conn.send(msg)
        conn.close()
        print("[PASS] Object creation requested")
        return True
    except Exception as e:
        print(f"[FAIL] {e}")
        return False

if __name__ == "__main__":
    results = []
    results.append(("Connection Test", test_connection()))
    results.append(("Get Scene Info Test", test_get_scene_info()))
    results.append(("Create Object Test", test_create_object()))
    
    print()
    print("=" * 60)
    print("Results:")
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: {status}")
    
    success_count = sum(1 for _, p in results if p)
    print(f"  {success_count}/{len(results)} tests passed")
    print("=" * 60)