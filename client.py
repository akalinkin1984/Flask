import requests


# Запросы для объявлений

# response = requests.post(
#     'http://127.0.0.1:5000/adv',
#     json = {'title': 'Первое объявление',
#             'description': 'бла-бла-бла',
#             'owner': 1}
# )


# response = requests.get(
#     'http://127.0.0.1:5000/adv/3',
# )


# response = requests.patch(
#     'http://127.0.0.1:5000/adv/3',
#     json = {'title': 'Первое объявление',
#             'description': 'Обновлено',
#             'owner': 1}
# )


# response = requests.delete(
#     'http://127.0.0.1:5000/adv/2',
# )




# Запросы для пользователей

# response = requests.post(
#     'http://127.0.0.1:5000/user',
#     json = {'name': 'Василий',
#             'mail': 'vasiliy@mail.ru',
#             'password': 'QWERTY12'}
# )


response = requests.get(
    'http://127.0.0.1:5000/user/1',
)


# response = requests.patch(
#     'http://127.0.0.1:5000/user/1',
#     json = {'name': 'Василий',
#             'mail': 'vasiliy123@mail.ru',
#             'password': 'QWERTY'}
# )


# response = requests.delete(
#     'http://127.0.0.1:5000/user/1',
# )


print(response.status_code)
print(response.json())