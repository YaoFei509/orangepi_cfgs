#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error
import sys, os
import time
import cgi

user = 'www'
pwd  = 'www'
#host = 'yfhomeserver.local'
host  = 'localhost'
db   = 'yfhome'

day3 = int(time.time()) - 3000
locs = ['Up Room', 'Up Out 18', 'Fish Zero', 'Down Room Zero' ]
loc_sql = "SELECT id from ds18b20 where location = %s "
temp_sql = "SELECT DATE_FORMAT(from_unixtime(time), '%Y/%m/%e %T') AS mtime, temperature FROM home_temp WHERE location = %s AND time > %s "

datas = []

try:
    cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
    cursor = cnx.cursor()
    #SQL = "INSERT INTO home_temp VALUES (0, %s, 0, %s, %s) "
    
    # for CGI header
    print("Content-type: image/png\n\n")

    # Read data from MySQL
    for l in locs:
    #    print(l)
        try:
            cursor.execute(loc_sql, (l,) )
            row = cursor.fetchone()

        except:
            print("no data")
            continue
            
        try:
            dsid = row[0]
            print(dsid, day3)
            
            cursor.execute(temp_sql, (dsid, day3))
            rows = cursor.fetchall()

            datas.append(rows)
            
        except Error as e:
            print("no temp data", e)
            continue
    

except Error as e:
    print("Error", e)

finally:
    cursor.close()
    cnx.close()
    

for r in datas:
    for row in r:
        print(row)
                
