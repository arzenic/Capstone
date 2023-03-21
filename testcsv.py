import csv
import timeit
""" for i in range(0, 1000000):
    with open('test.csv', 'a', newline='') as f:
        fieldnames = ['position', 'score']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow({'position':i, 'score': i%10}) """

with open('test.csv', 'r') as f:
    reader = csv.DictReader(f)
    start = timeit.default_timer()
    for row in reader:
        if row['position'] == str(999999):
            print("yes")
stop = timeit.default_timer()

print('Time: ', stop - start) 

