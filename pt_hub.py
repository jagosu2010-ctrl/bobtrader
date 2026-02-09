import tkinter as tk
from tkinter import ttk
import time
from pt_config import ConfigManager
from pt_volume_dashboard import VolumeDashboard
from pt_risk_dashboard import RiskDashboard

class PowerTraderHub(tk.Tk):
    def __init__(self):
        # 1. Create the Splash Screen first
        self.withdraw() # Hide the main root window during init
        self.splash = tk.Toplevel()
        self.splash.title("PowerTrader AI Initializing")
        self.splash.geometry("400x200")
        self.splash.overrideredirect(True) # Remove window borders
        
        # Center the splash screen
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width // 2) - 200
        y = (screen_height // 2) - 100
        self.splash.geometry(f"+{x}+{y}")

        tk.Label(self.splash, text="PowerTrader AI", font=("Arial", 18, "bold")).pack(pady=(40, 5))
        self.status_var = tk.StringVar(value="Starting Neural Engine...")
        tk.Label(self.splash, textvariable=self.status_var).pack()
        
        self.progress = ttk.Progressbar(self.splash, length=300, mode='determinate')
        self.progress.pack(pady=20)
        
        # 2. Start the asynchronous initialization
        self.splash.update()
        self.after(500, self._initialize_system)
        super().__init__()

    def _initialize_system(self):
        """Sequential initialization with splash screen updates."""
        try:
            # Step 1: Config
            self.status_var.set("Loading Configuration...")
            self.progress['value'] = 25
            self.splash.update()
            
            self.config_manager = ConfigManager()
            self.config_manager.reload()
            self.settings_getter = self.config_manager.get
            
            trading_cfg = self.config_manager.get().trading
            self.coins = trading_cfg.get("coins", ["BTC"]) if isinstance(trading_cfg, dict) else ["BTC"]
            
            # Step 2: Main Window Setup
            self.status_var.set("Building Dashboards...")
            self.progress['value'] = 60
            self.splash.update()
            
            self.title("PowerTrader AI Hub")
            self.geometry("1400x820")
            self._build_layout()
            
            # Step 3: Finalize
            self.status_var.set("Ready.")
            self.progress['value'] = 100
            self.splash.update()
            
            time.sleep(0.5) # Brief pause to show 100% completion
            self.splash.destroy()
            self.deiconify() # Show the main window
            
        except Exception as e:
            self.status_var.set(f"Critical Error: {e}")
            print(f"[Hub] Startup Failure: {e}")

    def _build_layout(self):
        """Builds the primary dashboard tabs."""
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)
        
        try:
            self.vol_tab = VolumeDashboard(self.tabs, self.coins)
            self.risk_tab = RiskDashboard(self.tabs, self.coins)
            
            self.tabs.add(self.vol_tab, text="Volume Analysis")
            self.tabs.add(self.risk_tab, text="Risk Management")
            
            # Add the Panic Button tab if it exists in your environment
            self._setup_panic_tab()
        except Exception as e:
            error_frame = ttk.Frame(self.tabs)
            ttk.Label(error_frame, text=f"Tab Error: {e}").pack(pady=20)
            self.tabs.add(error_frame, text="Error")

    def _setup_panic_tab(self):
        """Emergency liquidation interface."""
        panic_frame = ttk.Frame(self.tabs)
        self.tabs.add(panic_frame, text="!!! PANIC !!!")
        
        ttk.Label(panic_frame, text="EMERGENCY LIQUIDATION", foreground="red", font=("Arial", 16, "bold")).pack(pady=50)
        
        try:
            from pt_panic import trigger_panic
            style = ttk.Style()
            style.configure("Emergency.TButton", foreground="red", font=("Arial", 12, "bold"))
            ttk.Button(panic_frame, text="FLATTEN ACCOUNT", style="Emergency.TButton", command=trigger_panic).pack(ipadx=20, ipady=20)
        except ImportError:
            pass

if __name__ == "__main__":
    app = PowerTraderHub()
    app.mainloop()