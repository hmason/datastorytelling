import requests

if __name__ == '__main__':
    data = requests.get("https://citibikenyc.com/stations/json")
    print data.text
