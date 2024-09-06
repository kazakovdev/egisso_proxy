import os
import time
import shutil
import yadisk
from datetime import datetime

folder_path = "out"  # Локальная папка для отслеживания
yandex_folder = "/ЕГИССО"  # Папка на Яндекс.Диске
token = "y0_AgAAAAAiw7rLAAxkDQAAAAEP_cpjAADg-awUMctBJrcfEqrG0K4xkx8NNQ"  # Токен для доступа к Яндекс.Диску
archive_name = "backup_egisso_startdash.zip"  # Имя архива
check_interval = 30 * 60  # Интервал проверки (30 минут)
log_file = "last_modification.txt"  # Файл для хранения времени последней модификации

y = yadisk.YaDisk(token=token)

def get_last_modification_time(folder):
    """Возвращает максимальное время последней модификации файлов в папке."""
    last_mod_time = 0
    for root, dirs, files in os.walk(folder):
        for f in files:
            file_path = os.path.join(root, f)
            mod_time = os.path.getmtime(file_path)
            if mod_time > last_mod_time:
                last_mod_time = mod_time
    return last_mod_time


def load_last_modification(log_file):
    """Загружает время последней модификации из файла."""
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            return float(f.read().strip())
    return 0


def save_last_modification(log_file, mod_time):
    """Сохраняет время последней модификации в файл."""
    with open(log_file, 'w') as f:
        f.write(str(mod_time))


def archive_folder(folder, archive_name):
    """Архивирует папку в zip-файл."""
    shutil.make_archive(archive_name.replace(".zip", ""), 'zip', folder)
    return archive_name


def upload_archive(archive_path, yandex_folder):
    """Загружает архив на Яндекс.Диск."""
    remote_path = os.path.join(yandex_folder, archive_path).replace("\\", "/")

    print(f"Uploading {archive_path} to {remote_path} on Yandex.Disk...")

    with open(archive_path, "rb") as f:
        y.upload(f, remote_path, overwrite=True, timeout=60)

    print(f"{archive_path} uploaded successfully.")


def main():
    """Главная функция"""
    # Загружаем последнее время изменения файлов
    last_modification = load_last_modification(log_file)

    while True:
        print(f"Checking for new files at {datetime.now()}...")

        # Проверяем текущее время последней модификации файлов в папке
        current_modification = get_last_modification_time(folder_path)

        # Если произошли изменения, архивируем и загружаем
        if current_modification > last_modification:
            print("Changes detected, creating new archive...")
            archive_path = archive_folder(folder_path, archive_name)
            upload_archive(archive_path, yandex_folder)

            # Обновляем время последней модификации в файле
            save_last_modification(log_file, current_modification)
        else:
            print("No changes detected, waiting for the next check.")

        print(f"Next check in {check_interval / 60} minutes.")
        time.sleep(check_interval)


if __name__ == "__main__":
    main()