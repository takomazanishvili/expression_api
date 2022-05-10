import sqlite3
import requests
import json

inp = input("აირჩიეთ სასურველი ოპერაცია: (+, -, *, /, random): ")

op = 'random'

if inp == '+':
    op = 'add'
elif inp == '-':
    op = 'sub'
elif inp == '*':
    op = 'mul'
elif inp == '/':
    op = 'div'

response = requests.get(
    f'https://x-math.herokuapp.com/api/{op}',
    params={
        'max': -1000,
        'min': 1000
    }
)

# task 1
json_data = response.json()

print(response.status_code)
print(json.dumps(dict(response.headers), indent=4))
print(json.dumps(json_data, indent=4))

# task 2
file_name = json_data['expression'].replace('/', 'div').replace('*', 'mul')
f = open(f"{file_name}.json", 'w')
json.dump(json_data, f)
f.close()

# task 3
print(f"{json_data['expression']} = {json_data['answer']}")

# task 4
# ვქმნით ცხრილს თუ უკვე არ არსებობს,
# რომელშიც გამოჩნდება id, პირველი და მეორე რიცხვი, სასურველი არითმეტიკული ოპერაცია და პასუხი.
con = sqlite3.connect('tako.sqlite3')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS expressions
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
              first INTEGER,
              second INTEGER,
              operation VARCHAR (2),
              expression VARCHAR (20),
              answer INTEGER )""")

# ცხრილში ვწერ API-დან მიღებულ ინფორმაციას.
cur.execute('''INSERT INTO expressions (first, second, operation, expression, answer) 
                        VALUES (:first, :second, :operation, :expression, :answer)''', json_data)

con.commit()
con.close()
