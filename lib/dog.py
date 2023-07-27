from os import name
import sqlite3
import ipdb

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()



class Dog:
    
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    def create_table():
        sql = """
            CREATE TABLE dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            );
        """

        CURSOR.execute(sql)

    def drop_table():
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()


        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]

    def create(name, breed):
        newDog = Dog(name, breed)
        newDog.save()

        return newDog

    def new_from_db(row):
        newDog = Dog(row[1], row[2])
        newDog.id = row[0]

        return newDog

    def get_all():
        sql = """
            SELECT * FROM dogs;
        """

        results = CURSOR.execute(sql).fetchall()

        dogs = []

        for record in results:
            dog = Dog.create(record[1], record[2])
            dog.id = record[0]
            dogs.append(dog)

        return dogs

    def find_by_name(name):
        sql = """
            SELECT * FROM dogs
            WHERE name = ?;
        """

        res = CURSOR.execute(sql, (name,)).fetchone()

        if res is None:
            return None

        dog = Dog.create(res[1], res[2])
        dog.id = res[0]

        return dog


    def find_by_id(id):
        sql = """
            SELECT * FROM dogs
            WHERE id = ?;
        """

        res = CURSOR.execute(sql, (id,)).fetchone();

        dog = Dog.create(res[1], res[2])
        dog.id = res[0]

        return dog

    def find_or_create_by(name, breed):
        sql = """
            SELECT * FROM dogs
            WHERE name = ? AND
            breed = ?
        """

        res = CURSOR.execute(sql, (name, breed)).fetchone()

        if res is None or len(res) == 0:
            dog = Dog.create(name, breed)
            dog.save()

            res = CURSOR.execute(sql, (name, breed)).fetchone()
            dog.id = res[0]

            return dog
        else:
            dog = Dog.create(res[1], res[2])
            dog.id = res[0]

            return dog

    def update(self):
        sql = """
            UPDATE dogs 
            SET name = ?, breed = ?
            WHERE id = ?;
        """

        CURSOR.execute(sql, (self.name, self.breed, self.id))