import tkinter as tk
from tkinter import ttk
import os
import threading
import time

class BattleFundHUD:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Battle Fund HUD")
        
        # Configure window properties
        self.root.attributes('-topmost', True)  # Stay on top
        self.root.attributes('-alpha', 0.9)     # Slight transparency
        self.root.resizable(False, False)       # Fixed size
        
        # Position on the left side of the screen
        self.root.geometry("250x150+50+100")
        
        # Configure style
        self.root.configure(bg='#2b2b2b')
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg='#2b2b2b', padx=10, pady=10)
        main_frame.pack(fill='both', expand=True)
        
        # Title label
        title_label = tk.Label(
            main_frame, 
            text="Battle Fund", 
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        title_label.pack(pady=(0, 10))
        
        # Content label
        self.content_label = tk.Label(
            main_frame,
            text="Loading...",
            font=('Arial', 10),
            fg='#00ff00',
            bg='#2b2b2b',
            wraplength=220,
            justify='left'
        )
        self.content_label.pack(fill='both', expand=True)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Status: Initializing",
            font=('Arial', 8),
            fg='#888888',
            bg='#2b2b2b'
        )
        self.status_label.pack(pady=(10, 0))
        
        # File path
        self.file_path = "battle_fund.txt"
        
        # Start the refresh thread
        self.running = True
        self.refresh_thread = threading.Thread(target=self.refresh_loop, daemon=True)
        self.refresh_thread.start()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def read_battle_fund_file(self):
        """Read the contents of battle_fund.txt file"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if content:
                        return content
                    else:
                        return "File is empty"
            else:
                return f"File '{self.file_path}' not found"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def update_display(self):
        """Update the display with current file contents"""
        content = self.read_battle_fund_file()
        current_time = time.strftime("%H:%M:%S")
        
        # Update content
        self.content_label.config(text=content)
        
        # Update status
        if "not found" in content or "Error" in content:
            self.status_label.config(text=f"Status: Error - {current_time}", fg='#ff4444')
        else:
            self.status_label.config(text=f"Status: OK - {current_time}", fg='#44ff44')
    
    def refresh_loop(self):
        """Background thread that refreshes the display every 2 seconds"""
        while self.running:
            try:
                # Schedule GUI update on main thread
                self.root.after(0, self.update_display)
                time.sleep(2)
            except Exception as e:
                print(f"Error in refresh loop: {e}")
                break
    
    def on_closing(self):
        """Handle window close event"""
        self.running = False
        self.root.destroy()
    
    def run(self):
        """Start the GUI"""
        # Initial update
        self.update_display()
        # Start the main loop
        self.root.mainloop()

if __name__ == "__main__":
    # Create and run the HUD
    hud = BattleFundHUD()
    hud.run()