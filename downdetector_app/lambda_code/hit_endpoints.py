import json
import requests

def load_endpts():
    endpts = None
    with open('config.json', 'r') as file:
        endpts = json.load(file)
    return endpts

def hit_endpoints(endpts):
    print(endpts)
    PASS = True
    for pt in endpts:
        route = endpts[pt]
        print("------------------------------------")
        print(pt)
        print(route)
        try:
            r = requests.get(route)
            print(r.status_code)
            if r.status_code == 200:
                print("End points check successful!")
                print("------------------------------------")
            else:
                PASS = False
                print(r.status_code)
                print("End points check failed!")
                print("------------------------------------")
                break
        except:
            PASS = False
            print("End points check failed!")
            print("------------------------------------")
            break

    return PASS

if __name__ == "__main__":
    endpts = load_endpts()
    hit_endpoints(endpts)