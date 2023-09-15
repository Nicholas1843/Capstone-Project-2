from tabulate import tabulate as tbl
import pyinputplus as pyip
import os
import phonenumbers as phone

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def show_categories(db1):
    header_cat = list(db1.values())[0]
    data_cat = list(db1.values())[1:]
    print(tbl(data_cat, header_cat, tablefmt="outline"))

def select_category(id, db1, db2):
    filter = {}
    category = db1.get(str(id))

    if category:
        for j, val in db2.items():
            if 'header' in j:
                filter[j] = val
            elif id == val[5]:
                filter[j] = val
        sort_important(filter)
        return True
    else:
        clear_screen()
        print(f'Category with ID {id} does not exist.')
        return False

def sort_oldest(db2):
    header_cont = list(db2.values())[0]
    data_cont = list(db2.values())[1:]
    print(tbl(data_cont, header_cont, tablefmt="outline"))

def sort_newest(db2):
    db2Keys = list(db2.keys())
    db2Keys.sort(reverse = True)
    sorted_db2 = {}
    for key in db2Keys:
        sorted_db2[key] = db2[key]

    header_sort = list(sorted_db2.values())[0]
    data_sort = list(sorted_db2.values())[1:]
    print(tbl(data_sort, header_sort, tablefmt="outline"))

def sort_newest_cat(id, db1, db2):
    filter = {}
    category = db1.get(str(id))

    if category:
        for j, val in db2.items():
            if 'header' in j:
                filter[j] = val
            elif id == val[5]:
                filter[j] = val
    sort_newest(filter)

def sort_oldest_cat(id, db1, db2):
    filter = {}
    category = db1.get(str(id))

    if category:
        for j, val in db2.items():
            if 'header' in j:
                filter[j] = val
            elif id == val[5]:
                filter[j] = val
        header1 = list(filter.values())[0]
        data1 = list(filter.values())[1:]
        print(tbl(data1, header1, tablefmt="outline"))
    else:
        print(f'Category with ID {id} not found.')

def sort_important(db2):
    important = {}
    other_data = {}
    for j, val in db2.items():
        if 'header' in j:
            important[j] = val
            other_data[j] = val
        elif val[6]:
            important[j] = val
        else:
            other_data[j] = val

    header_imp = list(important.values())[0]
    data_imp = list(important.values())[1:]
    data_other = list(other_data.values())[1:]
    print(tbl(data_imp + data_other, header_imp, tablefmt="outline"))

def add_contact(id, contact_id, temp, db2, data_warn):
    contact_id += 1
    name = pyip.inputStr('Enter new contact name: ').title()
    email = pyip.inputEmail('Enter the Email of the contact: ', blank = True)
    website = pyip.inputURL('Enter the Website of the contact: ', blank = True)

    while True:
        string_phone = pyip.inputStr('Enter the phone number of the contact (e.g. +62 XXXXXXX): +62 ')
        string_phone = '+62' + string_phone
        phone_num = phone.parse(string_phone)
        phone_valid = phone.is_valid_number(phone_num)
        if phone_valid == False:
            print("Invalid phone number format. Please enter a valid phone number.")
        elif phone_valid == True:
            phone_format = phone.format_number(phone_num, phone.PhoneNumberFormat.INTERNATIONAL)
            break
    
    important = pyip.inputYesNo("Would you like to mark this contact as 'Important'? (yes/no): ")
    if important == 'yes':
        important = True
    elif important == 'no':
        important = False

    warn = False
    for key, val in db2.items():
        if val[1] == name:
            data_warn_temp = db2[key]
            data_warn += [data_warn_temp]
            warn = True

    temp.update({str(contact_id): [contact_id, name, email, website, phone_format, id, important]})
    return temp, warn, data_warn, contact_id
    
def update_contact(id, id2, db1, db2):
    category = db1.get(str(id))
    edit = ''
    found = False
    if category:
        for j, val in db2.items():
            if id2 == val[0] and id == val[5]:
                edit = pyip.inputChoice(['Name', 'Email', 'Website', 'Phone Number', 'Category', 'Important'], 
                    "What would you like to edit? [Name, Email, Website, Phone Number, Category, Important]: ")
                found = True
    else:
        clear_screen()
        print(f'Category with ID {id} not found.')
    
    if found == False:
        clear_screen()
        print(f'Contact with ID {id2} not found inside category.')
    
    temp = {}
    data_warn = []
    db2ls = list(db2.values())[id2]

    if edit == 'Name':
        name = pyip.inputStr('Enter new contact name: ').title()
        warn = False
        for key, val in db2.items():
            if val[1] == name:
                data_warn_temp = db2[key]
                data_warn += [data_warn_temp]
                warn = True

        temp.update({str(id2): [id2, name, db2ls[2], db2ls[3], db2ls[4], db2ls[5], db2ls[6]]})
        header_temp = list(db2.values())[0]
        data_temp = list(temp.values())
        clear_screen()
        print(tbl(data_temp, header_temp, tablefmt = "outline"))

        if warn == True:
            print(f"\nWARNING! Contacts already exists in database.")
            print(tbl(data_warn, header_temp, tablefmt = 'outline'))

        confirm = pyip.inputYesNo(prompt = 'Are you sure you want to edit this contact? (yes/no): ')
        if confirm == 'yes':
            db2.update(temp)
        clear_screen()

    if edit == 'Email':
        email = pyip.inputEmail('Enter the new Email of the contact: ', blank = True)
        temp.update({str(id2): [id2, db2ls[1], email, db2ls[3], db2ls[4], db2ls[5], db2ls[6]]})
        header_temp = list(db2.values())[0]
        data_temp = list(temp.values())
        clear_screen()
        print(tbl(data_temp, header_temp, tablefmt = "outline"))
        confirm = pyip.inputYesNo(prompt = 'Are you sure you want to edit this contact? (yes/no): ')
        if confirm == 'yes':
            db2.update(temp)
        clear_screen()

    if edit == 'Website':
        website = pyip.inputURL('Enter the new Website of the contact: ', blank = True)
        temp.update({str(id2): [id2, db2ls[1], db2ls[2], website, db2ls[4], db2ls[5], db2ls[6]]})
        header_temp = list(db2.values())[0]
        data_temp = list(temp.values())
        clear_screen()
        print(tbl(data_temp, header_temp, tablefmt = "outline"))
        confirm = pyip.inputYesNo(prompt = 'Are you sure you want to edit this contact? (yes/no): ')
        if confirm == 'yes':
            db2.update(temp)
        clear_screen()

    if edit == 'Phone Number':
        while True:
            string_phone = pyip.inputStr('Enter the phone number of the contact (e.g. +62 XXXXXXX): +62 ')
            string_phone = '+62' + string_phone
            phone_num = phone.parse(string_phone)
            phone_valid = phone.is_valid_number(phone_num)
            if phone_valid == False:
                print("Invalid phone number format. Please enter a valid phone number.")
            elif phone_valid == True:
                phone_format = phone.format_number(phone_num, phone.PhoneNumberFormat.INTERNATIONAL)
                break
        temp.update({str(id2): [id2, db2ls[1], db2ls[2], db2ls[3], phone_format, db2ls[5], db2ls[6]]})
        header_temp = list(db2.values())[0]
        data_temp = list(temp.values())
        clear_screen()
        print(tbl(data_temp, header_temp, tablefmt = "outline"))
        confirm = pyip.inputYesNo(prompt = 'Are you sure you want to edit this contact? (yes/no): ')
        if confirm == 'yes':
            db2.update(temp)
        clear_screen()

    if edit == 'Category':
        cat_id = pyip.inputInt('Enter an existing Category ID to move the contact into: ')
        category = db1.get(str(cat_id))
        if category:
            temp.update({str(id2): [id2, db2ls[1], db2ls[2], db2ls[3], db2ls[4], cat_id, db2ls[6]]})
            header_temp = list(db2.values())[0]
            data_temp = list(temp.values())
            clear_screen()
            print(tbl(data_temp, header_temp, tablefmt = "outline"))
            confirm = pyip.inputYesNo(prompt = 'Are you sure you want to edit this contact? (yes/no): ')
            if confirm == 'yes':
                db2.update(temp)
                db1.update({str(id): [id, list(db1.values())[id][1], list(db1.values())[id][2]-1]})
                db1.update({str(cat_id): [cat_id, list(db1.values())[cat_id][1], list(db1.values())[cat_id][2]+1]})
                clear_screen()
        else:
            clear_screen()
            print(f'Category with ID {cat_id} does not exist.')

    if edit == 'Important':
        important = pyip.inputYesNo("Would you like to mark this contact as 'Important'? (yes/no): ")
        if important == 'yes':
            important = True
        elif important == 'no':
            important = False
        temp.update({str(id2): [id2, db2ls[1], db2ls[2], db2ls[3], db2ls[4], db2ls[5], important]})
        header_temp = list(db2.values())[0]
        data_temp = list(temp.values())
        clear_screen()
        print(tbl(data_temp, header_temp, tablefmt = "outline"))
        confirm = pyip.inputYesNo(prompt = 'Are you sure you want to edit this contact? (yes/no): ')
        if confirm == 'yes':
            db2.update(temp)
        clear_screen()

def show(db1, db2):
    clear_screen()
    PROMPT = '''
===View Contacts===

1. Show Categories
2. Select Category
3. Show All Contacts
4. Show Important
5. Back To Main Menu
'''
    PROMPT2 = '''
1. Sort by Newest
2. Sort by Oldest
3. Back'''

    while True:
        print(PROMPT)
        menu_show = pyip.inputInt(prompt = 'Choose Menu[1-5]: ', min = 1, max = 5)

        if menu_show == 1: # Show all categories
            clear_screen()
            show_categories(db1)

        elif menu_show == 2: # Select category ID
            clear_screen()
            id = pyip.inputInt(prompt = 'Select Category ID: ')
            exist = select_category(id, db1, db2)

            while exist == True:
                print(PROMPT2)
                submenu_show = pyip.inputInt('Choose Menu[1-3]: ', min = 1, max = 3)
                if submenu_show == 1:
                    clear_screen()
                    sort_newest_cat(id, db1, db2)
                if submenu_show == 2:
                    clear_screen()
                    sort_oldest_cat(id, db1, db2)
                if submenu_show == 3:
                    clear_screen()
                    break

        elif menu_show == 3: # Show all contacts
            clear_screen()
            sort_important(db2)
            while True:
                print(PROMPT2)
                show3 = pyip.inputInt('Choose Menu[1-3]: ', min = 1, max = 3)
                if show3 == 1:
                    clear_screen()
                    sort_newest(db2)
                if show3 == 2:
                    clear_screen()
                    sort_oldest(db2)
                if show3 == 3:
                    clear_screen()
                    break

        elif menu_show == 4: # Show contacts marked 'Important'
            clear_screen()
            important = {}
            for j, val in db2.items():
                if 'header' in j:
                    important[j] = val
                elif val[6] == True:
                    important[j] = val
            header_imp = list(important.values())[0]
            data_imp = list(important.values())[1:]
            print(tbl(data_imp, header_imp, tablefmt="outline"))

            while True:
                print(PROMPT2)
                show4 = pyip.inputInt('Choose Menu[1-3]: ', min = 1, max = 3)
                if show4 == 1:
                    clear_screen()
                    sort_newest(important)
                if show4 == 2:
                    clear_screen()
                    sort_oldest(important)
                if show4 == 3:
                    clear_screen()
                    break

        elif menu_show == 5: # Back to main menu
            clear_screen()
            break

def add(db1, db2):
    clear_screen()
    PROMPT = '''
===Add Contacts===

1. Add New Categories
2. Select Category
3. Back to Main Menu'''

    PROMPT2 = '''
1. Add contact
2. Add multiple contacts
3. Sort by Newest
4. Sort by Oldest
5. Back'''

    while True:
        show_categories(db1)
        print(PROMPT)
        menu_add = pyip.inputInt(prompt = 'Choose Menu[1-3]: ', min = 1, max = 3)

        if menu_add == 1: # Add new category(s)
            clear_screen()

            temp = {}
            add1 = pyip.inputInt(prompt = 'Enter the number of categories to add: ', min = 1)
            category_id = len(db1) - 1
            data_warn = []
            for i in range(add1):
                name = pyip.inputStr('Enter new category name: ').title()
                warn = False
                for key, val in db1.items():
                    if val[1] == name:
                        data_warn_temp = db1[key]
                        data_warn += [data_warn_temp]
                        warn = True
                category_id += 1
                temp.update({str(category_id): [category_id, name, 0]})

            clear_screen()
            header_temp = list(db1.values())[0]
            data_temp = list(temp.values())

            print(tbl(data_temp, header_temp, tablefmt = 'outline'))
            
            if warn == True:
                    print(f"\nWARNING! Categories already exists in database.")
                    print(tbl(data_warn, header_temp, tablefmt = 'outline'))

            confirm = pyip.inputYesNo(prompt = 'Are you sure you want to add these categories? (yes/no): ')
            if confirm == 'yes':
                db1.update(temp)
            clear_screen()

        if menu_add == 2: # Select category
            clear_screen()
            id = pyip.inputInt(prompt = 'Select Category ID: ')
            exist = select_category(id, db1, db2)

            while exist == True:
                print(PROMPT2)
                submenu_add = pyip.inputInt('Choose Menu[1-3]: ', min = 1, max = 5)
                if submenu_add == 1:
                    clear_screen()
                    temp = {}
                    contact_id = len(db2) -1
                    data_warn = []
                    count = 0

                    temp, warn, data_warn, contact_id = add_contact(id, contact_id, temp, db2, data_warn)
                    
                    count += 1

                    clear_screen()
                    header_temp = list(db2.values())[0]
                    data_temp = list(temp.values())
                    print(tbl(data_temp, header_temp, tablefmt = "outline"))

                    if warn == True:
                        print(f"\nWARNING! Contacts already exists in database.")
                        print(tbl(data_warn, header_temp, tablefmt = 'outline'))

                    confirm = pyip.inputYesNo(prompt = 'Are you sure you want to add this contact? (yes/no): ')
                    if confirm == 'yes':
                        db2.update(temp)
                        db1.update({str(id): [id, list(db1.values())[id][1], list(db1.values())[id][2]+1]})
                    clear_screen()
                    select_category(id, db1, db2)

                if submenu_add == 2:
                    clear_screen()
                    temp = {}
                    contact_id = len(db2) -1
                    data_warn = []
                    warn_loop = False

                    add1 = pyip.inputInt(prompt = 'Enter the number of contacts to add: ', min = 2)
                    for i in range(add1):
                        temp, warn, data_warn, contact_id = add_contact(id, contact_id, temp, db2, data_warn)
                        if warn == True:
                            warn_loop = True
                        clear_screen()

                    header_temp = list(db2.values())[0]
                    data_temp = list(temp.values())
                    print(tbl(data_temp, header_temp, tablefmt = "outline"))

                    if warn_loop == True:
                        print(f"\nWARNING! Contacts already exists in database.")
                        print(tbl(data_warn, header_temp, tablefmt = 'outline'))

                    confirm = pyip.inputYesNo(prompt = 'Are you sure you want to add these contacts? (yes/no): ')
                    if confirm == 'yes':
                        db2.update(temp)
                        db1.update({str(id): [id, list(db1.values())[id][1], list(db1.values())[id][2]+add1]})
                    clear_screen()
                    select_category(id, db1, db2)

                if submenu_add == 3:
                    clear_screen()
                    sort_newest_cat(id, db1, db2)
                
                if submenu_add == 4:
                    clear_screen()
                    sort_oldest_cat(id, db1, db2)

                if submenu_add == 5:
                    break

        if menu_add == 3: # Back to main menu
            break

    clear_screen()

def update(db1, db2):
    clear_screen()
    PROMPT = '''===Change Contact Details===
1. Change Category Name
2. Select Category
3. Show All Contacts
4. Back To Main Menu'''

    PROMPT2 = '''
1. Change Contact Detail
2. Sort by Newest
3. Sort by Oldest
4. Back'''

    while True:
        show_categories(db1)
        print(PROMPT)
        menu_update = pyip.inputInt(prompt = 'Choose Menu[1-4]: ', min = 1, max = 4)

        if menu_update == 1:
            clear_screen()
            show_categories(db1)
            id = pyip.inputInt('Enter Category ID to edit: ', min = 1)
            category = db1.get(str(id))
            temp = {}
            data_warn = []

            if category:
                new_category_name = pyip.inputStr('Enter the new Category Name: ').title()
                temp.update({str(id): [id, new_category_name, list(db1.values())[id][2]]})
            else:
                clear_screen()
                print(f'Category with ID {id} not found.')
                continue
            
            data_temp = list(temp.values())
            header_temp = list(db1.values())[0]
            clear_screen()
            print(tbl(data_temp, header_temp, tablefmt = "outline"))

            warn = False
            for key, val in db1.items():
                if val[1] == new_category_name:
                    data_warn_temp = db1[key]
                    data_warn += [data_warn_temp]
                    warn = True
            
            if warn == True:
                        print(f"\nWARNING! Category Name already exists in database.")
                        print(tbl(data_warn, header_temp, tablefmt = 'outline'))

            confirm = pyip.inputYesNo(prompt = 'Are you sure you want to change this category name? (yes/no): ')
            if confirm == 'yes':
                db1.update(temp)
            clear_screen()

        if menu_update == 2:
            clear_screen()
            show_categories(db1)
            id = pyip.inputInt(prompt = 'Select Category ID: ')
            exist = select_category(id, db1, db2)

            while exist == True:
                print(PROMPT2)
                submenu_update = pyip.inputInt('Choose Menu[1-4]: ', min = 1, max = 4)

                if submenu_update == 1:
                    clear_screen()
                    select_category(id, db1, db2)
                    id2 = pyip.inputInt('Enter Contact ID to edit: ', min = 1)
                    update_contact(id, id2, db1, db2)
                    select_category(id, db1, db2)


                if submenu_update == 2:
                    clear_screen()
                    sort_newest_cat(id, db1, db2)

                if submenu_update == 3:
                    clear_screen()
                    sort_oldest_cat(id, db1, db2)

                if submenu_update == 4:
                    break

        if menu_update == 3:
            clear_screen()
            sort_important(db2)

            while True:
                print(PROMPT2)
                submenu_update = pyip.inputInt('Choose Menu[1-4]: ', min = 1, max = 4)

                if submenu_update == 1:
                    clear_screen()
                    sort_important(db2)
                    id2 = pyip.inputInt('Enter Contact ID to edit: ', min = 1)
                    id = 0
                    for j, val in db2.items():
                        if id2 == val[0]:
                            id = val[5]
                    if id == 0:
                        print(f'Contact with ID {id2} not found.')
                    else:
                        update_contact(id, id2, db1, db2)
                        sort_important(db2)

                if submenu_update == 2:
                    clear_screen()
                    sort_newest(db2)

                if submenu_update == 3:
                    clear_screen()
                    sort_oldest(db2)

                if submenu_update == 4:
                    break

        if menu_update == 4:
            break

def delete():
    clear_screen()
    PROMPT = ''''''