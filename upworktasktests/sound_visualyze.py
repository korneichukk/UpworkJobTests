import numpy as np
import moviepy.editor as mp
from moviepy.video.VideoClip import TextClip
from moviepy.editor import concatenate_videoclips
import matplotlib.pyplot as plt
from moviepy.video.io.bindings import mplfig_to_npimage
from pathlib import Path

# Load your audio
audio_path = (
    "/home/jesus/code/UpworkTaskTests/upworktasktests/file_example_MP3_700KB.mp3"
)
audio_clip = mp.AudioFileClip(audio_path)

# Set up some parameters
duration = audio_clip.duration
fps = 30
total_frames = int(duration * fps)


def make_frame(t):
    fig, ax = plt.subplots(figsize=(8, 4))

    # Replace this with your own logic for generating the visualization
    # For example, you can use FFT to analyze the audio and generate visuals

    # Example: simple visualization using a sine wave
    freq = np.sin(2 * np.pi * t)
    ax.plot([0, 1], [0, freq], "b")

    ax.set_xlim(0, 1)
    ax.set_ylim(-1, 1)
    ax.set_title("Sound Visualizer")

    frame = mplfig_to_npimage(fig)
    plt.close(fig)
    return frame


# Create a VideoClip with the visualizer
visualizer_clip = mp.VideoClip(make_frame, duration=duration)

# Combine the audio and visualizer clips
final_clip = mp.concatenate_videoclips([visualizer_clip.set_audio(audio_clip)])

# Export the final video
output_path = "output_visualizer.mp4"
final_clip.write_videofile(output_path, codec="libx264", fps=fps)

print("Visualizer video generated successfully!")
