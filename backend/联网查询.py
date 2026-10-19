from config import BOCHA_SEARCH_URL, BOCHA_API_KEY

def web_content(qus):
    import requests
    import json

    url = BOCHA_SEARCH_URL

    payload = json.dumps({
      "query": qus,
      "summary": True,
      "count": 3
    })

    headers = {
      'Authorization': 'Bearer ' + BOCHA_API_KEY,
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    ans = ""
    for i in range(len(response.json()['data']['webPages']['value'])):
        ans += response.json()['data']['webPages']['value'][i]['summary']
    return ans
