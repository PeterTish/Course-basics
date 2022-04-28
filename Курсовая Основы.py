import requests
import os
import json
import os.path
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
    'count': 3
}

def json_photos(url):
    '''Функция возвращает json из фотографий с альбома'''
    res = requests.get(url, params=params)
    photos = res.json()['response']['items']
    return photos


def get_photo():
    '''Функция возвращает список словаре, где ключ - имя фото (по количеству лайков), значение - url фото'''
    photos_list = []
    photos = json_photos(url)
    for p in photos:
        url_photos = p['sizes'][-1]['url']
        name_photos = p['likes']['count']
        id_photos = p['id']
        size = p['sizes'][-1]['type']
        photos_dict = {'name_photos':name_photos, 'url_photos':url_photos, 'id_photos':id_photos, 'size':size}
        photos_list.append(photos_dict)
    return photos_list


def saved_photo():
    '''Функция сохраняет фотографии (именем является количество лайков), если фотография с таким именем уже существует
    сохраняется фотография с именем 63.420810960, где 63 - количество лайков, 420810960 - id фотографии'''
    # photos_list = get_photo()
    # path = os.getcwd()
    for dict in photos_list:
        api = requests.get(dict['url_photos'])
        check = os.path.exists(f'{dict["name_photos"]}.jpg')
        if check == False:
            print(f'File {dict["name_photos"]}.jpg saved')
            with open(f'{dict["name_photos"]}.jpg','wb') as file:
                    file.write(api.content)
        else:
            print(f'File {dict["name_photos"]}.jpg exists, saved as {str(dict["name_photos"])}.{str(dict["id_photos"])}.jpg')
            with open(f'{str(dict["name_photos"])}.{str(dict["id_photos"])}.jpg', 'wb') as file:
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

def json_file():
    json_output_list = []
    for p in photos_list:
        del p['url_photos']
        del p['id_photos']
        json_output_list.append(p)
        with open('photo_file.json', 'w') as f:
            json.dump(json_output_list, f)


# def json_file():
#     json_output = {}
#     json_output_list = []
#
#     for files in files_jpg:
#         file_name = files
#         for p in photos:
#             size = p['sizes'][-1]['type']
#         json_output = {'file_name':file_name, 'size':size}
#         json_output_list.append(json_output)
#
#         with open('photo_file.json', 'w') as f:
#             json.dump(json_output_list, f)
#     return json_output_list


if __name__ == '__main__':
    photos = json_photos(url)
    photos_list = get_photo()
    path = os.getcwd()

    saved_photo()

    file = os.listdir(path)
    files_jpg = [i for i in file if i.endswith('.jpg')]

    json_file()

    with open('token ya.txt', 'r') as file:
        token = file.read().strip()

    for jpg in files_jpg:
        full_path = os.path.join(path, jpg)
        token = token
        file_name = full_path
        path_to_file = jpg
        uploader = YaUploader(token)
        result = uploader.upload_file(path_to_file)























