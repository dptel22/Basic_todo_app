import functions
import FreeSimpleGUI as sg

label = sg.Text("Type in a todo")
input_box = sg.InputText(tooltip="Enter a todo", key='todo')
add_button = sg.Button("Add")
display_box = sg.Listbox(values=functions.get_todos(), key='todos',
                         enable_events=True, size=[45, 10])
edit_button = sg.Button('Edit')

window = sg.Window('My todo app',
                   layout=[[label], [input_box, add_button], [display_box, edit_button]],
                   font=('Times New Roman', 12))
while True:
    event, values = window.read()

    match event:
        case 'Add':
            todos = functions.get_todos()
            new_todo = values['todo']
            todos.append(new_todo)
            functions.write_todos(todos)
            window['todo'].update('')  # Clear input after adding
            window['todos'].update(functions.get_todos())  # Refresh the listbox

        case 'Edit':
            # Add your edit functionality here
            todo_to_edit = values['todos'][0]
            new_todo = values['todo']

            todos = functions.get_todos()
            index = todos.index(todo_to_edit)
            todos[index] = new_todo

            functions.write_todos(todos)
            window['todos'].update(values=todos)

        case 'todos':
            window['todos'].update(values=values['todos'])

        case sg.WINDOW_CLOSED:  # Fixed: no parentheses
            break

window.close()