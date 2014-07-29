import json

def extract(filename, **kwargs):
    f = open(filename, 'r')
    deserialized_json = json.load(f)
    return get_text(deserialized_json)


def get_text(deserialized_json):
    if isinstance(deserialized_json, dict):
        result = ''
        for key in deserialized_json:
            result += ' ' + get_text(deserialized_json[key])
        return result
    
    if isinstance(deserialized_json, basestring):
        return deserialized_json
    else:
        return ''