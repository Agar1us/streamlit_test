import streamlit as st
import pandas as pd
import numpy as np
import time
from termcolor import colored
import base64

import streamlit_scrollable_textbox as stx
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
import bcrypt
import os

st.set_page_config(layout="wide")

# Set up database using SQLAlchemy
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Spectral:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inknut+Antiqua:wght@300;400;500;600;700&display=swap');
    [data-testid="stTabs"] {background-color: rgba(0, 0, 0, 0.6); border-radius: 15px; padding-left: 20px; padding-right: 20px; padding-top: 20px; padding-bottom: 20px;};
    [data-testid="stHorizontalBlock"] {justify-content:center;};
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, 
    unsafe_allow_html=True
) 

_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""

def response_generator(userq):
    # st.markdown("""
    #             <div class="Thoth" style="font-family: Inknut Antiqua; font-weight: 600; line-height: 14px; word-wrap: break-word; ">THOTH</div></br>"""
    #             , unsafe_allow_html=True)    
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)
    
    yield f'\n'


# Helper functions for authentication
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def register_user(username, password):
    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password)
    session.add(new_user)
    session.commit()

def authenticate_user(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and check_password(user.password, password):
        return True
    return False

# Function to apply background image
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        # encoded_image = image_file.read()
        main_bg_ext = "png"
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(image_path, "rb").read()).decode()});
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

def login_page():
    username = st.text_input("Имя пользователя", key='auth_user')
    password = st.text_input("Пароль", type="password", key='auth_pass')
    if st.button("Войти"):
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Авторизация выполнена успешно!")
            st.rerun()
            st.rerun()
        else:
            st.error("Неверное имя пользователя или пароль")

def register_page():
    username = st.text_input("Имя пользователя", key='reg_user')
    password = st.text_input("Пароль", type="password", key='reg_pass')
    if st.button("Зарегистрироваться"):
        if session.query(User).filter_by(username=username).first():
            st.error("Имя пользователя уже существует")
        else:
            register_user(username, password)
            st.success("Регистрация прошла успешно! Пожалуйста, войдите в систему.")
            st.rerun()
            st.rerun()

# Main application logic
def main():
    # Sidebar control
    add_bg_from_local("background.png")
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        col_empty_1, col3, col_empty_2 = st.columns([1, 2, 1], gap='medium', vertical_alignment="top")
        with col3:
            tab1, tab2 = st.tabs(["Логин", "Регистрация"])
            with tab1:
                st.write('Рады видеть!')
                login_page()
            with tab2:
                st.write('Давайте знакомиться!')
                register_page()

    else:
        # User is logged in
        logged_sidebar = st.sidebar
        logged_sidebar.title(f"Привет, {st.session_state.username}!")
        logged_sidebar.title('')
        
        welcome_state = logged_sidebar.button('О решении')
        solution_state = logged_sidebar.button('Чат-бот')
        
        if welcome_state:
                st.session_state.solution_page = False
        if solution_state:
            st.session_state.solution_page = True
        
        # Welcome Page
        if 'solution_page' not in st.session_state:
            st.session_state.solution_page = False
        
        if not st.session_state.solution_page:
            # Add background image (you can set different images for different pages)
            add_bg_from_local("background.png")
            
            col_wel_1, col_wel_2,col_wel_3 = st.columns([1, 2, 1], gap='large')
            # Create text with a custom app title
            with col_wel_2:
                st.markdown('''
                    <div class="Section1" style="width: 704px; height: 141px; flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 16px; display: inline-flex">
                    <div class="StColums" style="flex-direction: column; justify-content: flex-start; align-items: flex-start; display: flex">
                        <div class="StTitle" style="width: 704px; justify-content: flex-start; align-items: flex-start; gap: 10px; display: inline-flex">
                        <div class="Body" style="flex: 1 1 0; color: white; font-size: 80px; font-family: Spectral; font-weight: 400; text-transform: uppercase; line-height: 80px; letter-spacing: 4px; word-wrap: break-word">Thoth</div>
                        </div>
                        <div class="StWrite" style="width: 704px; justify-content: flex-start; align-items: flex-start; gap: 10px; display: inline-flex">
                        <div class="Megamen"><span style="color: white; font-size: 20px; font-family: Spectral; font-weight: 400; line-height: 20px; letter-spacing: 1px; word-wrap: break-word">от</span><span style="color: white; font-size: 20px; font-family: Inknut Antiqua; font-weight: 600; line-height: 20px; letter-spacing: 1px; word-wrap: break-word"> megamen</span></div>
                        </div>
                    </div>
                    ''', 
                    unsafe_allow_html=True)
                st.markdown("""
                    **Преимущества решения**:
                    - Оптимизация работы с большими данными.
                    - Ускорение работы аналитиков.
                    - Улучшение таргетинга и производительности кампаний.
                """)
                
                if st.button("Перейти к решению"):
                    st.session_state.solution_page = True
                    st.rerun()
                    st.rerun()
        else:
            # Add background image for the solution page
            add_bg_from_local("background.png")

            # Solution page content
            st.title("Панель управления")

            col_sol_1, col_sol_2 = st.columns([1, 2], gap='large')

            # Left column: Graphs and media display
            with col_sol_1:
                st.header("Визуализация данных")
                st.write("Графики и медиафайлы из базы данных")
                # Placeholder for graphs and media files
                st.image("sample.png", caption="Пример визуализации данных")
                # st.audio("sample_audio.mp3", format="audio/mp3")
                # st.video("sample_video.mp4")

            # Right column: Chatbot interaction
            with col_sol_2:
                st.header("Чат-помощник")
                st.markdown(
                    """
                    <br>
                    """, 
                    unsafe_allow_html=True
                )
                if "messages" not in st.session_state:
                    st.session_state.messages = []

                if prompt := st.chat_input("Спросите бота здесь"):
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": prompt})
                                   
                    # Display user message in chat message container
                    with st.chat_message("user"):
                        st.markdown(prompt)
                        
                    # Display assistant response in chat message container
                    with st.chat_message("assistant"):
                        response = st.write_stream(response_generator(prompt))
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        
                if st.button("Очистить историю"):
                    st.session_state.messages = []
                
                st.divider()
                with st.expander('Ваша история чата здесь'):
                    for message in st.session_state.messages:
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])
                        if message["role"] == 'assistant':
                            st.divider()
                                

        # Logout button in the sidebar
        if logged_sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.solution_page = False
            st.session_state.chat_history = []
            st.rerun()
            st.rerun()
            

# Run the app
if __name__ == '__main__':
    main()