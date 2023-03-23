import requests






def send_details(phone,name,due,mode,amount):
    if phone:
        url = "https://www.fast2sms.com/dev/bulkV2"
        if due > 0 :
            payload = f"sender_id=TXTIND&message=Hi {name}, Transaction {amount}Rs | {mode} Sucessfull!\nDue : {due}Rs\nThankyou! &language=english &route=v3&numbers={phone}"
        else:
            payload = f"sender_id=TXTIND&message=Hi {name}, Transaction {amount}Rs | {mode} Sucessfull!\n Due : 0Rs \n Thankyou! &language=english &route=v3&numbers={phone}"

        headers = {
    'authorization': "B98nOsTqGScVmtR0Xrb3whizxIo2CAykHfeUNYgjdKQF4D7auPTGwc80J26uIpFf3Yin7EmKHsQ1vzLj",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)  
    else :
        return False









