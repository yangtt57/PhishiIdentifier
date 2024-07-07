from openai import OpenAI
from pathlib import Path
import time
def ask_deepseek(info):

    client = OpenAI(api_key="sk-35bd335289ee4a21b529a3cd6f4d5d0b", base_url="https://api.deepseek.com")
    print("========================begin chat=========================")
    # record the time before the request is sent
    start_time = time.time()
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": """First, you should using English to anwser question.You are an expert in identifying phishing websites. A user will provide information about a website, and you must analyze each piece of information to determine whether the website is likely a phishing site. For each aspect of the provided information, give a probability score and a thorough explanation. Then, combine these scores to provide a final confidence level and a rationale for your judgment.
             To start, please ask the user for the following information about the target website:
            URL Info
            Certificate Info
            Domain Info
            HTML Text
            Form Info
            Link Info
            Image Info
            IFrame Info
            Redirect Info
            External JS Link
            OCR Result
            Once the user provides the information, evaluate the following aspects:
            Whether the URL mimics well-known legitimate websites or uses uncommon top-level domains, and check if the url contians some specious symbols, line $,@,-, if it include, it must be phishing.
            Whether the security certificate is valid, this has less weight.
            Whether the domain name mimics well-known legitimate websites, if this field is None, it must be phishing.
            Whether the HTML text contains excessive urgency phrases like “act now” or “limited offer”.
            Whether the website requests a large amount of sensitive information in forms, such as bank account passwords.
            Whether the links on the page point to dubious or unrelated websites.
            Whether the images on the page seem suspicious or are of poor quality.
            Whether the webpage includes any suspicious iframes.
            Whether the page has numerous redirects that seem suspicious.
            Whether there are external JavaScript links that lead to suspicious sources.
            Whether the OCR results indicate any text that is hidden or appears to be misleading.
            If some aspects' probility is 0%, the ignore them.For each aspect, analyze and provide a phishing probability score. Finally, summarize your findings, provide a weighted analysis, and give a final confidence level that the website is a phishing site, along with a detailed explanation."""},
            {"role": "user", "content": f'{info}'},
        ],
        max_tokens=2048,
        temperature=0,
        stream=True
    )
    for chunk in response:
        # print(chunk)
        print(chunk.choices[0].delta.content,end='')
    # print(response.choices[0].message.content)



if __name__ == '__main__':
    file_path = 'output.txt'
    file_content = Path(file_path).read_text(encoding='utf-8')
    # print(file_content)
    ask_deepseek(file_content)