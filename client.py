import requests


# Запросы для объявлений

# response = requests.post(
#     'http://127.0.0.1:5000/adv',
#     json = {'title': 'New Oбъявление',
#             'description': 'hard',
#             'owner': 5}
# )


# response = requests.get(
#     'http://127.0.0.1:5000/adv/1',
# )


# response = requests.patch(
#     'http://127.0.0.1:5000/adv/3',
#     json = {'title': 'Второе объявление',
#             'description': 'Обновлено',
#             'owner': 3}
# )


# response = requests.delete(
#     'http://127.0.0.1:5000/adv/2',
# )




# Запросы для пользователей

response = requests.post(
    'http://127.0.0.1:5000/user',
    json = {'name': 'Петр1111',
            'email': 'petya1@mail.ru',
            'password': '11QWERTY4587'}
)


# response = requests.get(
#     'http://127.0.0.1:5000/user/3',
# )


# response = requests.patch(
#     'http://127.0.0.1:5000/user/3',
#     json = {'name': 'John',
#             'email': 'john@mail.ru',
#             'password': '12345qwe'}
# )


# response = requests.delete(
#     'http://127.0.0.1:5000/user/

# )


print(response.status_code)
print(response.json())