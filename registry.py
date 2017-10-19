# coding: utf-8
from _winreg import *  # NOQA


roots_hives = {
    "HKEY_CLASSES_ROOT": HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_USER": HKEY_CURRENT_USER,
    "HKEY_LOCAL_MACHINE": HKEY_LOCAL_MACHINE,
    "HKEY_USERS": HKEY_USERS,
    "HKEY_PERFORMANCE_DATA": HKEY_PERFORMANCE_DATA,
    "HKEY_CURRENT_CONFIG": HKEY_CURRENT_CONFIG,
    "HKEY_DYN_DATA": HKEY_DYN_DATA
}


def parse_key(key):
    key = key.upper()
    root_hive_name, partial_key = key.split('\\', 1)
    root_hive = roots_hives.get(root_hive_name)

    if not root_hive:
        raise Exception('root hive "{}" was not found'.format(root_hive_name))

    return partial_key, root_hive


def get_values(key, fields, flags=KEY_READ | KEY_WOW64_64KEY):
    partial_key, root_hive = parse_key(key)

    with ConnectRegistry(None, root_hive) as reg:
        with OpenKey(reg, partial_key, 0, flags) as key_object:
            data = {}
            for field in fields:
                try:
                    value, type = QueryValueEx(key_object, field)
                    data[field] = value
                except WindowsError:
                    pass

            return data


def get_value(key, field, flags=KEY_READ | KEY_WOW64_64KEY):
    values = get_values(key, [field], flags)
    return values.get(field)


def set_value(key, field, value, type=REG_SZ,
              flags=KEY_WRITE | KEY_WOW64_64KEY):
    partial_key, root_hive = parse_key(key)
    try:
        with ConnectRegistry(None, root_hive) as reg:
            with OpenKey(reg, partial_key, 0, flags) as key_object:
                try:
                    SetValueEx(key_object, field, 0, type, value)
                    return True
                finally:
                    CloseKey(key_object)
    except WindowsError:
        return False
