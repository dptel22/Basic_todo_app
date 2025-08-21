FILEPATH = 'files/todos.txt'


def get_todos(filepath=FILEPATH):
    """
    Read todos from a text file and return them as a list of strings.
    """
    with open(filepath, 'r') as file_local:
        todos_local = file_local.readlines()
    return todos_local


def write_todos(todos_arg, filepath=FILEPATH):
    """
    Write a list of todos to a text file.
    """
    with open(filepath, 'w') as file_local:
        file_local.writelines(todos_arg)

if __name__ == '__main__':
    print("hello ")
    print(get_todos())