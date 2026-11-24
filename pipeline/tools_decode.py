import json
def load_result(path, tag):
    t=json.load(open(path))[0]['text'].strip()
    if t.startswith('"'):
        t,_=json.JSONDecoder(strict=False).raw_decode(t)
    return t[t.index(tag)+len(tag):]
