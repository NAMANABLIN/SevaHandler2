from json import dump, load

js_name = 'data.json'
data_example = '{"stickers": {}, "reactions": {}}'


def get_data() -> dict:
    return load(open(js_name, 'r'))


def update_data(data: dict) -> None:
    dump(data, open(js_name, 'w'))


def create_data() -> None:
    with open(js_name, 'w') as f:
        f.write(data_example)