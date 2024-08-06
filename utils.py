import os
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain


def get_chat_response(prompt, memory, openai_api_key, openai_base_url):
    if openai_api_key == "os":
        openai_api_key = os.getenv("OPENAI_API_KEY")

    if openai_base_url == "":
        model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)
    else:
        model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key, base_url=openai_base_url)

    chain = ConversationChain(llm=model, memory=memory)

    response = chain.invoke({"input": prompt})

    return response["response"]

# 测试代码
# memory = ConversationBufferMemory(return_messaes=True)
# print(get_chat_response("说明牛顿第一定律？", memory, "os", "https://api.aigc369.com/v1"))
# print(get_chat_response("我上一个问题是？", memory, "os", "https://api.aigc369.com/v1"))