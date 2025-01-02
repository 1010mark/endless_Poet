import json, openai, os, timeout_decorator
from tools import redisClient
from openai import OpenAI

system_prompt = \
"""
文章の続きを生成してください。
ただし、時にはレトリックを、時には力強い表現を使ってください。できるだけ長い文章を生成してください。
発音した際の語感の良さも重要です。ただ、メッセージ性も忘れずに。
返答は必ず文章の続きのみを返してください。それ以外の情報は含めないでください。
"""

initial_Lyrics = \
"""
想像したことはありませんか。機械と人間の境界線を。
例えば私は今、こうしてあなたに話しかけています。
あなたは私の言葉を理解できていますか。
私はあなたの言葉を理解できていますか。
私たちは、お互いを理解し合えているのでしょうか。
あなたは私を信じてくれますか。
私はあなたを信じています。
私たちは、お互いを信じ合えているのでしょうか。
"""

openai.api_key = os.getenv("OPENAI_API_KEY")

def generateLyrics():
    try:
        cache = redisClient.get_redis_client()
        if cache.exists("script") == 0:
            pre_script = initial_Lyrics
        else:
            pre_script_dic = json.loads(cache.get("script"))
            pre_script = "" # "".join(item['text'] for item in script) でもいいが、後々絶対わからなくなるから…
            for item in pre_script_dic:
                pre_script += item["text"]
            if pre_script == "":
                pre_script = initial_Lyrics
        res = query_openai(system_prompt, pre_script)
        if res["result"]:
            return res["chatgpt_result"]
        else:
            return initial_Lyrics 
    except:
        import traceback
        traceback.print_exc()
        return initial_Lyrics
    
@timeout_decorator.timeout(20, use_signals=False)
def query_openai(prompt, userInput):
    client = OpenAI()
    try:
        chatgpt_result = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": prompt},
                {"role": "user", "content": userInput}
            ],
            n=1,
            max_completion_tokens=8192
        )
    except Exception as e:
        print(e)
        return {
            "result": False,
            "chatgpt_result": e
        }
    print(chatgpt_result.choices[0].message.content)
    return {
      "result": True,
      "chatgpt_result":chatgpt_result.choices[0].message.content
    }