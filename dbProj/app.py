from datetime import datetime
from models import User, Room, Category, Service, Promo, Reservation, Review


def main_menu():
    print("1. Войти")
    print("2. Регистрация")
    print("0. Выход")


def admin_menu():
    print("1. Управление номерами")
    print("2. Управление категориями")
    print("3. Управление услугами")
    print("4. Управление промокодами")
    print("5. Просмотр клиентов")
    print("6. Просмотр всех броней")
    print("0. Выход")


def client_menu():
    print("1. Забронировать номер")
    print("2. Подписаться на услуги")
    print("3. Оставить отзыв")
    print("4. Просмотреть историю бронирований")
    print("5. Просмотреть номера")
    print("0. Выход")


def login():
    email = input("Введите email: ")
    password = input("Введите пароль: ")
    user = User.get_by_email(email)

    if user and user.password == password:
        print(f"Добро пожаловать, {user.name}!")
        return user
    else:
        print("Неверный логин или пароль.")
        return None


def register():
    name = input("Введите имя: ")
    email = input("Введите email: ")
    phone = input("Введите телефон: ")
    password = input("Введите пароль: ")
    role_id = int(input("Введите роль (1 - администратор, 2 - клиент): "))
    User.create(name, email, phone, password, role_id)
    print("Регистрация успешна.")


def manage_rooms():
    while True:
        print("\nУправление номерами:")
        print("1. Добавить номер")
        print("2. Просмотреть номера")
        print("3. Удалить номер")
        print("0. Назад")

        choice = input("Выберите действие: ")

        if choice == '1':
            number = int(input("Введите номер: "))
            category_id = int(input("Введите ID категории: "))
            status = input("Введите статус: ")
            capacity = int(input("Введите вместимость: "))
            Room.create(number, category_id, status, capacity)
            print("Номер добавлен.")
        elif choice == '2':
            rooms = Room.get_all()
            print("Список номеров:")
            for room in rooms:
                print(f"ID: {room[0]}, Номер: {room[1]}, Категория ID: {room[2]}, Статус: {room[3]}, Вместимость: {room[4]}")
        elif choice == '3':
            room_id = int(input("Введите ID номера для удаления: "))
            Room.delete(room_id)
            print("Номер удален.")
        elif choice == '0':
            break


def manage_categories():
    while True:
        print("\nУправление категориями:")
        print("1. Добавить категорию")
        print("2. Просмотреть категории")
        print("3. Удалить категорию")
        print("0. Назад")

        choice = input("Выберите действие: ")

        if choice == '1':
            name = input("Введите название категории: ")
            cost = int(input("Введите стоимость: "))
            Category.create(name, cost)
            print("Категория добавлена.")
        elif choice == '2':
            categories = Category.get_all()
            print("Список категорий:")
            for category in categories:
                print(f"ID: {category[0]}, Название: {category[1]}, Стоимость: {category[2]}")
        elif choice == '3':
            category_id = int(input("Введите ID категории для удаления: "))
            Category.delete(category_id)
            print("Категория удалена.")
        elif choice == '0':
            break


def manage_services():
    while True:
        print("\nУправление услугами:")
        print("1. Добавить услугу")
        print("2. Просмотреть услуги")
        print("3. Удалить услугу")
        print("0. Назад")

        choice = input("Выберите действие: ")

        if choice == '1':
            name = input("Введите название услуги: ")
            cost = int(input("Введите стоимость: "))
            Service.create(name, cost)
            print("Услуга добавлена.")
        elif choice == '2':
            services = Service.get_all()
            print("Список услуг:")
            for service in services:
                print(service)
        elif choice == '3':
            service_id = int(input("Введите ID услуги для удаления: "))
            Service.delete(service_id)
            print("Услуга удалена.")
        elif choice == '0':
            break


def manage_promos():
    while True:
        print("\nУправление промокодами:")
        print("1. Добавить промокод")
        print("2. Просмотреть промокоды")
        print("3. Удалить промокод")
        print("0. Назад")

        choice = input("Выберите действие: ")

        if choice == '1':
            code = input("Введите промокод: ")
            discount = int(input("Введите скидку: "))
            description = input("Введите описание: ")
            until_date = input("Введите дату окончания (YYYY-MM-DD): ")
            Promo.create(code, discount, description, until_date)
            print("Промокод добавлен.")
        elif choice == '2':
            promos = Promo.get_all()
            print("Список промокодов:")
            for promo in promos:
                print(promo)
        elif choice == '3':
            promo_id = int(input("Введите ID промокода для удаления: "))
            Promo.delete(promo_id)
            print("Промокод удален.")
        elif choice == '0':
            break

def view_clients():
    clients = User.get_all()
    print("Список клиентов:")
    for client in clients:
        print(f"ID: {client[0]}, Имя: {client[1]}, Email: {client[2]}, Телефон: {client[3]}, Роль ID: {client[4]}")

def view_all_reservations():
    reservations = Reservation.get_all()
    print("Список броней:")
    for reservation in reservations:
        print(reservation)

def subscribe_to_service(user):
    print("Доступные услуги:")
    services = Service.get_all()
    for service in services:
        print(f"ID: {service[0]}, Название: {service[1]}, Стоимость: {service[2]}")

    service_id = int(input("Введите ID услуги, на которую хотите подписаться: "))
    latest_reservation = Reservation.get_latest_reservation(user.id)

    if latest_reservation:
        print(f"Услуга с ID {service_id} добавлена к последней броне (ID: {latest_reservation[0]}).")

        Reservation.add_service_to_reservation(latest_reservation[0], service_id)
    else:
        print("У вас нет активных броней.")


def leave_review(user):
    latest_reservation = Reservation.get_latest_reservation(user.id)

    if latest_reservation:
        content = input("Введите текст отзыва: ")
        rate = int(input("Введите оценку (1-5): "))

        reservation_id = latest_reservation[0]

        Review.create(user.id, content, rate, reservation_id)
        print("Отзыв оставлен на вашу последнюю бронь.")
    else:
        print("У вас нет активных броней, на которые можно оставить отзыв.")


def apply_promo_code(user):
    promo_code = input("Введите промокод: ")
    promo = Promo.get_all()
    for p in promo:
        if p[1] == promo_code:
            print(f"Промокод {promo_code} применен! Скидка: {p[2]}%")
            return
    print("Неверный промокод.")


def book_room(user):
    room_id = int(input("Введите ID номера: "))
    in_date = input("Введите дату заезда (YYYY-MM-DD): ")
    out_date = input("Введите дату выезда (YYYY-MM-DD): ")

    promo_code = input("Введите промокод (если есть): ")
    promo_id = None

    if promo_code:
        promo = Promo.get_all()
        for p in promo:
            if p[1] == promo_code:
                promo_id = p[0]
                print(f"Промокод {promo_code} применен! Скидка: {p[2]}%")
                break

    Reservation.create_reservation(user.id, room_id, in_date, out_date, promo_id, 1)
    print("Номер забронирован.")



def view_reservations(user):
    reservations = Reservation.get_all()
    print("История бронирований:")
    for reservation in reservations:
        if reservation[1] == user.id:
            print(reservation)

def show_rooms():
    rooms = Room.get_all()
    print("Список номеров:")
    for room in rooms:
        print(
            f"ID: {room[0]}, Номер: {room[1]}, Категория ID: {room[2]}, Статус: {room[3]}, Вместимость: {room[4]}")

def main():
    while True:
        main_menu()
        choice = input("Выберите действие: ")

        if choice == '1':
            user = login()
            if user:
                if user.role_id == 2:
                    while True:
                        admin_menu()
                        admin_choice = input("Выберите действие: ")
                        if admin_choice == '1':
                            manage_rooms()
                        elif admin_choice == '2':
                            manage_categories()
                        elif admin_choice == '3':
                            manage_services()
                        elif admin_choice == '4':
                            manage_promos()
                        elif admin_choice == '5':
                            view_clients()
                        elif admin_choice == '6':
                            view_all_reservations()
                        elif admin_choice == '0':
                            break
                elif user.role_id == 1:
                    while True:
                        client_menu()
                        client_choice = input("Выберите действие: ")
                        if client_choice == '1':
                            book_room(user)
                        elif client_choice == '2':
                            subscribe_to_service(user)
                        elif client_choice == '3':
                            leave_review(user)
                        elif client_choice == '4':
                            view_reservations(user)
                        elif client_choice == '5':
                            show_rooms()
                        elif client_choice == '0':
                            break
        elif choice == '2':
            register()
        elif choice == '0':
            break


if __name__ == "__main__":
    main()