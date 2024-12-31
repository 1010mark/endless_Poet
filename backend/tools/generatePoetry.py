import requests
from pydub import AudioSegment
import math, io
from sudachipy import tokenizer, dictionary

# VOICEVOXエンジンのURL
BASE_URL = "http://voicevox_engine:50021"
tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.C 

def get_tokens(text):
    text = text.replace("\n", "")
    tokens = []
    chunk = ""

    for m in tokenizer_obj.tokenize(text, mode):
        chunk += m.surface()
        if m.part_of_speech()[0] in ["助詞", "助動詞"]:
            tokens.append(chunk)
            chunk = ""

    if chunk:
        tokens.append(chunk)
    # print(tokens)
    result = []
    current = ""
    for token in tokens:
        # print(f"current: {current}, token: {token}")
        if len(token) <= 2 and len(result) > 0 and result[-1][-1] not in "。、":
            current += token
        else:
            if current:  # すでに結合中の文字列があれば追加
                if current[0] in "、。" and len(result) > 0:
                    result[-1] += current[0]
                    result.append(current[1:])
                else: result.append(current)
                current = token
            else:
                result.append(token)

    if current:  # 最後に残った文字列を追加
        result.append(current)
    
    return result    

# アクセント句を取得
def get_accent_phrases(text, speaker_id):
    response = requests.post(
        f"{BASE_URL}/audio_query",
        params={"text": text, "speaker": speaker_id},
    )
    response.raise_for_status()
    audio_query = response.json()
    return [phrase["moras"] for phrase in audio_query["accent_phrases"]]

# 音声合成
def synthesize_voice(text, speaker_id, BPM):
    audio_query = requests.post(
        f"{BASE_URL}/audio_query",
        params={"text": text, "speaker": speaker_id},
    ).json();
    audio_query["postPhonemeLength"] = 0
    audio_query["prePhonemeLength"] = 0
    audio_query["speedScale"] = BPM/120
    response = requests.post(
        f"{BASE_URL}/synthesis",
        json=audio_query,
        params={"speaker": speaker_id},
    )
    response.raise_for_status()
    return response.content

# メイン処理
def generate_audio_on_bpm(text, SPEAKER_ID = 47, BPM = 120, max_duration = 60):
    BEAT_DURATION = 60 / BPM  # 1拍の長さ（秒）
    silence_adjust = 0.02 * 120 / BPM # レイテンシ調整
    # アクセント句を取得
    # accent_phrases = get_accent_phrases(text, SPEAKER_ID)
    accent_phrases = get_tokens(text)
    print(accent_phrases)
    one_beat_duration = BEAT_DURATION
    script = []
    combined_audio = AudioSegment.silent(duration=0)  # 空のオーディオ
    for i, phrase in enumerate(accent_phrases):
        # アクセント句を文字列に変換
        # phrase_text = "".join(mora["text"] for mora in phrase if mora["text"])
        phrase_text = phrase
        # print(f"Processing accent phrase: {phrase_text}")

        # 音声生成
        audio_data = synthesize_voice(phrase_text, SPEAKER_ID, BPM)
        
        # 一時ファイルとして保存せず、直接操作
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")
        
        # BPMに基づいて間隔を挿入
        now_length = combined_audio.duration_seconds
        target_duration = math.ceil(now_length / one_beat_duration) * one_beat_duration - silence_adjust
        # print("now:" + str(now_length))
        # print("after:" + str(combined_audio.duration_seconds))
        if now_length + audio_segment.duration_seconds > max_duration:
            break
        
        script.append({"time": now_length, "text": phrase_text})
        combined_audio += audio_segment
        combined_audio += AudioSegment.silent(duration=(target_duration - now_length)*1000)
        

    # 最終音声を保存
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # combined_audio.export(f"poetry_reading_bpm_{timestamp}.wav", format="wav")
    # print(f"音声ファイルを保存しました: poetry_reading_bpm_{timestamp}.wav")
    return {"script": script, "AudioSegment": combined_audio}