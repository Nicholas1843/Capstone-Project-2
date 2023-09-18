from tabulate import tabulate as tbl
import pyinputplus as pyip
import os
import phonenumbers as phone
import datetime
import getpass

username = getpass.getuser()

def clear_screen(): 
    """Function to clear terminal
    """    
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def show_categories(db1):
    """Function to print categories table

    Args:
        db1 (dict): Categories database
    """    
    header_cat = list(db1.values())[0]
    data_cat = list(db1.values())[1:]
    print(tbl(data_cat, header_cat, tablefmt="outline"))

def select_category(id, db1, db2):
    """Function to show contacts inside specified category

    Args:
        id (int): Category index
        db1 (dict): Category database
        db2 (dict): Contact database

    Returns:
        bool: Boolean to only run while loop when category ID exists
        filter (dict): Filtered contacts
    """    
    filter = {}
    category = db1.get(str(id))

    if category: # Run code if category is True (not empty)
        for j, val in db2.items():
            if 'header' in j:
                filter[j] = val
            elif id == val[5]: # Add key-value pair to dictionary if category ID matches
                filter[j] = val
        sort_important(filter)
        return True, filter
    else:
        clear_screen()
        show_categories(db1)
        print(f'Category with ID {id} does not exist.')
        return False, filter

def sort_oldest(db2):
    """Function to sort contact database in ascending index order

    Args:
        db2 (dict): Contact database
    """    
    header_cont = list(db2.values())[0]
    data_cont = list(db2.values())[1:]
    print(tbl(data_cont, header_cont, tablefmt="outline"))

def sort_newest(db2):
    """Function to sort contact database in descending index order

    Args:
        db2 (dict): Contact database
    """    
    db2Keys = list(db2.keys())
    db2Keys.sort(reverse = True)
    sorted_db2 = {}
    for key in db2Keys:
        sorted_db2[key] = db2[key]

    header_sort = list(sorted_db2.values())[0]
    data_sort = list(sorted_db2.values())[1:]
    print(tbl(data_sort, header_sort, tablefmt="outline"))

def sort_newest_cat(id, db1, db2):
    """Function to sort filtered contact database in ascending index order

    Args:
        id (int): Category index
        db1 (dict): Category database
        db2 (dict): Contact database
    """    
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
    """Function to sort filtered contact database in descending index order

    Args:
        id (int): Category index
        db1 (dict): Category database
        db2 (dict): Contact database
    """    
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
        print(f'Category with ID {id} does not exist.')

def sort_important(db2):
    """Function to push important contacts up (default)

    Args:
        db2 (dict): Contact database
    """    
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
    """Function to add contact into database

    Args:
        id (int): Category index
        contact_id (int): Contact index (-1 for looping)
        temp (dict): Temporary database
        db2 (dict): Contact database
        data_warn (dict): Database to show warning if duplicate
    """    
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
    """Function to edit contact

    Args:
        id (int): Category index
        id2 (int): Contact index
        db1 (dict): Category database
        db2 (dict): Contact database
    """    
    edit = ''
    found = False
    for j, val in db2.items():
        if id2 == val[0] and id == val[5]:
            edit = pyip.inputChoice(['Name', 'Email', 'Website', 'Phone Number', 'Category', 'Important'], 
                "What would you like to edit? [Name, Email, Website, Phone Number, Category, Important]: ")
            found = True
    
    if found == False:
        clear_screen()
        select_category(id, db1, db2)
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
            print(f"\nWARNING! Contact already exists in database.")
            print(tbl(data_warn, header_temp, tablefmt = 'outline'))
            pyip.inputStr('Press Enter to return', blank = True)
        else:
            confirm = pyip.inputYesNo(prompt = 'Are you sure you want to edit this contact? (yes/no): ')
            if confirm == 'yes':
                db2.update(temp)
                print(f'{edit} successfully changed')
                pyip.inputStr('Press Enter to return', blank = True)                
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
            print(f'{edit} successfully changed')
            pyip.inputStr('Press Enter to return', blank = True)
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
            print(f'{edit} successfully changed')
            pyip.inputStr('Press Enter to return', blank = True)            
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
            print(f'{edit} successfully changed')
            pyip.inputStr('Press Enter to return', blank = True)            
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
                print(f'{edit} successfully changed')
                pyip.inputStr('Press Enter to return', blank = True)                
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
            print(f'{edit} successfully changed')
            pyip.inputStr('Press Enter to return', blank = True)            
        clear_screen()

def delete_contact(id, id2, db1, db2):
    """Function to delete contact

    Args:
        id (int): Category index
        id2 (int): Contact index
        db1 (dict): Category database
        db2 (dict): Contact database
    """    
    clear_screen()
    select_category(id, db1, db2)
    found = False
    temp = {}
    for j, val in db2.items():
        if id2 == val[0] and id == val[5]:
            temp[str(id2)] = db2[str(id2)]
            found = True

    if found == False:
        clear_screen()
        print(f'Contact with ID {id2} not found inside category.')
    else:
        header_temp = list(db2.values())[0]
        data_temp = list(temp.values())
        clear_screen()
        print(tbl(data_temp, header_temp, tablefmt = "outline"))
        if db2[str(id2)][6] == True:
            print("Warning! You have marked this contact as Important.")
        confirm = pyip.inputYesNo(prompt = 'Are you sure you want to DELETE this contact? (yes/no): ')
        if confirm == 'yes':
            change_description = f"Deleted contact '{list(db2.values())[id2][1]}' from category {list(db1.values())[id][1]}"
            record_change(username, change_description)
            del db2[str(id2)]
            for key, value in db2.copy().items():
                if key == "header":
                    continue
                elif int(key) > id2: 
                    new_key = str(int(key)-1)
                    value[0] = int(new_key)
                    db2[new_key] = value
                    del db2[key]
            db1.update({str(id): [id, list(db1.values())[id][1], list(db1.values())[id][2]-1]})
            print('Contact successfully deleted')
            pyip.inputStr('Press Enter to return', blank = True)
        clear_screen()
    
def show(db1, db2):
    """Function for the Show/Read Menu

    Args:
        db1 (dict): Category database
        db2 (dict): Contact database
    """    
    clear_screen()
    PROMPT = '''
===View Contacts===

1. Select Category
2. Show All Contacts
3. Show Important
4. Back To Main Menu
'''
    PROMPT2 = '''
1. Sort by Newest
2. Sort by Oldest
3. Back'''
    show_categories(db1)

    while True:
        print(PROMPT)
        menu_show = pyip.inputInt(prompt = 'Choose Menu[1-4]: ', min = 1, max = 4)

        if menu_show == 1: # Select category IDc
            clear_screen()
            show_categories(db1)
            id = pyip.inputInt(prompt = 'Select Category ID: ')
            clear_screen()
            exist, filter = select_category(id, db1, db2)

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
                    show_categories(db1)
                    break

        elif menu_show == 2: # Show all contacts
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
                    show_categories(db1)
                    break

        elif menu_show == 3: # Show contacts marked 'Important'
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
                    show_categories(db1)
                    break

        elif menu_show == 4: # Back to main menu
            clear_screen()
            break

def add(db1, db2):
    """Function for the Add/Create Menu

    Args:
        db1 (dict): Category database
        db2 (dict): Contact database
    """    
    clear_screen()
    PROMPT = '''
===Add Contacts===

1. Add New Categories
2. Select Category
3. Back to Main Menu'''

    PROMPT2 = '''
1. Add a contact into the Category
2. Add multiple contacts into the Category
3. Sort by Newest
4. Sort by Oldest
5. Back'''
    show_categories(db1)

    while True:
        print(PROMPT)
        menu_add = pyip.inputInt(prompt = 'Choose Menu[1-3]: ', min = 1, max = 3)

        if menu_add == 1: # Add new category(s)
            clear_screen()

            temp = {}
            add_cat = pyip.inputInt(prompt = 'Enter the number of categories to add: ', min = 0)
            category_id = len(db1) - 1
            data_warn = []
            warn_loop = False
            for i in range(add_cat):
                name = pyip.inputStr('Enter new category name: ').title()
                for key, val in db1.items():
                    if val[1] == name:
                        data_warn_temp = db1[key]
                        data_warn += [data_warn_temp]
                        warn_loop = True
                category_id += 1
                temp.update({str(category_id): [category_id, name, 0]})

            clear_screen()
            header_temp = list(db1.values())[0]
            data_temp = list(temp.values())

            print(tbl(data_temp, header_temp, tablefmt = 'outline'))
            
            if warn_loop == True:
                print(f"\nWARNING! Categories already exists in database.")
                print(tbl(data_warn, header_temp, tablefmt = 'outline'))
            if add_cat > 0:
                confirm = pyip.inputYesNo(prompt = 'Are you sure you want to add these categories? (yes/no): ')
                if confirm == 'yes':
                    db1.update(temp)
                    change_description = f"Added category '{name}'"
                    record_change(username, change_description)
                    print('Category successfully added')
                    pyip.inputStr('Press Enter to return', blank = True)
            clear_screen()
            show_categories(db1)

        if menu_add == 2: # Select category
            clear_screen()
            show_categories(db1)
            id = pyip.inputInt(prompt = 'Select Category ID: ')
            clear_screen()
            exist, filter = select_category(id, db1, db2)

            while exist == True:
                print(PROMPT2)
                submenu_add = pyip.inputInt('Choose Menu[1-3]: ', min = 1, max = 5)
                if submenu_add == 1:
                    clear_screen()
                    temp = {}
                    contact_id = len(db2) -1
                    data_warn = []

                    temp, warn, data_warn, contact_id = add_contact(id, contact_id, temp, db2, data_warn)

                    clear_screen()
                    header_temp = list(db2.values())[0]
                    data_temp = list(temp.values())
                    print(tbl(data_temp, header_temp, tablefmt = "outline"))

                    if warn == True:
                        print(f"\nWARNING! Contact already exists in database.")
                        print(tbl(data_warn, header_temp, tablefmt = 'outline'))
                        pyip.inputStr('Press Enter to return', blank = True)
                    else:
                        confirm = pyip.inputYesNo(prompt = 'Are you sure you want to add this contact? (yes/no): ')
                        if confirm == 'yes':
                            db2.update(temp)
                            db1.update({str(id): [id, list(db1.values())[id][1], list(db1.values())[id][2]+1]})
                            print('Contact successfully added')
                            pyip.inputStr('Press Enter to return', blank = True)
                    clear_screen()
                    select_category(id, db1, db2)

                if submenu_add == 2:
                    clear_screen()
                    temp = {}
                    contact_id = len(db2) -1
                    data_warn = []
                    warn_loop = False

                    add_loop = pyip.inputInt(prompt = 'Enter the number of contacts to add: ', min = 0)
                    for i in range(add_loop):
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

                    if add_loop > 0:
                        confirm = pyip.inputYesNo(prompt = 'Are you sure you want to add these contacts? (yes/no): ')
                        if confirm == 'yes':
                            db2.update(temp)
                            db1.update({str(id): [id, list(db1.values())[id][1], list(db1.values())[id][2]+add_loop]})
                            print('Contacts successfully added')
                            pyip.inputStr('Press Enter to return', blank = True)
                    clear_screen()
                    select_category(id, db1, db2)

                if submenu_add == 3:
                    clear_screen()
                    sort_newest_cat(id, db1, db2)
                
                if submenu_add == 4:
                    clear_screen()
                    sort_oldest_cat(id, db1, db2)

                if submenu_add == 5:
                    clear_screen()
                    show_categories(db1)
                    break

        if menu_add == 3: # Back to main menu
            break

    clear_screen()

def update(db1, db2):
    """Function for the Update Menu

    Args:
        db1 (dict): Category database
        db2 (dict): Contact database
    """    
    clear_screen()
    PROMPT = '''
===Change Contact Details===

1. Change Category Name
2. Select Category
3. Show All Contacts
4. Back To Main Menu'''

    PROMPT2 = '''
1. Change detail of a contact in this category
2. Sort by Newest
3. Sort by Oldest
4. Back'''
    show_categories(db1)

    while True:
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
                show_categories(db1)
                print(f'Category with ID {id} does not exist.')
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
                pyip.inputStr('Press Enter to return', blank = True)
            else:
                confirm = pyip.inputYesNo(prompt = 'Are you sure you want to change this category name? (yes/no): ')
                if confirm == 'yes':
                    db1.update(temp)
                    print('Category name successfully changed')
                    pyip.inputStr('Press Enter to return', blank = True)
            clear_screen()
            show_categories(db1)

        if menu_update == 2:
            clear_screen()
            show_categories(db1)
            id = pyip.inputInt(prompt = 'Select Category ID: ')
            clear_screen()
            exist, filter = select_category(id, db1, db2)

            while exist == True:
                print(PROMPT2)
                submenu_update = pyip.inputInt('Choose Menu[1-4]: ', min = 1, max = 4)

                if submenu_update == 1:
                    clear_screen()
                    select_category(id, db1, db2)
                    id2 = pyip.inputInt('Enter Contact ID to edit: ', min = 1)
                    clear_screen()
                    update_contact(id, id2, db1, db2)
                    select_category(id, db1, db2)

                if submenu_update == 2:
                    clear_screen()
                    sort_newest_cat(id, db1, db2)

                if submenu_update == 3:
                    clear_screen()
                    sort_oldest_cat(id, db1, db2)

                if submenu_update == 4:
                    clear_screen()
                    select_category(id, db1, db2)
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
                        clear_screen()
                        sort_important(db2)
                        print(f'Contact with ID {id2} does not exist.')
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
                    clear_screen()
                    show_categories(db1)
                    break

        if menu_update == 4:
            break

def delete(db1, db2):
    """Function for the Delete Menu

    Args:
        db1 (dict): Category database
        db2 (dict): Contact database
    """    
    clear_screen()
    PROMPT = '''
===Delete Contacts===

1. Select Category
2. Show All Contacts
3. Back to Main Menu
'''
    PROMPT2 = '''
1. Delete a contact in this Category
2. Delete multiple contacts in this Category
3. Sort by Newest
4. Sort by Oldest
5. Back
'''
    PROMPT3 = '''
1. Delete a contact
2. Delete multiple contacts
3. Sort by Newest
4. Sort by Oldest
5. Back'''
    show_categories(db1)

    while True:
        print(PROMPT)
        menu_delete = pyip.inputInt(prompt = 'Choose Menu[1-3]: ', min = 1, max = 3)
        
        if menu_delete == 1:
            clear_screen()
            show_categories(db1)
            id = pyip.inputInt(prompt = 'Select Category ID: ')
            clear_screen()
            exist, filter = select_category(id, db1, db2)

            while exist == True:
                print(PROMPT2)
                submenu_delete = pyip.inputInt('Choose Menu[1-5]: ', min = 1, max = 5)

                if submenu_delete == 1:
                    clear_screen()
                    select_category(id, db1, db2)
                    id2 = pyip.inputInt('Select Contact ID to delete: ', min = 1)
                    delete_contact(id, id2, db1, db2)
                    select_category(id, db1, db2)

                if submenu_delete == 2:
                    clear_screen()
                    exist, filter = select_category(id, db1, db2)
                    del_loop = pyip.inputInt('Enter the number of contacts to delete: ', min = 0)
                    if del_loop > len(filter)-1:
                        clear_screen()
                        select_category(id, db1, db2)
                        print(f'You only have {len(filter)-1} contacts in this category.')
                    else:
                        for i in range(del_loop):
                            id2 = pyip.inputInt('Select Contact ID to delete: ', min = 1)
                            delete_contact(id, id2, db1, db2)

                if submenu_delete == 3:
                    clear_screen()
                    sort_newest_cat(id, db1, db2)

                if submenu_delete == 4:
                    clear_screen()
                    sort_oldest_cat(id, db1, db2)
        
                if submenu_delete == 5:
                    clear_screen()
                    show_categories(db1)
                    break

        if menu_delete == 2:
            clear_screen()
            sort_important(db2)
        
            while True:
                print(PROMPT3)
                submenu_delete = pyip.inputInt('Choose Menu[1-5]: ', min = 1, max = 5)
                
                if submenu_delete == 1:
                    clear_screen()
                    sort_important(db2)
                    id2 = pyip.inputInt('Select Contact ID to delete: ', min = 1)
                    id = 0
                    for j, val in db2.items():
                        if id2 == val[0]:
                            id = val[5]

                    if id == 0:
                        clear_screen()
                        sort_important(db2)
                        print(f'Contact with ID {id2} does not exist.')
                    else:
                        delete_contact(id, id2, db1, db2)
                        sort_important(db2)

                if submenu_delete == 2:
                    clear_screen()
                    sort_important(db2)
                    del_loop = pyip.inputInt('Enter the number of contacts to delete: ', min = 0)
                    if del_loop > len(db2)-1:
                        clear_screen()
                        sort_important(db2)
                        print(f'You only have {len(db2)-1} contacts.')
                    else:
                        for i in range(del_loop):
                            id2 = pyip.inputInt('Select Contact ID to delete: ', min = 1)
                            id = 0
                            for j, val in db2.items():
                                if id2 == val[0]:
                                    id = val[5]                            
                            if id == 0:
                                clear_screen()
                                sort_important(db2)
                                print(f'Contact with ID {id2} does not exist.')
                            else:
                                delete_contact(id, id2, db1, db2)
                                sort_important(db2)

                if submenu_delete == 3:
                    clear_screen()
                    sort_newest(db2)

                if submenu_delete == 4:
                    clear_screen()
                    sort_oldest(db2)

                if submenu_delete == 5:
                    clear_screen()
                    show_categories(db1)
                    break    
            
        if menu_delete == 3:
            break

change_history = []

def record_change(username, description):
    """Function to record change in the history log

    Args:
        username (str): The username of the user making the change
        description (str): Description of the change
    """
    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    change_entry = {
        'timestamp': timestamp,
        'user': username,
        'description': description
    }
    change_history.append(change_entry)


def show_history():
    """Function to display change history
    """
    clear_screen()
    print("=== Change History ===")
    for i in change_history:
        print(f"Timestamp: {i['timestamp']} | User: {i['user']} | Description: {i['description']}")
    pyip.inputStr('Press Enter to return', blank = True)