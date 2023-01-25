import os
import csv
import sqlite3

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'backend', 'foodgram', 'db.sqlite3')
files_folder = os.path.join(base_dir, 'data')

print('base_dir:', base_dir)
print('db_path:', db_path)
print('files_folder:', files_folder)

def load_ingredients(cursor, dictionary_reader):
    to_db = (
        [(row['id'], row['name'], row['measurement_unit'])
            for row in dictionary_reader]
    )
    cursor.execute('DELETE FROM recipes_ingredient;')
    cursor.executemany(
        'INSERT INTO recipes_ingredient (id, name, measurement_unit) VALUES (?, ?, ?);',
        to_db
    )

FILES = {
    'ingredients': load_ingredients,
}


if __name__ == '__main__':
    print('connect to db:', db_path)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for file, loader in FILES.items():
        file_path = os.path.join(files_folder, file + '.csv')
        with open(file_path, 'r', encoding='utf8') as f:
            print('loading from file: {} ...'.format(file))
            dr = csv.DictReader(f, delimiter=';')
            loader(cursor, dr)
            connection.commit()
            print('success!')
            print('')

    connection.close()

