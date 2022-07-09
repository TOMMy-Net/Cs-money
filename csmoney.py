import sys
from fake_useragent import UserAgent
import requests
import json
import csv
import multiprocessing
import time

ua = UserAgent()

def collect_data(type, max_price, min_price):
    global offset, data_item
    offset = 0
    batch_size = 60
    result = []
    count = 0
    try:
        while True:
            for item in range(offset, offset + batch_size, 60):

                url = f'https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=40&isStore=true&limit=60&maxPrice={max_price}&minPrice={min_price}&offset={item}&type={type}&withStack=true'
                time.sleep(0.18)
                response = requests.get(url=url, headers={'user-agent': f'{ua.random}'})
                offset += batch_size
                data = response.json()
                items = data.get('items')


                for i in items:

                    if type == 2:
                        if i.get('overprice') is not None and i.get('overprice') < -17:
                            item_full_name = i.get('fullName')
                            item_3d = i.get('3d')
                            item_price = i.get('price')
                            item_over_price = i.get('overprice')
                            data_item = {
                                'full_name': item_full_name,
                                'overprice': item_over_price,
                                'item_price': item_price,
                                '3d': item_3d,
                            }

                            result.append(data_item)
                    else:
                        if i.get('overprice') is not None and i.get('overprice') < float(-19.5) and i.get('stickers') is not None:
                            item_full_name = i.get('fullName')
                            item_3d = i.get('3d')
                            item_price = i.get('price')
                            item_over_price = i.get('overprice')
                            #item_stickers = i.get('stickers')
                            #for stic in item_stickers:
                                #data_item['stickers'].append(stic['name'])
                            data_item = {
                                'full_name': item_full_name,
                                'overprice': item_over_price,
                                'item_price': item_price,
                                '3d': item_3d,
                                #'stickers': []
                            }

                            result.append(data_item)
                    return result
                count += 1
                print(f'Page #{count}')
                print(url)

    except Exception:
        with open('result.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

#if __name__ == '__main__':
    #collect_data(3)