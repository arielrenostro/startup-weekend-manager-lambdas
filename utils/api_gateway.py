import json


def get_json_body(event):
    body = event.get('body')
    if body:
        try:
            return json.loads(body)
        except:
            pass


def get_headers(event):
    return event.get('headers', {})
