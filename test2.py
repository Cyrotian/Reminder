import pyodbc
import datetime as da

database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()
dt = '00:30'
print(type(dt))
dt2 = da.datetime.strptime(dt, "%H:%M")
print(type(dt2))
print('time = ',dt2.strftime("%H:%M:%S") )
print(type(dt2.strftime("%H:%M:%S")))

print(dt2)
t = cursor.execute("select CONVERT(varchar(15),CAST(? AS TIME),8)", dt2).fetchall()

print(t)
