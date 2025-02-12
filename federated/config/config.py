import yaml


def device_definition(device: dict) -> dict:
    input_string = device["def"]
    parts = input_string.split()

    result = {
        "name": parts[0],
        "qtd": int(parts[1]),
        "type": parts[2]
    }

    return result


def link_definition(link: dict) -> dict:
    input_string = link["def"]
    parts = input_string.split()

    result = {
        "d1": parts[0],
        "d2": parts[1],
        "type": parts[2]
    }

    return result


class Config:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.config = yaml.safe_load(f)

    def get(self, key):
        return self.config.get(key)

    def data(self):
        return self.config

# # Exemplo de uso
# config = Config('flower/config.yaml')
# print(config.data())
# server = config.get(server)
# print(server["memory"])
