import json as jsmodule

def jsopen(path):
    with open(path, 'r') as f:
        json = jsmodule.loads(f.read())
    return json

def jsave(data, path):
    with open(path, 'w') as f:
        jsmodule.dump(data, f, indent=4)