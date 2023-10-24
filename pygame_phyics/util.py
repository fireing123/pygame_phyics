import json as jsmodule

def jsopen(path):
    with open(path, 'r') as f:
        json = jsmodule.loads(f.read())
    return json