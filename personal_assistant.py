import pandas as pd
import json
import os
from datetime import datetime

# Путь к файлам данных
NOTES_FILE = 'data/notes.json'
TASKS_FILE = 'data/tasks.json'
CONTACTS_FILE = 'data/contacts.json'
FINANCE_FILE = 'data/finance.json'


# Проверка существования файлов и создание пустых, если они не существуют
def initialize_files():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(FINANCE_FILE):
        with open(FINANCE_FILE, 'w') as f:
            json.dump([], f)


# Загрузка данных из JSON файла
def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


# Сохранение данных в JSON файл
def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)


# Основное меню приложения
def main_menu():
    print("Добро пожаловать в Персональный помощник!")
    print("Выберите действие:")
    print("1. Управление заметками")
    print("2. Управление задачами")
    print("3. Управление контактами")
    print("4. Управление финансовыми записями")
    print("5. Калькулятор")
    print("6. Выход")


# Функция для управления заметками
def manage_notes():
    notes = load_data(NOTES_FILE)

    while True:
        print("\nУправление заметками:")
        print("1. Добавить заметку")
        print("2. Просмотреть заметки")
        print("3. Просмотреть подробности заметки")
        print("4. Редактировать заметку")
        print("5. Удалить заметку")
        print("6. Импорт заметок из CSV")
        print("7. Экспорт заметок в CSV")
        print("8. Назад")

        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите заголовок заметки: ")
            content = input("Введите содержимое заметки: ")
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            note = {'id': len(notes) + 1, 'title': title, 'content': content, 'timestamp': timestamp}
            notes.append(note)
            save_data(NOTES_FILE, notes)
            print("Заметка добавлена!")

        elif choice == '2':
            for note in notes:
                print(f"{note['id']}: {note['title']} ({note['timestamp']})")

        elif choice == '3':
            note_id = int(input("Введите ID заметки для просмотра: "))
            note = next((n for n in notes if n['id'] == note_id), None)
            if note:
                print(f"Заголовок: {note['title']}\nСодержимое: {note['content']}\nДата: {note['timestamp']}")
            else:
                print("Заметка не найдена.")

        elif choice == '4':
            note_id = int(input("Введите ID заметки для редактирования: "))
            note = next((n for n in notes if n['id'] == note_id), None)
            if note:
                new_title = input(f"Введите новый заголовок (текущий: {note['title']}): ")
                new_content = input(f"Введите новое содержимое (текущее: {note['content']}): ")
                note['title'] = new_title or note['title']
                note['content'] = new_content or note['content']
                note['timestamp'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                save_data(NOTES_FILE, notes)
                print("Заметка обновлена!")
            else:
                print("Заметка не найдена.")

        elif choice == '5':
            note_id = int(input("Введите ID заметки для удаления: "))
            notes = [n for n in notes if n['id'] != note_id]
            save_data(NOTES_FILE, notes)
            print("Заметка удалена!")

        elif choice == '6':
            import_notes()

        elif choice == '7':
            export_notes()

        elif choice == '8':
            break


def import_notes():
    file_name = input("Введите имя CSV-файла для импорта (например, notes.csv): ")
    try:
        df = pd.read_csv(file_name)
        notes = load_data(NOTES_FILE)

        for _, row in df.iterrows():
            note = {
                'id': len(notes) + 1,
                'title': row['title'],
                'content': row['content'],
                'timestamp': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
            notes.append(note)

        save_data(NOTES_FILE, notes)
        print(f"Заметки успешно импортированы из {file_name}.")

    except Exception as e:
        print(f"Ошибка при импорте: {e}")


def export_notes():
    file_name = input("Введите имя CSV-файла для экспорта (например, notes_export.csv): ")
    notes = load_data(NOTES_FILE)

    df = pd.DataFrame(notes)
    df.to_csv(file_name, index=False)

    print(f"Заметки успешно экспортированы в {file_name}.")


# Функция для управления задачами
def manage_tasks():
    tasks = load_data(TASKS_FILE)

    while True:
        print("\nУправление задачами:")
        print("1. Добавить задачу")
        print("2. Просмотреть задачи")
        print("3. Отметить задачу как выполненную")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Импорт задач из CSV")
        print("7. Экспорт задач в CSV")
        print("8. Назад")

        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            priority = input("Введите приоритет (Высокий/Средний/Низкий): ")
            due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ")

            task = {
                'id': len(tasks) + 1,
                'title': title,
                'description': description,
                'done': False,
                'priority': priority,
                'due_date': due_date,
                'timestamp': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }

            tasks.append(task)
            save_data(TASKS_FILE, tasks)
            print("Задача добавлена!")

        elif choice == '2':
            for task in tasks:
                status = "Выполнена" if task['done'] else "Не выполнена"
                print(
                    f"{task['id']}: {task['title']} [{status}] (Приоритет: {task['priority']}, Срок: {task['due_date']})")

        elif choice == '3':
            task_id = int(input("Введите ID задачи для отметки как выполненной: "))
            task = next((t for t in tasks if t['id'] == task_id), None)

            if task:
                task['done'] = True
                save_data(TASKS_FILE, tasks)
                print(f"Задача '{task['title']}' отмечена как выполненная.")

            else:
                print("Задача не найдена.")

        elif choice == '4':
            task_id = int(input("Введите ID задачи для редактирования: "))
            task = next((t for t in tasks if t['id'] == task_id), None)

            if task:
                new_title = input(f"Введите новый заголовок (текущий: {task['title']}): ")
                new_description = input(f"Введите новое описание (текущее: {task['description']}): ")

                task['title'] = new_title or task['title']
                task['description'] = new_description or task['description']

                save_data(TASKS_FILE, tasks)
                print(f"Задача '{task['id']}' обновлена.")

            else:
                print("Задача не найдена.")

        elif choice == '5':
            task_id = int(input("Введите ID задачи для удаления: "))
            tasks = [t for t in tasks if t['id'] != task_id]

            save_data(TASKS_FILE, tasks)
            print(f"Задача с ID '{task_id}' удалена.")

        elif choice == '6':
            import_tasks()

        elif choice == '7':
            export_tasks()

        elif choice == '8':
            break


def import_tasks():
    file_name = input("Введите имя CSV-файла для импорта (например, tasks.csv): ")

    try:
        df = pd.read_csv(file_name)
        tasks = load_data(TASKS_FILE)

        for _, row in df.iterrows():
            task = {
                'id': len(tasks) + 1,
                'title': row['title'],
                'description': row.get('description', ''),
                'done': row.get('done', False),
                'priority': row.get('priority', ''),
                'due_date': row.get('due_date', ''),
                'timestamp': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
            tasks.append(task)

        save_data(TASKS_FILE, tasks)
        print(f"Задачи успешно импортированы из {file_name}.")

    except Exception as e:
        print(f"Ошибка при импорте: {e}")


def export_tasks():
    file_name = input("Введите имя CSV-файла для экспорта (например, tasks_export.csv): ")
    tasks = load_data(TASKS_FILE)

    df = pd.DataFrame(tasks)
    df.to_csv(file_name, index=False)

    print(f"Задачи успешно экспортированы в {file_name}.")


# Функция для управления контактами
def manage_contacts():
    contacts = load_data(CONTACTS_FILE)

    while True:
        print("\nУправление контактами:")
        print("1. Добавить контакт")
        print("2. Поиск контакта")
        print("3. Редактировать контакт")
        print("4. Удалить контакт")
        print("5. Импорт контактов из CSV")
        print("6. Экспорт контактов в CSV")
        print("7. Назад")

        choice = input("Выберите действие: ")

        if choice == '1':
            name = input("Введите имя контакта: ")
            phone = input("Введите номер телефона: ")
            email = input("Введите адрес электронной почты: ")

            contact = {'id': len(contacts) + 1, 'name': name, 'phone': phone, 'email': email}
            contacts.append(contact)
            save_data(CONTACTS_FILE, contacts)
            print(f"Контакт '{name}' добавлен!")

        elif choice == '2':
            search_term = input('Введите имя или номер телефона для поиска контакта: ')
            found_contacts = [c for c in contacts if search_term in c["name"] or search_term in c["phone"]]

            if found_contacts:
                for contact in found_contacts:
                    print(
                        f"{contact['id']}: {contact['name']} (Телефон: {contact['phone']}, Email: {contact['email']})")
            else:
                print('Контакты не найдены.')

        elif choice == '3':
            contact_id = int(input('Введите ID контакта для редактирования: '))
            contact_to_edit = next((c for c in contacts if c["id"] == contact_id), None)

            if contact_to_edit:
                new_name = input(f'Новое имя (текущее "{contact_to_edit["name"]}"): ')
                new_phone = input(f'Новый телефон (текущий "{contact_to_edit["phone"]}"): ')
                new_email = input(f'Новый email (текущий "{contact_to_edit["email"]}"): ')

                contact_to_edit["name"] = new_name or contact_to_edit["name"]
                contact_to_edit["phone"] = new_phone or contact_to_edit["phone"]
                contact_to_edit["email"] = new_email or contact_to_edit["email"]

                save_data(CONTACTS_FILE, contacts)
                print('Контакт обновлён!')
            else:
                print('Контакт не найден.')

        elif choice == "4":
            contact_id = int(input('Введите ID контакта для удаления: '))
            contacts = [c for c in contacts if c["id"] != contact_id]
            save_data(CONTACTS_FILE, contacts)
            print('Контакт удалён!')

        elif choice == "5":
            import_contacts()

        elif choice == "6":
            export_contacts()

        elif choice == "7":
            break


def import_contacts():
    file_name = input('Введите имя CSV-файла для импорта (например contacts.csv): ')

    try:
        df = pd.read_csv(file_name)

        contacts = load_data(CONTACTS_FILE)

        for _, row in df.iterrows():
            contact = {
                "id": len(contacts) + 1,
                "name": row["name"],
                "phone": row.get('phone', ''),
                "email": row.get('email', '')
            }
            contacts.append(contact)

        save_data(CONTACTS_FILE, contacts)
        print(f'Контакты успешно импортированы из {file_name}.')

    except Exception as e:
        print(f'Ошибка при импорте контактов: {e}')


def export_contacts():
    file_name = input('Введите имя CSV-файла для экспорта (например contacts_export.csv): ')
    contacts = load_data(CONTACTS_FILE)

    df = pd.DataFrame(contacts)
    df.to_csv(file_name, index=False)

    print(f'Контакты успешно экспортированы в {file_name}.')


#Функция для управления финансами
def manage_finance():
    finance_records = load_data(FINANCE_FILE)

    while True:
        print("\nУправление финансовыми записями:")
        print("1. Добавить запись")
        print("2. Просмотреть записи")
        print("3. Удалить запись")
        print("4. Импорт записей из CSV")
        print("5. Экспорт записей в CSV")
        print("6. Генерация финансового отчета за период")
        print("7. Назад")

        choice = input("Выберите действие: ")

        if choice == "1":
            amount = float(
                input("Введите сумму операции (положительное число для доходов и отрицательное для расходов): "))
            category = input("Введите категорию операции (например, Еда): ")
            date = input("Введите дату операции (ДД-ММ-ГГГГ): ")
            description = input("Введите описание операции: ")

            record = {
                "id": len(finance_records) + 1,
                "amount": amount,
                "category": category,
                "date": date,
                "description": description,
                "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }

            finance_records.append(record)
            save_data(FINANCE_FILE, finance_records)
            print("Запись добавлена!")


        elif choice == "2":

            filter_choice = input(
                "Фильтровать записи по (1) дате или (2) категории? (нажмите Enter для просмотра всех записей): ")

            if filter_choice == '1':

                start_date = input("Введите начальную дату (ДД-ММ-ГГГГ): ")

                end_date = input("Введите конечную дату (ДД-ММ-ГГГГ): ")

                start_date_obj = datetime.strptime(start_date, "%d-%m-%Y")

                end_date_obj = datetime.strptime(end_date, "%d-%m-%Y")

                filtered_records = [

                    record for record in finance_records

                    if start_date_obj <= datetime.strptime(record["date"], "%d-%m-%Y") <= end_date_obj

                ]

            elif filter_choice == '2':

                category_filter = input("Введите категорию для фильтрации: ")

                filtered_records = [

                    record for record in finance_records

                    if record["category"].lower() == category_filter.lower()

                ]

            else:

                filtered_records = finance_records

            if filtered_records:

                for record in filtered_records:
                    type_record = "Доход" if record["amount"] > 0 else "Расход"

                    amount_str = f"{record['amount']:,.2f}"  # Форматирование суммы с разделением тысяч

                    print(
                        f"{record['id']}: {type_record} ({amount_str}) - Категория: {record['category']}, Дата: {record['date']}")

            else:

                print('Записи не найдены.')

        elif choice == "3":
            record_id = int(input("Введите ID записи для удаления: "))
            finance_records = [r for r in finance_records if r["id"] != record_id]
            save_data(FINANCE_FILE, finance_records)
            print("Запись удалена!")

        elif choice == "4":
            import_finance()

        elif choice == "5":
            export_finance()

        elif choice == "6":
            generate_financial_report(finance_records)

        elif choice == "7":
            break


def generate_financial_report(finance_records):
    start_date = input("Введите начальную дату (ДД-ММ-ГГГГ): ")
    end_date = input("Введите конечную дату (ДД-ММ-ГГГГ): ")

    start_date_obj = datetime.strptime(start_date, "%d-%m-%Y")
    end_date_obj = datetime.strptime(end_date, "%d-%m-%Y")

    filtered_records = [
        record for record in finance_records
        if start_date_obj <= datetime.strptime(record["date"], "%d-%m-%Y") <= end_date_obj
    ]

    total_income = sum(record["amount"] for record in filtered_records if record["amount"] > 0)
    total_expense = sum(record["amount"] for record in filtered_records if record["amount"] < 0)
    balance = total_income + total_expense

    print(f"\nФинансовый отчет за период с {start_date} по {end_date}:")
    print(f"Общий доход: {total_income:.2f} руб.")
    print(f"Общие расходы: {total_expense:.2f} руб.")
    print(f"Баланс: {balance:.2f} руб.")


def import_finance():
    file_name = input('Введите имя CSV-файла для импорта (например finance.csv): ')

    try:
        df = pd.read_csv(file_name)
        finance_records = load_data(FINANCE_FILE)

        for _, row in df.iterrows():
            record = {
                "id": len(finance_records) + 1,
                "amount": row["amount"],
                "category": row.get('category', ''),
                "date": row.get('date', ''),
                "description": row.get('description', ''),
                "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
            finance_records.append(record)

        save_data(FINANCE_FILE, finance_records)
        print(f'Записи успешно импортированы из {file_name}.')

    except Exception as e:
        print(f'Ошибка при импорте записей: {e}')


def export_finance():
    file_name = input('Введите имя CSV-файла для экспорта (например finance_export.csv): ')
    finance_records = load_data(FINANCE_FILE)

    df = pd.DataFrame(finance_records)
    df.to_csv(file_name, index=False)

    print(f'Записи успешно экспортированы в {file_name}.')


# Функция калькулятора
def calculator():
    while True:
        expression = input("\nВведите выражение для вычисления (или введите 'выход' для выхода): ")

        if expression.lower() == "выход":
            break

        try:
            result = eval(expression)
            print(f"Результат: {result}")

        except ZeroDivisionError:
            print("Ошибка: Деление на ноль.")

        except Exception as e:
            print(f"Ошибка при вычислении: {e}")


# Основной цикл приложения
if __name__ == "__main__":
    initialize_files()

    while True:
        main_menu()
        action = input("Выберите действие: ")

        if action == '1':
            manage_notes()

        elif action == '2':
            manage_tasks()

        elif action == '3':
            manage_contacts()

        elif action == '4':
            manage_finance()

        elif action == '5':
            calculator()

        elif action == '6':
            print("Выход из приложения.")
            break

        else:
            print("Неверный выбор, попробуйте снова.")