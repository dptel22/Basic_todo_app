import streamlit as st
import functions

todos = functions.get_todos()

st.title("My todo app")
st.text("This is app is there to increase your productivity")

for todo in todos:
    st.checkbox(todo)


st.text_input(label='', placeholder='Add new todo')