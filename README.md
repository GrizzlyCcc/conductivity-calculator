# Conductivity Calculator / 电导率计算器

一个基于 Python tkinter 的桌面 GUI 工具，用于计算固体材料的电导率。

## 功能特点

- 📐 根据材料的 **长度、宽度、厚度** 和 **电阻值** 计算电导率
- 🔄 支持多种长度单位（米、厘米、毫米、微米、英寸）
- ⚡ 支持多种电阻单位（Ω、kΩ、MΩ）
- 📊 支持多种电导率单位输出（S/m、S/cm、S/mm）
- 🧮 内置计算公式说明和单位换算参考
- 🖥️ 简洁直观的图形界面

## 计算公式

```
σ = (1 / R) × (L / (W × H))

其中：
- σ = 电导率 (S/m)
- R = 电阻 (Ω)
- L = 长度 (m)
- W = 宽度 (m)
- H = 高度/厚度 (m)
```

## 快速开始

### 方式一：直接运行可执行文件

下载 [dist/conductivity.exe](dist/conductivity.exe)，双击运行即可。

### 方式二：从源码运行

```bash
# 确保已安装 Python 3.6+
python conductivity.py
```

### 方式三：打包为可执行文件

**使用 PyInstaller：**
```bash
pip install pyinstaller
pyinstaller pyinstaller/conductivity.spec
```

**使用 cx_Freeze：**
```bash
pip install cx-freeze
python setup.py build
```

## 项目结构

```
conductivity-calculator/
├── conductivity.py          # 主程序源码
├── setup.py                 # cx_Freeze 打包配置
├── requirements.txt         # 依赖说明
├── .gitignore               # Git 忽略规则
├── LICENSE                  # MIT 许可证
├── README.md                # 本文件
├── pyinstaller/
│   └── conductivity.spec    # PyInstaller 打包配置
└── dist/
    └── conductivity.exe     # 预编译的可执行文件
```

## 许可证

本项目基于 MIT 许可证开源。
