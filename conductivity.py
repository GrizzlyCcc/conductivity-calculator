import tkinter as tk
from tkinter import ttk, messagebox

class ConductivityCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("电导率计算器")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure('TFrame', background='white')
        self.style.configure('Header.TFrame', background='#2c3e50')
        self.style.configure('Header.TLabel', background='#2c3e50', foreground='white', font=('Arial', 16, 'bold'))
        self.style.configure('Title.TLabel', font=('Arial', 12))
        self.style.configure('Input.TLabel', font=('Arial', 10, 'bold'), foreground='#34495e')
        self.style.configure('Result.TLabel', font=('Courier New', 24, 'bold'), foreground='#27ae60')
        self.style.configure('Unit.TLabel', font=('Arial', 14), foreground='#7f8c8d')
        self.style.configure('Calculate.TButton', font=('Arial', 12, 'bold'))
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题区域
        self.header_frame = ttk.Frame(self.main_frame, style='Header.TFrame')
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(self.header_frame, text="电导率计算器", style='Header.TLabel')
        title_label.pack(pady=15)
        
        subtitle_label = ttk.Label(self.header_frame, text="根据材料的尺寸和电阻值计算电导率", style='Title.TLabel')
        subtitle_label.pack(pady=(0, 15))
        
        # 创建输入区域
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=10)
        
        # 长度输入
        ttk.Label(self.input_frame, text="长度 (L)", style='Input.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.length_var = tk.DoubleVar(value=10.0)
        self.length_entry = ttk.Entry(self.input_frame, textvariable=self.length_var, width=15)
        self.length_entry.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        self.length_unit = tk.StringVar(value="cm")
        length_units = ttk.Combobox(self.input_frame, textvariable=self.length_unit, width=10, state="readonly")
        length_units['values'] = ('m', 'cm', 'mm', 'um', 'in')
        length_units.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(0, 10))
        
        # 宽度输入
        ttk.Label(self.input_frame, text="宽度 (W)", style='Input.TLabel').grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.width_var = tk.DoubleVar(value=1.0)
        self.width_entry = ttk.Entry(self.input_frame, textvariable=self.width_var, width=15)
        self.width_entry.grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        
        self.width_unit = tk.StringVar(value="cm")
        width_units = ttk.Combobox(self.input_frame, textvariable=self.width_unit, width=10, state="readonly")
        width_units['values'] = ('m', 'cm', 'mm', 'um', 'in')
        width_units.grid(row=3, column=1, sticky=tk.W, padx=(5, 0), pady=(0, 10))
        
        # 高度输入
        ttk.Label(self.input_frame, text="高度/厚度 (H)", style='Input.TLabel').grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.height_var = tk.DoubleVar(value=0.1)
        self.height_entry = ttk.Entry(self.input_frame, textvariable=self.height_var, width=15)
        self.height_entry.grid(row=5, column=0, sticky=tk.W, pady=(0, 10))
        
        self.height_unit = tk.StringVar(value="cm")
        height_units = ttk.Combobox(self.input_frame, textvariable=self.height_unit, width=10, state="readonly")
        height_units['values'] = ('m', 'cm', 'mm', 'um', 'in')
        height_units.grid(row=5, column=1, sticky=tk.W, padx=(5, 0), pady=(0, 10))
        
        # 电阻输入
        ttk.Label(self.input_frame, text="电阻 (R)", style='Input.TLabel').grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        self.resistance_var = tk.DoubleVar(value=5.0)
        self.resistance_entry = ttk.Entry(self.input_frame, textvariable=self.resistance_var, width=15)
        self.resistance_entry.grid(row=7, column=0, sticky=tk.W, pady=(0, 10))
        
        self.resistance_unit = tk.StringVar(value="ohm")
        resistance_units = ttk.Combobox(self.input_frame, textvariable=self.resistance_unit, width=10, state="readonly")
        resistance_units['values'] = ('ohm', 'kohm', 'mohm')
        resistance_units.grid(row=7, column=1, sticky=tk.W, padx=(5, 0), pady=(0, 10))
        
        # 电导率单位选择
        ttk.Label(self.input_frame, text="电导率单位", style='Input.TLabel').grid(row=8, column=0, sticky=tk.W, pady=(0, 5))
        self.conductivity_unit = tk.StringVar(value="S/m")
        conductivity_units = ttk.Combobox(self.input_frame, textvariable=self.conductivity_unit, width=15, state="readonly")
        conductivity_units['values'] = ('S/m', 'S/cm', 'S/mm')
        conductivity_units.grid(row=9, column=0, sticky=tk.W, pady=(0, 10))
        
        # 计算按钮
        self.calculate_btn = ttk.Button(self.input_frame, text="计算电导率", command=self.calculate, style='Calculate.TButton')
        self.calculate_btn.grid(row=10, column=0, columnspan=2, pady=20, sticky=tk.W+tk.E)
        
        # 结果区域
        self.result_frame = ttk.LabelFrame(self.main_frame, text="电导率结果")
        self.result_frame.pack(fill=tk.X, pady=10)
        
        self.result_var = tk.StringVar(value="0.0000000")
        result_label = ttk.Label(self.result_frame, textvariable=self.result_var, style='Result.TLabel')
        result_label.pack(pady=10)
        
        self.unit_var = tk.StringVar(value="S/m")
        unit_label = ttk.Label(self.result_frame, textvariable=self.unit_var, style='Unit.TLabel')
        unit_label.pack(pady=(0, 10))
        
        # 公式说明区域
        self.formula_frame = ttk.LabelFrame(self.main_frame, text="计算公式")
        self.formula_frame.pack(fill=tk.X, pady=10)
        
        formula_text = tk.Text(self.formula_frame, height=8, wrap=tk.WORD, font=('Arial', 10))
        formula_text.pack(fill=tk.BOTH, padx=5, pady=5)
        
        formula_content = """电导率 σ 的计算公式为：

σ = (1 / R) × (L / (W × H))

其中：
• R = 电阻（单位：欧姆）
• L = 长度（单位：米）
• W = 宽度（单位：米）
• H = 高度/厚度（单位：米）

单位换算：
1 cm = 0.01 m, 1 mm = 0.001 m, 1 μm = 10⁻⁶ m, 1 inch = 0.0254 m
1 kΩ = 1000 Ω, 1 MΩ = 10⁶ Ω, 1 S/cm = 100 S/m, 1 S/mm = 1000 S/m"""
        
        formula_text.insert(tk.END, formula_content)
        formula_text.config(state=tk.DISABLED)
        
        # 绑定事件
        self.conductivity_unit.trace('w', self.update_unit_display)
        
    def calculate(self):
        try:
            # 获取输入值
            length = self.length_var.get()
            width = self.width_var.get()
            height = self.height_var.get()
            resistance = self.resistance_var.get()
            
            # 验证输入
            if length <= 0 or width <= 0 or height <= 0 or resistance <= 0:
                messagebox.showerror("输入错误", "所有数值必须大于零！")
                return
            
            # 单位转换因子（转换为米）
            length_conversion = {
                'm': 1,
                'cm': 0.01,
                'mm': 0.001,
                'um': 1e-6,
                'in': 0.0254
            }
            
            # 电阻单位转换因子（转换为欧姆）
            resistance_conversion = {
                'ohm': 1,
                'kohm': 1000,
                'mohm': 1000000
            }
            
            # 转换为标准单位（米和欧姆）
            length_m = length * length_conversion[self.length_unit.get()]
            width_m = width * length_conversion[self.width_unit.get()]
            height_m = height * length_conversion[self.height_unit.get()]
            resistance_ohm = resistance * resistance_conversion[self.resistance_unit.get()]
            
            # 计算电导率（S/m）
            conductivity = (1 / resistance_ohm) * (length_m / (width_m * height_m))
            
            # 根据选择的单位进行转换
            unit = self.conductivity_unit.get()
            if unit == 'S/cm':
                conductivity /= 100  # 1 S/m = 0.01 S/cm
            elif unit == 'S/mm':
                conductivity /= 1000  # 1 S/m = 0.001 S/mm
            
            # 格式化结果，保留7位小数
            if abs(conductivity) < 1e-7 and conductivity != 0:
                result_str = "{:.7e}".format(conductivity)
            else:
                result_str = "{:.7f}".format(conductivity)
            
            self.result_var.set(result_str)
            
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数值！")
        except ZeroDivisionError:
            messagebox.showerror("计算错误", "除零错误！请检查输入值。")
    
    def update_unit_display(self, *args):
        self.unit_var.set(self.conductivity_unit.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = ConductivityCalculator(root)
    root.mainloop()