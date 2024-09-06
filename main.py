import requests
import json
import time
import datetime
import concurrent.futures as pool
import threading
import random
from threading import Lock
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
lock = Lock()
ddosed = []


def go(terr_id, d, proxy_list):

    dates = ['2024-06-01','2024-05-01', '2024-04-01',
              '2024-03-01',
          '2024-01-01', '2024-02-01',
         '2023-12-01', '2023-11-01',  '2023-10-01', '2023-09-01',
              '2023-08-01',     '2023-07-01',     '2023-06-01',
              '2023-05-01',
               '2023-04-01','2023-03-01','2023-02-01','2023-01-01',
              '2022-01-01','2022-02-01','2022-03-01',
               '2022-04-01','2022-05-01','2022-06-01','2022-07-01','2022-08-01','2022-09-01','2022-10-01','2022-11-01','2022-12-01',

             #  '2021-01-01','2021-02-01','2021-03-01',
             # '2021-04-01','2021-05-01','2021-06-01','2021-07-01','2021-08-01','2021-09-01','2021-10-01','2021-11-01',
             #  '2021-12-01',
               # '2020-01-01', '2020-02-01', '2020-03-01',
               # '2020-04-01', '2020-05-01', '2020-06-01', '2020-07-01', '2020-08-01', '2020-09-01', '2020-10-01',
               # '2020-11-01', '2020-12-01'
             ]

    headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,be;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': "session-cookie-mdc=17ef5fd5b5b5ad3851c34f5fbeb261f5fe7cb6f22c0e2ca22062ed1594b473e09e193cada48459ae0f7045075282dfa3",
    'DNT': '1',
    'Host': 'ka.egisso.ru',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': f"""Mozilla/{random.randint(1,10)}.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36""",
    }

    a = {}
    global ddosed
    for date in dates[::-1]:
        print('load ', date, terr_id)
        while True:
            try:
                proxies = {'http': random.choice(proxy_list)}

                print('using proxy:', proxies['http'])
                print(f"""http://ka.egisso.ru/reporting/Data?uuid=50fe5856-1e78-4634-825b-df77910ff10c&dataVersion=16.02.2021%2005.12.21.208&dsCode=gridData&paramPeriod={date}T00%3A00%3A00.000Z&paramPeriodicity=-1&territory={terr_id}&paramONMSZ=-1&paramRecipientCategories={d}""")

                response = requests.get(f"https://ka.egisso.ru/reporting/Data?uuid=50fe5856-1e78-4634-825b-df77910ff10c&dataVersion=16.02.2021%2005.12.21.208&dsCode=gridData&paramPeriod={date}T00%3A00%3A00.000Z&paramPeriodicity=-1&territory={terr_id}&paramONMSZ=-1&paramRecipientCategories={d}",
                                        headers=headers,
                                        proxies=proxies if proxies['http'] != 'noproxy' else None,
                                        timeout=120,
                                        verify=False)
                if response.status_code == 200:
                    time.sleep(1)
                    break

                print('timeout, next proxy...')
                time.sleep(30)
            except:
                time.sleep(30)
                continue


        data_json = json.loads(response.text)
        if not data_json['data']:
            print('there is no territory ', terr_id, ' in dash: ', d)
            continue
        data_json.update({'region_id': terr_id, 'date': date})
        a.update({date: data_json})
        print(d, data_json)
        time.sleep(2)
    with open(f'./out/out_{d}_{terr_id}_{int(datetime.datetime.now().timestamp())}.json', 'w') as f:
        json.dump(a, f, ensure_ascii=False)


db = [1, 2, 3, 4, 5, 6, 7, 8, 9,
      10, 11, 12, 13, 14, 15, 16, 17
      ]

proxy_list = [
    'noproxy',
   # 'http://141.98.133.214:5500',
  #  'http://109.68.210.39:5500',
   # 'http://tq0lws:X7kx0lR07a@109.107.160.105:5500',
]

executor = pool.ThreadPoolExecutor(max_workers=2)

used = []

def get_unused_proxy():
    global used
    unused = [x for x in proxy_list if x not in used]
    if len(unused) == 0:
        used.pop(0)
    unused = [x for x in proxy_list if x not in used]
    rand = random.choice(unused)
    used.append(rand)
    return rand

print(db)

for d in db:
    print('START DASHBOARD: ', d)
    for i in [x for x in range(1, 100) if x not in (2, 6, 9, 13, 16, 31, 21, 43, 74, 23, 39, 62, 59, 51, 48, 72)]:
        executor.submit(go, i, d, proxy_list)


