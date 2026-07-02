"""
Training Auto-Clicker with GUI
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import sys
from auto_clicker import TrainingAutoClicker
from config import SITE_NAME

class AutoClickerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title(f"{SITE_NAME} Auto-Clicker")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        
        # Set icon color
        self.window.configure(bg='#2c3e50')
        
        self.clicker = None
        self.running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.window, bg='#34495e', height=80)
        title_frame.pack(fill='x')
        
        title_label = tk.Label(
            title_frame,
            text=f"✈️ {SITE_NAME} Auto-Clicker",
            font=('Arial', 20, 'bold'),
            bg='#34495e',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Instructions
        instructions_frame = tk.Frame(self.window, bg='#2c3e50')
        instructions_frame.pack(pady=20, padx=20)
        
        instructions = [
            "1. Click 'LAUNCH BROWSER' below",
            f"2. Login to {SITE_NAME} in the browser",
            "3. Click 'LAUNCH' or 'VIEW COURSE' to start your course",
            "4. Click 'START AUTO-CLICKING' below",
            "5. Sit back and relax! 😊"
        ]
        
        for instruction in instructions:
            label = tk.Label(
                instructions_frame,
                text=instruction,
                font=('Arial', 11),
                bg='#2c3e50',
                fg='white',
                anchor='w'
            )
            label.pack(fill='x', pady=3)
        
        # Buttons
        button_frame = tk.Frame(self.window, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        self.launch_btn = tk.Button(
            button_frame,
            text="🚀 LAUNCH BROWSER",
            font=('Arial', 14, 'bold'),
            bg='#3498db',
            fg='white',
            width=20,
            height=2,
            command=self.launch_browser,
            cursor='hand2'
        )
        self.launch_btn.pack(pady=10)
        
        self.start_btn = tk.Button(
            button_frame,
            text="▶️ START AUTO-CLICKING",
            font=('Arial', 14, 'bold'),
            bg='#27ae60',
            fg='white',
            width=20,
            height=2,
            command=self.start_clicking,
            state='disabled',
            cursor='hand2'
        )
        self.start_btn.pack(pady=10)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹️ STOP",
            font=('Arial', 14, 'bold'),
            bg='#e74c3c',
            fg='white',
            width=20,
            height=2,
            command=self.stop_clicking,
            state='disabled',
            cursor='hand2'
        )
        self.stop_btn.pack(pady=10)
        
        # Status log
        log_label = tk.Label(
            self.window,
            text="Status:",
            font=('Arial', 10, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        log_label.pack(pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            self.window,
            height=8,
            width=70,
            font=('Consolas', 9),
            bg='#1a1a1a',
            fg='#00ff00'
        )
        self.log_text.pack(padx=20, pady=(0, 20))
        
        self.log("Ready to start! Click 'LAUNCH BROWSER' to begin.")
        
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
    def launch_browser(self):
        """Launch browser and setup"""
        self.log("🔧 Launching Chrome browser...")
        self.launch_btn.config(state='disabled')

        def launch_thread():
            self.clicker = TrainingAutoClicker(gui_mode=True)
            if self.clicker.setup_browser():
                self.log("✅ Browser launched successfully!")
                self.log("📋 Please login and launch your course...")
                self.log("📋 Then click START AUTO-CLICKING below")
                self.start_btn.config(state='normal')
            else:
                self.log("❌ Failed to launch browser")
                self.launch_btn.config(state='normal')

        threading.Thread(target=launch_thread, daemon=True).start()
        
    def start_clicking(self):
        """Start auto-clicking"""
        self.log("\n🔄 Switching to course tab...")

        # First switch to the course tab
        if not self.clicker.switch_to_course_tab_and_mute():
            self.log("❌ Could not find course tab. Make sure you clicked LAUNCH!")
            return

        self.log("🚀 Starting auto-clicker...")
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.running = True

        def run_thread():
            self.clicker.running = True
            self.clicker.run(skip_setup=True)

        threading.Thread(target=run_thread, daemon=True).start()
        
    def stop_clicking(self):
        """Stop auto-clicking"""
        self.log("\n⏹️ Stopping auto-clicker...")
        self.running = False
        if self.clicker:
            self.clicker.running = False
        self.stop_btn.config(state='disabled')
        self.start_btn.config(state='normal')
        self.log("✅ Stopped")
        
    def run(self):
        """Run the GUI"""
        self.window.mainloop()

if __name__ == "__main__":
    app = AutoClickerGUI()
    app.run()

