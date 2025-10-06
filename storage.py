import csv
from datetime import datetime

def log_transaction(filepath, entry):
    entry['Date'] = datetime.today().strftime("%Y-%m-%d")
    entry['Week'] = datetime.today().isocalendar()[1]
    entry['Buffer'] = ''

    with open(filepath, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Date', 'Type', 'Source/Vendor', 'Amount',
            'Status', 'Notes', 'Week', 'Buffer'
        ])
        writer.writerow(entry)
