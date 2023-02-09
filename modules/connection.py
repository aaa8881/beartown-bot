import sqlite3


def get_index():
    return get_ticket_data('sequence')[0][0]


def save_index(number: int, ticket, user):
    conn = sqlite3.connect('data/tickets.db')
    cursor = conn.cursor()
    cursor.execute(f'UPDATE sequence SET number = {number}')
    cursor.execute(f'INSERT INTO opened VALUES ("{ticket}", "{user}")')
    conn.commit()
    conn.close()


def get_ticket_data(table: str):
    conn = sqlite3.connect('data/tickets.db')
    cursor = conn.cursor()
    options = cursor.execute(f'SELECT * FROM {table}').fetchall()
    conn.close()
    return options


def delete_ticket_data(table: str, column: str, value: (str, int)):
    conn = sqlite3.connect('data/tickets.db')
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {table} WHERE {column} = "{value}"')
    conn.commit()
    conn.close()
