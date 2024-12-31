import os, json, random
from pydub import AudioSegment
from tools import redisClient

"""
    backend
        - tools
        - resources (ignored on git)
            - Kick
                - 1.wav (BPM120, 8bars)
            - Snare
            …
            - Ambient
                - ~.wav (BPM?120, 32bars)
"""
initial_instrument_dict = {
    "Bass": "",
    "Clap": "",
    "Cowbell": "",
    "Cymbal": "",
    "Epec": "",
    "Hihat": "",
    "Kick": "",
    "Punch": "",
    "Synth": "",
    "Tom": ""
}

# Camel CaseとSnake Caseが混在してる。
def generateInstruments():
    try:
        instruments_dict = get_instruments_dict()
        inst = AudioSegment.silent(duration=0)
        for i in range(4):
            instruments_dict = update_instruments_dict(instruments_dict)
            print(instruments_dict)
            set_instruments_dict(instruments_dict)
            inst += overlay_Ambient(synthesize_instruments(instruments_dict))
        print("generateInstruments success")
        return inst 
    except:
        print("generateInstruments failed")
        import traceback
        traceback.print_exc()
        return AudioSegment.silent(duration=64 * 1000)

def get_instruments_dict():
    global initial_instrument_dict
    cache = redisClient.get_redis_client()
    if cache.exists("instruments_dict") == 0:
        cache.set("instruments_dict", json.dumps(initial_instrument_dict))
        instruments_dict = initial_instrument_dict
    else:
        instruments_dict = json.loads(cache.get("instruments_dict"))
    return instruments_dict

def set_instruments_dict(instruments_dict):
    cache = redisClient.get_redis_client()
    cache.set("instruments_dict", json.dumps(instruments_dict))
    return instruments_dict
    
def synthesize_instruments(instruments_dict):
    inst_silent_instrument_probability = os.getenv('INST_SILENT_INSTRUMENT_PROBABILITY', '0.05')
    try:
        inst_silent_instrument_probability = float(inst_silent_instrument_probability)
    except ValueError:
        inst_silent_instrument_probability = 0.05
    if random.random() < inst_silent_instrument_probability:
        return AudioSegment.silent(duration= 16*1000)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.abspath(os.path.join(script_dir, "..", "resources"))
    inst_limit_str = os.getenv('INST_LIMIT', '6')
    try:
        inst_limit = int(inst_limit_str)
    except ValueError:
        inst_limit = 6
    combined = AudioSegment.silent(duration=16 * 1000)
    count = 0
    for instrument, identifier in instruments_dict.items():
        if count >= inst_limit:
            break
        if identifier == "":
            continue
        wav_path = os.path.join(resources_dir, instrument, f"{identifier}.wav")
        if os.path.exists(wav_path):
            try:
                sound = AudioSegment.from_wav(wav_path)
                combined = combined.overlay(sound)
                count += 1
            except Exception as e:
                import traceback
                traceback.print_exc()
                pass
        else:
            pass
    return combined

def overlay_Ambient(audio_segment):
    inst_silent_ambient_probability = os.getenv("INST_SILENT_AMBIENT_PROBABILITY", "0.01")
    try:
        inst_silent_ambient_probability = float(inst_silent_ambient_probability)
    except ValueError:
        inst_silent_ambient_probability = 0.01
    if random.random() < inst_silent_ambient_probability:
        return AudioSegment.silent(duration=64*1000)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ambient_dir = os.path.abspath(os.path.join(script_dir, '..', 'resources', 'Ambient'))
    if not os.path.isdir(ambient_dir):
        return audio_segment
    wav_files = [""]
    try:
        for file_name in os.listdir(ambient_dir):
            file_path = os.path.join(ambient_dir, file_name)
            if os.path.isfile(file_path) and file_name.lower().endswith('.wav'):
                wav_files.append(file_name)
    except Exception as e:
        return audio_segment
    selected_wav = random.choice(wav_files)
    if selected_wav == "":
        return audio_segment
    selected_path = os.path.join(ambient_dir, selected_wav)
    try:
        ambient_sound = AudioSegment.from_wav(selected_path)
        combined = audio_segment.overlay(ambient_sound)
        return combined
    except Exception as e:
        return audio_segment

def update_instruments_dict(instruments_dict): # 確率的更新 
    update_rate_str = os.getenv('INST_UPDATE_PROBABIlITY', '0.5')
    try:
        update_rate = float(update_rate_str)
    except ValueError:
        update_rate = 0.5
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.abspath(os.path.join(script_dir, '..', 'resources'))
    for instrument in instruments_dict.keys():
        rand = random.random()
        if rand < update_rate:
            instrument_dir = os.path.join(resources_dir, instrument)
            if os.path.isdir(instrument_dir):
                wav_files = []
                try:
                    for file_name in os.listdir(instrument_dir):
                        file_path = os.path.join(instrument_dir, file_name)
                        if os.path.isfile(file_path) and file_name.lower().endswith('.wav'):
                            wav_files.append(file_name)
                except Exception as e:
                    wav_files = []

                if wav_files: # これは len(wav_files) == 0 と同じ
                    identifiers = []
                    for wav_file in wav_files:
                        identifier, _ = os.path.splitext(wav_file)
                        identifiers.append(identifier)
                    new_identifier = random.choice(identifiers)
                    instruments_dict[instrument] = new_identifier
                else:
                    instruments_dict[instrument] = ""
            else:
                instruments_dict[instrument] = ""
    return instruments_dict
