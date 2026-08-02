import sys
import csv

sys.path.insert(0, r"C:\Users\Full stop\Desktop")
import kisssoft_com_utils as kc

ks = kc.connect()
ks.SetSilentMode(1)
kc.load_module_and_file(ks, "Z012", r"C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12")
kc.calculate(ks)

rows = []
print("Sweep ZR[0].x.nul:")
for v in [-0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5]:
    kc.set_var(ks, "ZR[0].x.nul", str(v))
    kc.calculate(ks)
    rows.append({"x": v, "SF": kc.get_result(ks, "ZPP[0].Fuss.SFnorm"), "SH": kc.get_result(ks, "ZPP[0].Flanke.SH")})

for r in rows:
    print(r)

best = max(rows, key=lambda r: r["SH"] if r["SH"] is not None else -1)
print("Best:", best)

kc.set_var(ks, "ZR[0].x.nul", str(best["x"]))
kc.calculate(ks)
sf_final = kc.get_result(ks, "ZPP[0].Fuss.SFnorm")
sh_final = kc.get_result(ks, "ZPP[0].Flanke.SH")
print(f"Final with x={best['x']}: SF={sf_final}, SH={sh_final}")

kc.generate_report(ks, r"C:\Program Files\KISSsoft AG\KISSsoft 2024\rpt\Z012resc.rpt", r"C:\Users\Full stop\Desktop\kisssoft_e2e_report.rtf", 0, 0)
print(r"Report saved: C:\Users\Full stop\Desktop\kisssoft_e2e_report.rtf")

csv_path = r"C:\Users\Full stop\Desktop\kisssoft_e2e_sweep.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    dw = csv.DictWriter(f, fieldnames=["x", "SF", "SH"])
    dw.writeheader()
    dw.writerows(rows)
print("CSV saved:", csv_path)

kc.release(ks)
