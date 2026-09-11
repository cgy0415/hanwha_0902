#환경변수 활용
# from openai import OpenAI

# client = OpenAI()

# response = client.responses.create(
#     model="gpt-5.6",
#     input="API 연결 테스트야. 성공이라고만 답해줘."
# )

# print(response.output_text)

#env 파일 활용
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6",
    input="API 연결 테스트야. 성공이라고만 답해줘."
)

print(response.output_text)