from tools import redisClient, generateAudio
from tools.convertBetweenBinAndAudioSegment import convert_audiosegment_to_binary
from datetime import datetime
import json

def update_audio():
    try:
        cache = redisClient.get_redis_client()
        audio = generateAudio.generateAudio()
        with cache.pipeline() as pipe:
            pipe.set("script", json.dumps(audio["script"])) 
            pipe.set("audio_binary", convert_audiosegment_to_binary(audio["AudioSegment"]))
            pipe.set("updated_at", int(datetime.now().timestamp()))
            pipe.execute()
    except Exception as e:
        import traceback
        traceback.print_exc()
        return "Something went wrong", 500