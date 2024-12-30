from flask_login import login_manager
from psycopg2._psycopg import cursor

from database import Database

db = Database(db_name='DMaDBMS', user='postgres', password='password')

class User:
    def __init__(self, id, name, email, phone, password, role_id):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.role_id = role_id
    @staticmethod
    def create(name, email, phone, password, role_id):
        query = "INSERT INTO users (name, email, phone, password, role_id) VALUES (%s, %s, %s, %s, %s)"
        db.execute_query(query, (name, email, phone, password, role_id))

    @staticmethod
    def get_by_email(email):
        query = "SELECT * FROM users WHERE email = %s"
        result = db.fetch_one(query, (email,))
        if result:
            return User(*result)
        return None

    @staticmethod
    def update_user_info(user_id, name, email, phone):
        db.execute_query(
            "CALL update_user_info(%s, %s, %s, %s)",
            (user_id, name, email, phone)
        )

    @staticmethod
    def get_all():
        query = "SELECT * FROM users"
        return db.fetch_all(query)

class Room:
    @staticmethod
    def create(number, category_id, status, capacity):
        query = "INSERT INTO rooms (number, category_id, status, capacity) VALUES (%s, %s, %s, %s)"
        db.execute_query(query, (number, category_id, status, capacity))

    @staticmethod
    def get_all():
        query = "SELECT * FROM rooms"
        return db.fetch_all(query)

    @staticmethod
    def delete(room_id):
        query = "DELETE FROM rooms WHERE id = %s"
        db.execute_query(query, (room_id,))

class Category:
    @staticmethod
    def create(name, cost):
        query = "INSERT INTO categories (name, cost) VALUES (%s, %s)"
        db.execute_query(query, (name, cost))

    @staticmethod
    def get_all():
        query = "SELECT * FROM categories ORDER BY id"
        return db.fetch_all(query)

    @staticmethod
    def delete(category_id):
        query = "DELETE FROM categories WHERE id = %s"
        db.execute_query(query, (category_id,))

class Service:
    @staticmethod
    def create(name, cost):
        query = "INSERT INTO services (name, cost) VALUES (%s, %s)"
        db.execute_query(query, (name, cost))

    @staticmethod
    def get_all():
        query = "SELECT * FROM services"
        return db.fetch_all(query)

    @staticmethod
    def delete(service_id):
        query = "DELETE FROM services WHERE id = %s"
        db.execute_query(query, (service_id,))

class Promo:
    @staticmethod
    def create(code, discount, description, until_date):
        query = "INSERT INTO promos (code, discount, description, until_date) VALUES (%s, %s, %s, %s)"
        db.execute_query(query, (code, discount, description, until_date))

    @staticmethod
    def get_all():
        query = "SELECT * FROM promos"
        return db.fetch_all(query)

    @staticmethod
    def delete(promo_id):
        query = "DELETE FROM promos WHERE id = %s"
        db.execute_query(query, (promo_id,))

class Reservation:
    @staticmethod
    def create_reservation(user_id, room_id, in_date, out_date, promo_id=None, payment_way_id=None):
        db.execute_query(
            "CALL create_reservation(%s, %s, %s, %s, %s, %s)",
            (user_id, room_id, in_date, out_date, promo_id, payment_way_id)
        )

    @staticmethod
    def add_service_to_reservation(reservation_id, service_id):
        db.execute_query(
            "CALL add_service_to_reservation(%s, %s)",
            (reservation_id, service_id)
        )

    @staticmethod
    def get_all():
        query = "SELECT * FROM reservations"
        return db.fetch_all(query)

    @staticmethod
    def get_user_reservations(user_id):
        return db.fetch_all(
            "SELECT * FROM get_user_reservations(%s)",
            (user_id,)
        )

    @staticmethod
    def get_latest_reservation(user_id):
        query = "SELECT * FROM reservations WHERE user_id = %s ORDER BY in_date DESC LIMIT 1"
        return db.fetch_one(query, (user_id,))

class Review:
    @staticmethod
    def create(user_id, text, rate, reservation_id):
        query = "INSERT INTO reviews (user_id, text, rate, reservation_id) VALUES (%s, %s, %s, %s)"
        db.execute_query(query, (user_id, text, rate, reservation_id))

    @staticmethod
    def get_all():
        query = "SELECT * FROM reviews"
        return db.fetch_all(query)

class Journal:
    @staticmethod
    def log_action(user_id, action):
        query = "INSERT INTO journals (user_id, action, date) VALUES (%s, %s, NOW())"
        db.execute_query(query, (user_id, action))

class PaymentWay:
    @staticmethod
    def create(name):
        query = "INSERT INTO payment_ways (name) VALUES (%s)"

class Role:
    @staticmethod
    def create(name):
        query = "INSERT INTO roles (name) VALUES (%s)"
