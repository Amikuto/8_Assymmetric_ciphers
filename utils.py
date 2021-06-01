from configparser import ConfigParser

config = ConfigParser()

def crypt_func(k, message):
    crypt = ''
    for i in message:
        crypt += chr(ord(i) ^ k)
    return crypt


def check_certificate(key: int) -> bool:
    config.read('server_settings.cfg')
    allowed_keys = map(int, config['certificates']['allowed_keys'].split(', '))
    if key in allowed_keys:
        return True
    else:
        return False


def encode_server_certificate_key(g: int, p: int) -> int:
    config.read('server_settings.cfg')
    b = int(config['keys']['b'])
    B = pow(g, b, p)
    return B


def decode_key(key: int, p: int):
    config.read('server_settings.cfg')
    b = int(config['keys']['b'])
    return pow(key, b, p)


def bind_socket(soc):
    config.read('server_settings.cfg')
    port_list = list(map(int, config['settings']['PORT'].split(', ')))
    for port in port_list:
        try:
            soc.bind(('', port))
            break
        except soc.error:
            continue


def encode_client_certificate_key() -> tuple[int, int, int]:
    config.read("client_settings.cfg")
    a = int(config['keys']['a'])
    p = int(config['keys']['p'])
    g = int(config['keys']['g'])
    A = int(pow(g, a, p))
    return g, p, A


def decode_key_from_server(key: int) -> int:
    config.read("client_settings.cfg")
    a = int(config['keys']['a'])
    p = int(config['keys']['p'])
    return pow(key, a, p)
