import os
import sys
import shutil
import winreg
import argparse


def file_create(file_name):
    # Получаем текущую директорию
    current_directory = os.getcwd()
    print("Текущая директория: " + current_directory)
    print("Создаем файл в данной директории с именем " + file_name)
    open(file_name, "w")
    print("Файл успешно создан!")


def file_delete(file_name):
    current_directory = os.getcwd()
    print("Текущая директория: " + current_directory)
    print("Удаляем файл в данной директории с именем " + file_name)
    if os.path.exists(file_name):
        os.remove(file_name)
        print("Файл успешно удален!")
    else:
        print("Файла с данным именем не существует, удаление файла невозможно")


def file_write(file_name, string):
    # Запись в файл с именем file_name строки str
    current_directory = os.getcwd()
    print("Текущая директория: " + current_directory)
    print("Записываем в файл с именем " + file_name + " строку " + string)
    if os.path.exists(file_name):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(string)
        print("Запись в файл прошла успешно!")
    else:
        print("Файл с заданным именем не существует, запись в файл невозможна")


def file_read(file_name):
    current_directory = os.getcwd()
    print("Текущая директория: " + current_directory)
    print("Читаем данные из файла с именем " + file_name)
    if os.path.exists(file_name):
        print("Данные из файла:\n---------------------------------------------------------------")
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                print(line)
        print("---------------------------------------------------------------")
        print("Чтение из файла прошло успешно!")
    else:
        print("Файл с заданным именем не существует, чтение из файла невозможна")


def file_copy(source, destination):
    # source - путь к изначальному файлу
    # copied - путь, куда нужно скопировать файл
    current_directory = os.getcwd()
    print("Текущая директория: " + current_directory)
    print("Копируем файл по пути " + source + " В файл по пути " + destination)
    if os.path.exists(source):
        try:
            shutil.copy2(source, destination)
            print("Копирование файла прошло успешно!")
        except FileNotFoundError:
            print("Папки для копирования не существует, копирование невозможно")
    else:
        print("Файл с заданным именем не существует, копирование файла невозможна")


def file_rename(source_file_name, new_file_name):
    current_directory = os.getcwd()
    print("Текущая директория: " + current_directory)
    print("Переименовываем файл с именем " + source_file_name + " В файл с именем " + new_file_name)
    if os.path.exists(source_file_name):
        os.rename(source_file_name, new_file_name)
        print("Переименовывание файла прошло успешно!")
    else:
        print("Файл с заданным именем не существует, переименовывание файла невозможна")


def reg_create(hkey, path, key_name):
    # Создает ключ реестра по пути key_name
    try:
        with winreg.OpenKey(hkey, path, 0, access=winreg.KEY_ALL_ACCESS) as key:
            winreg.CreateKey(key, key_name)
        print("Ключ с именем " + key_name + " был успешно создан")
    except FileNotFoundError:
        print("Не удалось создать ключ с именем " + key_name)


def reg_delete(hkey, path, key_name):
    try:
        with winreg.OpenKey(hkey, path, 0, access=winreg.KEY_ALL_ACCESS) as key:
            winreg.DeleteKey(key, key_name)
        print("Ключ с именем " + key_name + " успешно удален")
    except FileNotFoundError:
        print("Не удалось удалить ключ с именем " + key_name)
        print("Ключа с заданным именем не существует")


def reg_write(hkey, path, key_name,
              param):
    try:
        with winreg.OpenKey(hkey, path, 0, access=winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, param)
        print("Запись значения в реестр прошла успешно")
    except FileNotFoundError:
        print("Не удалось записать значение ключа реестра, ключа с данным именем не существует")


# Создание файла (--file_create || -fc)
# Удаление файла (--file_remove || -frm)
# Запись в файл (--file_write || -fw)
# Чтение из файла (--file_read || -frd)
# Копирование файла (--file_copy || -fcp)
# Переименование (--file_rename || -frn)


def create_parser():
    parser = argparse.ArgumentParser(description="File system and registry management")

    parser.add_argument("--file_create", "-fc", nargs=1, default=None,
                        help="Creating file with the specified name",
                        metavar='<filename>')
    parser.add_argument("--file_remove", "-frm", nargs=1, default=None,
                        help="Deleting file with the specified name",
                        metavar='<filename>')
    parser.add_argument("--file_write", "-fw", nargs=2, default=None,
                        help="Writes the entered string to a file <filename>",
                        metavar=('<filename>', '<string>')
                        )
    parser.add_argument("--file_read", "-frd", nargs=1, default=None,
                        help="Prints text from file <filename>",
                        metavar="<filename>")
    parser.add_argument("--file_copy", "-fcp", nargs=2, default=None,
                        help="Copies file from <source filename> to <destination filename>",
                        metavar=("<source_filename>", "<destination_filename>")
                        )
    parser.add_argument("--file_rename", "-frn", nargs=2, default=None,
                        help="Renames file <filename> to <new_filename>",
                        metavar=("<filename>", "<new_filename>")
                        )
    parser.add_argument("--reg_create", "-rc", nargs=3, default=None,
                        help="Creates a key in the registry path <path> with the name <key_name>",
                        metavar=("<HKEY>(HKEY_CLASSES_ROOT = 1, HKEY_CURRENT_USER = 2,"
                                 "HKEY_LOCAL_MACHINE = 3, HKEY_USERS = 4, HKEY_CURRENT_CONFIG = 5)",
                                 "<path>", "<key_name>")
                        )
    parser.add_argument("--reg_delete", "-rd", nargs=3, default=None,
                        help="Deletes a key in the register at <path> with the name <key_name>",
                        metavar=("<HKEY>(HKEY_CLASSES_ROOT = 1, HKEY_CURRENT_USER = 2,"
                                 "HKEY_LOCAL_MACHINE = 3, HKEY_USERS = 4, HKEY_CURRENT_CONFIG = 5)",
                                 "<path>", "<key_name>")
                        )
    parser.add_argument("--reg_write", "-rw", nargs=4, default=None,
                        help="Writes <value> value to registry <path> with <key_name> key",
                        metavar=("<HKEY>(HKEY_CLASSES_ROOT = 1, HKEY_CURRENT_USER = 2,"
                                 "HKEY_LOCAL_MACHINE = 3, HKEY_USERS = 4, HKEY_CURRENT_CONFIG = 5)",
                                 "<path>", "<key_name>", "<value>")
                        )

    return parser


def get_hkey(num):
    if int(num) == 1:
        return winreg.HKEY_CLASSES_ROOT
    elif int(num) == 2:
        return winreg.HKEY_CURRENT_USER
    elif int(num) == 3:
        return winreg.HKEY_LOCAL_MACHINE
    elif int(num) == 4:
        return winreg.HKEY_USERS
    elif int(num) == 5:
        return winreg.HKEY_CURRENT_CONFIG
    else:
        return -1


def choose_action(args):
    if args.file_create:
        file_create(args.file_create[0])
    elif args.file_remove:
        file_delete(args.file_remove[0])
    elif args.file_write:
        file_write(args.file_write[0], args.file_write[1])
    elif args.file_read:
        file_read(args.file_read[0])
    elif args.file_copy:
        file_copy(args.file_copy[0], args.file_copy[1])
    elif args.file_rename:
        file_rename(args.file_rename[0], args.file_rename[1])
    elif args.reg_create:
        hkey = get_hkey(args.reg_create[0])
        if hkey == -1:
            print("Данные введены неправильно...")
            return
        else:
            reg_create(hkey, args.reg_create[1], args.reg_create[2])
    elif args.reg_delete:
        hkey = get_hkey(args.reg_delete[0])
        if hkey == -1:
            print("Данные введены неправильно...")
            return
        else:
            reg_delete(hkey, args.reg_delete[1], args.reg_delete[2])
    elif args.reg_write:
        hkey = get_hkey(args.reg_write[0])
        if hkey == -1:
            print("Данные введены неправильно...")
            return
        else:
            reg_write(hkey, args.reg_write[1], args.reg_write[2], args.reg_write[3])
    else:
        print("Ошибка считывания ключей командной строки")
        return


if __name__ == '__main__':
    print()
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    choose_action(args)
