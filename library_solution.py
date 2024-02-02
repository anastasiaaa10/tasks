from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import argparse
import json


class TaskStatus(Enum):
    New = 'новая'
    Processing = 'выполняется'
    Review = 'ревью'
    Completed = 'выполнено'
    Canceled = 'отменено'

@dataclass
class Task:
    title: str
    description: str
    status: TaskStatus
    established: str
    status_change_time: str


class TaskManager:
    def __init__(self, tasks=None):
        self.tasks = tasks or []

    def add_task(self, task):
        self.tasks.append(task)

    def change_task_status(self, task, new_status):
        task.status = new_status
        task.status_change_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_tasks_in_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            tasks_data = [vars(task) for task in self.tasks]
            json.dump(tasks_data, file, ensure_ascii=False)

    def load_tasks_from_file(self, filename):
        with open(filename, 'r') as file:
            tasks_data = json.load(file)
            self.tasks = [Task(**data) for data in tasks_data]

def main():
    parser = argparse.ArgumentParser(description='Управление задачами в менеджере задач.')
    # Добавляю аргумент
    parser.add_argument('file', metavar='file', type=str, help='Имя файла для сохранения или загрузки задач')
    # Парсим аргументы
    args = parser.parse_args()
    # Сам файл
    with open('tasks.json', 'r', encoding='utf-8') as file:
        data = file.read()
        if not data.strip():
            with open('tasks.json', 'w') as json_file:
                json.dump([], json_file, ensure_ascii=False)
    try:
        task_manager = TaskManager()
        task_manager.load_tasks_from_file(args.file)
        print('Задачи успешно загружены из файла.')
    except FileNotFoundError:
        print('Файл не найден. Создан новый менеджер задач.')

    while True:
        print('\nМеню:')
        print('1. Добавить задачу;')
        print('2. Изменить статус задачи;')
        print('3. Сохранить и выйти.')

        option = input('Выберите действие (1, 2 или 3): ')

        if option == '1':
            title = input('Введите название задачи: ')
            description = input('Введите описание задачи: ')
            status = TaskStatus.New.value
            established = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            status_change_time = established
            new_task = Task(title, description, status, established, status_change_time)
            task_manager.add_task(new_task)
            print('Задача успешно добавлена.')

        elif option == '2':
            if not task_manager.tasks:
                print('(!!!) Нет доступных задач.')
            else:
                for i, task in enumerate(task_manager.tasks):
                    print(f'{i + 1}. {task.title} - {task.status}')
                task_index = input('Выберите номер задачи для изменения статуса: ')
                try:
                    task_index = int(task_index) - 1
                    if 0 <= task_index < len(task_manager.tasks):
                        try:
                            new_status = input('Введите новый статус задачи: ')
                            task_manager.change_task_status(task_manager.tasks[task_index], TaskStatus(new_status).value)
                            print('Статус задачи успешно изменен.')
                        except:
                            print('(!!!) Нет такого статуса. Доступные:\n'
                                  '1. новая;\n'
                                  '2. выполняется;\n'
                                  '3. ревью;\n'
                                  '4. выполнено;\n'
                                  '5. отменено.\n'
                                  '(!!!)')

                    else:
                        print('(!!!) Неверный номер задачи.')
                except:
                    print('(!!!) Введите номер задачи целым числом.')

        elif option == '3':
            task_manager.save_tasks_in_file(args.file)
            print('Задачи сохранены. Завершение работы.')
            break

        else:
            print('(!!!) Неверный выбор. Пожалуйста, выберите действие 1, 2 или 3.')


if __name__ == '__main__':
    main()
