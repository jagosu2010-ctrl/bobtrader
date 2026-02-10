import tkinter as tk
from tkinter import ttk
import threading
try:
    from pt_correlation import CorrelationAnalyzer, calculate_portfolio_correlation
    from pt_position_sizing import PositionSizer
    _RISK_AVAILABLE = True
except Exception as _risk_err:
    CorrelationAnalyzer = None
    calculate_portfolio_correlation = None
    PositionSizer = None
    _RISK_IMPORT_ERROR = _risk_err
    _RISK_AVAILABLE = False
from pt_config import ConfigManager
import os

class RiskDashboard(ttk.Frame):
    def __init__(self, parent, coin_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.coin_list = coin_list

        # 1. Establish Configuration with dictionary-safe access
        cm = ConfigManager()
        analytics_cfg = cm.get().analytics
        
        if isinstance(analytics_cfg, dict):
            self.db_path = analytics_cfg.get("database_path", "hub_data/trades.db")
        else:
            # Fallback to default path if config section is missing
            self.db_path = "hub_data/trades.db"

        # If correlation/position sizing modules are unavailable, show an error panel
        if not _RISK_AVAILABLE:
            err_frame = ttk.Frame(self)
            ttk.Label(err_frame, text="Risk modules unavailable", foreground="red", font=("Arial", 14, "bold")).pack(pady=20)
            ttk.Label(err_frame, text=f"Import error: {_RISK_IMPORT_ERROR}").pack(pady=10)
            err_frame.pack(fill="both", expand=True)
            return

        # 2. Initialize Analyzers
        self.corr_analyzer = CorrelationAnalyzer(self.db_path)
        self.sizer = PositionSizer(self.db_path)

        self._setup_ui()

    def _setup_ui(self):
        """Initializes the layout for correlation and position sizing."""
        # Top control bar
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Button(top, text="Refresh Analysis", command=self.refresh).pack(side="left")
        self.status_lbl = ttk.Label(top, text="Ready")
        self.status_lbl.pack(side="left", padx=10)

        # Split: Left (Correlation), Right (Sizing)
        paned = ttk.Panedwindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=10, pady=5)

        left_frame = ttk.Frame(paned)
        right_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        paned.add(right_frame, weight=1)

        # --- Correlation Matrix Section ---
        corr_frame = ttk.LabelFrame(left_frame, text="Correlation Matrix (30 Days)")
        corr_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.matrix_canvas = tk.Canvas(corr_frame, bg="#000000") 
        self.matrix_canvas.pack(fill="both", expand=True)

        # --- Position Sizing Section ---
        size_frame = ttk.LabelFrame(right_frame, text="Volatility-Adjusted Position Sizing")
        size_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Calculator inputs
        calc_frame = ttk.Frame(size_frame)
        calc_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(calc_frame, text="Account Balance: $").grid(row=0, column=0, sticky="w")
        self.balance_var = tk.DoubleVar(value=10000.0)
        ttk.Entry(calc_frame, textvariable=self.balance_var, width=10).grid(row=0, column=1)

        ttk.Label(calc_frame, text="Risk %:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.risk_var = tk.DoubleVar(value=2.0)
        ttk.Entry(calc_frame, textvariable=self.risk_var, width=5).grid(row=0, column=3)

        ttk.Button(calc_frame, text="Calculate", command=self._calculate_sizing).grid(row=0, column=4, padx=10)

        # Results table
        cols = ("Coin", "Volatility (ATR%)", "Rec. Size $", "Factor")
        self.size_tree = ttk.Treeview(size_frame, columns=cols, show="headings")
        for c in cols:
            self.size_tree.heading(c, text=c)
            self.size_tree.column(c, width=80)

        self.size_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def refresh(self):
        """Triggers the background analysis thread."""
        self.status_lbl.config(text="Analyzing...")
        threading.Thread(target=self._run_analysis, daemon=True).start()

    def _run_analysis(self):
        """Calculates matrix data in background to prevent UI freeze."""
        try:
            # Correlation calculation
            matrix = self.corr_analyzer.calculate_correlation_matrix(self.coin_list)

            # Update UI on main thread
            self.after(0, lambda: self._draw_matrix(matrix))
            self.after(0, lambda: self.status_lbl.config(text="Updated Successfully"))

        except Exception as e:
            self.after(0, lambda: self.status_lbl.config(text=f"Analysis Error: {e}"))

    def _draw_matrix(self, matrix):
        """Renders the heat-map on the canvas."""
        self.matrix_canvas.delete("all")
        n = len(self.coin_list)
        if n == 0: return

        # Ensure dynamic scaling to fit current window size
        w = self.matrix_canvas.winfo_width()
        h = self.matrix_canvas.winfo_height()
        cell_w = w / (n + 1)
        cell_h = h / (n + 1)

        # Draw Labels
        for i, coin in enumerate(self.coin_list):
            self.matrix_canvas.create_text((i + 1.5) * cell_w, 0.5 * cell_h, text=coin, fill="white")
            self.matrix_canvas.create_text(0.5 * cell_w, (i + 1.5) * cell_h, text=coin, fill="white")

        # Draw Matrix Cells with Color Heatmap
        for i, coin_a in enumerate(self.coin_list):
            for j, coin_b in enumerate(self.coin_list):
                val = 1.0 if i == j else matrix.get(coin_a, {}).get(coin_b, 0.0)

                # Color logic: Red (Strong Positive), Green (Low), Yellow (Moderate)
                if val > 0.7:
                    color = "#880000" # Dark Red
                elif val < 0.3:
                    color = "#004400" # Dark Green
                else:
                    color = "#444400" # Dark Yellow

                x1, y1 = (i + 1) * cell_w, (j + 1) * cell_h
                x2, y2 = x1 + cell_w, y1 + cell_h

                self.matrix_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#222222")
                self.matrix_canvas.create_text((x1+x2)/2, (y1+y2)/2, text=f"{val:.2f}", fill="white")

    def _calculate_sizing(self):
        """Computes recommended sizes based on balance and risk."""
        balance = self.balance_var.get()
        risk_pct = self.risk_var.get() / 100.0

        for i in self.size_tree.get_children():
            self.size_tree.delete(i)

        for coin in self.coin_list:
            # Fetch volatility from DB logic
            metrics = self.sizer.get_volatility(coin)
            # Default to 5% ATR if data unavailable
            atr_val = metrics.atr_pct if (metrics and hasattr(metrics, 'atr_pct')) else 0.05
            
            rec = self.sizer.calculate_position_size(balance, risk_pct, atr_val)

            self.size_tree.insert("", "end", values=(
                coin, 
                f"{atr_val*100:.1f}%", 
                f"${rec.recommended_size_usd:,.2f}", 
                f"{rec.volatility_factor:.2f}x"
            ))