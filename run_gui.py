import tkinter as tk
from tkinter import ttk
import os
import threading
import time

class ProTankiHUD:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ProTanki Crystal Prediction HUD")
        
        # Configure window properties
        self.root.attributes('-topmost', True)  # Stay on top
        self.root.attributes('-alpha', 0.9)     # Slight transparency
        self.root.resizable(False, False)       # Fixed size
        
        # Position on the left side of the screen
        self.root.geometry("350x700+50+100")
        
        # Configure style
        self.root.configure(bg='#2b2b2b')
        
        # Create main frame with scrollable area
        main_frame = tk.Frame(self.root, bg='#2b2b2b', padx=10, pady=10)
        main_frame.pack(fill='both', expand=True)
        
        # Title label
        title_label = tk.Label(
            main_frame, 
            text="ProTanki Crystal Prediction", 
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        title_label.pack(pady=(0, 10))
        
        # Battle Fund Section
        self.create_section(main_frame, "Battle Fund", '#00ff00')
        self.battle_fund_label = self.create_content_label(main_frame)
        
        # Scores Section
        self.create_section(main_frame, "Team Scores", '#ffff00')
        self.red_score_label = self.create_content_label(main_frame, "Red Score: Loading...")
        self.blue_score_label = self.create_content_label(main_frame, "Blue Score: Loading...")
        
        # Crystal Distribution Section
        self.create_section(main_frame, "Crystal Distribution", '#ff8800')
        self.ratio_label = self.create_content_label(main_frame)
        
        # Scoreboards Section
        self.create_section(main_frame, "Scoreboards", '#ff0088')
        self.red_scoreboard_label = self.create_content_label(main_frame, "Red Scoreboard: Loading...")
        self.blue_scoreboard_label = self.create_content_label(main_frame, "Blue Scoreboard: Loading...")
        
        # Diamond Distribution Section
        self.create_section(main_frame, "Diamond Distribution", '#00ffff')
        self.red_diamonds_label = self.create_content_label(main_frame, "Red Diamonds: Loading...")
        self.blue_diamonds_label = self.create_content_label(main_frame, "Blue Diamonds: Loading...")
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Status: Initializing",
            font=('Arial', 8),
            fg='#888888',
            bg='#2b2b2b'
        )
        self.status_label.pack(pady=(15, 0))
        
        # File paths
        self.file_paths = {
            'battle_fund': 'battle_fund.txt',
            'red_score': 'red_score.txt', 
            'blue_score': 'blue_score.txt',
            'ratio': 'ratio.txt',
            'red_scoreboard': 'red_scoreboard.txt',
            'blue_scoreboard': 'blue_scoreboard.txt',
            'red_diamonds': 'red_diamonds.txt',
            'blue_diamonds': 'blue_diamonds.txt'
        }
        
        # Start the refresh thread
        self.running = True
        self.refresh_thread = threading.Thread(target=self.refresh_loop, daemon=True)
        self.refresh_thread.start()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_section(self, parent, title, color):
        """Create a section header"""
        section_label = tk.Label(
            parent,
            text=title,
            font=('Arial', 10, 'bold'),
            fg=color,
            bg='#2b2b2b'
        )
        section_label.pack(anchor='w', pady=(10, 2))
    
    def create_content_label(self, parent, initial_text="Loading..."):
        """Create a content label for displaying file contents"""
        label = tk.Label(
            parent,
            text=initial_text,
            font=('Arial', 9),
            fg='#ffffff',
            bg='#2b2b2b',
            wraplength=320,
            justify='left',
            anchor='w'
        )
        label.pack(anchor='w', padx=(10, 0), pady=(0, 5))
        return label
        
    def read_battle_fund_file(self):
        """Read the contents of battle_fund.txt file"""
        return self.read_file('battle_fund')
    
    def read_file(self, file_key):
        """Read the contents of a specified file"""
        try:
            file_path = self.file_paths.get(file_key)
            if not file_path:
                return f"Unknown file key: {file_key}"
                
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if content:
                        return content
                    else:
                        return "File is empty"
            else:
                return f"File '{file_path}' not found"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def read_diamond_file(self, file_key):
        """Read diamond files and format them for display"""
        try:
            file_path = self.file_paths.get(file_key)
            if not file_path:
                return f"Unknown file key: {file_key}"
                
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    if lines:
                        # Convert to integers and format as a comma-separated list
                        diamonds = [int(line.strip()) for line in lines if line.strip().isdigit()]
                        if len(diamonds) <= 5:
                            return ', '.join(map(str, diamonds))
                        else:
                            # Show first 5 and indicate more
                            first_five = ', '.join(map(str, diamonds[:5]))
                            return f"{first_five}... ({len(diamonds)} total)"
                    else:
                        return "File is empty"
            else:
                return f"File '{file_path}' not found"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def update_display(self):
        """Update the display with current file contents"""
        current_time = time.strftime("%H:%M:%S")
        error_count = 0
        
        # Update Battle Fund
        battle_fund_content = self.read_file('battle_fund')
        self.battle_fund_label.config(text=f"Amount: {battle_fund_content}")
        if "not found" in battle_fund_content or "Error" in battle_fund_content:
            error_count += 1
        
        # Update Red Score
        red_score_content = self.read_file('red_score')
        self.red_score_label.config(text=f"Red Score: {red_score_content}")
        if "not found" in red_score_content or "Error" in red_score_content:
            error_count += 1
        
        # Update Blue Score
        blue_score_content = self.read_file('blue_score')
        self.blue_score_label.config(text=f"Blue Score: {blue_score_content}")
        if "not found" in blue_score_content or "Error" in blue_score_content:
            error_count += 1
        
        # Update Ratio
        ratio_content = self.read_file('ratio')
        self.ratio_label.config(text=f"Ratio: {ratio_content}")
        if "not found" in ratio_content or "Error" in ratio_content:
            error_count += 1
        
        # Update Red Scoreboard
        red_scoreboard_content = self.read_file('red_scoreboard')
        self.red_scoreboard_label.config(text=f"Red: {red_scoreboard_content}")
        if "not found" in red_scoreboard_content or "Error" in red_scoreboard_content:
            error_count += 1
        
        # Update Blue Scoreboard
        blue_scoreboard_content = self.read_file('blue_scoreboard')
        self.blue_scoreboard_label.config(text=f"Blue: {blue_scoreboard_content}")
        if "not found" in blue_scoreboard_content or "Error" in blue_scoreboard_content:
            error_count += 1
        
        # Update Red Diamonds
        red_diamonds_content = self.read_diamond_file('red_diamonds')
        self.red_diamonds_label.config(text=f"Red: {red_diamonds_content}")
        if "not found" in red_diamonds_content or "Error" in red_diamonds_content:
            error_count += 1
        
        # Update Blue Diamonds
        blue_diamonds_content = self.read_diamond_file('blue_diamonds')
        self.blue_diamonds_label.config(text=f"Blue: {blue_diamonds_content}")
        if "not found" in blue_diamonds_content or "Error" in blue_diamonds_content:
            error_count += 1
        
        # Update status
        if error_count > 0:
            self.status_label.config(text=f"Status: {error_count} errors - {current_time}", fg='#ff4444')
        else:
            self.status_label.config(text=f"Status: All OK - {current_time}", fg='#44ff44')
    
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
    hud = ProTankiHUD()
    hud.run()