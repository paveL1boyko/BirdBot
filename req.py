import os
import subprocess
import sys


def create_virtualenv_and_install_requirements(directory):
    # Имя виртуального окружения
    venv_name = "venv"

    # Путь к виртуальному окружению
    venv_path = os.path.join(directory, venv_name)

    # Создание виртуального окружения
    subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)

    # Установка зависимостей из requirements.txt, если файл существует
    requirements_file = os.path.join(directory, 'requirements.txt')
    if os.path.isfile(requirements_file):
        # Установка зависимостей
        subprocess.run([os.path.join(venv_path, 'bin', 'pip'), 'install', '-r', requirements_file], check=True)
        print(f"Установлены зависимости из {requirements_file} в {directory}")
    else:
        print(f"Файл requirements.txt не найден в {directory}")


def main():
    # Проходим по всем подкаталогам в текущем каталоге
    for entry in os.listdir('.'):
        if os.path.isdir(entry):
            print(f"Обработка каталога: {entry}")
            create_virtualenv_and_install_requirements(entry)


if __name__ == "__main__":
    main()
