#!/usr/bin/env python3
"""
Agent Connection Tests

Verify that:
1. Connection to blender-mcp works
2. All commands are recognized
3. Commands execute properly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blender_mcp_client import (
    create_object,
    modify_object,
    delete_object,
    apply_material,
    get_scene_info,
    get_objects,
    export_scene,
    run_code,
    set_camera_view
)


def test_connection():
    """Test that we can connect to the server"""
    print("=" * 60)
    print("Test 1: Connection Test")
    print("=" * 60)
    print()
    
    # Simple ping command
    response = get_scene_info()
    
    if response:
        print(f"[PASS] Connection successful")
        print(f"Response: {response}")
        return True
    else:
        print(f"[FAIL] Cannot connect to server")
        print(f"Expected: Connection to port {os.path.dirname(os.path.dirname(os.path.__file__))}/mcp-server")
        return False


def test_create_object():
    """Test object creation"""
    print()
    print("=" * 60)
    print("Test 2: Create Object Test")
    print("=" * 60)
    print()
    
    response = create_object("cube", "test_cube")
    
    if response:
        print(f"[PASS] Object created")
        print(f"Response: {response}")
        return True
    else:
        print(f"[FAIL] Object creation failed")
        return False


def test_modify_object():
    """Test object modification"""
    print()
    print("=" * 60)
    print("Test 3: Modify Object Test")
    print("=" * 60)
    print()
    
    response = modify_object("test_cube", position=[1, 0, 0])
    
    if response:
        print(f"[PASS] Object modified")
        print(f"Response: {response}")
        return True
    else:
        print(f"[FAIL] Object modification failed")
        return False


def test_delete_object():
    """Test object deletion"""
    print()
    print("=" * 60)
    print("Test 4: Delete Object Test")
    print("=" * 60)
    print()
    
    response = delete_object("test_cube")
    
    if response:
        print(f"[PASS] Object deleted")
        print(f"Response: {response}")
        # Recreate for other tests
        create_object("cube", "test_cube")
        return True
    else:
        print(f"[FAIL] Object deletion failed")
        return False


def test_apply_material():
    """Test material application"""
    print()
    print("=" * 60)
    print("Test 5: Apply Material Test")
    print("=" * 60)
    print()
    
    response = apply_material("test_cube", "red")
    
    if response:
        print(f"[PASS] Material applied")
        print(f"Response: {response}")
        return True
    else:
        print(f"[FAIL] Material application failed")
        return False


def test_get_objects():
    """Test getting object list"""
    print()
    print("=" * 60)
    print("Test 6: Get Objects Test")
    print("=" * 60)
    print()
    
    response = get_objects()
    
    if response:
        print(f"[PASS] Objects retrieved")
        print(f"Response: {response}")
        return True
    else:
        print(f"[FAIL] Cannot get objects")
        return False


def test_set_camera_view():
    """Test setting camera view"""
    print()
    print("=" * 60)
    print("Test 7: Set Camera View Test")
    print("=" * 60)
    print()
    
    response = set_camera_view("perspective")
    
    if response:
        print(f"[PASS] Camera view set")
        print(f"Response: {response}")
        return True
    else:
        print(f"[FAIL] Cannot set camera view")
        return False


def test_run_code():
    """Test running code"""
    print()
    print("=" * 60)
    print("Test 8: Run Code Test")
    print("=" * 60)
    print()
    
    response = run_code("print('hello from mcp')")
    
    if response:
        print(f"[PASS] Code executed")
        print(f"Response: {response}")
        return True
    else:
        print(f"[FAIL] Code execution failed")
        return False


def test_export_scene():
    """Test scene export"""
    print()
    print("=" * 60)
    print("Test 9: Export Scene Test")
    print("=" * 60)
    print()
    
    # Use a temp path
    response = export_scene("glb", "/tmp/test_export")
    
    if response:
        print(f"[PASS] Scene exported")
        print(f"Response: {response}")
        return True
    else:
        print(f"[FAIL] Scene export failed")
        return False


def test_all_commands():
    """Test all commands work"""
    print()
    print("=" * 60)
    print("Test 10: All Commands Test")
    print("=" * 60)
    print()
    
    print("Testing 9 commands...")
    
    tests = [
        ("Connection", test_connection),
        ("Create Object", test_create_object),
        ("Modify Object", test_modify_object),
        ("Delete Object", test_delete_object),
        ("Apply Material", test_apply_material),
        ("Get Objects", test_get_objects),
        ("Set Camera View", test_set_camera_view),
        ("Run Code", test_run_code),
        ("Export Scene", test_export_scene),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        if test_func():
            passed += 1
        else:
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed}/{passed+failed} passed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    all_passed = test_all_commands()
    
    if all_passed:
        print()
        print("All tests passed! ✓")
        sys.exit(0)
    else:
        print()
        print("Some tests failed! ✗")
        sys.exit(1)