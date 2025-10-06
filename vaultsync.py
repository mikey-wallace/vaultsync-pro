import csv

def update_buffer(filepath):
    buffer = 0
    rows = []

    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            amount = float(row['Amount'])
            if row['Type'] == 'Income':
                buffer += amount
            elif row['Type'] == 'Bill':
                buffer += amount  # Bills are negative
            row['Buffer'] = buffer
            rows.append(row)

    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    return buffer
