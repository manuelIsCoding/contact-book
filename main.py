"""
    Contact book
    ~~~~~~~~~~~~~
    Code by: Manuel Rubio © 2020
    Description:
        This is a beginner project, it's a contact book in that use
        a Command Line Interface to create, read, update, and delete
        contacts that will be saved in a database by using SQLite3.
    Lang: es_MX
"""
from typing import List, Tuple, Callable
import os
import sys
import functools
import time
from cli.menu import Menu
from helpers.sqliteconnect import SQLiteConnect


def _create_database(func: Callable) -> Callable:
    """Decorator that creates the `.contacts.db` database if it not exists.
    The decorator is always called when you call the main function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        abs_path = os.path.abspath(os.getcwd()) + '/.contacts.db'
        if not os.path.exists(abs_path):
            with SQLiteConnect(abs_path) as db_connection:
                cursor = db_connection.cursor()
                cursor.execute('CREATE TABLE contacts '
                               '(name, phone_num);')
                db_connection.commit()
        return func(*args, **kwargs)
    return wrapper

def display_all_contacts() -> None:
    """Select all the contacts from the table `contacts` in the database
    and shows they.
    If there are not contacts, just shows `Without contacts`.
    """
    with SQLiteConnect('.contacts.db') as db_connection:
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

def save_contact(name: str, phone_num: str) -> str:
    """Insert a contact with `name` and `phone_num` on table `contacts`
    in database."""
    with SQLiteConnect('.contacts.db') as db_connection:
        cursor = db_connection.cursor()
        cursor.execute('INSERT INTO contacts VALUES (?, ?)',
                       (name, phone_num))
        db_connection.commit()
        return '¡Contacto guardado satisfactoriamente!\n'

def _search_contact(name: str) -> tuple:
    """Internal function used to search a contact using `name`
    parameter."""
    with SQLiteConnect('.contacts.db') as db_connection:
        cur = db_connection.cursor()
        cur.execute('SELECT * FROM contacts WHERE name=:name;',
                    {'name': name})
        contact = cur.fetchone()
        db_connection.commit()
        return contact

def edit_contact(name: str) -> str:
    """Edit the contact found by `name` parameter."""
    contact = _search_contact(name)
    if type(contact) == tuple:
        print('AVISO: Deje la entrada que no desee editar vacía.\n')

        new_name = input('Nuevo nombre: ')
        new_phone_num = input('Nuevo teléfono: ')
        if not new_name.strip():
            new_name = contact[0]
        if not new_phone_num.strip():
            new_phone_num = contact[1]

        with SQLiteConnect('.contacts.db') as db_connection:
            cursor = db_connection.cursor()
            cursor.execute('''
                UPDATE contacts
                SET name=:new_name, phone_num=:new_phone_num
                WHERE name=:name;
            ''', {
                'new_name': new_name,
                'new_phone_num': new_phone_num,
                'name': name})
            db_connection.commit()
            return '¡Contacto editado satisfactoriamente!'
    
    return f'\nContacto "{name}" no encontrado.'

def delete_contact(name: str) -> str:
    """Deletes a contact found by `name` parameter."""
    contact = _search_contact(name)
    if type(contact) == tuple:
        with SQLiteConnect('.contacts.db') as db_connection:
            cursor = db_connection.cursor()
            cursor.execute('DELETE FROM contacts WHERE name=:name',
                          {'name': name})
            db_connection.commit()
            return f'El contacto "{name}" ha sido eliminado.'
    
    return f'\nContacto "{name}" no encontrado.'

@_create_database
def main() -> None:
    """Contains main functionalities and some implementations from
    app modules."""
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
