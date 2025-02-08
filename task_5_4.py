'''
Personal helper bot
version: pre-alfa 0.0.4 
'''
import sys
from re import search
from pathlib import Path
from colorama import init, Fore, Back, Style

# Initializing the colorama
init(autoreset=True)

# constants
DB_NAME = './contacts.db'
GREATING = '''
   ____  ____  ____  ____   __   __ _   __   __        
  (  _ \(  __)(  _ \/ ___) /  \ (  ( \ / _\ (  )       
   ) __/ ) _)  )   /\___ \(  O )/    //    \/ (_/\     
  (__)  (____)(__\_)(____/ \__/ \_)__)\_/\_/\____/     
 _  _  ____  __    ____  ____  ____    ____   __  ____ 
/ )( \(  __)(  )  (  _ \(  __)(  _ \  (  _ \ /  \(_  _)
) __ ( ) _) / (_/\ ) __/ ) _)  )   /   ) _ ((  O ) )(  
\_)(_/(____)\____/(__)  (____)(__\_)  (____/ \__/ (__)                                      
'''

HELP = '''
commands:
\thelp | h | ? : this help
\thello : print greetings
\tadd | ad <name> <phone> : add new contact
\tchange | ch <name> <phone> : change contact's phone
\tphone | ph <name> : show phone number of <name>
\tall | a : show all contacts
\tremove | rm <name> : remove contact
\tclear : clear database
\tclose | exit | e : exit
'''


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"\nGive me {Fore.YELLOW}name{Style.RESET_ALL} and {Fore.YELLOW}phone{Style.RESET_ALL} please.\n"
        except KeyError:
            return f"\n{Fore.YELLOW}Give me name please.{Style.RESET_ALL}\n"
        except IndexError:
            pass
        except AttributeError:
            return f"\n{Fore.YELLOW}Give me name and phone please.{Style.RESET_ALL}\n"

    return inner


def dict_sort(contacts: dict, sort_by=0, rvrs=False) -> dict:
    '''
    Dictionary sorting

    Input:
        contacts:           a dictionary for sorting
        sort_by= 0 | 1 :    if sort_by=0 then dictionary will be sorted by keys, 
                            if sort_by=1 dictionary will be sorted by value, default sort_by=0
        rvrs= False | True: forward or reverse direction sorting, default rvrs=False - forward direction

    Output:
        sorted dictionary
    '''

    return dict(sorted(contacts.items(), key=lambda x: x[sort_by].lower(), reverse=rvrs))


def db_is_exist(path) -> bool:
    '''
    Checking the existence of a database file
    '''
    return (True if Path(path).exists() else False)


def clear_contact(contacts: dict):
    '''
    Delete all information from the database
    '''
    contacts.clear()
    return f"\n{Fore.YELLOW}Phone book is empty.{Style.RESET_ALL}\n"


def read_db(db_name, contacts: dict):
    '''
    Reading information from the database
    '''
    with open(db_name, 'r') as db:
        contacts_data = db.readlines()

    for st in contacts_data:
        add_contact(st.split(';'), contacts)


def write_db(db_name, contacts: dict):
    '''
    Writing information to the database
    '''

    contacts = dict_sort(contacts)
    with open(db_name, 'w') as db:
        for name, phone in contacts.items():
            db.writelines(f"{name};{phone}\n")
    return f"\n{Fore.GREEN}The database was updated.{Style.RESET_ALL}\n"


def max_field_length(data: dict):
    """
    Calculating the maximum length among dictionary fields. Preparing for future use
    """
    if not data:
        return 0
    return max(len(str(key)) for key in data.keys())


def normalize_phone(phone_number: str) -> str:
    '''
    Clear the phone number
    '''
    return search(r'-?\d+(\.\d+)?', phone_number).group()


def parse_input(user_input: str):
    '''
    User input processing
    '''
    cmd, *args = user_input.strip().split()
    return cmd.lower(), *args


@input_error
def add_contact(args, contacts: dict):
    '''
    Adding user's information
    '''

    *name_parts, phone = args
    name = " ".join(name_parts).strip()
    phone = normalize_phone(args.pop())

    contacts[name] = phone
    contacts = dict_sort(contacts)

    return f"\n{Fore.GREEN}Contact added.{Style.RESET_ALL}\n"


@input_error
def change_contact(args, contacts: dict):
    '''
    Changing user's information
    '''

    *name_parts, phone = args
    name = " ".join(name_parts).strip()
    phone = normalize_phone(phone)

    contacts[name] = phone
    return f"\n{Fore.GREEN}Contact changed.{Style.RESET_ALL}\n"


def show_contact(args, contacts: dict):
    '''
    Show information about user
    '''
    if not args:
        return f"\n{Fore.YELLOW}Enter correct information: show <name>{Style.RESET_ALL}\n"

    name = " ".join(args).strip()

    return f"\n{name}'s {Fore.WHITE}phone number is {contacts.get(name)}\n" if contacts.get(name) else f"\n'{Fore.RED}{name}{Style.RESET_ALL}' does not exist.\n"


def show_all_contact(contacts: dict):
    '''
    Show all information
    '''
    if not contacts:
        return f"{Fore.YELLOW}Phone book is empty.{Style.RESET_ALL}"

    l = 57
    result = "\n" + "-" * l + "\n"
    result += "|\t" + f"{Fore.GREEN}Name{Style.RESET_ALL}" + \
        "\t\t|\t\t" + f"{Fore.GREEN}Phone{Style.RESET_ALL}" + "\t\t|\n"
    result += "-" * l + "\n"

    for name, phone in contacts.items():
        result += "|\t" + f"{Fore.WHITE}{name}{Style.RESET_ALL}" + str("\t" if len(name) < 8 else "") + \
            "\t|\t" + f"{Fore.YELLOW}{phone}{Style.RESET_ALL}" + \
            str("\t" if len(phone) < 8 else "") + "\t\t|\n"
        result += "-" * l + "\n"

    return result


@input_error
def remove_contact(args, contacts: dict):
    '''
    Removing information about user
    '''

    # *name_parts, phone = args
    name = " ".join(args).strip()

    del contacts[name]

    return f"\n{Fore.GREEN}Contact removed.{Style.RESET_ALL}\n"


def main():
    """
    Main function to execute the script.
    """

    print(f"{Fore.GREEN}{GREATING}{Style.RESET_ALL}")
    print(HELP, "\n")

    contacts = {}

    if db_is_exist(DB_NAME):
        read_db(DB_NAME, contacts)
        contacts = dict_sort(contacts)

    while True:
        user_input = input(
            f"{Fore.WHITE}Enter a command or 'h' for help:{Style.RESET_ALL} ")
        if user_input:
            command, *args = parse_input(user_input)
            command = command.lower().strip()
        else:
            command = "help"

        if command in ["close", "exit", "quit", "e", "q"]:
            if db_is_exist(DB_NAME):
                answer = input(
                    f"\n{Fore.RED}The database exists. Do you want to rewrite all the data? (y/N):{Style.RESET_ALL} ").lower().strip()
            else:
                answer = input(
                    f"\n{Fore.RED}The database not exists. Do you want to create new database? (y/N):{Style.RESET_ALL} ").lower().strip()
            if answer != 'y':
                print(
                    f"\n{Fore.YELLOW}The database was not updated.{Style.RESET_ALL}\n")
            else:
                print(write_db(DB_NAME, contacts))
            break
        elif command in ["help", "h", "?"]:
            print(HELP)
        elif command in ["hello", "h"]:
            print(f"\n{Fore.YELLOW}How can I help you?{Style.RESET_ALL}\n")
        elif command in ["add", "ad"]:
            print(add_contact(args, contacts))
        elif command in ["change", "ch"]:
            print(change_contact(args, contacts))
        elif command in ["phone", "ph", "show", "sh"]:
            print(show_contact(args, contacts))
        elif command in ["all", "a"]:
            print(show_all_contact(contacts))
        elif command in ["remove", "rm"]:
            print(remove_contact(args, contacts))
        elif command == "clear":
            answer = input(
                f"{Fore.RED}Are you sure to clear all data? (y/N):{Style.RESET_ALL} ").lower().strip()
            if answer == "y":
                print(clear_contact(contacts))
                print("\n")
            else:
                print("\n")
        else:
            print(f"\n{Fore.RED}Invalid command.{Style.RESET_ALL}\n")

    print(f"\n{Back.WHITE}Good bye!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
