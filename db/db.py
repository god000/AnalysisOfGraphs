import sqlite3
 
conn = sqlite3.connect("mydatabase.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
 
# Создание таблицы
cursor.execute("""CREATE TABLE AUD_USD_H4
              (green_period integer, red_period integer, profit integer,
               count_orders integer, income_points integer, loose_points integer)
           """)

'''cursor.execute("""INSERT INTO albums
                  VALUES ('Glow', 'Andy Hunter', '7/24/2012',
                  'Xplore Records', 'MP3')"""
               )'''
 
# Сохраняем изменения
conn.commit()