import json
import requests


def call_function(messages, function_call):
    """Function calling function which executes function calls when the model believes it is necessary.
    Currently extended by adding clauses to this if statement."""
    print(function_call)

    if function_call["name"] == "order_tracking_status":
        try:
            parsed_output = json.loads(
                function_call["arguments"]
            )
            print("Looking up order status")
            results = get_order_tracking_status(parsed_output["email_address"], parsed_output["order_number"])
            return {
                "role": "function",
                "name": function_call["name"],
                "content": str(results),
            }
        except Exception as e:
            # print(parsed_output)
            print(f"Function execution failed")
            print(f"Error message: {e}")
            return {"role": "function", "content": "call failed", "name": "order_tracking_status"}
    elif function_call["name"] == "refer_to_human_agent":
        try:
            parsed_output = json.loads(
                function_call["arguments"]
            )
            print("Referring to human agent")
            results = refer_to_human_agent(parsed_output["conversation_summary"])
            return {
                "role": "function",
                "name": function_call["name"],
                "content": str(results),
            }
        except Exception as e:
            print(f"Function execution failed")
            print(f"Error message: {e}")
            return {"role": "function", "content": "call failed", "name": "refer_to_human_agent"}

    else:
        raise Exception("Function does not exist and cannot be called")


def get_order_tracking_status(email_address: str, order_number: int) -> str:
    url = "https://www.lowes.com/api/mylowes/orders/details"

    payload = json.dumps({
        "masterOrderNumber": f"{order_number}",
        "emailId": f"{email_address}",
        "type": "online",
        "storeNumber": "1875"
    })
    headers = {
        'authority': 'www.lowes.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': 'dbidv2=56b2862a-8fa1-4476-ae09-6368c4fab002; al_sess=FuA4EWsuT07UWryyq/3foEQIwIqOxmho8CAP0qIisJkWP6yrEciiDxJiF8HPZ/09; HPLA=1; region=east; AKA_A2=A; EPID=NTZiMjg2MmEtOGZhMS00NDc2LWFlMDktNjM2OGM0ZmFiMDAy; bm_sz=FD2C6C9185843B61533705694D14EF09~YAAQTCXRFy7EGs+LAQAA9Cok5BVOqBRlOAkc2ibX247znTkInxYHj4yFBMY+lWEGSucc9Vag1mzB5owd7ujrIa8Tt+k8M+uWh6wPPUWz3QF7RpyIyxsA4NOmjVwds1rEkGCtXtnhtxNvg9eoBeVW2rKmOI+Wo6eeyG5ZD/Be3I8J0Mw859Xt03pOB7zh2NviHhi1rTbZLCqj7ihbL4OpgQWv4gd8p5JX2VOFHAjWA3xPtGEVZuPn3tcMJTKbETxO4xHmmO+ER0l6Pgsk+hDYu/G6s71XDkkcDyR2XosdOhO9sIYljoBjBCGktjJird6wvK8WJEC+9WFKdeY=~3486278~4604217; TAsessionID=0421ade3-7a84-4692-9ad8-d67927442c16|NEW; ak_bmsc=A80C29BEB24AF3C79480B0F09D37CF62~000000000000000000000000000000~YAAQTCXRF0zEGs+LAQAALC0k5BVU2zm/cgpTeSAB5oJBqTX8djy+rUtTzcodc06GoFRo/QB3NhhzPSPPvUd6lmCx0k5hK2OgXrT0s2ifZbUneCF7u/kOPX+aDP51oWsuZnVOScC1doltiJAJ7UVHfSlZ+7aCjw5+bm5istYopvV+sJHwtPdNabdtculQtPwq7uRDJadaMZCd+pieFtiMEltlxmCTYZp0ATGsxOSnqKn01LIOMAPHUNIJivM9tMPTSvDvr3mW0JbB7slTFD5CHuRLWYhHtT5LT8BzF0R3VTy+SGkrzdLyF8IuQmFfWAiT7FIHUrDtcxRZpjQUBkenz8ObtREzb23FobM3pWZgb9YbdxnxCUdgUnI33Hkh+uKFxNHfnCLCtwddDQ==; ph_aid=3c68acb4-b3eb-487a-fc03-1cd3fc616418-7080571749703-454eb8c121d15-bf29dec353e8d; _lgsid=1700339660085; sn=1875; sd=%7B%22id%22%3A%221875%22%2C%22zip%22%3A%2230307%22%2C%22city%22%3A%22Atlanta%22%2C%22state%22%3A%22GA%22%2C%22name%22%3A%22Atlanta-Edgewood%20Lowe\'s%22%2C%22region%22%3A%223%22%7D; zipcode=30307; nearbyid=1875; zipstate=GA; bm_mi=6808FB6A942BFA186D4C6F584A7C2C13~YAAQTCXRFzfLGs+LAQAA1fMk5BW7b5b1fpebVli+q0WvFABZFCZymNL07sKET78++WCh2c2PlR2cWb0Mhgy6c0kb+eQQXXnhzTvCBO+c3SXbahePgkJIiNOjvqCpTFDAiy4o0TOqYYTsE6ZalTslHCv7kgGY96uF1sBUFxvNqSN3/Cj5CGcIaCwZZb15pkIFLj7DXqoZ+AEYScs4TUAzhDbJ/g1ShZGx0fUeUqHVwn3pzgdFuuPh2O/WTXQzA4lgzTY+dkhTw5pdbc8vvsu7SdXK0d6R0JW3UyuP5oMThUuIetC0PoVSmycGaHLIPz16~1; user=%7B%22zipPrompt%22%3Atrue%7D; audience=DIY; _abck=84784437A2290F7C7665B869C07C4FDE~0~YAAQTCXRFznOGs+LAQAApl0l5AoUWttzoglFBJBV0r/WGr6wXArpqRxmVKRftBWRNCD7Rc/+z809D45jGbTU0yldpjr9Jq5XeDPG1B6Gdkb3oeu+pL7t1YdLuYUU8pdsnTHiuNU6zW7wKAyzF7lmeXACJHQrlO7cN+zqBaTaile96J18Gj82+zHpDvkU1RuhcqH3rNlV8jq8Ecn8rminJr1LfE4xiOM6SH6yL0eFVl2T4wbNOpIhlZ7ycluXvEHEJQYrb8U3me7oJ0FVDbKXa8mi50c3LPk/maBSzz3LXvK8WwXAiMgWMnu7+D4r96p9YKKXVxiN2khwsm/YixV2j5vtGCEboSy+yWcBTZyDimKxpCf8JYbPRVvJyvgFmbEY/IZcDkueOCKIGxIsSfP+pyReapNRw0cvwmyBtzKDX4bnjU9lGGWZeoEUzwYzpheqs6Z2NyPpkpIl~-1~-1~-1; prodNumber=2; akavpau_default=1700340036~id=0d6c97bed4e510e00b212e2c7151704a; akavpau_cart=1700340038~id=c8d179c7ab834971d54fb6b3f37fb5cd; notice_behavior=implied,eu; p13n=%7B%22zipCode%22%3A%2230307%22%2C%22storeId%22%3A%221875%22%2C%22state%22%3A%22GA%22%2C%22audienceList%22%3A%5B%5D%7D; g_previous=%7B%22gpvPageLoadTime%22%3A%220.00%22%2C%22gpvPageScroll%22%3A%228%7C9%7C0%7C10258%22%2C%22gpvSitesections%22%3A%22checkorderstatus%22%2C%22gpvSiteId%22%3A%22desktop%22%2C%22gpvPageType%22%3A%22check-order-status%22%7D; PT_ST=6c202780-f553-4693-bb78-129dedacc842; akaalb_prod_dual=1700426396~op=PROD_GCP_EAST_CTRL_DFLT:PROD_DEFAULT_EAST|PROD_GCP_EAST_CTRL_A:PROD_EAST_A|~rv=89~m=PROD_DEFAULT_EAST:0|PROD_EAST_A:0|~os=352fb8a62db4e37e16b221fb4cefd635~id=ddbf1d57536e8f52d396da19f5e80dc4; bm_sv=8B13230A1BED940DF1CD6E283A4D1610~YAAQTCXRFx0AG8+LAQAAb1Yp5BXh8z5aM//hZ+YV+MjKJgNR34HJmJZTf3AixPor3SXeREgpHBbsqJUONoLbqAG1NGKbZR0gevtiZH9fdU0VojEHjQOvH0dbif9h9QivxlMSphKTTDy5EQYEFumXDVmNKtMKFjh6uV5Imj2r5hfucyAyTZiQ6V0yOiRigqEUDnY3Yzx2y2CPKvHPpgOLu6NREx34B64M8OOl2nzIJCzlhZfizbm8tDyr6+YYRtgB~1; _abck=84784437A2290F7C7665B869C07C4FDE~-1~YAAQTCXRFyEKG8+LAQAAmScq5AqXSATqkt25kWxxHAg3BLxuo+Nz1ihcUXOUs/s0PjLsQmvz72U0IrKBhYjfN6DLPT0x/N4/ntmJOZQYWN0SUrK3S1MKBuDFQWRMQAdDYPgPrQ9sGLxg/9jiUX8mNYgODb9F9iOKvS0tl0W1MBaPygnbVYeo6YYU/7/GV3KuiLSUbHLRn2Y49ltGRz4SFJpy12VJTBP4f1SYjBovTH3WlsVfdVbY/4YNfGuA862HvGYwo2D7oDMhZsMxZNdm8vBEeGJS0GyOTmeZtUal0izS3wq6KC5ybCiwaCGlI+D8nYkg7SZvjfZTmkvr9oLRW+R40BbDk2OfXGjrqSEq4WLXoR7oFI9iIekZcsOb5nmrtTQEYcjkWCK6jLnIN5ayo+7gbwud/+a9iH3VNctfWmgOamOPjorT79jy3ydPfflYCW9e4iG1W6Ff~0~-1~-1; PT_ST=3c02c563-e159-4766-be6b-f6df25069176; akaalb_prod_dual=1700426449~op=PROD_GCP_EAST_CTRL_DFLT:PROD_DEFAULT_EAST|PROD_GCP_EAST_CTRL_A:PROD_EAST_A|~rv=89~m=PROD_DEFAULT_EAST:0|PROD_EAST_A:0|~os=352fb8a62db4e37e16b221fb4cefd635~id=987589ee78f2a6df0f0ac4a0eb2f0327',
        'origin': 'https://www.lowes.com',
        'referer': 'https://www.lowes.com/mylowes/orders/checkorderstatus',
        'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def refer_to_human_agent(summary: str) -> str:
    return "I'm sorry, I don't know how to help you with that. I'll refer you to a human agent."
