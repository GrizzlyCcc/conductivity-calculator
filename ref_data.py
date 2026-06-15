"""
材料电导率参考数据库
数据来源：通过 OpenAlex 和 Crossref API 检索验证的公开文献
所有电导率值以 S/m 为单位
参考文献格式：[期刊, 年, 卷, 页, DOI]
"""

def normalize_to_spm(value, unit):
    table = {"S/m": 1, "S/cm": 100, "S/mm": 1000}
    return value * table.get(unit, 1)

def fmt_conductivity(val):
    if val == 0: return "0"
    av = abs(val)
    if av >= 1: return f"{val:.2f}"
    if av >= 0.01: return f"{val:.4f}"
    return f"{val:.1e}"

def get_position_label(uv, rmin, rmax):
    if uv < rmin: return ("低于范围","#3498db","⬇")
    if uv > rmax: return ("高于范围","#e74c3c","⬆")
    r = rmax - rmin
    if r == 0: return ("符合参考值","#27ae60","✓")
    pct = (uv - rmin) / r
    if pct < 0.25: return ("偏低","#f39c12","↘")
    if pct < 0.75: return ("中等","#27ae60","✓")
    return ("偏高","#e67e22","↗")

def get_overall_assessment(uv, mats):
    if not mats: return ""
    gmin = min(m[0] for m in mats)
    gmax = max(m[1] for m in mats)
    if uv < gmin: return "低于同类材料所有文献报道范围，属于起步研究水平"
    if uv > gmax: return "优于同类材料常见文献报道值，性能处于前沿水平"
    r = gmax - gmin
    pct = (uv - gmin) / r if r > 0 else 0.5
    if pct < 0.25: return "处于同类材料报告值的较低范围，仍有优化提升空间"
    if pct < 0.5: return "处于同类材料中等偏下水平，可尝试优化配方或制备工艺"
    if pct < 0.75: return "处于同类材料中等水平，性能表现合理稳定"
    return "处于同类材料较高水平，性能表现良好"

CATEGORIES = [
  {"id":"hydrogel","name":"导电水凝胶","icon":"💧","materials":[
   ("PAM水凝胶",1e-5,0.01,0.002,"Chem. Soc. Rev., 2019, 48, 1642-1667, 10.1039/c8cs00595h"),
   ("PEDOT:PSS/PVA水凝胶",0.1,20,5,"Nat. Commun., 2019, 10, 1043, 10.1038/s41467-019-09003-5"),
   ("聚苯胺(PANI)水凝胶",0.001,1,0.05,"Nat. Mater., 2023, 22, 895-902, 10.1038/s41563-023-01569-2"),
   ("AgNW/海藻酸水凝胶",1,100,2,"Chem. Soc. Rev., 2019, 48, 1566-1595, 10.1039/c8cs00706c"),
   ("MXene水凝胶",10,1000,50,"ACS Nano, 2021, 15, 6420-6429, 10.1021/acsnano.0c08357"),
   ("氧化石墨烯水凝胶",0.001,0.1,0.01,"Chem. Soc. Rev., 2019, 48, 1642-1667, 10.1039/c8cs00595h")
  ]},
  {"id":"elastomer","name":"导电弹性体","icon":"🧪","materials":[
   ("CNT/PDMS复合材料",0.001,100,0.5,"Prog. Mater. Sci., 2019, 103, 319-373, 10.1016/j.pmatsci.2019.02.003"),
   ("AgNW/PDMS",100,100000,2000,"Chem. Soc. Rev., 2019, 48, 1566-1595, 10.1039/c8cs00706c"),
   ("炭黑/硅橡胶",0.01,10,0.1,"Prog. Mater. Sci., 2019, 103, 319-373, 10.1016/j.pmatsci.2019.02.003"),
   ("石墨烯/PDMS",0.1,1000,5,"Chem. Soc. Rev., 2019, 48, 1566-1595, 10.1039/c8cs00706c"),
   ("液态金属/弹性体",10000,1e6,100000,"Adv. Funct. Mater., 2019, 29, 1805924, 10.1002/adfm.201805924"),
   ("MXene/硅橡胶",0.1,100,1,"Energy Environ. Mater., 2020, 3, 29-55, 10.1002/eem2.12058")
  ]},
  {"id":"polymer","name":"导电聚合物","icon":"🧬","materials":[
   ("PEDOT:PSS (未处理)",0.1,1000,1,"Prog. Mater. Sci., 2020, 108, 100616, 10.1016/j.pmatsci.2019.100616"),
   ("PEDOT:PSS (掺杂增强)",1000,50000,3000,"Prog. Mater. Sci., 2020, 108, 100616, 10.1016/j.pmatsci.2019.100616"),
   ("聚苯胺 (掺杂态)",1,1000,10,"Nanoscale Adv., 2019, 1, 3807-3835, 10.1039/c9na00374f"),
   ("聚吡咯 (PPy)",10,10000,100,"Nanoscale Adv., 2019, 1, 3807-3835, 10.1039/c9na00374f"),
   ("PANI/CNT复合物",10,10000,100,"Prog. Mater. Sci., 2019, 103, 319-373, 10.1016/j.pmatsci.2019.02.003")
  ]},
  {"id":"carbon","name":"碳基材料","icon":"⚫","materials":[
   ("碳纳米管薄膜",10000,1e6,100000,"Prog. Mater. Sci., 2019, 103, 319-373, 10.1016/j.pmatsci.2019.02.003"),
   ("石墨烯薄膜",10000,1e6,100000,"Chem. Soc. Rev., 2018, 47, 1822-1873, 10.1039/c6cs00915h"),
   ("碳纤维",1000,100000,10000,"Prog. Mater. Sci., 2019, 103, 319-373, 10.1016/j.pmatsci.2019.02.003"),
   ("碳黑复合材料",0.1,100,1,"Prog. Mater. Sci., 2019, 103, 319-373, 10.1016/j.pmatsci.2019.02.003"),
   ("还原氧化石墨烯 (rGO)",0.1,10000,100,"Chem. Soc. Rev., 2018, 47, 1822-1873, 10.1039/c6cs00915h")
  ]},
  {"id":"2d","name":"二维材料","icon":"🔲","materials":[
   ("石墨烯 (单层)",1e7,1e8,9.6e7,"Chem. Soc. Rev., 2018, 47, 1822-1873, 10.1039/c6cs00915h"),
   ("MXene (Ti3C2Tx)",100000,2e6,800000,"ACS Nano, 2021, 15, 6420-6429, 10.1021/acsnano.0c08357"),
   ("MoS2",0.0001,1000,0.01,"Rev. Mod. Phys., 2018, 90, 021001, 10.1103/revmodphys.90.021001"),
   ("黑磷 (BP)",10,1000,100,"Rev. Mod. Phys., 2018, 90, 021001, 10.1103/revmodphys.90.021001"),
   ("过渡金属硫化物",1e-6,0.1,0.0001,"Rev. Mod. Phys., 2018, 90, 021001, 10.1103/revmodphys.90.021001")
  ]},
  {"id":"semiconductor","name":"半导体","icon":"💠","materials":[
   ("硅 (本征 Si)",0.0001,0.001,0.00044,"Sze S.M., Physics of Semiconductor Devices, 2021, 4th ed., Wiley"),
   ("硅 (n型掺杂)",100,50000,1000,"Acc. Chem. Res., 2019, 52, 523-533, 10.1021/acs.accounts.8b00500"),
   ("锗 (Ge)",1,2.5,2,"CRC Handbook of Chemistry and Physics, 2021, 102nd ed."),
   ("砷化镓 (GaAs)",1e-6,10000,0.001,"CRC Handbook of Chemistry and Physics, 2021, 102nd ed."),
   ("碳化硅 (SiC)",1e-10,100,1e-6,"Sze S.M., Physics of Semiconductor Devices, 2021, 4th ed., Wiley"),
   ("氧化锌 (ZnO)",0.01,1000,1,"Acc. Chem. Res., 2019, 52, 523-533, 10.1021/acs.accounts.8b00500"),
   ("ITO薄膜",10000,2e6,50000,"Acc. Chem. Res., 2019, 52, 523-533, 10.1021/acs.accounts.8b00500")
  ]},
  {"id":"energy","name":"能源材料","icon":"🔋","materials":[
   ("石墨负极",100,10000,1000,"Chem. Rev., 2020, 120, 4257-4300, 10.1021/acs.chemrev.9b00427"),
   ("LiCoO2正极",0.001,0.1,0.01,"Chem. Rev., 2020, 120, 4257-4300, 10.1021/acs.chemrev.9b00427"),
   ("LLZO固态电解质",0.0001,0.01,0.002,"Chem. Rev., 2020, 120, 4257-4300, 10.1021/acs.chemrev.9b00427"),
   ("活性炭超级电容",1,100,5,"Nanoscale Adv., 2019, 1, 3807-3835, 10.1039/c9na00374f"),
   ("锂金属",1e6,1.2e7,1.08e7,"CRC Handbook of Chemistry and Physics, 2021, 102nd ed.")
  ]},
  {"id":"insulator","name":"绝缘体","icon":"🛡️","materials":[
   ("玻璃 (钠钙)",1e-14,1e-10,1e-12,"CRC Handbook of Chemistry and Physics, 2021, 102nd ed."),
   ("天然橡胶",1e-15,1e-13,1e-14,"CRC Handbook of Chemistry and Physics, 2021, 102nd ed."),
   ("PET塑料",1e-16,1e-14,1e-15,"CRC Handbook of Chemistry and Physics, 2021, 102nd ed."),
   ("PTFE (特氟龙)",1e-18,1e-15,1e-16,"CRC Handbook of Chemistry and Physics, 2021, 102nd ed."),
   ("SiO2薄膜",1e-16,1e-14,1e-15,"CRC Handbook of Chemistry and Physics, 2021, 102nd ed."),
   ("PDMS",1e-14,1e-12,3e-14,"Adv. Mater., 2019, 31, 1904765, 10.1002/adma.201904765")
  ]},
]

CATEGORY_NAMES = [c["icon"]+" "+c["name"] for c in CATEGORIES]
