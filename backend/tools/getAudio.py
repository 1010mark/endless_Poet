from tools import redisClient
from tools.convertBetweenBinAndAudioSegment import convert_binary_to_audiosegment
import json
from pydub import AudioSegment

def get_audio():
    try:
        cache = redisClient.get_redis_client()
        # if cache.exists("script") == 0 or cache.exists("audio_binary") == 0:
        #    updateAudio.update_audio()
        with cache.pipeline() as pipe:
            pipe.get("script")
            pipe.get("audio_binary")
            pipe.get("updated_at")
            results = pipe.execute()            
        script = json.loads(results[0])
        audioSegment = convert_binary_to_audiosegment(results[1]) 
        return {"script": script, "AudioSegment": audioSegment, "updated_at": results[2]}
    except Exception:
        import traceback
        traceback.print_exc()
        print("音声取得失敗しました～～！！！！")
        return {
            "script": [],
            "AudioSegment": AudioSegment.silent(duration=64 * 1000),
            "updated_at": "0"
        }