from ffmpeg import FFmpeg
from uuid import uuid4
import os


def ffmpeg_convert(audio_stream):
    save_location = str(uuid4()) + ".webm"
    output_filename = str(uuid4()) + ".wav"

    audio_stream.save(save_location)
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(save_location)
        .output(
            output_filename,
            {"codec:v": "libx264"},
            vf="scale=1280:-1",
            preset="veryslow",
            crf=24,
        )
    )

    ffmpeg.execute()
    os.remove(save_location)
    return output_filename
