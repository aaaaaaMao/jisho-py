import requests
import json

JISHO_API = 'https://jisho.org/api/v1/search/words?keyword='

def search_keyword(keyword, mock=False):
    if mock:
        with open('./mock.json', encoding='utf-8') as f:
            data = json.load(f)
            return format_data(data['data'])
    else:
        response = requests.get(JISHO_API + keyword)
        data = json.loads(response.text)
        if len(data['data']) != 0:
            return format_data(data['data'])

def format_data(data):
    result = []
    for item in data:
        japanese_list = item['japanese']
        jlpt = format_jlpt(item['jlpt'])
        senses = format_senses(item['senses'])
        for japanese in japanese_list:
            japanese['jlpt'] = jlpt
            japanese['senses'] = senses
            result.append(japanese)
    return result

def format_senses(senses):
    result = []
    fields = [
        'english_definitions',
        'parts_of_speech',
        'restrictions',
        'english_definitions'
    ]
    for item in senses:
        content = ''
        for field in fields:
            if len(item[field]) != 0:
                content = content + field + ': \n\t - ' + '\n\t - '.join(item[field]) + '\n'
        result.append(content)
    return result

def format_jlpt(jlpt):
    return ' | '.join(jlpt)

if __name__ == '__main__':
    print(search_keyword('home'))