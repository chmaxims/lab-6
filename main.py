import sqlite3
from flask import Flask, render_template_string

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('new_year.db')
    conn.row_factory = sqlite3.Row
    return conn

def add_db(conn):
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS gifts (
                ФИО TEXT NOT NULL,
                Подарок TEXT NOT NULL,
                Стоимость INTEGER NOT NULL,
                Статус TEXT NOT NULL)
                ''')
    cursor.execute("SELECT COUNT(*) FROM gifts LIMIT 1")
    ex = cursor.fetchone() is not None

    if not ex:
        data = [
            ('Иван Иванович', 'Санки', 2000, 'Куплен'),
            ('Ирина Сергеевна', 'Цветы', 3000, 'Не куплен'),
            ('Юлия Анатольевна', 'Книга', 1000, 'Куплен'),
            ('Евгения Викторовна', 'Конфеты', 500, 'Куплен'),
            ('Петр Васильевич', 'Самокат', 5000, 'Не куплен'),
            ('Анна Владимировна', 'Телефон', 10000, 'Не куплен'),
            ('Григорий Петрович', 'Костюм', 4000, 'Куплен'),
            ('Светлана Игоревна', 'Шампанское', 1000, 'Не куплен'),
            ('Максим Викторович', 'Настольная игра', 2500, 'Куплен'),
            ('Ольга Афанасьевна', 'Велосипед', 7000, 'Куплен')
        ]
        cursor.executemany("INSERT INTO gifts (ФИО, Подарок, Стоимость, Статус) VALUES (?, ?, ?, ?)", data)
        conn.commit()

with get_db_connection() as conn:
    add_db(conn)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gifts")
    rows = cursor.fetchall()
    for row in rows:
        print(f"{row['ФИО']} - {row['Подарок']} - {row['Стоимость']} - {row['Статус']}")

@app.route('/')
def index():
    with get_db_connection() as conn:
        gifts = conn.execute('SELECT * FROM gifts').fetchall()

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Список подарков на Новый год</title>
        <style>
            body {
                text-align: center;
            }
            table {
                margin: 0 auto;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 10px;
            }
            th {
                background-color: #97c3b9;
            }
        </style>
    </head>
    <body>
        <h1>Список подарков на Новый год</h1>
        <table>
            <tr>
                <th>ФИО</th>
                <th>Подарок</th>
                <th>Стоимость</th>
                <th>Статус</th>
            </tr>
    """

    for gift in gifts:
        html_content += f"""
        <tr>
            <td>{gift['ФИО']}</td>
            <td>{gift['Подарок']}</td>
            <td>{gift['Стоимость']}</td>
            <td>{gift['Статус']}</td>
        </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    return render_template_string(html_content)


if __name__ == '__main__':
    app.run()