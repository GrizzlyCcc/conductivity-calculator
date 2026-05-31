from cx_Freeze import setup, Executable

setup(
    name="ConductivityCalculator",
    version="1.0.0",
    description="固体材料电导率计算器 - Solid Material Conductivity Calculator",
    executables=[Executable("conductivity.py", base="Win32GUI")],
)
