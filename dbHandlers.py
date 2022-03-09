from mysql.connector import MySQLConnection, Error
import mysql.connector
from config import host, USER, passwd, database

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


def any_product(model, cursor, site):

    print(model + ' уже есть')
    cursor.execute(f"SELECT * from products  WHERE model = '{str(model)}' and from_site = '{site}'")
    have = cursor.fetchone()
    return have


def setNull(site):
    conn = create_connection(host, USER, passwd, database)
    cursor = conn.cursor()
    cursor.execute(f'UPDATE products set stock=0 where from_site = "{site}"')
    conn.commit()


def add_product(product):
    conn = create_connection(host, USER, passwd, database)
    cursor = conn.cursor()
    if 'model' in product:
        if product['model']!='':
            have = any_product(product['model'], cursor, 'goldident.ru')
            if have==None:
                sql = "INSERT INTO products (name, price,special_price, images, category, description, sku,model, stock, brend, atribute, from_site) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (product['name'],
                       product['price'],
                       product['special_price'],
                       product['images'],
                       product['category'],
                        product['desc'],
                       product['sku'],
                       product['model'],
                       product['stock'],
                       product['brend'],
                       str(product['atrs']),
                       'goldident.ru')
                cursor.execute(sql, val)
                conn.commit()
                print(product['name']+ ' parsed')
            else:
                cursor.execute(f'UPDATE products set stock="{product["stock"]}", price="{product["price"]}", special_price ="{product["special_price"]}"  WHERE model="{product["model"]}"')
                print(product['name'] + ' updated')
                conn.commit()
    cursor.close()
    conn.close()




# DROP TABLE IF EXISTS `products`;
# CREATE TABLE `products` (
#   `id` int(11) NOT NULL,
#   `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `price` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `special_price` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `images` text COLLATE utf8mb4_unicode_ci NOT NULL,
#   `category1` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `category2` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
#   `sku` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `stock` int(11) NOT NULL,
#   `brend` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `atribute` text COLLATE utf8mb4_unicode_ci NOT NULL,
#   `from_site` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
#   `similar` text COLLATE utf8mb4_unicode_ci NOT NULL,
#   `art` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;