from functions import get_todos, write_todos
import time
time.strftime("%d")

while True:
    user_action = input("Type an option of: add, edit, complete, show, exit:\n ")
    user_action = user_action.strip()

    if user_action.startswith("add"):
        todo = user_action[4:]

        todos = get_todos()

        todos.append(todo + '\n')

        write_todos(todos)

    elif user_action.startswith("edit"):
        try:
            number = int(user_action[5:])
            number = number - 1

            todos = get_todos()

            new_todo = input("Enter a new todo: ")
            todos[number] = new_todo + '\n'

            write_todos(todos)

        except ValueError:
            print(  "Your command is not valid")
            continue

    elif user_action.startswith("complete"):
        try:
            number = int(user_action[9:])
            number = number - 1

            todos = get_todos()

            todo_to_remove = todos[number].strip('\n')
            todos.pop(number)

            write_todos(todos)

            message = f"Todo {todo_to_remove} was completed on {time.strftime("%d/%m/%Y")} at {time.strftime("%H:%M:%S")}"
            print(message)

        except IndexError:
            print("There is not item with that index")
            continue 
            
    elif user_action.startswith("show"):

        todos = get_todos()

        new_todos = [item.strip('\n') for item in todos]

        for index, item  in enumerate(new_todos):
            print(f"{index+1}. {item}")

    elif user_action.startswith("exit"):
        break

    else:
        print("Command not valid")

print("Bye")