import asyncio
from tools import updateAudio

async def schedule_audio_update():
    while True:
        current_time = asyncio.get_event_loop().time()
        seconds = int(current_time) % 60
        
        if seconds % 20 == 0: # 20秒ごとに更新
            print("Running update_audio()...")
            asyncio.create_task(asyncio.to_thread(updateAudio.update_audio))  
            await asyncio.sleep(2)
        await asyncio.sleep(0.2)


async def main():
    asyncio.create_task(asyncio.to_thread(updateAudio.update_audio))
    asyncio.create_task(schedule_audio_update())
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
