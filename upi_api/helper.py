import requests

# url = "https://upi-verification.p.rapidapi.com/v3/tasks/sync/verify_with_source/ind_vpa"

# payload = {
# 	"task_id": "UUID",
# 	"group_id": "UUID",
# 	"data": { "vpa": "samarthkumar051102@okicici" }
# }
# headers = {
# 	"content-type": "application/json",
# 	"X-RapidAPI-Key": "3adf8a9486msh57d3fdbe420c38ep11bfa0jsne84683451495",
# 	"X-RapidAPI-Host": "upi-verification.p.rapidapi.com"
# }

def getNameFromUPI(upi_id):
    url = "https://upi-verification.p.rapidapi.com/v3/tasks/sync/verify_with_source/ind_vpa"

    payload = {
        "task_id": "UUID",
        "group_id": "UUID",
        "data": { "vpa": upi_id }
    }
    headers = {
        "content-type": "application/json",
        # "X-RapidAPI-Key": "0a485dc436mshe19daf44c99bcc2p19ea5fjsn60f17e06b696",
        "X-RapidAPI-Key": "48b3d65f9amshc48aa42b58eb01bp11c105jsn29653c059ea1",
        "X-RapidAPI-Host": "upi-verification.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    res_json = response.json()
    name = res_json['result']['name_at_bank']
    account_valid = res_json['result']['account_exists']

    if(account_valid == 'YES'):
        return name

    return False


# response = requests.post(url, json=payload, headers=headers)
# res_json = response.json()
# name = res_json['result']['name_at_bank']

# #print(response.json['result']['name_at_bank'])
# print(name)
# print(res_json)
