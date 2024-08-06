import streamlit as st
from utils import get_chat_response
from langchain.memory import ConversationBufferMemory

st.title("💬Clone ChatGPT")

with st.sidebar:
    # 换行需要在\n前面加两个空格
    openai_api_key = st.text_input("请输入OpenAI API密钥：  \n(使用系统环境变量输os即可)", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/api-keys)")
    openai_base_url = st.text_input("请输入第三方base_url，  \n若为OpenAI API密钥则留空", type="default")
    st.markdown("```https://api.aigc369.com/v1```  \n~~方便我复制base_url~~")

    # 使用HTML和CSS创建一个绿色按钮，并设置按钮样式
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: #4CAF50;
            color: #ffffff; /* 初始字体颜色 */
            border: none;
            border-radius: 5px;
            padding: 0.5em 1em;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            width: 220px; /* 固定宽度 */
            text-align: center;
        }
        div.stButton > button:hover {
            background-color: #45a049;
            color: #ffffff; /* 悬浮时字体颜色 */
        }
        div.stButton > button:active {
            background-color: #45a049; /* 点击时保持悬浮状态的背景颜色 */
            color: #ffffff; /* 点击时保持悬浮状态的字体颜色 */
        }
        </style>
        """,unsafe_allow_html=True)
    new_chat = st.button("New Chat✍")

# 点击新建聊天按钮删除memory和messages
if new_chat:
    with st.spinner("新建聊天中，请稍后"):
        if "memory" in st.session_state:
            del st.session_state["memory"]
        if "messages" in st.session_state:
            del st.session_state["messages"]

# 创建初始memory和messages
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "你好，我是你的AI助手，有什么可以帮助你的"}]

# 显示所有messages
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 输入prompt，获取response并显示结果。逻辑其实就是打印先前内容，然后显示一输入一输出
prompt = st.chat_input()
if prompt:
    if not openai_api_key:
        st.info("请输入你的OpenAI API Key")
        st.stop()
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中，请稍后..."):
        response = get_chat_response(prompt, st.session_state["memory"], openai_api_key, openai_base_url)

    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)


