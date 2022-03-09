from config import host, USER, passwd, database
from mysql.connector import MySQLConnection, Error
import mysql.connector
import csv

csvfile = 'export.csv'

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        # print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def main():
    row = ['name', 'price', 'special_price', 'images', 'category1','category2','description','sku','stock','brend','from_site','similar',]
    for x in range(50):
        row.append('atr'+str(x))
    # print(row)
    conn = create_connection(host, USER, passwd, database)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from products")
    products = cursor.fetchall()
    with open(csvfile, "w", newline='' , encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(row)  # write headers

        for cur in products:
            line = []
            line.append(cur[1])
            line.append(cur[2])
            line.append(cur[3])
            line.append(cur[4])
            line.append(cur[5])
            line.append(cur[6])
            line.append(cur[7].replace('\n', ' '))
            line.append(cur[8])
            line.append(cur[9])
            line.append(cur[10])
            line.append(cur[12])
            line.append(cur[13])
            arr_attr = cur[11].replace('[', '').replace(']', '').split(',')
            for attr in arr_attr:
                line.append(attr)
            csv_writer.writerow(line)
            # print(line)



if __name__ == '__main__':
    main()

