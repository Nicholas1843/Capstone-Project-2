import yellowpages as yp
import pyinputplus as pyip
import csv
import os

# Dictionary 1 containing Categories
path = r'C:\Users\Nicholas Aprilie\OneDrive\Documents\Purwadhika\VSCode\Data\yellowpages1.csv'
df1 = {}

with open(path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    header = next(csv_reader)
    df1['header'] = header[1:]

    for row in csv_reader:
        id = str(row[0])
        values = row[1:]
        df1[id] = [int(values[0]), values[1], int(values[2])]
# print(df1)

# Dictionary 2 containing contacts
path = r'C:\Users\Nicholas Aprilie\OneDrive\Documents\Purwadhika\VSCode\Data\yellowpages2.csv'
df2 = {}

with open(path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    header = next(csv_reader)
    df2['header'] = header[1:]

    for row in csv_reader:
        id = str(row[0])
        values = row[1:]
        if values[6] == 'True':
            values[6] = True
        elif values[6] == 'False':
            values[6] = False
        df2[id] = [int(values[0]), values[1], values[2], values[3], values[4], int(values[5]), values[6]]
# print(df2)


PROMPT = '''
===Business Contacts in Yogyakarta===

1. View Contacts
2. Add Contacts
3. Edit Contacts
4. Delete Contacts
5. Quit
6. Show History (WIP)
'''

def main():
    global df1
    global df2

    while True:
        yp.clear_screen()
        print(PROMPT)
        menu = pyip.inputInt(prompt = 'Choose Menu[1-6]: ', min = 1, max = 6)

        if menu == 1:
            yp.show(df1, df2)
        elif menu == 2:
            yp.add(df1, df2)
        elif menu == 3:
            yp.update(df1, df2)
        elif menu == 4:
            yp.delete(df1, df2)
        elif menu == 5:
            break
        elif menu == 6:
            yp.show_history()
        else:
            print('Option unavailable.')

if __name__ == '__main__':
    main()