import pyodbc

database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()

dt = '00:30'

t = cursor.execute("select CONVERT(varchar(15),CAST(? AS TIME),8)", dt).fetchall()

print(t)
