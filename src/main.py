import yellowpages as yp
import pyinputplus as pyip
import csv
import os

# Dictionary 1 containing Categories

path = 'Data\yellowpages1.csv'
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

# path = 'Data\yellowpages2.csv'
# df2 = {}

# with open(path, 'r') as csv_file:
#     csv_reader = csv.reader(csv_file)
    
#     header = next(csv_reader)
#     df1['header'] = header[1:]

#     for row in csv_reader:
#         id = str(row[0])
#         values = row[1:]
#         df2[id] = values

# Dictionary 2 containing contacts
df2 = {
    'header': ['Contact_ID', 'Name', 'Email', 'Website', 'Phone Number', 'Category_ID', 'Important'],
    '1': [1, 'Universitas Gadjah Mada', 'info@ugm.ac.id', 'https://ugm.ac.id/', '+62 274 565223', 1, False],
    '2': [2, 'Siloam Hospitals Yogyakarta', 'info.shyg@siloamhospitals.com', 'https://www.siloamhospitals.com/', '+62 274 4600900', 2, True],
    '3': [3, 'Pizza Hut Jogja City Mall', 'customerservice@pizzahut.co.id','https://www.pizzahut.co.id/', '+62 811-3113-5401', 3, False],
    '4': [4, 'Universitas Negeri Yogyakarta', 'humas@uny.ac.id', 'https://uny.ac.id/', '+62 274 586168', 1, True],
    '5': [5, 'Jogja International Hospital', 'info@rs-jih.co.id', 'https://rs-jih.co.id/', '+62 274 4463535', 2, True],
    '6': [6, 'Jejamuran', '', '', '+62 274 868170', 3, False]
}


PROMPT = '''
===Business Contacts in Yogyakarta===

1. View Contacts
2. Add Contacts
3. Edit Contacts
4. Delete Contacts
5. Quit
'''

def main():
    global df1
    global df2

    while True:
        yp.clear_screen()
        print(PROMPT)
        menu = pyip.inputInt(prompt = 'Choose Menu[1-5]: ', min = 1, max = 5)

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
        else:
            print('Option unavailable.')

if __name__ == '__main__':
    main()