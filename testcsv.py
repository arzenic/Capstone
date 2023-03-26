import csv
import timeit
for i in range(0, 10):
    with open('test.csv', 'a', newline='') as f:
        fieldnames = ['position', 'score']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'position':i, 'score': i%10})

