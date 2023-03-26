import csv
""" with open('states.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['position'] == str_board:
                            col = int(row['column']) """

with open('states.csv', 'a', newline='') as f:
                fieldnames = ['position', 'column']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerow({'position': 1, 'column':2})

