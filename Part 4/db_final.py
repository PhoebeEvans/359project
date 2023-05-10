import PySimpleGUI as sg
import sqlite3
import csv, os
import re

# Methods to connect/diconnect the database
def create_connection(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    return conn, cursor

def close_connection(conn):
    conn.commit()
    conn.close()

def display_all_digital_displays(conn, cursor):
    cursor.execute('''SELECT * FROM DigitalDisplay;''')
    results = cursor.fetchall()

    headers = ['Serial No', 'Scheduler System', 'Model No']
    data = []

    for row in results:
        data.append([row[0], row[1], row[2]])

    display_gui = [
        [sg.Text("Digital Displays:")],
        [sg.Table(values=data, headings=headers, display_row_numbers=False, auto_size_columns=True, num_rows=min(25, len(data)), key='table', enable_events=True)],
        [sg.Text("Additional Information: ")],
        [sg.Text("Model No: "), sg.Text("", size=(0, 1), key='modelNo')],
        [sg.Text("Width: "), sg.Text("", size=(0, 1), key='width')],
        [sg.Text("Height: "), sg.Text("", size=(0, 1), key='height')],
        [sg.Text("Weight: "), sg.Text("", size=(0, 1), key='weight')],
        [sg.Text("Depth: "), sg.Text("", size=(0, 1), key='depth')],
        [sg.Text("Screen Size: "), sg.Text("", size=(0, 1), key='screensize')],
        [sg.Button('Return to Menu')]
    ]

    display_window = sg.Window('Digital Displays', display_gui, modal=True, element_justification='c', size=(600, 400))

    while True:
        event, values = display_window.read()

        if event == sg.WIN_CLOSED or event == 'Return to Menu':
            break

        if event == 'table' and values['table']:
            selected_row_index = values['table'][0]  # Get the selected row index
            if selected_row_index is not None:
                selected_row_data = data[selected_row_index]  # Get the data of the selected row
                selected_row_data = selected_row_data[2]

                cursor.execute('''SELECT * FROM Model WHERE modelNo="''' + selected_row_data + '''";''')
                target_results = cursor.fetchall()

                target_results = re.sub(r"[\(\)\[\]\']",'',str(target_results))
                info = target_results.split(',')

                modelNo = info[0]
                display_window["modelNo"].update(value=modelNo)
                width = info[1]
                display_window["width"].update(value=width)
                height = info[2]
                display_window["height"].update(value=height)
                weight = info[3]
                display_window["weight"].update(value=weight)
                depth = info[4]
                display_window["depth"].update(value=depth)
                screenSize = info[5]
                display_window["screensize"].update(value=screenSize)

    display_window.close()
    
def search_digital_displays(conn, cursor):
    data = []
    
    search_gui = [
        [sg.Text('Scheduler system'), sg.Combo(["Smart", "Random", "Virtue"], key='scheduler')],
        [sg.Table(values=data, headings=['Serial No', 'Scheduler System', 'Model No'], display_row_numbers=False, auto_size_columns=True, num_rows=min(25, len(data)), key='table')],
        [sg.Button('Search'), sg.Button('Return to Menu')]
    ]
    
    insert_window = sg.Window('Search Digital Display', search_gui, modal=True, element_justification='c', size=(600, 400))

    while True:
        event, values = insert_window.read()

        if event == sg.WIN_CLOSED or event == 'Return to Menu':
            break

        if event == 'Search':
            schedulerSystem = values['scheduler']
            
            if not schedulerSystem:
                sg.popup('All fields must be filled out!')
                continue
            
            
            data = []
            cursor.execute('''SELECT * FROM DigitalDisplay WHERE schedulerSystem LIKE ?;''', ('%' + schedulerSystem + '%',))
            results = cursor.fetchall()

            
            for row in results:
                data.append([row[0], row[1], row[2]])
            

            insert_window['table'].update(values=data)
            insert_window['table'].update(num_rows=min(25, len(data)))
            insert_window['table'].update(visible=True)

    insert_window.close()
    
def insert_digital_display(conn, cursor):
    cursor.execute('''SELECT * FROM Model;''')
    results = cursor.fetchall()

    list_modelNo = [['Model No']]
    for row in results:
        list_modelNo.append([row[0]])

    insert_gui = [
        [sg.Text('Serial No.'), sg.InputText(key='serialNo')],
        [sg.Text('Scheduler System'), sg.InputText(key='schedulerSystem')],
        [sg.Text('Model No.'), sg.Combo(list_modelNo, key='modelNo')],
        [sg.Table(values=[['', '', '']], headings=['Serial No', 'Scheduler System', 'Model No'], display_row_numbers=False, auto_size_columns=True, num_rows=10, key='table', visible=False)],
        [sg.Button('Insert new Digital Display'), sg.Button('Return to Menu')]
    ]

    insert_window = sg.Window('Insert Digital Display', insert_gui, modal=True, element_justification='c', size=(600, 400))

    while True:
        event, values = insert_window.read()

        if event == sg.WIN_CLOSED or event == 'Return to Menu':
            break

        if event == 'Insert new Digital Display':
            serialNo = values['serialNo']
            schedulerSystem = values['schedulerSystem']
            modelNo = values['modelNo']

            if not serialNo or not schedulerSystem or not modelNo:
                sg.popup('All fields must be filled out!')
                continue

            cursor.execute('''SELECT * FROM DigitalDisplay WHERE SerialNo = ?;''', (serialNo,))
            result = cursor.fetchone()

            if result:
                sg.popup('A Digital Display with the same Serial No. already exists!')
            else:
                modelNo = re.sub(r"[\(\)\[\]\']",'',str(modelNo))
                cursor.execute('''INSERT INTO DigitalDisplay (SerialNo, SchedulerSystem, ModelNo) VALUES (?, ?, ?);''', (serialNo, schedulerSystem, modelNo))
                conn.commit()
                sg.popup('Digital Display added successfully!')

                # Update table with the new Digital Display
                cursor.execute('''SELECT * FROM DigitalDisplay;''')
                results = cursor.fetchall()
                data = [[row[0], row[1], row[2]] for row in results]
                insert_window['table'].update(values=data)
                insert_window['table'].update(visible=True)

    insert_window.close()

def delete_digital_display(conn, cursor):
    cursor.execute('''SELECT * FROM DigitalDisplay;''')
    results = cursor.fetchall()

    data = [['Serial No', 'Scheduler System', 'Model No']]
    for row in results:
        data.append([row[0], row[1], row[2]])

    delete_gui = [
        [sg.Text("Digital Displays:")],
        [sg.Table(values=data, headings=data[0], display_row_numbers=False, auto_size_columns=True, num_rows=min(25, len(data)), key='table', enable_events=True)],
        [sg.Text('Serial No.'), sg.InputText(key='serialNo')],
        [sg.Table(values=[['', '', '']], headings=['Serial No', 'Scheduler System', 'Model No'], display_row_numbers=False, auto_size_columns=True, num_rows=10, key='table1', visible=False)],
        [sg.Table(values=[['', '', '', '', '', '']], headings=['Model No', 'Width', 'Height', 'Weight', 'Depth', 'Screen Size'], display_row_numbers=False, auto_size_columns=True, num_rows=10, key='table2', visible=False)],
        [sg.Button('Delete Digital Display'), sg.Button('Return to Menu')]
    ]

    delete_window = sg.Window('Delete Digital Display', delete_gui, modal=True, element_justification='c', size=(800, 500))

    while True:
        event, values = delete_window.read()

        if event == sg.WIN_CLOSED or event == 'Return to Menu':
            break

        if event == 'table' and values['table']:
            selected_row_index = values['table'][0]  # Get the selected row index
            if selected_row_index is not None:
                selected_row_data = data[selected_row_index]  # Get the data of the selected row
                delete_window['serialNo'].update(selected_row_data[0])

        if event == 'Delete Digital Display':
            serialNo = values['serialNo']

            if not serialNo:
                sg.popup('Serial No. field is empty!')
                continue

            cursor.execute('''SELECT * FROM DigitalDisplay WHERE SerialNo = ?;''', (serialNo,))
            result = cursor.fetchone()

            if not result:
                sg.popup('No Digital Display found with the given Serial No.!')
            else:
                modelNo_to_check = result[2]
                cursor.execute('''DELETE FROM DigitalDisplay WHERE SerialNo = ?;''', (serialNo,))
                conn.commit()
                sg.popup('Digital Display deleted successfully!')

                cursor.execute('''SELECT * FROM DigitalDisplay WHERE ModelNo = ?;''', (modelNo_to_check,))
                results = cursor.fetchall()

                if not results:
                    cursor.execute('''DELETE FROM Model WHERE ModelNo = ?;''', (modelNo_to_check,))
                    conn.commit()
                    sg.popup(f'Model {modelNo_to_check} deleted successfully!')

                # Update table with the new Digital Display
                cursor.execute('''SELECT * FROM DigitalDisplay;''')
                results = cursor.fetchall()
                data = [[row[0], row[1], row[2]] for row in results]
                delete_window['table'].update(values=data)
                delete_window['table'].update(visible=True)

                # Update table2 with the new Model data
                cursor.execute('''SELECT * FROM Model;''')
                results = cursor.fetchall()
                data2 = [[row[0], row[1], row[2], row[3], row[4], row[5]] for row in results]
                delete_window['table2'].update(values=data2)
                delete_window['table2'].update(visible=True)

    delete_window.close()

def update_digital_display(conn, cursor):
    cursor.execute('''SELECT * FROM DigitalDisplay;''')
    results = cursor.fetchall()
    data = [[row[0], row[1], row[2]] for row in results]

    cursor.execute('''SELECT * FROM Model;''')
    results = cursor.fetchall()

    list_modelNo = [['Model No']]
    for row in results:
        list_modelNo.append([row[0]])


    update_gui = [
        [sg.Table(values=data, headings=['Serial No', 'Scheduler System', 'Model No'], display_row_numbers=False, auto_size_columns=True, num_rows=10, key='table', enable_events=True, select_mode='browse')],
        [sg.Text('Selected Serial No.'), sg.InputText(key='selectedSerialNo', disabled=True)],
        [sg.Button('Update Digital Display'), sg.Button('Return to Menu')]
    ]

    update_window = sg.Window('Update Digital Display', update_gui, modal=True, element_justification='c', size=(600, 400))

    while True:
        event, values = update_window.read()

        if event == sg.WIN_CLOSED or event == 'Return to Menu':
            break

        if event == 'table' and values['table']:
            selected_row_index = values['table'][0]  # Get the selected row index
            if selected_row_index is not None:
                selected_row_data = data[selected_row_index]  # Get the data of the selected row
                update_window['selectedSerialNo'].update(selected_row_data[0])

        if event == 'Update Digital Display':
            storedSerialNo = values['selectedSerialNo']

            if not storedSerialNo:
                sg.popup('No row is selected!')
                continue

            selected_row_data = next((row for row in data if row[0] == storedSerialNo), None)

            update_popup_gui = [
                [sg.Text('Serial No.'), sg.InputText(selected_row_data[0], key='serialNo')],
                [sg.Text('Scheduler System'), sg.InputText(selected_row_data[1], key='schedulerSystem')],
                [sg.Text('Model No.'), sg.Combo(list_modelNo, key='modelNo')],
                [sg.Button(f"Update {storedSerialNo}"), sg.Button('Cancel')]
            ]

            update_popup_window = sg.Window('Update Digital Display', update_popup_gui, modal=True, element_justification='c')

            while True:
                popup_event, popup_values = update_popup_window.read()

                if popup_event == sg.WIN_CLOSED or popup_event == 'Cancel':
                    break

                if popup_event == f"Update {storedSerialNo}":
                    serialNo = popup_values['serialNo']
                    schedulerSystem = popup_values['schedulerSystem']
                    modelNo = popup_values['modelNo']

                    if not serialNo or not schedulerSystem or not modelNo:
                        sg.popup('All fields must be filled out!')
                        continue

                    modelNo = re.sub(r"[\(\)\[\]\']",'',str(modelNo))

                    cursor.execute('''UPDATE DigitalDisplay SET SerialNo = ?, SchedulerSystem = ?, ModelNo = ? WHERE SerialNo = ?;''', (serialNo, schedulerSystem, str(modelNo), storedSerialNo))
                    conn.commit()
                    sg.popup('Digital Display updated successfully!')

                    # Update the table with the new Digital Display data
                    cursor.execute('''SELECT * FROM DigitalDisplay;''')
                    results = cursor.fetchall()
                    data = [[row[0], row[1], row[2]] for row in results]
                    update_window['table'].update(values=data)

                    break

            update_popup_window.close()

    update_window.close()

def new_model_window(conn, cursor):
    cursor.execute('''SELECT * FROM Model;''')
    results = cursor.fetchall()

    data = [['Model No', 'Width', 'Height', 'Weight', 'Depth', 'Screen Size']]
    for row in results:
        data.append([row[0], row[1], row[2], row[3], row[4], row[5]])

    modal_gui = [[sg.Table(values=data, headings=['Model No', 'Width', 'Height', 'Weight', 'Depth', 'Screen Size'], display_row_numbers=False, auto_size_columns=True, num_rows=10, key='table', enable_events=True, select_mode='browse')],
                    [sg.Text('Selected Model No.'), sg.InputText(key='selectedSerialNo', disabled=True)],
                    [sg.Button('Add a Model'), sg.Button('Update a Model')],
                    [sg.Button('Return to Menu')]]

    modal_window = sg.Window('Model Menu', modal_gui, modal=True, element_justification='c', size=(600, 400))

    while True:
        event, values = modal_window.read()

        if event == sg.WIN_CLOSED or event == 'Return to Menu':
            break

        if event == 'table' and values['table']:
            selected_row_index = values['table'][0]  # Get the selected row index
            if selected_row_index is not None:
                selected_row_data = data[selected_row_index]  # Get the data of the selected row
                modal_window['selectedSerialNo'].update(selected_row_data[0])

        if event == 'Update a Model':
            storedSerialNo = values['selectedSerialNo']

            if not storedSerialNo:
                sg.popup('No row is selected!')
                continue

            selected_row_data = next((row for row in data if row[0] == storedSerialNo), None)

            update_model_popup_gui = [
                [sg.Text('Model No.'), sg.InputText(selected_row_data[0], key='serialNo')],
                [sg.Text('Width'), sg.InputText(selected_row_data[1], key='width')],
                [sg.Text('Height'), sg.InputText(selected_row_data[2], key='height')],
                [sg.Text('Weight'), sg.InputText(selected_row_data[3], key='weight')],
                [sg.Text('Depth'), sg.InputText(selected_row_data[4], key='depth')],
                [sg.Text('Screen Size'), sg.InputText(selected_row_data[5], key='screen')],
                [sg.Button(f"Update {storedSerialNo}"), sg.Button('Cancel')]
            ]

            update_model_popup_gui = sg.Window('Update Model', update_model_popup_gui, modal=True, element_justification='c')

            while True:
                popup_event, popup_values = update_model_popup_gui.read()

                if popup_event == sg.WIN_CLOSED or popup_event == 'Cancel':
                    break

                if popup_event == f"Update {storedSerialNo}":
                    modelNo = popup_values['serialNo']
                    width = popup_values['width']
                    height = popup_values['height']
                    weight = popup_values['weight']
                    depth = popup_values['depth']
                    screen = popup_values['screen']

                    if not modelNo or not width or not height or not weight or not depth or not screen:
                        sg.popup('All fields must be filled out!')
                        continue

                    cursor.execute('''UPDATE Model SET ModelNo = ?, Width = ?, Height = ?, Weight = ?, Depth = ?, ScreenSize = ? WHERE ModelNo = ?;''', (modelNo, width, height, weight, depth, screen, storedSerialNo))
                    conn.commit()
                    sg.popup('Digital Display updated successfully!')

                    # Update the table with the new Digital Display data
                    cursor.execute('''SELECT * FROM Model;''')
                    results = cursor.fetchall()

                    data = [['Model No', 'Width', 'Height', 'Weight', 'Depth', 'Screen Size']]
                    for row in results:
                        data.append([row[0], row[1], row[2], row[3], row[4], row[5]])
                    modal_window['table'].update(values=data)

                    break

                update_model_popup_gui.close()

        if event == 'Add a Model':
            add_model_popup_gui = [
                [sg.Text('Model No.'), sg.InputText(key='serialNo')],
                [sg.Text('Width'), sg.InputText(key='width')],
                [sg.Text('Height'), sg.InputText(key='height')],
                [sg.Text('Weight'), sg.InputText(key='weight')],
                [sg.Text('Depth'), sg.InputText(key='depth')],
                [sg.Text('Screen Size'), sg.InputText(key='screen')],
                [sg.Button(f"Add"), sg.Button('Cancel')]
                ]

            add_model_popup_window = sg.Window('Add Model', add_model_popup_gui, modal=True, element_justification='c')

            while True:
                event, values = add_model_popup_window.read()

                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break

                if event == 'Add':
                    modelNo = values['serialNo']
                    width = values['width']
                    height = values['height']
                    weight = values['weight']
                    depth = values['depth']
                    screen = values['screen']

                    if not modelNo or not width or not height or not weight or not depth or not screen:
                        sg.popup('All fields must be filled out!')
                        continue

                    cursor.execute('''SELECT * FROM Model WHERE ModelNo = ?;''', (modelNo,))
                    result = cursor.fetchone()

                    if result:
                        sg.popup('A Model with the same Model No. already exists!')
                    else:
                        cursor.execute('''INSERT INTO Model (ModelNo, Width, Height, Weight, Depth, ScreenSize) VALUES (?, ?, ?, ?, ?, ?);''', (modelNo, width, height, weight, depth, screen))
                        conn.commit()
                        sg.popup('Model added successfully!')

                        # Update table with the new Digital Display
                        cursor.execute('''SELECT * FROM Model;''')
                        results = cursor.fetchall()

                        data = [['Model No', 'Width', 'Height', 'Weight', 'Depth', 'Screen Size']]
                        for row in results:
                            data.append([row[0], row[1], row[2], row[3], row[4], row[5]])
                        modal_window['table'].update(values=data)
                    add_model_popup_window.close()

    modal_window.close()


def open_menuGUI(conn, cursor):
    menuGUI = [[sg.Text('Database connection was a success! ', justification='center')],
          [sg.Text('Select an option:  ', justification='center')],
          [sg.Button("                   Display all Digital Displays                   ")],
          [sg.Button("Search all Digital Displays given a scheduler system")],
          [sg.Button("                   Insert a new Digital Display                   ")],
          [sg.Button("                      Delete a Digital Display                    ")],
          [sg.Button("                      Update a Digital Display                    ")],
          [sg.Button("                        Create a new Model                       ")],
          [sg.Button("                     Close Connection and Exit                    ")]]
    menuWindow = sg.Window("Database Menu", menuGUI, modal=True, element_justification='c')
    choice = None
    while True:
        event, values = menuWindow.read()

        if event == sg.WIN_CLOSED or event == "                     Close Connection and Exit                    ":
            break

        # Handle "Display all Digital Displays" button event
        if event == "                   Display all Digital Displays                   ":
            menuWindow.hide()
            display_all_digital_displays(conn, cursor)
            menuWindow.un_hide()
            
            
        # Handle "Display all Digital Displays" button event
        if event == "Search all Digital Displays given a scheduler system":
            menuWindow.hide()
            search_digital_displays(conn, cursor)
            menuWindow.un_hide()

        # Handle "Insert a new Digital Display" button event
        if event == "                   Insert a new Digital Display                   ":
            menuWindow.hide()
            insert_digital_display(conn, cursor)
            menuWindow.un_hide()

        # Handle "Delete a Digital Display" button event
        if event == "                      Delete a Digital Display                    ":
            menuWindow.hide()
            delete_digital_display(conn, cursor)
            menuWindow.un_hide()

        # Handle "Update a Digital Display" button event
        if event == "                      Update a Digital Display                    ":
            menuWindow.hide()
            update_digital_display(conn, cursor)
            menuWindow.un_hide()

        # Handle "Create a new Modal" button event
        if event == "                        Create a new Model                       ":
            menuWindow.hide()
            new_model_window(conn, cursor)
            menuWindow.un_hide()

    menuWindow.close()

def open_newTable(conn, cursor, dbName):
    newTableLayout = [[sg.Text('The Digital Display table does not exist in this database: '), sg.Text(dbName)],
          [sg.Text('Would you like to create the table?')],
          [sg.Button('No', bind_return_key=True), sg.Button('Yes')]]

    tableWindow = sg.Window("Table Exception", newTableLayout, modal=True, element_justification='c')

    while True:
        event, values = tableWindow.read()

        if event == sg.WIN_CLOSED or event == 'No':
            break

        if event == 'Yes':
            cursor.execute( ''' CREATE TABLE DigitalDisplay (
                                    serialNo        CHAR (10) PRIMARY KEY,
                                    schedulerSystem CHAR (10),
                                    modelNo         CHAR (10) REFERENCES Model (modelNo) 
                            ); ''' )
            cursor.execute( ''' CREATE TABLE Model (
                                    modelNo    CHAR (10)      PRIMARY KEY,
                                    width      NUMERIC (6, 2),
                                    height     NUMERIC (6, 2),
                                    weight     NUMERIC (6, 2),
                                    depth      NUMERIC (6, 2),
                                    screenSize NUMERIC (6, 2) 
                            ); ''' )
            results = cursor.fetchall()
            tableWindow.close()
            open_menuGUI(conn, cursor)
    tableWindow.close()

def main():
    sg.theme('Reds')
    working_directory = os.getcwd()

    connectionGUI = [[sg.Text('Browse and select the database: '), sg.Text(size=(15,1))],
          [sg.InputText(key='database-input'),
          sg.FileBrowse(initial_folder=working_directory)],
          [sg.Button('Connect', bind_return_key=True), sg.Button('Exit')]]

    window = sg.Window('Database Connection', connectionGUI)

    # Event method
    while True:
        # This gets the information inputted by the user (prints to the console the results)
        event, dbName = window.read()
        print(event, dbName)

        # Closes the application when the Exit button is selected
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        # Connects the GUI to the database entered by the user
        if event == 'Connect':
            # Connects the database and queries all digital displays in the DigitalDiplay 
            conn, cursor = create_connection(dbName['database-input'])

            try:
                cursor.execute( ''' SELECT * FROM DigitalDisplay;  ''')
                results = cursor.fetchall()
            except sqlite3.OperationalError as e:
                message = e.args[0]
                if message.startswith("no such table"):
                    print("Table 'DigitalDisplays' does not exist")
                    window.hide()
                    open_newTable(conn, cursor, dbName)
                    window.un_hide()
                    continue

            # Checks to see if there are records in the DigitalDisplay table
            if results:
                print("Database Connection Success:")
                print("Digital Displays:")
                for row in results:
                    serialNo = row[0]
                    schedulerSystem = row[1]
                    modelNo = row[2]
                    print(serialNo + "   " + schedulerSystem + "   " + modelNo)
                window.hide()
                open_menuGUI(conn, cursor)
                window.un_hide()
            # If there are no records in the digital display, nothing will happen
            else:
                print("There are no digital displays in the table")
                window.hide()
                open_menuGUI(conn, cursor)
                window.un_hide()

    window.close()

if __name__ == "__main__":
    main()