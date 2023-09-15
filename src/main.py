import yellowpages as yp
import pyinputplus as pyip

# Data Frame 1 containing Categories
df1 = {
    'header': ['Category_ID', 'Category', 'Number of entries'],
    '1': [1, 'Universities', 2],
    '2': [2, 'Hospitals', 2],
    '3': [3, 'Restaurants', 2]
}

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