import requests


response = requests.post(
    'http://127.0.0.1:5000/adv',
    json = {'title': 'Холодильник',
            'description': 'Отличный холодильник',
            'owner': 'Иван'}
)


# response = requests.get(
#     'http://127.0.0.1:5000/adv/56',
# )


# response = requests.patch(
#     'http://127.0.0.1:5000/adv/6',
#     json = {'title': 'Телевизор',
#             'description': 'Хороший телевизор',
#             }
# )


# response = requests.delete(
#     'http://127.0.0.1:5000/adv/3',
# )

print(response.status_code)
print(response.json())
