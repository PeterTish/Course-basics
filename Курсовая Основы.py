import requests
from pprint import pprint
with open('Token.txt', 'r') as file:
    token = file.read().strip()

# 45205654
# 28438168 - кейкс id

url = 'https://api.vk.com/method/photos.get'
params = {
    'owner_id': '45205654',
    'access_token': token,
    'v':'5.131',
    'album_id': 'profile',
    'rev': 0,
    'extended': 1,
    'count': 2
}
def json_photos(url):
    '''Функция возвращает json из фотографий с альбома'''
    res = requests.get(url, params=params)
    photos = res.json()['response']['items']
    return photos


def get_photo(json_photos):
    '''Функция возвращает список словаре, где ключ - имя фото (по количеству лайков), значение - url фото'''
    photos_list = []
    for p in json_photos(url):
        url_photos = p['sizes'][-1]['url']
        name_photos = p['likes']['count']
        photos_dict = {name_photos: url_photos}
        photos_list.append(photos_dict)


    return photos_list


def saved_photo(get_photo):
    '''Функция сохраняет фотографии (именем является количество лайков)'''
    for dict in get_photo(json_photos):
        for k,v in dict.items():
            api = requests.get(v)
            with open(f'{k}.jpg','wb') as file:
                file.write(api.content)
    return 'files saved'



class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        # pprint(response.json())
        return response.json()

    def upload_file(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        href = self.get_upload_link(disk_file_path=path_to_file).get("href", "")
        response = requests.put(href, data=open(file_name, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print(f"File {file_name} upload")

import json
def json_file():
    json_output = {}
    json_output_list = []
    for p in json_photos(url):
        url_photos = p['sizes'][-1]['url']
        name_photos = p['likes']['count']
        photos_dict = {name_photos: url_photos}

        size = p['sizes'][-1]['type']
        file_name = f'{name_photos}.jpg'
        json_output = {'file_name' : file_name, 'size' : size}
        json_output_list.append(json_output)

        with open('photo_file.json', 'w') as f:
            json.dump(json_output_list, f)


import os

if __name__ == '__main__':
    saved_photo(get_photo)
    json_file()
    path = os.getcwd()
    file = os.listdir(path)
    files_jpg = [i for i in file if i.endswith('.jpg')]
    with open('token ya.txt', 'r') as file:
        token = file.read().strip()

    for jpg in files_jpg:
        full_path = os.path.join(path, jpg)
        token = token
        file_name = full_path
        path_to_file = jpg
        uploader = YaUploader(token)
        result = uploader.upload_file(path_to_file)























