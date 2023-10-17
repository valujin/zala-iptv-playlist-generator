# Импортируем модули json и requests для работы с данными в формате JSON и HTTP-запросами
# import json
import requests

# Задаем ссылку на файл с данными
url = "http://fe.svc.ott.zala.by/CacheClientJson/json/ChannelPackage/list_channels?channelPackageId=59028300&locationId=1111&from=0&to=9999"

# Отправляем GET-запрос по ссылке и получаем ответ
response = requests.get(url)

# Проверяем, что ответ успешный (код 200)
if response.status_code == 200:
    # Преобразуем содержимое ответа в формат JSON и сохраняем в переменную data
    data = response.json()
else:
    # Выводим сообщение об ошибке, если ответ не успешный
    print(f"Ошибка при получении данных по ссылке {url}. Код ответа: {response.status_code}")

# Создаем пустой список для хранения строк плейлиста
playlist = []

# Добавляем первую строку плейлиста, которая указывает формат и кодировку
playlist.append("#EXTM3U")

# Проходим по списку каналов в данных
for channel in data["channels_list"]:
    # Проверяем, что канал не зашифрован
    if channel["isOttEncrypted"] == "0" and channel["videoServerProtocol"] == "hls":
        # Добавляем строку с информацией о канале, включая имя и логотип
        playlist.append(f'#EXTINF:-1 tvg-name="{channel["bcname"]}" tvg-logo="{channel["logo"]}",{channel["bcname"]}')
        # Добавляем строку с ссылкой на поток канала
        playlist.append(f'{channel["ottURL"]}')

# Соединяем все строки плейлиста в одну строку с помощью символа переноса строки
playlist = "\n".join(playlist)

# Открываем файл для записи плейлиста и записываем в него строку плейлиста
with open("zala.m3u", "w") as f:
    f.write(playlist)

# Выводим сообщение об успешном создании плейлиста
print("Плейлист IPTV успешно создан!")