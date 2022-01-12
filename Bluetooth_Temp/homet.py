#!/usr/bin/python3

import mysql.connector
import sys, os
import time
import cgi

user = 'www'
pwd  = 'www'
#host = 'yfhomeserver.local'
host  = 'localhost'
db   = 'yfhome'

day3 = int(time.time()) - 3000

try:
    cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
    cursor = cnx.cursor()
    #SQL = "INSERT INTO home_temp VALUES (0, %s, 0, %s, %s) "
    
    # for CGI header
    print("Content-type: image/png\n\n")

    locs = ['Up Room', 'Up Out 18', 'Fish Zero', 'Down Room Zero' ]
    loc_sql = "SELECT id from ds18b20 where location = %s "
    temp_sql = "SELECT DATE_FORMAT(from_unixtime(time), '%Y/%m/%e %T') AS mtime, temperature FROM home_temp WHERE location = %s AND time > %d "
    
    for l in locs:
        print(l)
        try:
            cursor.execute(loc_sql, (l,) )
            row = cursor.fetchone()

        except:
            print("no data")
            continue
            
        try:
            dsid = row[0]
            print(dsid, day3)
            
            cursor.execute(temp_sql, (dsid, day3, ))
            rows = cursor.fetchall()

            for row in rows:
                print(row[0])
                
        except:
            print("no temp data")
            continue

except Error as e:
    print("Error", e)

finally:
    cursor.close()
    cnx.close()
    
