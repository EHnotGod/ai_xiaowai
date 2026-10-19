from config import TOOL_API_KEY, TOOL_BASE_URL, TOOL_MODEL
from openai import OpenAI
def usewhattools(qus:str):
    client = OpenAI(
        api_key=TOOL_API_KEY,
        base_url=TOOL_BASE_URL,
    )
    quetion = """
        问题：""" + qus + """
        可用工具：校园知识查询、天气查询、时间查询
        请根据问题直接输出回答时需要使用的工具（如果不需要工具，请回答不需要工具）,
        回答格式：需要工具：{工具名1}、{工具名2}...
        """
    print(quetion)
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
    return ans