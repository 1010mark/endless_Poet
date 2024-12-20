from tools import generatePoetry
from tools.generateLyrics import generateLyrics

def generateAudio():
    try:
        poetry = generatePoetry.generate_audio_on_bpm(generateLyrics())
        # TODO: ここでinstを追加する https://github.com/magenta/magenta
        return poetry
    except Exception as e:
        import traceback
        traceback.print_exc()
        return "Something went wrong", 500