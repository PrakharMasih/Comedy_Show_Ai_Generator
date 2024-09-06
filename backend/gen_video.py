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
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # Split the text by , and .
    paragraphs = [p.strip() for p in re.split(r"[,.]", input_text) if p.strip()]

    # Create Necessary Folders
    os.makedirs("audio", exist_ok=True)
    os.makedirs("images", exist_ok=True)
    os.makedirs("videos", exist_ok=True)

    async def process_paragraph(para: str, i: int):
        sanitized_text = re.sub(r'[^a-zA-Z0-9\s]', '', para)

        async def generate_image():
            try:
                response = await client.images.generate(
                    model="dall-e-3",
                    prompt=sanitized_text,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                return response.data[0].url
            except openai.BadRequestError as e:
                print(f"OpenAI API error for image generation: {e}")
                return None

        async def generate_audio():
            try:
                response = await client.audio.speech.create(
                    model="tts-1-hd",
                    voice="fable",
                    input=para
                )
                return response
            except Exception as e:
                print(f"OpenAI API error for audio generation: {e}")
                return None

        image_url, audio_response = await asyncio.gather(
            generate_image(),
            generate_audio()
        )

        if image_url and audio_response:
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor() as pool:
                await asyncio.gather(
                    loop.run_in_executor(pool, urllib.request.urlretrieve, image_url, f"images/image{i}.jpg"),
                    loop.run_in_executor(pool, audio_response.stream_to_file, f"audio/voiceover{i}.mp3")
                )
            return i, para
        else:
            print(f"Failed to generate image or audio for paragraph {i}")
            return None

    # Process all paragraphs concurrently
    tasks = [asyncio.create_task(process_paragraph(para, i)) for i, para in enumerate(paragraphs, start=1)]
    results = await asyncio.gather(*tasks)

    # Filter out None results
    valid_results = [result for result in results if result is not None]

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
        video_files = list(pool.map(create_video_clip, valid_results))

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