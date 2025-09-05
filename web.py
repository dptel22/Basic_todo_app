import streamlit as st
import functions

todos = functions.get_todos()

def add_todo():
    todo = st.session_state["new_todo"]
    todos.append(todo)
    functions.write_todos(todos)



st.title("My todo app")
st.text("This is app is there to increase your productivity")

for todo in todos:
    st.checkbox(todo)


st.text_input(label='', placeholder='Add new todo', on_change=add_todo, key='new_todo')