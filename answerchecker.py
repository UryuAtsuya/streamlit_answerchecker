import os
import streamlit as st
from openai import OpenAI
import base64
import tempfile

# --- 設定 ---
MODEL = "gpt-4o"
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# --- Streamlitアプリケーション ---
st.title("手書き回答チェック")

question = st.text_area("問題文を入力してください:")
correct_answer = st.text_input("正答を入力してください:")

uploaded_image = st.file_uploader("回答画像をアップロードしてください", type=["jpg", "png", "jpeg"])

def encode_image(image_file):
    with open(image_file, "rb") as f:
        image_data = f.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
    return base64_image

if st.button("回答をチェック"):
    if question and correct_answer and uploaded_image:
        # 一時ファイルを作成
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_image.read())
            temp_file_path = temp_file.name

        base64_image = encode_image(temp_file_path)

        # 一時ファイルを削除
        os.remove(temp_file_path)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"問題: {question}\n正答: {correct_answer}\n\nこの画像に書かれている回答は正答ですか？"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}} # 修正箇所
                    ]
                }
            ],
        )
        result = response.choices[0].message.content
        st.write("回答:", result)
    else:
        st.warning("問題文、正答、回答画像を全て入力してください。")
