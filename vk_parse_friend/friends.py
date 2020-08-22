import requests
import json
import datetime

API = 'https://api.vk.com/method/'
TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'

def age_from_birthday(born):
    if len(born.split('.')) != 3:
        return None
    born = datetime.datetime.strptime(born, "%d.%m.%Y").date()
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def get_id(token, uid):
    res = requests.get\
    (f"{API}users.get?v=5.71&access_token={TOKEN}&user_ids={uid}")
    data = json.loads(res.text)
    return data['response'][0]['id']

def get_friends(token, vk_id):
    res = requests.get\
    (f"{API}friends.get?v=5.71&access_token={TOKEN}&user_id={vk_id}&fields=bdate")
    data = json.loads(res.text)
    return data['response']['items']

def calc_age(uid):
    token = TOKEN
    vk_id = get_id(token, uid)
    friends = get_friends(token, vk_id)
    ages = [age_from_birthday(x['bdate']) for x in friends if 'bdate' in x]
    res = {}
    for age in ages:
        if age is None:
            continue
        if age not in res:
            res[age] = 0
        res[age] += 1
    res = list(res.items())
    res = sorted(res, key = lambda x: x[0])
    return sorted(res, key = lambda x: x[1], reverse=True)


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
