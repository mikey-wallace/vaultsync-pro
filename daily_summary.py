import csv
from datetime import datetime

def get_daily_summary(filepath):
    current_week = datetime.today().isocalendar()[1]
    summary = {}

    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        buffer = 0
        for row in reader:
            if int(row["Week"]) != current_week:
                continue
            day = row["Date"]
            if day not in summary:
                summary[day] = {"Income": [], "Bills": [], "Buffer": 0}
            amount = float(row["Amount"])
            if row["Type"] == "Income":
                summary[day]["Income"].append(row)
                buffer += amount
            elif row["Type"] == "Bill":
                summary[day]["Bills"].append(row)
                buffer += amount
            summary[day]["Buffer"] = buffer

    return summary
