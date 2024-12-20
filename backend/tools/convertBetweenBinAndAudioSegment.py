import io
from pydub import AudioSegment

def convert_audiosegment_to_binary(audio_segment, format = "wav"):
    with io.BytesIO() as buffer: # with文を使うことで、bufferを使い終わったら自動的にclose()される。メモリ解放。
        audio_segment.export(buffer, format=format)
        return buffer.getvalue()

def convert_binary_to_audiosegment(binary_data, format = "wav"):
    with io.BytesIO(binary_data) as buffer:
        return AudioSegment.from_file(buffer, format=format)