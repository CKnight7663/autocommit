from film_person import *
from film_list_database import *
def set_film(user_name):
    film_name = input("Name > ")
    if film_name in film_list:
        print("ERROR: 002\n'Item is already listed'")
        set_film("user_name")
    else:
        film_genre = input("Genre > ")
        film_importance = input("Importance > ")
        fw = open("film_list_database.py", "a")
        fw.write("\nfilm_list['%s'] = '%s'" % (film_name, film_importance))
        if film_genre in film_genre_list:
            pass
        else:
            fw.write("\nfilm_genre_list.append('%s')" % (film_genre))
        fw.write("\nfilm_genre_dict['%s'] = '%s'\n" % (film_name, film_genre))
        fw.close()
        master_function(user_name)  

def master_function(user):
    if type(user) == str:
        pass
    else:
        user = log_function()
    function_request = input(">>> ")
    if function_request == "add":
        set_film("user_name")
    elif function_request == "append":
        film_append(user)    
    elif function_request == "print":
        print_films(user)
    elif function_request == "end":
        exit()
    elif function_request == "person":
        set_person(0)
    elif function_request == "relog":
        master_function(0)
    else:
        print("ERROR: 001\nUnkown Fuction Call")
        master_function(user)

def film_append(user):
    film = input("Film to append > ")
    fw = open("film_person.py", 'a')
    fw.write("\n{}_list.append('{}')".format(user.lower(), film))
    fw.close()
    master_function(user)

def print_films(user):
    for i in range(100):
        for k, v in film_list.items():
            z = 100 - i
            if int(v) == z:
                #if k in  
                
                print(k)
    master_function(user)

def set_person(user_name):
    if user_name == 0:
        person_name = (input("Name > "))
    else:
        person_name = user_name
    fa = open("film_person.py", "a")
    fa.write("\n%s_list = [" % ((person_name).lower()))
    fa.close()
    count = 0
    for i in film_list:
        film_check(i, count)
        count = 1
    fa = open("film_person.py", "a")
    fa.write("]\n")
    fa.write("user_list.append('%s')\n\n" % (person_name))
    fa.close()
    master_function(user_name)

def film_check(i, count):
    fc = open("film_person.py", "a")
    check = input(i + " > ")
    if check == "y":
        if count == 0:
            fc.write("'" + i + "'")
        else:
            fc.write(", " + "'" + i + "'")

    elif check == "n":
        pass
    else:
        print("ERROR: 003\nInvalid answer (y/n)\n")
        film_check(i, count)
    fc.close()
        
def log_function():
    user_name = input("User >>> ")
    if user_name in user_list:
        pass
    else:
        print("ERROR: 004\nInvalid User\n")
        log_conditon = 1
        while log_conditon == 1:
            user_creation_check = input("Create a user ? ") 
            if user_creation_check == "y":
                log_conditon = 0
                set_person(user_name)
            elif user_creation_check == "n":
                log_conditon = 0
                log_function()
            else:
                print("ERROR: 003\nInvalid answer (y/n)\n")
    #user_list = eval(eval(user_name.lower())_list)
        

master_function(0)