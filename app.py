import os
from google.oauth2 import service_account
from google.cloud import texttospeech
import io
import streamlit as st

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='web-speaking-7d89f9a5d1b1.json'
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
   client = texttospeech.TextToSpeechClient(credentials=credentials)

def synthesize_speech(text, lang='日本語',gender='Defalut'):
    gender_type = {
        'デフォルト':texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        '男性':texttospeech.SsmlVoiceGender.MALE,
        '女性':texttospeech.SsmlVoiceGender.FEMALE,
        'ニュートラル':texttospeech.SsmlVoiceGender.NEUTRAL
    }
    lang_code = {
        '英語':'en-US',
        '日本語':'ja-JP'
    }
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code[lang], ssml_gender=gender_type[gender]
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response

st.title('音声出力ツール')

st.markdown('## ①データ準備')

input_option = st.selectbox(
    '入力データの選択',
    ('直接入力','テキストファイル')
)

input_data = None

if input_option == '直接入力':
    input_data = st.text_area('こちらにテキストを入力してください','ここに入力された文字が読み上げられます。')

else:
    uploaded_file = st.file_uploader('テキストファイルをアップロードしてください', ['txt'])
    if uploaded_file is not None:
        content = uploaded_file.read()
        input_data = content.decode()

if input_data is not None:
    st.write('以下が入力されたデータです。↓')
    st.code(input_data)
    st.markdown('## ②パラメータ設定')
    st.markdown('### 言語と話者の性別選択')

    lang = st.radio(   
        '言語を選択してください',
        ('日本語', '英語')
    )

    gender = st.selectbox(   
        '読み上げ音声の性別を選択してください。',
        ('デフォルト', '男性' ,'女性', 'ニュートラル')
    )

    st.markdown('### 音声合成')

    st.write('こちらの文章で音声生成を行いますか？')
    if st.button('開始'):
        comment = st.empty()
        comment.write('音声出力を開始します')
        response = synthesize_speech(input_data, lang=lang ,gender=gender)
        st.audio(response.audio_content)
        comment.write('完了しました')
