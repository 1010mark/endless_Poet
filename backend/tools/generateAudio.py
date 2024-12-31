from tools import generatePoetry, generateInstruments
from tools.generateLyrics import generateLyrics
from pydub import AudioSegment
import numpy as np
import os

def generateAudio():
    try:
        script = generateLyrics()
        base = AudioSegment.silent(duration=96 * 1000)
        
        voice_volume_plus_str = os.getenv('VOICE_VOLUME_PLUS', '2')
        try:
            voice_volume_plus = int(voice_volume_plus_str)
        except ValueError:
            voice_volume_plus = 2
        poetry = generatePoetry.generate_audio_on_bpm(script)
        poetry["AudioSegment"] += voice_volume_plus
        
        # inst_volume_minus_str = os.getenv('INST_VOLUME_MINUS', '2')
        # try:
        #     inst_volume_minus = int(inst_volume_minus_str)
        # except ValueError:
        #     inst_volume_minus = 2
        # inst = generateInstruments.generateInstruments() - inst_volume_minus
        inst = generateInstruments.generateInstruments()
        combined = base.overlay(poetry["AudioSegment"])
        combined = combined.overlay(inst)
        # combined = add_reverb(combined)
        combined = combined[:64 * 1000]
        return {
            "script": poetry["script"],
            "AudioSegment": combined
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "script": {},
            "AudioSegment": AudioSegment.silent(duration=64 * 1000)
        }
        
# 参考元: https://qiita.com/Tadataka_Takahashi/items/1c1681bc2e931b92bca9
def add_reverb(sound, reverberance=50, damping=50, room_scale=75):
    # パラメータを正規化
    reverberance = max(0, min(100, reverberance)) / 100
    damping = max(0, min(100, damping)) / 100
    room_scale = max(0, min(100, room_scale)) / 100
    
    # 音声データを numpy 配列に変換
    samples = np.array(sound.get_array_of_samples())
    
    # リバーブのパラメータを設定
    delay_samples = int(sound.frame_rate * room_scale * 0.1)
    decay = 1 - damping
    
    # リバーブを適用
    reverb_samples = np.zeros_like(samples)
    for i in range(len(samples)):
        if i < delay_samples:
            reverb_samples[i] = samples[i]
        else:
            reverb_samples[i] = samples[i] + reverberance * decay * reverb_samples[i - delay_samples]
    
    # 結果を AudioSegment に戻す
    reverb_audio = sound._spawn(reverb_samples.tobytes())
    return reverb_audio