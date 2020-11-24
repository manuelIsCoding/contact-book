"""
    Contact book
    ~~~~~~~~~~~~~
    Code by: Manuel Rubio © 2020
    Description:
        This is a beginner project, it's a contact book in that use
        a Command Line Interface to create, read, update, and delete
        contacts that will be saved in a database by using SQLite3.
"""
from typing import List, Tuple
import os
import sys
import sqlite3
import functools
import time
from cli.menu import Menu


def create_database(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        abs_path = os.path.abspath(os.getcwd()) + '/.contacts.db'
        if not os.path.exists(abs_path):
            try:
                db_connection = sqlite3.connect(abs_path)
                cursor = db_connection.cursor()
                cursor.execute('CREATE TABLE contacts '
                               '(name, phone_num);')
                db_connection.commit()
            except sqlite3.Error as err:
                print(err)
            finally:
                if db_connection:
                    db_connection.close()
        return func(*args, **kwargs)
    return wrapper

def display_all_contacts():
    try:
        db_connection = sqlite3.connect('.contacts.db')
        cursor = db_connection.cursor()
        cursor.execute('SELECT * FROM contacts;')
        all_contacts = cursor.fetchall()
        if all_contacts:
            print('Contactos:')
            for id, contact in enumerate(all_contacts):
                name, phone_num = contact
                print(f'{id + 1}: {name} - {phone_num}')
            time.sleep(1)
            print('\n')
        else:
            print('Sin contactos.\n')
        db_connection.commit()
    except sqlite3.Error as err:
        print(err)
    finally:
        if db_connection:
            db_connection.close()

def save_contact(name: str, phone_num: str) -> str:
    try:
        db_connection = sqlite3.connect('.contacts.db')
        cursor = db_connection.cursor()
        cursor.execute('INSERT INTO contacts VALUES (?, ?)',
                       (name, phone_num))
        db_connection.commit()
        return '¡Contacto guardado satisfactoriamente!\n'
    except sqlite3.Error as err:
        return err
    finally:
        if db_connection:
            db_connection.close()        

def _search_contact(name: str) -> tuple:
    try:
        conn = sqlite3.connect('.contacts.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM contacts WHERE name=:name;',
                    {'name': name})
        contact = cur.fetchone()
        conn.commit()
        return contact
    except sqlite3.Error as err:
        return err
    finally:
        if conn:
            conn.close()

def edit_contact(name: str) -> str:
    contact = _search_contact(name)
    if type(contact) == tuple:    
        print('AVISO: Deje la entrada que no desee editar vacía.\n')
        new_name = input('Nuevo nombre: ')
        new_phone_num = input('Nuevo teléfono: ')
        if not new_name:
            new_name = contact[0]
        elif not new_phone_num:
            new_phone_num = contact[1]

        try:
            db_connection = sqlite3.connect('.contacts.db')
            cursor = db_connection.cursor()
            cursor.execute('''
                UPDATE contacts
                SET name=?, phone_num=?
                WHERE name=?;
            ''', (new_name, new_phone_num, name))
            db_connection.commit()
            return '¡Contacto editado satisfactoriamente!'
        except sqlite3.Error as err:
            return err
        finally:
            if db_connection:
                db_connection.close()
    
    return f'\nContacto "{name}" no encontrado.'

def delete_contact(name: str) -> str:
    contact = _search_contact(name)
    if type(contact) == tuple:
        try:
            db_connection = sqlite3.connect('.contacts.db')
            cursor = db_connection.cursor()
            cursor.execute('DELETE FROM contacts WHERE name=:name',
                          {'name': name})
            db_connection.commit()
            return f'El contacto "{name}" ha sido eliminado.'
        except sqlite3.Error as err:
            return err
        finally:
            if db_connection:
                db_connection.close()
    
    return f'\nContacto "{name}" no encontrado.'

@create_database
def main() -> None:
    display_all_contacts()
    cli_options = [
        'Guardar un contacto',
        'Editar un contacto',
        'Eliminar un contacto',
        'Salir'
    ]
    cli_menu = Menu(cli_options)
    cli_menu.display()

    user_option = cli_menu.get_option('Selecciona: ')
    if user_option == cli_options[-1]:
        sys.exit(0)
    elif user_option == cli_options[0]:
        name = input('Nombre: ')
        phone_num = input('Teléfono: ')
        print(save_contact(name, phone_num))
    elif user_option == cli_options[1]:
        display_all_contacts()
        name = input('Nombre del contacto a editar: ')
        print(edit_contact(name))
    elif user_option == cli_options[2]:
        display_all_contacts()
        name = input('Nombre del contacto a eliminar: ')
        print(delete_contact(name))
    
    main()


if __name__ == "__main__":
    main()
