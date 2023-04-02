# CS359 Semester Project - Part 3 - Python subprograms
# Phoebe Evans
# Lauren Glaser
# Ty Bergman

import sqlite3
import sys

def create_connection(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    return conn, cursor

def close_connection(conn):
    conn.commit()
    conn.close()

#For query no.1
def findSiteatStreetName(conn, cursor, input):
    cursor.execute("SELECT * " +
                   "FROM Site " +
                   "WHERE UPPER(TRIM(address)) LIKE ?", ('%' + input + '%',))
    
    results = cursor.fetchall()
    
    if results:
        print(f"Sites on street {input}:")
        for row in results:
            print(row)
    else:
        print("No sites were found on this street")
        
    return
 
#For query no.2
def digitaldisplayfromSchedulersystem(conn, cursor, input):
    
    #format input with capital first letter
    input = input.lower()
    input = input.title()

    cursor.execute("SELECT dd.serialNo, dd.modelNo, ts.name " +
                   "FROM DigitalDisplay AS dd " +
                   "JOIN Specializes AS sp ON sp.modelNo = dd.modelNo " +
                   "JOIN TechnicalSupport AS ts ON ts.empID = sp.empID " +
                   "WHERE dd.schedulerSystem = ?", (input,))
    
    results = cursor.fetchall()
 
    if results:
        for row in results:
            print(row)
    else:
        print("No matching digital displays")
        
    return

#For query no.3
def salesmen(conn, cursor):
    cursor.execute("SELECT name, COUNT(name) AS cnt " +
                   "FROM Salesman " +
                   "GROUP BY name " +
                   "ORDER BY name ASC")
   
    results = cursor.fetchall()
   
    if results:
        print("Name                 cnt")
        print("------------------------")
        count = 0
        for row in results:
            count += 1
           
        
        c = 0
        form = [[0 for x in range(3)] for y in range(count)]
        for row in results:
            name, cnt = row
                           
            if cnt > 1:
                cursor.execute("SELECT * FROM Salesman WHERE name = ?", (name,))
                duplicate_salesmen = cursor.fetchall()
                sales = ""
                form[c][0] = name
               
                form[c][1] = cnt
               
                sales = ""
                for salesman in duplicate_salesmen:
                    sId, sName, sGender = salesman
                    sales = sales + (f"({sId},{sName},'{sGender}')")
                form[c][2] = sales  
                c += 1
               
            else:   
                form[c][0] = name
               
                form[c][1] = cnt
                form[c][2] = ""
                c += 1
               
        for row in form:
            print("{:20} {:2} {:20}".format(*row))
               
    else:
        print("No salesmen found")

    return
 
#For query no.4
def findClientsPhoneNumber(conn, cursor, input):

    #format number with hypens if no hyphens present
    if input.isdecimal() and len(input) == 10:
        s1 = input[:3]
        s2 = input[3:6]
        s3 = input[6:]
        input = s1 + '-' + s2 + '-' + s3
    
    # Execute the query
    cursor.execute('SELECT name ' +
                   'FROM Client ' +
                   'WHERE phone=?', (input,))

    # Fetch the results
    results = cursor.fetchall()

    # Check if any results were found and print the name
    if results:
        print(f"Clients with phone number {input}:")
        for row in results:
            name = row[0]
            print(name)
    else:
        print("No clients found with the given phone number")

    return

#For query no.5
def getAdmWorkHoursASC(conn, cursor):
    
    cursor.execute('SELECT A1.empID, A1.name, A2.hours ' +
                    'FROM Administrator AS A1, AdmWorkHours AS A2 ' +
                    'WHERE A1.empID=A2.empID ' +
                    'ORDER BY A2.hours ASC')
    
    results = cursor.fetchall()

    for row in results:
        print(row)

    return

#For query no.6
def findTechnicalSupportSpecialization(conn, cursor, input):

    cursor.execute( 'SELECT A2.name ' +
                    'FROM Specializes AS A1, TechnicalSupport AS A2 ' +
                    'WHERE A1.empID=A2.empID AND A1.modelNo=?', (input,))
    
    results = cursor.fetchall()

    for row in results:
        print(row)

    return

#For query no.7
def orderSalesmanByDecreasingAverageCommissionRate(conn, cursor):
 
    cursor.execute( 'SELECT A1.name, AVG(A2.commissionRate) ' +
                    'FROM Salesman AS A1, Purchases AS A2 ' +
                    'WHERE A1.empID=A2.empID ' +
                    'GROUP BY A1.name ' +
                    'ORDER BY A2.commissionRate DESC ')
    
    results = cursor.fetchall()
 
    for row in results:
        print(row)
 
    return

#For query no.8
def countEmployeeNumbersByRole(conn, cursor):

    cursor.execute( "SELECT 'Administrator' AS Role, COUNT(*) AS cnt " +
                    'FROM Administrator UNION ' +
                    "SELECT 'Salesman' AS Role, COUNT(*) AS cnt " +
                    'FROM Salesman UNION ' +
                    "SELECT 'Technicians' AS Role, COUNT(*) AS cnt " +
                    'FROM TechnicalSupport')

    results = cursor.fetchall()
    
    print("Role           cnt")
    print("-------------")
    
    counter = 0
    x = 0
    for row in results:
        counter += 1
        
    formatter = [[0 for x in range(2)] for y in range(counter)]
    for row in results:
        role, cnt = row
        
        formatter[x][0] = role
        formatter[x][1] = cnt
        
        x += 1
        
    for row in formatter:
            print("{:15} {:1}".format(*row))

 

    return
    

def main():
    # Replace 'your_database.db' with the name of the SQLite database file
    database = 'ABC.db'

    # Establish a connection and create a cursor
    conn, cursor = create_connection(database)

    if len(sys.argv) < 2:
        print("Please provide at least one argument.")
        return

    command = sys.argv[1]
    parameter = None

    if len(sys.argv) > 2:
        parameter = sys.argv[2]

    if command == '1' and parameter != None:
        findSiteatStreetName(conn, cursor, parameter)

    elif command == '2' and parameter != None:
        digitaldisplayfromSchedulersystem(conn, cursor, parameter)

    elif command == '3':
        salesmen(conn, cursor)

    elif command == '4' and parameter != None:
        findClientsPhoneNumber(conn, cursor, parameter)
    
    elif command == '5':
        getAdmWorkHoursASC(conn, cursor)
    
    elif command == '6' and parameter != None:
        findTechnicalSupportSpecialization(conn, cursor, parameter)
    
    elif command == '7':
        orderSalesmanByDecreasingAverageCommissionRate(conn, cursor)

    elif command == '8':
        countEmployeeNumbersByRole(conn, cursor)

    else:
        print("Unknown command.")

    # Commit and close the connection
    close_connection(conn)

if __name__ == '__main__':
    main()