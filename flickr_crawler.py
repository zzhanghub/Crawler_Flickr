import json
import flickrapi
import urllib
import os

import time
import random

config_license = json.load(open('./flickr_config.json', 'r'))
config = config_license['config']
license_dic = config_license['license_dic']
API_KEY = config['flickr_api_key']
API_SECRET = config['flickr_api_secret']
save_root = config['save_root']
flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, cache=True)

keywords_file = open(config['keywords_file'], 'r')
keywords_tag_dic = json.load(keywords_file)
keywords = keywords_tag_dic.keys()

url_keys = config['url_keys']
lic_ids = config['license_id'].replace(' ', '')


for ikeyword in keywords:
    im_dir = os.path.join(save_root, 'Img', ikeyword)
    lic_dir = os.path.join(save_root, 'Lic', ikeyword)
    os.makedirs(im_dir, exist_ok=True)
    os.makedirs(lic_dir, exist_ok=True)

    # Searching
    try:
        photos = flickr.walk(text=keywords_tag_dic[ikeyword], extras=url_keys + ', license, owner_name',
                             license=lic_ids, per_page=300, media='photos', sort='relevance', pages=1)
    except Exception as e:
        print('Walking Error')
        continue

    # download images and make license_jsons
    for photo in photos:
        url_keys_list = url_keys.replace(' ', '').split(',')
        for item in url_keys_list:
            url = photo.get(item)
            if url != None:
                break

        if(str(url) != "None"):
            try:
                urllib.request.urlretrieve(url, os.path.join(
                    im_dir, (photo.get('id') + "." + os.path.basename(url).split(".")[1])))
                photo_dic = {
                    'id': photo.get('id'),
                    'owner': photo.get('owner'),
                    'ownername': photo.get('ownername'),
                    'flickr_url': url,
                    'license_id': photo.get('license'),
                    'license_name': license_dic[photo.get('license')]
                }
                photo_json = json.dumps(
                    photo_dic, ensure_ascii=False, indent=4)

                with open(os.path.join(lic_dir, (photo.get('id')+'.json')), 'w') as f:
                    f.write(photo_json)
                
                time.sleep(3 * random.random())

            except Exception as e:
                print(str(e))
                continue
