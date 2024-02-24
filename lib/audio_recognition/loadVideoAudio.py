from moviepy.editor import VideoFileClip
from pydub import AudioSegment

# Load the MP4 video file
video_path = 'VID-20161015-WA0010.mp4'  # Replace 'path_to_your_video.mp4' with the path to your video file
video_clip = VideoFileClip(video_path)

# Cut the video based on the end time
# For example, if you want to cut the first 10 seconds of the video
end_time = 5  # End time in seconds
cut_video_clip = video_clip.subclip(0, end_time)

# Extract the audio from the cut video
extracted_audio = cut_video_clip.audio

# Write the extracted audio to a WAV file
output_audio_path = './extracted_audio.wav'  # Path for the output WAV file
extracted_audio.write_audiofile(output_audio_path, codec='pcm_s16le')  # 'pcm_s16le' is the codec for WAV format

print(f"Audio extracted and saved to {output_audio_path}")


# Step 4: Load the new audio and cut it based on start and end seconds
start_time = 1200  # Start time in milliseconds
end_time = 2000  # End time in milliseconds
audio_segment = AudioSegment.from_wav(output_audio_path)
cut_audio = audio_segment[start_time:end_time]

# Save the cut audio to a new WAV file
cut_audio_path = 'cut_audio.wav'
cut_audio.export(cut_audio_path, format="wav")