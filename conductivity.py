import tkinter as tk
from tkinter import ttk, messagebox
import ref_data
import sys
import os

# Ensure ref_data.py is found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class ConductivityCalculator:
    LEN_UNITS = ("m", "cm", "mm", "um", "in")
    RES_UNITS = ("ohm", "kohm", "mohm")
    COND_UNITS = ("S/m", "S/cm", "S/mm")
    LU = {"m": 1, "cm": 0.01, "mm": 0.001, "um": 1e-6, "in": 0.0254}
    RU = {"ohm": 1, "kohm": 1000, "mohm": 1000000}

    def __init__(self, root):
        self.root = root
        self.root.title("电导率计算器")
        self.root.geometry("620x950")
        self.root.resizable(False, False)
        self.sigma_spm = 0.0

        st = ttk.Style()
        st.configure("TFrame", background="white")
        st.configure("Hd.TFrame", background="#2c3e50")
        st.configure("Hd.TLabel", background="#2c3e50", foreground="white", font=("Arial", 16, "bold"))
        st.configure("Sub.TLabel", font=("Arial", 12))
        st.configure("In.TLabel", font=("Arial", 10, "bold"), foreground="#34495e")
        st.configure("Res.TLabel", font=("Courier New", 24, "bold"), foreground="#27ae60")
        st.configure("Un.TLabel", font=("Arial", 14), foreground="#7f8c8d")
        st.configure("Btn.TButton", font=("Arial", 12, "bold"))

        mf = ttk.Frame(root, padding="10")
        mf.pack(fill=tk.BOTH, expand=True)

        # Header
        hf = ttk.Frame(mf, style="Hd.TFrame")
        hf.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(hf, text="电导率计算器", style="Hd.TLabel").pack(pady=15)
        ttk.Label(hf, text="根据材料的尺寸和电阻值计算电导率", style="Sub.TLabel").pack(pady=(0, 15))

        # Input Frame
        self.ifr = ttk.Frame(mf)
        self.ifr.pack(fill=tk.X, pady=5)

        self.unit_vars = {}
        def add_row(row, label, var, default, units, unit_key):
            ttk.Label(self.ifr, text=label, style="In.TLabel").grid(row=row, column=0, sticky=tk.W, pady=(0, 2))
            ttk.Entry(self.ifr, textvariable=var, width=15).grid(row=row+1, column=0, sticky=tk.W, pady=(0, 8))
            uv = tk.StringVar(value=default)
            self.unit_vars[unit_key] = uv
            c = ttk.Combobox(self.ifr, textvariable=uv, values=units, width=10, state="readonly")
            c.grid(row=row+1, column=1, sticky=tk.W, padx=(5, 0), pady=(0, 8))

        self.lv = tk.DoubleVar(value=10.0)
        self.wv = tk.DoubleVar(value=1.0)
        self.hv = tk.DoubleVar(value=0.1)
        self.rv = tk.DoubleVar(value=5.0)
        self.cv = tk.StringVar(value="S/m")

        add_row(0, "长度 (L)", self.lv, "cm", self.LEN_UNITS, "len")
        add_row(2, "宽度 (W)", self.wv, "cm", self.LEN_UNITS, "wid")
        add_row(4, "高度/厚度 (H)", self.hv, "cm", self.LEN_UNITS, "hei")
        add_row(6, "电阻 (R)", self.rv, "ohm", self.RES_UNITS, "res")

        ttk.Label(self.ifr, text="电导率单位", style="In.TLabel").grid(row=8, column=0, sticky=tk.W, pady=(0, 2))
        cc = ttk.Combobox(self.ifr, textvariable=self.cv, values=self.COND_UNITS, width=15, state="readonly")
        cc.grid(row=9, column=0, sticky=tk.W, pady=(0, 10))

        self.btn = ttk.Button(self.ifr, text="计算电导率", command=self.calc, style="Btn.TButton")
        self.btn.grid(row=10, column=0, columnspan=2, pady=10, sticky=tk.W + tk.E)

        # Result Frame
        self.rf = ttk.LabelFrame(mf, text="计算结果")
        self.rf.pack(fill=tk.X, pady=8)
        self.rv_text = tk.StringVar(value="")
        self.rl = ttk.Label(self.rf, textvariable=self.rv_text, style="Res.TLabel")
        self.rl.pack(pady=8)
        self.unit_text = tk.StringVar(value="")
        ttk.Label(self.rf, textvariable=self.unit_text, style="Un.TLabel").pack(pady=(0, 8))

        # Comparison Frame
        self.cf = ttk.LabelFrame(mf, text="📊 材料性能对比")
        self.cf.pack(fill=tk.X, pady=8)

        # Category row
        cr = ttk.Frame(self.cf)
        cr.pack(fill=tk.X, pady=(5, 8))
        ttk.Label(cr, text="选择材料类别：", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.cat_var = tk.StringVar()
        self.cat_cb = ttk.Combobox(cr, textvariable=self.cat_var, values=ref_data.CATEGORY_NAMES, width=26, state="readonly")
        self.cat_cb.pack(side=tk.LEFT, padx=(5, 0))
        self.cat_cb.bind("<<ComboboxSelected>>", self.on_cat_change)

        # User value
        self.uv_fr = ttk.Frame(self.cf)
        self.uv_fr.pack(fill=tk.X, pady=(0, 6))
        self.uv_lb = ttk.Label(self.uv_fr, text="你的材料：--", font=("Arial", 12, "bold"), foreground="#2980b9")
        self.uv_lb.pack()

        # Scrollable ref list
        self.rlf = ttk.Frame(self.cf)
        self.rlf.pack(fill=tk.BOTH, expand=True, pady=(0, 6))
        self.canv = tk.Canvas(self.rlf, height=280, highlightthickness=0)
        self.sbar = ttk.Scrollbar(self.rlf, orient=tk.VERTICAL, command=self.canv.yview)
        self.inner = ttk.Frame(self.canv)
        self.inner.bind("<Configure>", lambda e: self.canv.configure(scrollregion=self.canv.bbox("all")))
        self.canv.create_window((0, 0), window=self.inner, anchor="nw")
        self.canv.configure(yscrollcommand=self.sbar.set)
        self.canv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Assessment
        self.af = ttk.Frame(self.cf)
        self.af.pack(fill=tk.X, pady=(0, 5))
        self.av = tk.StringVar(value="")
        ttk.Label(self.af, textvariable=self.av, font=("Arial", 10), wraplength=560,
                  foreground="#856404", background="#fff9e6").pack(fill=tk.X, padx=2, pady=4)

        self._hide_comp()

        # Formula
        ff = ttk.LabelFrame(mf, text="计算公式")
        ff.pack(fill=tk.X, pady=8)
        ft = tk.Text(ff, height=7, wrap=tk.WORD, font=("Arial", 10))
        ft.pack(fill=tk.BOTH, padx=5, pady=5)
        ft.insert(tk.END, "电导率 σ = (1/R) × (L/(W×H))\n\n"
                  "单位换算：1 cm = 0.01 m, 1 mm = 0.001 m, 1 μm = 10⁻⁶ m, 1 in = 0.0254 m\n"
                  "         1 kΩ = 1000 Ω, 1 MΩ = 10⁶ Ω, 1 S/cm = 100 S/m, 1 S/mm = 1000 S/m")
        ft.config(state=tk.DISABLED)

    # --- helpers ---
    def _hide_comp(self):
        self.cf.pack_forget()

    def _show_comp(self):
        self.cf.pack(fill=tk.X, pady=8, before=self.root.winfo_children()[0].winfo_children()[-1])

    def _get(self, key):
        return self.unit_vars[key].get()

    # --- calculation ---
    def calc(self):
        try:
            L = self.lv.get()
            W = self.wv.get()
            H = self.hv.get()
            R = self.rv.get()
        except tk.TclError:
            messagebox.showerror("输入错误", "请输入有效数值！")
            return
        if L <= 0 or W <= 0 or H <= 0 or R <= 0:
            messagebox.showerror("输入错误", "所有数值必须大于零！")
            return

        Lm = L * self.LU.get(self._get("len"), 1)
        Wm = W * self.LU.get(self._get("wid"), 1)
        Hm = H * self.LU.get(self._get("hei"), 1)
        Ro = R * self.RU.get(self._get("res"), 1)

        sigma = (1 / Ro) * (Lm / (Wm * Hm))
        unit = self.cv.get()
        disp = sigma
        if unit == "S/cm":
            disp /= 100
        elif unit == "S/mm":
            disp /= 1000

        if abs(disp) < 1e-7 and disp != 0:
            s = f"{disp:.7e}"
        else:
            s = f"{disp:.7f}"

        self.rv_text.set(s)
        self.unit_text.set(unit)
        self.sigma_spm = sigma

        self.cat_cb.current(0)
        self._build_comp(0)

    # --- comparison ---
    def on_cat_change(self, event=None):
        idx = self.cat_cb.current()
        if idx >= 0:
            self._build_comp(idx)

    def _build_comp(self, idx):
        cat = ref_data.CATEGORIES[idx]
        self.cat_var.set(ref_data.CATEGORY_NAMES[idx])
        self._show_comp()

        uv = ref_data.fmt_conductivity(self.sigma_spm)
        self.uv_lb.config(text=f"你的材料：{uv} S/m")

        for w in self.inner.winfo_children():
            w.destroy()

        for m in cat["materials"]:
            name, vmin, vmax, typ, ref_str = m
            pos = ref_data.get_position_label(self.sigma_spm, vmin, vmax)
            rng = f"{ref_data.fmt_conductivity(vmin)} ~ {ref_data.fmt_conductivity(vmax)} S/m"

            row = ttk.Frame(self.inner)
            row.pack(fill=tk.X, pady=(0, 4), padx=4)

            top = ttk.Frame(row)
            top.pack(fill=tk.X)
            ttk.Label(top, text=name, font=("Arial", 10, "bold"), width=20, anchor=tk.W).pack(side=tk.LEFT)
            ttk.Label(top, text=rng, font=("Courier New", 9), foreground="#555").pack(side=tk.LEFT, padx=(8, 8))
            ttk.Label(top, text=f"{pos[2]} {pos[0]}", font=("Arial", 9, "bold"), foreground=pos[1]).pack(side=tk.RIGHT)

            bot = ttk.Frame(row)
            bot.pack(fill=tk.X)
            ttk.Label(bot, text=f"[{ref_str}]", font=("Arial", 8), foreground="#95a5a6", wraplength=560).pack(anchor=tk.W)

        mats = list(zip([m[1] for m in cat["materials"]], [m[2] for m in cat["materials"]]))
        assess = ref_data.get_overall_assessment(self.sigma_spm, mats)
        self.av.set(f"📌 {assess}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ConductivityCalculator(root)
    root.mainloop()
