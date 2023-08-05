import requests

def get_phone_data(number):
    print("Method started")

    url = "https://veriphone.p.rapidapi.com/verify"

    querystring = {"phone":number}

    headers = {
        "X-RapidAPI-Key": "0a485dc436mshe19daf44c99bcc2p19ea5fjsn60f17e06b696",
        "X-RapidAPI-Host": "veriphone.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    print(response.json())

    data = {
        "carrier":response.json()["carrier"],
        "phone_region":response.json()["phone_region"]
    }

    print("DATA IN HELPER")
    print(data)

    print("HELPER ENDED")

    return data

