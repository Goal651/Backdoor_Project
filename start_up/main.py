import winreg
import sys
import os

def add_to_user_startup():
    """Add to startup for current user only - NO ADMIN NEEDED!"""
    try:
        # Open current user's registry (always writable by the user)
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        # Set the value
        python_exe = sys.executable
        script_path = os.path.abspath(__file__)
        command = f'"{python_exe}" "{script_path}"'
        
        winreg.SetValueEx(key, "MyApp Wow", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        
        print("✓ Successfully added to startup (your account only)")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def remove_from_user_startup():
    """Remove from startup - also NO ADMIN NEEDED!"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        winreg.DeleteValue(key, "MyApp")
        winreg.CloseKey(key)
        
        print("✓ Removed from startup")
        return True
        
    except FileNotFoundError:
        print("Not in startup")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Test it
if __name__ == "__main__":
    print("Testing startup registration...")
    print("(No admin rights needed!)")
    print("-" * 40)
    
    # Add to startup
    if add_to_user_startup():
        print("\nCheck your startup programs:")
        print("1. Press Ctrl+Shift+Esc (Task Manager)")
        print("2. Go to 'Startup apps' tab")
        print("3. Look for 'MyApp'")
    
    # Uncomment to remove:
    # remove_from_user_startup()