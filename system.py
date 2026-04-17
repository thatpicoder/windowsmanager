"""
Windows System Manager
Monitor CPU, GPU, RAM, Disk, Network, and other system statistics
"""

import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import threading
import time
from datetime import datetime
import platform
import math


class SystemManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows System Manager")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.is_running = True
        self.update_interval = 1000
        
        self.setup_ui()
        self.start_update_thread()
    
    def setup_ui(self):
        """Setup the user interface"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_label = ttk.Label(main_frame, text="System Monitor", font=("Arial", 26, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 0))
        
        subtitle_label = ttk.Label(main_frame, text="made by bitetheapple", font=("Arial", 20, "italic"))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        cpu_frame = ttk.Frame(notebook)
        notebook.add(cpu_frame, text="CPU")
        self.setup_cpu_tab(cpu_frame)
        
        memory_frame = ttk.Frame(notebook)
        notebook.add(memory_frame, text="Memory")
        self.setup_memory_tab(memory_frame)
        
        disk_frame = ttk.Frame(notebook)
        notebook.add(disk_frame, text="Disk")
        self.setup_disk_tab(disk_frame)
        
        network_frame = ttk.Frame(notebook)
        notebook.add(network_frame, text="Network")
        self.setup_network_tab(network_frame)
        
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="System Info")
        self.setup_info_tab(info_frame)
        
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
    
    def setup_cpu_tab(self, parent):
        """Setup CPU tab"""
        content = ttk.Frame(parent, padding="10")
        content.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(content, text="CPU Usage:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.cpu_usage_label = ttk.Label(content, text="0%", font=("Arial", 20, "bold"), foreground="blue")
        self.cpu_usage_label.grid(row=0, column=1, sticky=tk.W, padx=20)
        
        self.cpu_progress = ttk.Progressbar(content, length=400, mode='determinate', maximum=100)
        self.cpu_progress.grid(row=0, column=2, sticky=(tk.W, tk.E), padx=10)
        
        ttk.Label(content, text="Cores (Logical):", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cpu_cores_label = ttk.Label(content, text="0", font=("Arial", 11))
        self.cpu_cores_label.grid(row=1, column=1, sticky=tk.W, padx=20)
        
        ttk.Label(content, text="Cores (Physical):", font=("Arial", 11)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.cpu_physical_cores_label = ttk.Label(content, text="0", font=("Arial", 11))
        self.cpu_physical_cores_label.grid(row=2, column=1, sticky=tk.W, padx=20)
        
        ttk.Label(content, text="Frequency:", font=("Arial", 11)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cpu_freq_label = ttk.Label(content, text="0 MHz", font=("Arial", 11))
        self.cpu_freq_label.grid(row=3, column=1, sticky=tk.W, padx=20)
        
        ttk.Label(content, text="Per-Core Usage:", font=("Arial", 11, "bold")).grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(15, 5))
        
        self.cpu_core_labels = []
        core_count = psutil.cpu_count()
        for i in range(min(core_count, 8)):
            frame = ttk.Frame(content)
            frame.grid(row=5+i, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=2)
            
            label = ttk.Label(frame, text=f"Core {i}:", width=10)
            label.pack(side=tk.LEFT)
            
            usage_label = ttk.Label(frame, text="0%", width=5)
            usage_label.pack(side=tk.LEFT, padx=5)
            
            progressbar = ttk.Progressbar(frame, length=300, mode='determinate', maximum=100)
            progressbar.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            self.cpu_core_labels.append((usage_label, progressbar))
        
        content.columnconfigure(2, weight=1)
    
    def setup_memory_tab(self, parent):
        """Setup Memory tab"""
        content = ttk.Frame(parent, padding="10")
        content.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(content, text="RAM Usage:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ram_usage_label = ttk.Label(content, text="0 GB / 0 GB", font=("Arial", 20, "bold"), foreground="green")
        self.ram_usage_label.grid(row=0, column=1, sticky=tk.W, padx=20)
        
        self.ram_progress = ttk.Progressbar(content, length=400, mode='determinate', maximum=100)
        self.ram_progress.grid(row=0, column=2, sticky=(tk.W, tk.E), padx=10)
        
        self.ram_percent_label = ttk.Label(content, text="0%", font=("Arial", 20, "bold"), foreground="green")
        self.ram_percent_label.grid(row=0, column=3, sticky=tk.W, padx=20)
        
        ttk.Label(content, text="Available:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ram_available_label = ttk.Label(content, text="0 GB", font=("Arial", 11))
        self.ram_available_label.grid(row=1, column=1, sticky=tk.W, padx=20)
        
        ttk.Label(content, text="Swap Usage:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky=tk.W, pady=(15, 5))
        self.swap_usage_label = ttk.Label(content, text="0 GB / 0 GB", font=("Arial", 11))
        self.swap_usage_label.grid(row=2, column=1, sticky=tk.W, padx=20)
        
        self.swap_progress = ttk.Progressbar(content, length=400, mode='determinate', maximum=100)
        self.swap_progress.grid(row=2, column=2, sticky=(tk.W, tk.E), padx=10)
        
        self.swap_percent_label = ttk.Label(content, text="0%", font=("Arial", 11))
        self.swap_percent_label.grid(row=2, column=3, sticky=tk.W, padx=20)
        
        content.columnconfigure(2, weight=1)
    
    def setup_disk_tab(self, parent):
        """Setup Disk tab"""
        content = ttk.Frame(parent, padding="10")
        content.pack(fill=tk.BOTH, expand=True)
        
        canvas_frame = ttk.Frame(content)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.disk_frames = {}
        self.disk_labels = {}
        
        partitions = psutil.disk_partitions()
        for idx, partition in enumerate(partitions):
            if partition.fstype:
                frame = ttk.LabelFrame(scrollable_frame, text=f"{partition.device} ({partition.fstype})", padding="5")
                frame.pack(fill=tk.X, expand=True, pady=5)
                
                usage_label = ttk.Label(frame, text="", font=("Arial", 10))
                usage_label.pack(anchor=tk.W, pady=2)
                
                progress = ttk.Progressbar(frame, length=400, mode='determinate', maximum=100)
                progress.pack(fill=tk.X, expand=True, pady=2)
                
                percent_label = ttk.Label(frame, text="0%", font=("Arial", 10))
                percent_label.pack(anchor=tk.W, pady=2)
                
                self.disk_frames[partition.device] = {
                    'progress': progress,
                    'usage_label': usage_label,
                    'percent_label': percent_label,
                    'mount': partition.mountpoint
                }
    
    def setup_network_tab(self, parent):
        """Setup Network tab"""
        content = ttk.Frame(parent, padding="10")
        content.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(content, text="Bytes Sent:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.net_sent_label = ttk.Label(content, text="0 MB", font=("Arial", 11))
        self.net_sent_label.grid(row=0, column=1, sticky=tk.W, padx=20)
        
        ttk.Label(content, text="Bytes Received:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.net_recv_label = ttk.Label(content, text="0 MB", font=("Arial", 11))
        self.net_recv_label.grid(row=1, column=1, sticky=tk.W, padx=20)
        
        ttk.Label(content, text="Packets Sent:", font=("Arial", 11)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.net_packets_sent_label = ttk.Label(content, text="0", font=("Arial", 11))
        self.net_packets_sent_label.grid(row=2, column=1, sticky=tk.W, padx=20)
        
        ttk.Label(content, text="Packets Received:", font=("Arial", 11)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.net_packets_recv_label = ttk.Label(content, text="0", font=("Arial", 11))
        self.net_packets_recv_label.grid(row=3, column=1, sticky=tk.W, padx=20)
        
        ttk.Label(content, text="Errors In:", font=("Arial", 11)).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.net_errin_label = ttk.Label(content, text="0", font=("Arial", 11))
        self.net_errin_label.grid(row=4, column=1, sticky=tk.W, padx=20)
        
        ttk.Label(content, text="Dropped In:", font=("Arial", 11)).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.net_dropin_label = ttk.Label(content, text="0", font=("Arial", 11))
        self.net_dropin_label.grid(row=5, column=1, sticky=tk.W, padx=20)
    
    def setup_info_tab(self, parent):
        """Setup System Info tab"""
        content = ttk.Frame(parent, padding="10")
        content.pack(fill=tk.BOTH, expand=True)
        
        info_text = f"""
System Information

Platform: {platform.platform()}
Processor: {platform.processor()}
Architecture: {platform.machine()}
Python Version: {platform.python_version()}
Hostname: {platform.node()}

Boot Time: {self.get_boot_time()}
System Uptime: {self.get_uptime()}
"""
        
        text_widget = tk.Text(content, height=15, width=80, font=("Courier", 10), relief=tk.SUNKEN)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(1.0, info_text)
        text_widget.config(state=tk.DISABLED)
        
        scrollbar = ttk.Scrollbar(content, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
    
    def get_boot_time(self):
        """Get system boot time"""
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        return str(bt)
    
    def get_uptime(self):
        """Get system uptime"""
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_hours = int(uptime_seconds // 3600)
        uptime_minutes = int((uptime_seconds % 3600) // 60)
        return f"{uptime_hours}h {uptime_minutes}m"
    
    def start_update_thread(self):
        """Start background thread for updating stats"""
        thread = threading.Thread(target=self.update_loop, daemon=True)
        thread.start()
    
    def update_loop(self):
        """Background update loop"""
        while self.is_running:
            self.root.after(0, self.update_stats)
            time.sleep(self.update_interval / 1000)
    
    def update_stats(self):
        """Update all statistics"""
        try:
            self.update_cpu_stats()
            self.update_memory_stats()
            self.update_disk_stats()
            self.update_network_stats()
            
            current_time = datetime.now().strftime("%H:%M:%S")
            self.status_label.config(text=f"Last updated: {current_time}")
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
    
    def update_cpu_stats(self):
        """Update CPU statistics"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        self.cpu_usage_label.config(text=f"{cpu_percent}%")
        self.cpu_progress['value'] = cpu_percent
        
        cores_logical = psutil.cpu_count()
        cores_physical = psutil.cpu_count(logical=False)
        self.cpu_cores_label.config(text=str(cores_logical))
        self.cpu_physical_cores_label.config(text=str(cores_physical))
        
        freq = psutil.cpu_freq()
        if freq:
            self.cpu_freq_label.config(text=f"{freq.current:.0f} MHz")
        
        per_cpu = psutil.cpu_percent(interval=0.1, percpu=True)
        for i, (usage_label, progressbar) in enumerate(self.cpu_core_labels):
            if i < len(per_cpu):
                usage_label.config(text=f"{per_cpu[i]:.0f}%")
                progressbar['value'] = per_cpu[i]
    
    def update_memory_stats(self):
        """Update memory statistics"""
        ram = psutil.virtual_memory()
        
        used_gb = ram.used / (1024**3)
        total_gb = ram.total / (1024**3)
        self.ram_usage_label.config(text=f"{used_gb:.2f} GB / {total_gb:.2f} GB")
        self.ram_progress['value'] = ram.percent
        self.ram_percent_label.config(text=f"{ram.percent:.1f}%")
        
        available_gb = ram.available / (1024**3)
        self.ram_available_label.config(text=f"{available_gb:.2f} GB")
        
        swap = psutil.swap_memory()
        swap_used_gb = swap.used / (1024**3)
        swap_total_gb = swap.total / (1024**3)
        self.swap_usage_label.config(text=f"{swap_used_gb:.2f} GB / {swap_total_gb:.2f} GB")
        self.swap_progress['value'] = swap.percent
        self.swap_percent_label.config(text=f"{swap.percent:.1f}%")
    
    def update_disk_stats(self):
        """Update disk statistics"""
        partitions = psutil.disk_partitions()
        for partition in partitions:
            if partition.device in self.disk_frames:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    used_gb = usage.used / (1024**3)
                    total_gb = usage.total / (1024**3)
                    
                    self.disk_frames[partition.device]['usage_label'].config(
                        text=f"{used_gb:.2f} GB / {total_gb:.2f} GB"
                    )
                    self.disk_frames[partition.device]['progress']['value'] = usage.percent
                    self.disk_frames[partition.device]['percent_label'].config(
                        text=f"{usage.percent:.1f}%"
                    )
                except PermissionError:
                    pass
    
    def update_network_stats(self):
        """Update network statistics"""
        net_io = psutil.net_io_counters()
        sent_mb = net_io.bytes_sent / (1024**2)
        recv_mb = net_io.bytes_recv / (1024**2)
        
        self.net_sent_label.config(text=f"{sent_mb:.2f} MB")
        self.net_recv_label.config(text=f"{recv_mb:.2f} MB")
        self.net_packets_sent_label.config(text=str(net_io.packets_sent))
        self.net_packets_recv_label.config(text=str(net_io.packets_recv))
        self.net_errin_label.config(text=str(net_io.errin))
        self.net_dropin_label.config(text=str(net_io.dropin))
    
    def on_closing(self):
        """Handle window closing"""
        self.is_running = False
        self.root.destroy()


def main():
    root = tk.Tk()
    app = SystemManager(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
