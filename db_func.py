from json import dump, load

js_name = 'data.json'


def get_data():
    return load(open(js_name, 'r'))


def update_data(data: dict) -> None:
    dump(data, open(js_name, 'w'))
