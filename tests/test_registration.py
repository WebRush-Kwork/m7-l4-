import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users


@pytest.fixture(scope="module")
def setup_database():
    create_db()
    yield
    os.remove('users.db')


def test_create_db(setup_database):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."


def test_add_new_user(setup_database):
    add_user('testuser', 'testuser@example.com', 'password123')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

    try:
        add_user('testuser', 'testuser2@example.com', 'password456')
    except Exception as e:
        assert str(e) == "Ошибка: Пользователь с таким логином уже существует."

def test_authenticate_user(setup_database):
    authenticate_user('testuser', 'password123')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser' AND password='password123';")
    user = cursor.fetchone()
    assert user, "Пользователь должен войти в аккаунт."
    try:
        authenticate_user('testuser', 'password123')
    except Exception as e:
        assert str(e) == "Ошибка: Пользователь неверно."

def test_display_users(setup_database):
    display_users()
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    assert users, "Список выведен успешно"



# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""
