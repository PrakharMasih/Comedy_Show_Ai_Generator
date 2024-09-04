# import openai
# import re, os
# from requests import get
# import urllib.request
# from gtts import gTTS
# from moviepy.editor import *

# async def generate_video(input_text: str):
#     # Set your OpenAI API key
#     openai.api_key = os.getenv("OPENAI_API_KEY")

#     # Split the text by , and .
#     paragraphs = re.split(r"[,.]", input_text)

#     # Create Necessary Folders
#     os.makedirs("audio", exist_ok=True)
#     os.makedirs("images", exist_ok=True)
#     os.makedirs("videos", exist_ok=True)

#     # Loop through each paragraph and generate an image for each
#     for i, para in enumerate(paragraphs[:-1], start=1):
#         para = para.strip()
#         if not para:
#             continue

#         # Generate image
#         response = openai.Image.create(prompt=para, n=1, size="1024x1024")
#         image_url = response['data'][0]['url']
#         urllib.request.urlretrieve(image_url, f"images/image{i}.jpg")

#         # Generate audio
#         tts = gTTS(text=para, lang='en', slow=False)
#         tts.save(f"audio/voiceover{i}.mp3")

#         # Create video clip
#         audio_clip = AudioFileClip(f"audio/voiceover{i}.mp3")
#         image_clip = ImageClip(f"images/image{i}.jpg").set_duration(audio_clip.duration)
#         text_clip = (TextClip(para, fontsize=50, color="white")
#                      .set_pos('center')
#                      .set_duration(audio_clip.duration))

#         video = CompositeVideoClip([image_clip.set_audio(audio_clip), text_clip])
#         video.write_videofile(f"videos/video{i}.mp4", fps=24)

#     # Combine all video clips
#     video_files = sorted(os.listdir("videos"), key=lambda f: int(re.sub('\D', '', f)))
#     clips = [VideoFileClip(f"videos/{file}") for file in video_files]

#     final_video = concatenate_videoclips(clips, method="compose")
#     final_video_path = "final_video.mp4"
#     final_video.write_videofile(final_video_path)

#     return final_video_path
import openai
from openai import AsyncOpenAI
import re, os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import urllib.request
from gtts import gTTS
from moviepy.editor import *

async def generate_video(input_text: str):
    # Set your OpenAI API key
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Split the text by , and .
    paragraphs = [p.strip() for p in re.split(r"[,.]", input_text) if p.strip()]

    # Create Necessary Folders
    os.makedirs("audio", exist_ok=True)
    os.makedirs("images", exist_ok=True)
    os.makedirs("videos", exist_ok=True)

    async def process_paragraph(para: str, i: int):
        client = AsyncOpenAI()
        response = await client.images.generate(prompt=para, n=1, size="1024x1024")
        # Generate image
        # response = await openai.Image.acreate(prompt=para, n=1, size="1024x1024")
        image_url = response.data[0].url
        
        # Run synchronous operations in a thread pool
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            await loop.run_in_executor(pool, urllib.request.urlretrieve, image_url, f"images/image{i}.jpg")
            
            # Generate audio
            tts = await loop.run_in_executor(pool, lambda: gTTS(text=para, lang='en', slow=False))
            await loop.run_in_executor(pool, tts.save, f"audio/voiceover{i}.mp3")

        return i, para

    # Process all paragraphs concurrently
    tasks = [asyncio.create_task(process_paragraph(para, i)) for i, para in enumerate(paragraphs, start=1)]
    results = await asyncio.gather(*tasks)

    # Create video clips
    def create_video_clip(result):
        i, para = result
        audio_clip = AudioFileClip(f"audio/voiceover{i}.mp3")
        image_clip = ImageClip(f"images/image{i}.jpg").set_duration(audio_clip.duration)
        text_clip = (TextClip(para, fontsize=50, color="white")
                     .set_pos('center')
                     .set_duration(audio_clip.duration))

        video = CompositeVideoClip([image_clip.set_audio(audio_clip), text_clip])
        video.write_videofile(f"videos/video{i}.mp4", fps=24)
        return f"videos/video{i}.mp4"

    # Create video clips concurrently
    with ThreadPoolExecutor() as pool:
        video_files = list(pool.map(create_video_clip, results))

    # Combine all video clips
    clips = [VideoFileClip(file) for file in video_files]

    final_video = concatenate_videoclips(clips, method="compose")
    final_video_path = "final_video.mp4"
    final_video.write_videofile(final_video_path)

    return final_video_path

# Example usage
async def main():
    input_text = "This is a test, It has multiple parts, Each part will be a separate clip"
    result = await generate_video(input_text)
    print(f"Final video generated: {result}")

if __name__ == "__main__":
    asyncio.run(main())