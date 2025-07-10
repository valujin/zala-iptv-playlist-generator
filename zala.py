# Импортируем модули json и requests для работы с данными в формате JSON и HTTP-запросами
# import json
import requests
from time import sleep
import urllib3

# Отключаем предупреждения о небезопасных SSL соединениях
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Задаем ссылку на файл с данными
# url = "http://fe.svc.ott.zala.by/CacheClientJson/json/ChannelPackage/list_channels?channelPackageId=59028300&locationId=1111&from=0&to=9999"

url_list = [
    'http://fe.svc.ott.zala.by/CacheClientJson/json/ChannelPackage/list_channels?channelPackageId=59028300&locationId=1111&from=0&to=9999',
    'http://fe.svc.ott.zala.by/CacheClientJson/json/ChannelPackage/list_channels?channelPackageId=5471515&locationId=10000081&from=0&to=9999&lang=RUS',
    'http://fe.svc.ott.zala.by/CacheClientJson/json/ChannelPackage/list_channels?channelPackageId=9119099&locationId=10000081&from=0&to=9999&lang=RUS',
    'http://fe.svc.ott.zala.by/CacheClientJson/json/ChannelPackage/list_channels?channelPackageId=9119102&locationId=10000081&from=0&to=9999&lang=RUS',
    'http://fe.svc.ott.zala.by/CacheClientJson/json/ChannelPackage/list_channels?channelPackageId=47320362&locationId=10000081&from=0&to=9999&lang=RUS',
    'http://fe.svc.ott.zala.by/CacheClientJson/json/ChannelPackage/list_channels?channelPackageId=175085983&locationId=10000081&from=0&to=9999&lang=RUS'
]

data = []

# Проходим по каждому URL в списке url_list
for url in url_list:
    # Отправляем GET-запрос по ссылке и получаем ответ
    response = requests.get(url, verify=False)
    
    # Проверяем, что ответ успешный (код 200)
    if response.status_code == 200:
        # Преобразуем содержимое ответа в формат JSON и добавляем в список data
        data.append(response.json()["channels_list"])
    else:
        # Выводим сообщение об ошибке, если ответ не успешный
        print(f"Ошибка при получении данных по ссылке {url}. Код ответа: {response.status_code}")

# Объединяем все полученные данные в один список
data = [channel for sublist in data for channel in sublist]
# Сортируем каналы по num
data.sort(key=lambda x: int(x["num"]))

# Создаем пустой список для хранения строк плейлиста
playlist = []
channel_list = []

# Добавляем первую строку плейлиста, которая указывает формат и кодировку
playlist.append("#EXTM3U")

# Проходим по списку каналов в данных
for channel in data:
    # Проверяем, что канал не зашифрован
    if channel["isOttEncrypted"] == "0" and channel["videoServerProtocol"] == "hls":
        # Проверяем, есть ли канал в playlist
        if channel["bcname"] in channel_list:
            continue
        # Проверяем, если название канала начинается с "Беларусь 4" и не содержит "Брест" - если да, то пропускаем
        if channel["bcname"].startswith("Беларусь 4") and "Брест" not in channel["bcname"]:
            continue
        # Проверяем ссылку на ответ 404
        try:
            test_url = channel["ottURL"].replace("https://", "http://")
            response = requests.head(test_url, verify=False, timeout=10)
            if response.status_code == 404:
                print(f"Канал {channel['bcname']} недоступен (404)")
                continue
        except requests.RequestException as e:
            print(f"Ошибка при проверке канала {channel['bcname']}: {e}")
            continue
        # Добавляем строку с информацией о канале, включая имя и логотип
        playlist.append(f'#EXTINF:-1 tvg-name="{channel["bcname"]}" tvg-logo="{channel["logo"]}",{channel["bcname"]}')
        # Добавляем строку с ссылкой на поток канала
        playlist.append(f'{channel["ottURL"]}')
        # Добавляем канал в список channel_list
        channel_list.append(channel["bcname"])
        print(f"Добавлен канал: {channel['num']} ({channel['bcname']})")

# Соединяем все строки плейлиста в одну строку с помощью символа переноса строки
playlist = "\n".join(playlist)

# Открываем файл для записи плейлиста и записываем в него строку плейлиста
with open("zala.m3u", "w") as f:
    f.write(playlist)

# Выводим сообщение об успешном создании плейлиста
print("Плейлист IPTV успешно создан!")