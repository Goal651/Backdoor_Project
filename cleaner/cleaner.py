#!/usr/bin/env python3
"""
Cleaner Application - Removes persistence features
Place in: backdoor-snake-game/cleaner/cleaner.py
Run: python cleaner.py
"""

import os
import sys
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path

class CleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Cleaner - Remove Persistence")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Set icon if exists
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        self.setup_ui()
        self.detect_persistence()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(
            self.root,
            text="System Persistence Cleaner",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=20)
        
        # Description
        desc_label = tk.Label(
            self.root,
            text="This tool will remove all persistence mechanisms\n"
                 "added by applications. Use this to clean your system.",
            font=("Arial", 10),
            fg="gray"
        )
        desc_label.pack(pady=10)
        
        # Warning
        warning_label = tk.Label(
            self.root,
            text="⚠️ WARNING: This will remove startup entries ⚠️",
            font=("Arial", 10, "bold"),
            fg="red"
        )
        warning_label.pack(pady=5)
        
        # Detected items frame
        items_frame = tk.Frame(self.root)
        items_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        items_label = tk.Label(
            items_frame,
            text="Detected Persistence Items:",
            font=("Arial", 11, "bold")
        )
        items_label.pack(anchor="w")
        
        # Listbox for detected items with scrollbar
        list_frame = tk.Frame(items_frame)
        list_frame.pack(fill="both", expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.items_listbox = tk.Listbox(
            list_frame,
            height=8,
            selectmode=tk.MULTIPLE,
            yscrollcommand=scrollbar.set,
            font=("Arial", 9)
        )
        self.items_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        
        scrollbar.config(command=self.items_listbox.yview)
        
        # Buttons frame
        button_frame = tk.Frame(items_frame)
        button_frame.pack(fill="x", pady=10)
        
        select_all_btn = tk.Button(
            button_frame,
            text="Select All",
            command=self.select_all,
            bg="blue",
            fg="white"
        )
        select_all_btn.pack(side=tk.LEFT, padx=5)
        
        deselect_all_btn = tk.Button(
            button_frame,
            text="Deselect All",
            command=self.deselect_all
        )
        deselect_all_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(
            button_frame,
            text="Refresh",
            command=self.refresh
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Clean button
        self.clean_btn = tk.Button(
            self.root,
            text="Remove Selected Items",
            command=self.clean_selected,
            bg="#ff6b6b",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            width=20
        )
        self.clean_btn.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 9)
        )
        self.status_label.pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate',
            length=400
        )
    
    def detect_persistence(self):
        """Detect persistence items"""
        self.items = []
        
        if platform.system() == "Windows":
            self.detect_windows_persistence()
        else:
            self.detect_linux_persistence()
        
        # Update listbox
        self.items_listbox.delete(0, tk.END)
        for item in self.items:
            self.items_listbox.insert(tk.END, item['description'])
        
        if self.items:
            self.clean_btn.config(state="normal")
            self.status_label.config(
                text=f"✅ Found {len(self.items)} persistence item(s)",
                fg="green"
            )
            # Select all by default
            self.select_all()
        else:
            self.clean_btn.config(state="disabled")
            self.status_label.config(
                text="✅ No persistence items found - System is clean",
                fg="green"
            )
    
    def detect_windows_persistence(self):
        """Detect Windows registry entries"""
        try:
            import winreg
            
            # Check Run registry key
            key_paths = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run")
            ]
            
            for hkey, subkey in key_paths:
                try:
                    with winreg.OpenKey(hkey, subkey, 0, winreg.KEY_READ) as regkey:
                        i = 0
                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(regkey, i)
                                # Look for suspicious names
                                suspicious = any(x in name.lower() for x in 
                                    ['windowsupdate', 'systemhelper', 'snake', 'game', 'helper'])
                                if suspicious or 'python' in value.lower():
                                    self.items.append({
                                        'type': 'registry',
                                        'hkey': hkey,
                                        'subkey': subkey,
                                        'name': name,
                                        'value': value,
                                        'description': f"Registry: {name} = {value[:50]}..."
                                    })
                                i += 1
                            except WindowsError:
                                break
                except:
                    pass
            
            # Check startup folder
            startup_folders = [
                os.path.join(os.getenv('APPDATA', ''), r'Microsoft\Windows\Start Menu\Programs\Startup'),
                os.path.join(os.getenv('PROGRAMDATA', ''), r'Microsoft\Windows\Start Menu\Programs\Startup')
            ]
            
            for folder in startup_folders:
                if os.path.exists(folder):
                    for file in os.listdir(folder):
                        if any(x in file.lower() for x in ['system', 'helper', 'update', 'snake']):
                            self.items.append({
                                'type': 'startup_file',
                                'path': os.path.join(folder, file),
                                'description': f"Startup File: {file}"
                            })
        
        except Exception as e:
            print(f"Error detecting Windows persistence: {e}")
    
    def detect_linux_persistence(self):
        """Detect Linux persistence"""
        # Check autostart directory
        autostart_dirs = [
            os.path.join(str(Path.home()), ".config", "autostart"),
            "/etc/xdg/autostart"
        ]
        
        for autostart_dir in autostart_dirs:
            if os.path.exists(autostart_dir):
                for file in os.listdir(autostart_dir):
                    if any(x in file.lower() for x in ['system', 'helper', 'snake']):
                        self.items.append({
                            'type': 'autostart',
                            'path': os.path.join(autostart_dir, file),
                            'description': f"Autostart: {file}"
                        })
        
        # Check crontab
        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout:
                lines = result.stdout.split('\n')
                for i, line in enumerate(lines):
                    if any(x in line.lower() for x in ['python', 'snake', 'helper']):
                        self.items.append({
                            'type': 'crontab',
                            'line': line,
                            'description': f"Crontab Line {i+1}: {line[:50]}..."
                        })
        except:
            pass
    
    def select_all(self):
        """Select all items in listbox"""
        self.items_listbox.selection_set(0, tk.END)
    
    def deselect_all(self):
        """Deselect all items"""
        self.items_listbox.selection_clear(0, tk.END)
    
    def refresh(self):
        """Refresh detection"""
        self.detect_persistence()
    
    def clean_selected(self):
        """Remove selected persistence items"""
        selected_indices = self.items_listbox.curselection()
        
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select items to remove.")
            return
        
        result = messagebox.askyesno(
            "Confirm Removal",
            f"Are you sure you want to remove {len(selected_indices)} selected item(s)?\n\n"
            "This action cannot be undone automatically."
        )
        
        if not result:
            return
        
        # Start progress bar
        self.progress.pack(pady=10)
        self.progress.start()
        self.clean_btn.config(state="disabled")
        self.root.update()
        
        # Remove items
        removed = 0
        failed = 0
        
        for idx in selected_indices:
            item = self.items[idx]
            try:
                if platform.system() == "Windows":
                    if item['type'] == 'registry':
                        self.remove_windows_registry(item['hkey'], item['subkey'], item['name'])
                        removed += 1
                    elif item['type'] == 'startup_file':
                        os.remove(item['path'])
                        removed += 1
                else:
                    if item['type'] == 'autostart':
                        os.remove(item['path'])
                        removed += 1
                    elif item['type'] == 'crontab':
                        self.remove_crontab(item['line'])
                        removed += 1
            except Exception as e:
                failed += 1
                print(f"Failed to remove: {e}")
        
        # Stop progress bar
        self.progress.stop()
        self.progress.pack_forget()
        
        # Show result
        messagebox.showinfo(
            "Cleanup Complete",
            f"✅ Successfully removed: {removed}\n"
            f"❌ Failed to remove: {failed}\n\n"
            "Some items may require administrator privileges."
        )
        
        # Refresh detection
        self.refresh()
    
    def remove_windows_registry(self, hkey, subkey, name):
        """Remove Windows registry entry"""
        try:
            import winreg
            with winreg.OpenKey(hkey, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
                winreg.DeleteValue(regkey, name)
        except Exception as e:
            raise e
    
    def remove_crontab(self, line):
        """Remove line from crontab"""
        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                lines = [l for l in lines if l != line]
                temp_cron = '\n'.join(lines)
                subprocess.run(['crontab', '-'], input=temp_cron, text=True)
        except Exception as e:
            raise e

def main():
    root = tk.Tk()
    app = CleanerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()