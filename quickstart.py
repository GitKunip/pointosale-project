import gspread
import ast

try:
    cred_file = "staff01.json"
    client = gspread.service_account(cred_file)
    database = client.open("Lamoza")

    def daily_balance_check(date):
        expense_database = database.worksheet("SALES | EXPENSES")
        last_date_row = len(expense_database.col_values(1))
        last_balance_row = len(expense_database.col_values(12))
        last_date = expense_database.cell(last_date_row, 1).value
        last_balance = expense_database.cell(last_balance_row, 12).value
        print(last_date)
        print(type(last_date))

    def sales_update(array_to_update):
        # array_to_update should be a list in the following form:
        # array_to_update = ['10/8/2022', '21:22:51', 'Hanif', 'GRABFOOD', 'GF653',
        #                    [[item_1, quantity_1], [item_2, quantity_2], [item_3, quantity_3]], total_sales, payment,
        #                    credit]
        sales_database = database.worksheet("SALES | EXPENSES")
        last_row = sales_database.col_values(6)
        start_row = len(last_row) + 1
        batch_array = [{
            'range': f'A{start_row}:E{start_row}',
            'values': [array_to_update[0:5]],
        }]
        i = 0
        for item, qty in array_to_update[5]:
            batch_array.append({'range': f'F{start_row + i}:G{start_row + i}', 'values': [[item, qty]]})
            i += 1
        batch_array.append({'range': f'H{start_row}', 'values': [[array_to_update[6]]]})
        if array_to_update[7]:
            batch_array.append({'range': f'I{start_row}', 'values': [[array_to_update[7]]]})
        if array_to_update[8]:
            batch_array.append({'range': f'K{start_row}', 'values': [[array_to_update[8]]]})
        sales_database.batch_update(batch_array)
        # Do you need to visually group the items ordered by merging vertically all columns except the items?
        # if start_row != end_row:
        #     sales_database.merge_cells(f'E{start_row}:E{end_row}')

    def expense_update(array_to_update):
        # array_to_update should be a list in the following form:
        # array_to_update = ['10/8/2022', '21:22', 'Hanif', 'EXPENSES', 'BELI GAS', 22000]
        expenses_database = database.worksheet("SALES | EXPENSES")
        last_row = expenses_database.col_values(6)
        start_row = len(last_row) + 1
        batch_array = [{
            'range': f'A{start_row}:D{start_row}',
            'values': [array_to_update[0:4]],
        }, {
            'range': f'F{start_row}',
            'values': [[array_to_update[4]]]
        }, {
            'range': f'J{start_row}',
            'values': [[array_to_update[5]]]
        }]
        expenses_database.batch_update(batch_array)

    def refresh_index(new, old):
        return [i for i, v in enumerate(new) if v != old[i]]

    def fetch_menu_data(menuObject, text, comboBox, refresh=0):
        menu_data = database.worksheet(f'MENU {text}')
        if refresh:
            comboBox.clear()
            menuObject.items = []
            for d in menu_data.get_all_records():
                comboBox.addItem(d['ITEMS'])
                menuObject.items.append(d['ITEMS'])
                menuObject.options[d['ITEMS']] = d['OPTIONS']
                if d['ITEMS'] == 'Extra Topping' or d['ITEMS'] == 'Additional Drinks Package':
                    try:
                        menuObject.prices[d['ITEMS']] = ast.literal_eval(d['PRICES'])
                    except SyntaxError:
                        pass
                else:
                    menuObject.prices[d['ITEMS']] = d['PRICES']
                menuObject.discounts[d['ITEMS']] = d['DISCOUNTS']
            # Below is the accurate way to update the changes but is inefficient
            # data = menu_data.get_all_records()
            # new_items = [d['ITEMS'] for d in data]
            # indices = refresh_index(new_items, menuObject.items)
            # for index in indices:
            #     menuObject.items[index] = new_items[index]

        else:
            for d in menu_data.get_all_records():
                comboBox.addItem(d['ITEMS'])
                menuObject.items.append(d['ITEMS'])
                menuObject.options[d['ITEMS']] = d['OPTIONS']
                if d['ITEMS'] == 'Extra Topping' or d['ITEMS'] == 'Additional Drinks Package':
                    try:
                        menuObject.prices[d['ITEMS']] = ast.literal_eval(d['PRICES'])
                    except SyntaxError:
                        pass
                else:
                    menuObject.prices[d['ITEMS']] = d['PRICES']
                menuObject.discounts[d['ITEMS']] = d['DISCOUNTS']

except:
    print('No Connection')
