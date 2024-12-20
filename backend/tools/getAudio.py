from tools import redisClient, updateAudio
from tools.convertBetweenBinAndAudioSegment import convert_binary_to_audiosegment
import json

def get_audio():
    try:
        cache = redisClient.get_redis_client()
        if cache.exists("script") == 0 or cache.exists("audio_binary") == 0:
            updateAudio.update_audio()
        with cache.pipeline() as pipe:
            pipe.get("script")
            pipe.get("audio_binary")
            pipe.get("updated_at")
            results = pipe.execute()
            script = json.loads(results[0])
            audio_binary = convert_binary_to_audiosegment(results[1]) 
            return {"script": script, "AudioSegment": audio_binary, "updated_at": results[2]}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return "Something went wrong", 500