from config import TOOL_API_KEY, TOOL_BASE_URL, TOOL_MODEL, WEATHER_HOST, WEATHER_PATH, WEATHER_APPCODE
import urllib, urllib3, sys, uuid
from openai import OpenAI
import json
def citytime(qus:str):
    client = OpenAI(
        api_key=TOOL_API_KEY,
        base_url=TOOL_BASE_URL,
    )
    quetion = """
        问题：""" + qus + """
        请根据问题提取查询信息：
        回答模板：
        城市名：{城市名}
        """
    content = [
        {
            "type": "text",
            "text": quetion
        }]
    chat_completion = client.chat.completions.create(
        messages=[{'role': 'user', 'content': content}],  # 使用该会话的历史记录
        model=TOOL_MODEL,
        stream=False
    )
    ans = chat_completion.model_dump()['choices'][0]['message']['content']
    lis = list(ans.split("："))
    d = dict()
    d["ct"] = lis[1]
    return d
def weather(qus):
    d = citytime(qus)

    host = WEATHER_HOST
    path = WEATHER_PATH
    method = 'GET'
    appcode = WEATHER_APPCODE
    querys = 'area='+d['ct']
    bodys = {}
    url = host + path + '?' + querys

    http = urllib3.PoolManager()
    headers = {
        'Authorization': 'APPCODE ' + appcode
    }
    response = http.request('GET', url, headers=headers)
    content = response.data.decode('utf-8')
    content = json.loads(content)
    ans = "城市" + d["ct"] + "从" + "接下来7天的天气预报为：\n"
    if (content):
        for i in range(7):
            xin = content["showapi_res_body"]["dayList"][i]
            temp1 = xin["day_air_temperature"]
            temp2 = xin["night_air_temperature"]
            yun1 = xin["day_weather"]
            yun2 = xin["night_weather"]
            feng = xin["day_wind_power"]
            time = xin["daytime"]
            ans += "时间" + str(time) + "，气温为" + str(temp1) + "到" + str(temp2) + "摄氏度，" + yun1 + "转" + yun2 + "，风力为" + feng + "\n"
    return ans

