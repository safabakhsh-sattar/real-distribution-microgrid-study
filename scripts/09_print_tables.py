import pandas as pd

for name in ["sensitivity_rural", "sensitivity_urban"]:
    df = pd.read_csv(f"results/{name}.csv")
    print(f"\n=== {name} ===")
    for col in ["nameplate_kW", "delivered_kW"]:
        t = df.pivot(index="bus", columns="scenario", values=col)
        if len(t) > 15:
            t = t.describe().loc[["min", "50%", "max"]]
        print(f"\n{col}")
        print(t.round(1).to_string())