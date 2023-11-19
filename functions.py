import json
import pandas as pd
import requests
from pandas import DataFrame

from home_depot_result import home_depot_result


def call_function(messages, function_call):
    """Function calling function which executes function calls when the model believes it is necessary.
    Currently extended by adding clauses to this if statement."""
    print(function_call)

    if function_call["name"] == "lookup_order_status":
        try:
            parsed_output = json.loads(
                function_call["arguments"]
            )
            print("Looking up order status")
            results = get_lookup_order_status(parsed_output["email_address"], parsed_output["order_number"])
            return {
                "role": "function",
                "name": function_call["name"],
                "content": str(results),
            }
        except Exception as e:
            # print(parsed_output)
            print(f"Function execution failed")
            print(f"Error message: {e}")
            return {"role": "function", "content": "call failed", "name": "lookup_order_status"}
    elif function_call["name"] == "lookup_product":
        try:
            parsed_output = json.loads(
                function_call["arguments"]
            )
            print("Looking up product sku")
            results = lookup_product(parsed_output["query"])
            return {
                "role": "function",
                "name": function_call["name"],
                "content": str(results),
            }
        except Exception as e:
            print(f"Function execution failed")
            print(f"Error message: {e}")
            return {"role": "function", "content": "call failed", "name": "lookup_product"}
    elif function_call["name"] == "get_product_listing":
        try:
            parsed_output = json.loads(
                function_call["arguments"]
            )
            print("retrieving product listing")
            results = get_product_listing(parsed_output["sku"])
            return {
                "role": "function",
                "name": function_call["name"],
                "content": str(results),
            }
        except Exception as e:
            print(f"Function execution failed")
            print(f"Error message: {e}")
            return {"role": "function", "content": "call failed", "name": "get_product_listing"}
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


def get_lookup_order_status(email_address: str, order_number: int) -> str:
    return home_depot_result
    # url = "https://www.lowes.com/api/mylowes/orders/details"
    #
    # payload = json.dumps({
    #     "masterOrderNumber": f"{order_number}",
    #     "emailId": f"{email_address}",
    #     "type": "online",
    #     "storeNumber": "1875"
    # })
    # headers = {
    #     'authority': 'www.lowes.com',
    #     'accept': 'application/json, text/plain, */*',
    #     'accept-language': 'en-US,en;q=0.9',
    #     'content-type': 'application/json',
    #     'cookie': 'dbidv2=56b2862a-8fa1-4476-ae09-6368c4fab002; al_sess=FuA4EWsuT07UWryyq/3foEQIwIqOxmho8CAP0qIisJkWP6yrEciiDxJiF8HPZ/09; HPLA=1; region=east; AKA_A2=A; EPID=NTZiMjg2MmEtOGZhMS00NDc2LWFlMDktNjM2OGM0ZmFiMDAy; bm_sz=FD2C6C9185843B61533705694D14EF09~YAAQTCXRFy7EGs+LAQAA9Cok5BVOqBRlOAkc2ibX247znTkInxYHj4yFBMY+lWEGSucc9Vag1mzB5owd7ujrIa8Tt+k8M+uWh6wPPUWz3QF7RpyIyxsA4NOmjVwds1rEkGCtXtnhtxNvg9eoBeVW2rKmOI+Wo6eeyG5ZD/Be3I8J0Mw859Xt03pOB7zh2NviHhi1rTbZLCqj7ihbL4OpgQWv4gd8p5JX2VOFHAjWA3xPtGEVZuPn3tcMJTKbETxO4xHmmO+ER0l6Pgsk+hDYu/G6s71XDkkcDyR2XosdOhO9sIYljoBjBCGktjJird6wvK8WJEC+9WFKdeY=~3486278~4604217; TAsessionID=0421ade3-7a84-4692-9ad8-d67927442c16|NEW; ak_bmsc=A80C29BEB24AF3C79480B0F09D37CF62~000000000000000000000000000000~YAAQTCXRF0zEGs+LAQAALC0k5BVU2zm/cgpTeSAB5oJBqTX8djy+rUtTzcodc06GoFRo/QB3NhhzPSPPvUd6lmCx0k5hK2OgXrT0s2ifZbUneCF7u/kOPX+aDP51oWsuZnVOScC1doltiJAJ7UVHfSlZ+7aCjw5+bm5istYopvV+sJHwtPdNabdtculQtPwq7uRDJadaMZCd+pieFtiMEltlxmCTYZp0ATGsxOSnqKn01LIOMAPHUNIJivM9tMPTSvDvr3mW0JbB7slTFD5CHuRLWYhHtT5LT8BzF0R3VTy+SGkrzdLyF8IuQmFfWAiT7FIHUrDtcxRZpjQUBkenz8ObtREzb23FobM3pWZgb9YbdxnxCUdgUnI33Hkh+uKFxNHfnCLCtwddDQ==; ph_aid=3c68acb4-b3eb-487a-fc03-1cd3fc616418-7080571749703-454eb8c121d15-bf29dec353e8d; _lgsid=1700339660085; sn=1875; sd=%7B%22id%22%3A%221875%22%2C%22zip%22%3A%2230307%22%2C%22city%22%3A%22Atlanta%22%2C%22state%22%3A%22GA%22%2C%22name%22%3A%22Atlanta-Edgewood%20Lowe\'s%22%2C%22region%22%3A%223%22%7D; zipcode=30307; nearbyid=1875; zipstate=GA; bm_mi=6808FB6A942BFA186D4C6F584A7C2C13~YAAQTCXRFzfLGs+LAQAA1fMk5BW7b5b1fpebVli+q0WvFABZFCZymNL07sKET78++WCh2c2PlR2cWb0Mhgy6c0kb+eQQXXnhzTvCBO+c3SXbahePgkJIiNOjvqCpTFDAiy4o0TOqYYTsE6ZalTslHCv7kgGY96uF1sBUFxvNqSN3/Cj5CGcIaCwZZb15pkIFLj7DXqoZ+AEYScs4TUAzhDbJ/g1ShZGx0fUeUqHVwn3pzgdFuuPh2O/WTXQzA4lgzTY+dkhTw5pdbc8vvsu7SdXK0d6R0JW3UyuP5oMThUuIetC0PoVSmycGaHLIPz16~1; user=%7B%22zipPrompt%22%3Atrue%7D; audience=DIY; _abck=84784437A2290F7C7665B869C07C4FDE~0~YAAQTCXRFznOGs+LAQAApl0l5AoUWttzoglFBJBV0r/WGr6wXArpqRxmVKRftBWRNCD7Rc/+z809D45jGbTU0yldpjr9Jq5XeDPG1B6Gdkb3oeu+pL7t1YdLuYUU8pdsnTHiuNU6zW7wKAyzF7lmeXACJHQrlO7cN+zqBaTaile96J18Gj82+zHpDvkU1RuhcqH3rNlV8jq8Ecn8rminJr1LfE4xiOM6SH6yL0eFVl2T4wbNOpIhlZ7ycluXvEHEJQYrb8U3me7oJ0FVDbKXa8mi50c3LPk/maBSzz3LXvK8WwXAiMgWMnu7+D4r96p9YKKXVxiN2khwsm/YixV2j5vtGCEboSy+yWcBTZyDimKxpCf8JYbPRVvJyvgFmbEY/IZcDkueOCKIGxIsSfP+pyReapNRw0cvwmyBtzKDX4bnjU9lGGWZeoEUzwYzpheqs6Z2NyPpkpIl~-1~-1~-1; prodNumber=2; akavpau_default=1700340036~id=0d6c97bed4e510e00b212e2c7151704a; akavpau_cart=1700340038~id=c8d179c7ab834971d54fb6b3f37fb5cd; notice_behavior=implied,eu; p13n=%7B%22zipCode%22%3A%2230307%22%2C%22storeId%22%3A%221875%22%2C%22state%22%3A%22GA%22%2C%22audienceList%22%3A%5B%5D%7D; g_previous=%7B%22gpvPageLoadTime%22%3A%220.00%22%2C%22gpvPageScroll%22%3A%228%7C9%7C0%7C10258%22%2C%22gpvSitesections%22%3A%22checkorderstatus%22%2C%22gpvSiteId%22%3A%22desktop%22%2C%22gpvPageType%22%3A%22check-order-status%22%7D; PT_ST=6c202780-f553-4693-bb78-129dedacc842; akaalb_prod_dual=1700426396~op=PROD_GCP_EAST_CTRL_DFLT:PROD_DEFAULT_EAST|PROD_GCP_EAST_CTRL_A:PROD_EAST_A|~rv=89~m=PROD_DEFAULT_EAST:0|PROD_EAST_A:0|~os=352fb8a62db4e37e16b221fb4cefd635~id=ddbf1d57536e8f52d396da19f5e80dc4; bm_sv=8B13230A1BED940DF1CD6E283A4D1610~YAAQTCXRFx0AG8+LAQAAb1Yp5BXh8z5aM//hZ+YV+MjKJgNR34HJmJZTf3AixPor3SXeREgpHBbsqJUONoLbqAG1NGKbZR0gevtiZH9fdU0VojEHjQOvH0dbif9h9QivxlMSphKTTDy5EQYEFumXDVmNKtMKFjh6uV5Imj2r5hfucyAyTZiQ6V0yOiRigqEUDnY3Yzx2y2CPKvHPpgOLu6NREx34B64M8OOl2nzIJCzlhZfizbm8tDyr6+YYRtgB~1; _abck=84784437A2290F7C7665B869C07C4FDE~-1~YAAQTCXRFyEKG8+LAQAAmScq5AqXSATqkt25kWxxHAg3BLxuo+Nz1ihcUXOUs/s0PjLsQmvz72U0IrKBhYjfN6DLPT0x/N4/ntmJOZQYWN0SUrK3S1MKBuDFQWRMQAdDYPgPrQ9sGLxg/9jiUX8mNYgODb9F9iOKvS0tl0W1MBaPygnbVYeo6YYU/7/GV3KuiLSUbHLRn2Y49ltGRz4SFJpy12VJTBP4f1SYjBovTH3WlsVfdVbY/4YNfGuA862HvGYwo2D7oDMhZsMxZNdm8vBEeGJS0GyOTmeZtUal0izS3wq6KC5ybCiwaCGlI+D8nYkg7SZvjfZTmkvr9oLRW+R40BbDk2OfXGjrqSEq4WLXoR7oFI9iIekZcsOb5nmrtTQEYcjkWCK6jLnIN5ayo+7gbwud/+a9iH3VNctfWmgOamOPjorT79jy3ydPfflYCW9e4iG1W6Ff~0~-1~-1; PT_ST=3c02c563-e159-4766-be6b-f6df25069176; akaalb_prod_dual=1700426449~op=PROD_GCP_EAST_CTRL_DFLT:PROD_DEFAULT_EAST|PROD_GCP_EAST_CTRL_A:PROD_EAST_A|~rv=89~m=PROD_DEFAULT_EAST:0|PROD_EAST_A:0|~os=352fb8a62db4e37e16b221fb4cefd635~id=987589ee78f2a6df0f0ac4a0eb2f0327',
    #     'origin': 'https://www.lowes.com',
    #     'referer': 'https://www.lowes.com/mylowes/orders/checkorderstatus',
    #     'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'same-origin',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    #     'x-requested-with': 'XMLHttpRequest'
    # }
    #
    # response = requests.request("POST", url, headers=headers, data=payload)
    #
    # return response.text


def lookup_product(query: str) -> DataFrame:
    df = pd.read_csv('home_depot_data.csv')
    # df['score'] = df['title'].apply(lambda x: fuzz.ratio(x, query))
    queries = query.split(" ")
    df['contains_queries'] = df['url'].str.contains('|'.join(queries), case=False)

    print(df[df["contains_queries"] == True])

    return df[df["contains_queries"] == True].head(5)['title']

    # url = "https://brickseek.com/api/brickseek-public"
    #
    # payload = {"params": {"search": query, "store_type": 10}, "url": "ajax/product_search"}
    # headers = {
    #     'authority': 'brickseek.com',
    #     'accept': '*/*',
    #     'accept-language': 'en-US,en;q=0.9',
    #     'baggage': 'sentry-environment=vercel-production,sentry-release=ca34a251f847fd72e72bf9f0656cea41aec74315,sentry-public_key=cdad1d45449541899fbf219ad1d6ebdb,sentry-trace_id=d9fb3a828b3045b688a444c93ebe25a0',
    #     'content-type': 'text/plain;charset=UTF-8',
    #     'cookie': '__cf_bm=HU3YnfBsggOePLMQc2lMbpEGvRS6XGg7aPex5VNdJ3Q-1700341559-0-AWvI96ju3QZHuINgeCgWv4wciLY8puzHv0o+iAitfuZARVg+dp4RAKSG/Pr0Gey2lUWsJj0ORKBaphLMq51IHpc=; cf_clearance=1Bd418eBhJTFAfAAdoK8d3I3EFpST.1ler5y0XFXf8k-1700341561-0-1-389cfab0.3c4718a5.6f9da550-0.2.1700341561',
    #     'origin': 'https://brickseek.com',
    #     'referer': 'https://brickseek.com/lowes-inventory-checker',
    #     'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'same-origin',
    #     'sentry-trace': 'd9fb3a828b3045b688a444c93ebe25a0-874f3c7351675e10-1',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
    # }
    #
    # response = requests.request("POST", url, headers=headers, data=payload)
    #
    # print(response.text)
    #
    # # The output is a JSON object
    # # Turn it into a python dictionary
    # response_dict = json.loads(response.text)
    #
    # return response_dict


# https://www.lowes.com/search?searchTerm=MRN12
def get_product_listing(sku: str):
    print("get_product_listing")
    url = f"https://www.lowes.com/search?searchTerm={sku}"

    payload = {}
    headers = {
        'authority': 'www.lowes.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': 'dbidv2=56b2862a-8fa1-4476-ae09-6368c4fab002; al_sess=FuA4EWsuT07UWryyq/3foEQIwIqOxmho8CAP0qIisJkWP6yrEciiDxJiF8HPZ/09; region=east; AKA_A2=A; EPID=NTZiMjg2MmEtOGZhMS00NDc2LWFlMDktNjM2OGM0ZmFiMDAy; bm_sz=FD2C6C9185843B61533705694D14EF09~YAAQTCXRFy7EGs+LAQAA9Cok5BVOqBRlOAkc2ibX247znTkInxYHj4yFBMY+lWEGSucc9Vag1mzB5owd7ujrIa8Tt+k8M+uWh6wPPUWz3QF7RpyIyxsA4NOmjVwds1rEkGCtXtnhtxNvg9eoBeVW2rKmOI+Wo6eeyG5ZD/Be3I8J0Mw859Xt03pOB7zh2NviHhi1rTbZLCqj7ihbL4OpgQWv4gd8p5JX2VOFHAjWA3xPtGEVZuPn3tcMJTKbETxO4xHmmO+ER0l6Pgsk+hDYu/G6s71XDkkcDyR2XosdOhO9sIYljoBjBCGktjJird6wvK8WJEC+9WFKdeY=~3486278~4604217; ph_aid=3c68acb4-b3eb-487a-fc03-1cd3fc616418-7080571749703-454eb8c121d15-bf29dec353e8d; sn=1875; sd=%7B%22id%22%3A%221875%22%2C%22zip%22%3A%2230307%22%2C%22city%22%3A%22Atlanta%22%2C%22state%22%3A%22GA%22%2C%22name%22%3A%22Atlanta-Edgewood%20Lowe\'s%22%2C%22region%22%3A%223%22%7D; zipcode=30307; nearbyid=1875; zipstate=GA; user=%7B%22zipPrompt%22%3Atrue%7D; audience=DIY; _abck=84784437A2290F7C7665B869C07C4FDE~0~YAAQTCXRFznOGs+LAQAApl0l5AoUWttzoglFBJBV0r/WGr6wXArpqRxmVKRftBWRNCD7Rc/+z809D45jGbTU0yldpjr9Jq5XeDPG1B6Gdkb3oeu+pL7t1YdLuYUU8pdsnTHiuNU6zW7wKAyzF7lmeXACJHQrlO7cN+zqBaTaile96J18Gj82+zHpDvkU1RuhcqH3rNlV8jq8Ecn8rminJr1LfE4xiOM6SH6yL0eFVl2T4wbNOpIhlZ7ycluXvEHEJQYrb8U3me7oJ0FVDbKXa8mi50c3LPk/maBSzz3LXvK8WwXAiMgWMnu7+D4r96p9YKKXVxiN2khwsm/YixV2j5vtGCEboSy+yWcBTZyDimKxpCf8JYbPRVvJyvgFmbEY/IZcDkueOCKIGxIsSfP+pyReapNRw0cvwmyBtzKDX4bnjU9lGGWZeoEUzwYzpheqs6Z2NyPpkpIl~-1~-1~-1; prodNumber=2; TAsessionID=a9359468-38d7-478b-98e3-860e86a1c42a|NEW; _lgsid=1700342200927; grs_search_token=HEAD:I3:1:NA:NA:b3dc2d9f6b133c15b34e9ca2541bf2dd; seo-partner=gDTMXB9g7l46qsQ3gCM3qCMsoDgSmXpC; ak_bmsc=A80C29BEB24AF3C79480B0F09D37CF62~000000000000000000000000000000~YAAQruULFz542duLAQAA5BRL5BXlhv5ALaFuOMlnw0rduBHyCy8g2x4aoRSl0bjIyvNthNZqx/oMOjDmsDXaGHch5h0UTU2NyX0uSZpoGaD5Nu7axdj83DCrq/+sLwzIF+fJuEVH082RuCsd8sgxzIPi+aapEk1DmwWZOWrcfpFqtAPPlKS4hBGcjW6jAPLFEwTsQpcqzKeAXG0WndvQa+UEg8LIHLTWhIG3AyrosHtIjhh9TgdBLz4qO+kJiBJqvCzsYmzgcVEJg2p63heU2mk81o1uHusoFpOr+9S4VG7ImIVxnOgpdloinc9kFQ3fhQRonCWzfX9mM9Fq3LvgL3lixNgkdAFbQv9D9uD9CtpqorrXUzYcP7R8Mm/bzUBSFPxQ3i1z0fynE9S9VeiyJ117QrGVbCo/hbzsZ1d2Bxa2T8plvUCFXGzma4B3IaB6uGdOqshQqEP5QGSiov1P; sbsd=spqmx35Jl1HZrCR8jTl/PwpARJNPMewXjZUqj7gbzQcY4wcZLgFQ9KZ5ScmDCPq9IQAJWPpG/ZzKqzHsEGcsMQieWXmXGHxPNFBLvWBK4e3P+9++e+Vt/LQ70pv2wTqJRSzpgXZKAD/1P3u8gwHUBNQ==; bm_mi=6808FB6A942BFA186D4C6F584A7C2C13~YAAQruULF1R42duLAQAAbx5L5BX3ooyVh0CCz1S9KEPjsw+YZ/EyDyiRfDZ5NN2w6tN4NyVhogBqJ40FFHb7E9ZsM3x5B5RHpjiDnd1z1t3nDhnLDCyQz/fDo28shr6/wtFLmRMzefrDK2MLPaoOmJ0HN2W/YgNp2H5LhNHPdClZqsrKDCbcI0Bu4PO/MREIY/7UYbVoV7Md1oZgMVxL42Rjsu7SKACEfGByzzysZCc8Fnlz66oecOp8+SMGPcsNk7+vrVklNCXi9VObPp5Zs02JmO4u3uGrTzHX91RvRNP5uLBmAcg3llq0XDnDUeLG~1; salsify_session_id=0869bdc0-eb71-4df8-8a00-2581bdc455a1; akavpau_default=1700342511~id=d12fe16cb50bff6560c1af6055b1278c; akavpau_cart=1700342513~id=d28f6ce6f94e835c9677ad1aa459d716; notice_behavior=implied,eu; p13n=%7B%22zipCode%22%3A%2230307%22%2C%22storeId%22%3A%221875%22%2C%22state%22%3A%22GA%22%2C%22audienceList%22%3A%5B%5D%7D; g_previous=%7B%22gpvPageLoadTime%22%3A%220.00%22%2C%22gpvPageScroll%22%3A%2226%7C27%7C0%7C3149%22%2C%22gpvSitesections%22%3A%22checkorderstatus%22%2C%22gpvSiteId%22%3A%22desktop%22%2C%22gpvPageType%22%3A%22check-order-status%22%7D; akaalb_prod_dual=1700428639~op=PROD_GCP_EAST_CTRL_DFLT:PROD_DEFAULT_EAST|PROD_GCP_EAST_CTRL_A:PROD_EAST_A|~rv=89~m=PROD_DEFAULT_EAST:0|PROD_EAST_A:0|~os=352fb8a62db4e37e16b221fb4cefd635~id=2cf1cd354d83c94f9da60e4ebbc25c6e; bm_sv=8B13230A1BED940DF1CD6E283A4D1610~YAAQruULF7R42duLAQAAVpBL5BUdn0LlPXETpnblyyruPK4VG5bVhjNMqHn059CHQH/1BiSLnADboIS3aZWm2HrbjSicvoG6MsTqumzNORm9VzKfH3+PRzhqk0m7XDglfg2qO03xrSoMhn2x0HtBaFHYUu+LPlZYRrrU+chMrVHtzp5i8JTx3grQiWcJnahnj5Dm2Nm6r3d22ifqZG1hcxA9oNG69Kbiwinwv2B0Dt7kbujRggMq+dV/rHHmdyNF~1; _abck=84784437A2290F7C7665B869C07C4FDE~-1~YAAQruULFyp82duLAQAAjltO5Aq5Z2Wy7IwrT8LGPETsMNBYgR3ioKo05jXyjh7pnHJE/6HuQ48H84Qlbz3pLV0XC0Em8SxGIWwx4/jtqFwVP2HseXKdmJJm7bO5DHvTg1K7wu1LyubY7qU+eSTAxOMgnJiKjMy10pGMnVIsgS5/3UWvZprfNvZWYVFT/q6FtVpK7EOXXyI+FIherVv1IQBngeQbxFFT3sZ9yGVgcpuXffHW5G2ph7UB3sKQCVyU+XovIpman//ZoiNIBUrp9NR5pOoIA6ui8Wg8N4cm/bBUGRfxBCw4je16mWTbZP5Jm0XQvREBYvBBR8mXhP/iZvReV8YCMg5zjerxzeT3MGyzIipoLQeLxLzr9I/SUG5cHN7mXh8YFvmbuppyhnBQCTKrnhm8wZ+6Ga0eHY0jz9zhgSijOECuGxpnV4mdtC/rX7hswdMyAmmj~0~-1~-1; ak_bmsc=A80C29BEB24AF3C79480B0F09D37CF62~000000000000000000000000000000~YAAQruULFyt82duLAQAAjltO5BUVgHseFizgyiwC7KNxfqvcDdkjtdW0+ykbMNKpCOBkYKvRomJO8hYi+7pVA6Oi5vIWP7qYR9hLzp5KZz8nWu3DkYMpaDqbMTD16nRwkh36KS/NYhosAjQABuYoOUYw1IbBsr1L/uKHHOJv+jLyZcdpI92BOATTt/x7ZmVxVTJMH3Po+92V7gsXFvbJr281h3e41RVJUpUD4KG+4OfnJTaHuGqK5z2+Iw0hRvJtKDnWaaG9/iCLxLwFm9tFO7+8hDMW7SdoolHwKZ0KeajzTbYkugFRiTbH0SyKnM2zqMIt0hJfvIYsPkwzvxXR23BYoEl//ocbzN1Egsiknd83AtUgDG0qTMNJ/fpS8ey0Lpic9jk+qxm1aIozuv6wqZMcN+pCVuOZXMrV1YYo6Iifzr2z9dtTtufBvFQI6UrLBYVStlorAkMNO1ieotC48iLQoZnWa7Cex0FFNQ==; akaalb_prod_dual=1700426449~op=PROD_GCP_EAST_CTRL_DFLT:PROD_DEFAULT_EAST|PROD_GCP_EAST_CTRL_A:PROD_EAST_A|~rv=89~m=PROD_DEFAULT_EAST:0|PROD_EAST_A:0|~os=352fb8a62db4e37e16b221fb4cefd635~id=987589ee78f2a6df0f0ac4a0eb2f0327',
        'referer': 'https://www.lowes.com/c/Departments',
        'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print("get_product_listing")
    return response.text


def refer_to_human_agent(summary: str):
    return summary
