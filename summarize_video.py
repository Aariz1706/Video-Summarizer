from moviepy.editor import VideoFileClip #Lets you load, cut, and save videos.
def summarize_video(input_path, output_path, duration=5):
    try:
        print(f"Processing {input_path}...")
        clip = VideoFileClip(input_path)
        short_clip = clip.subclip(0, min(duration, clip.duration))
        short_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
        print(f"✅ Summarized video saved to: {output_path}")
    except Exception as e:
        print(f"❌ Error: {e}")
# Example usage
input_video = "uploads/lockdown_side_effects.mp4"
output_video = "uploads/lockdown_short.mp4"
summarize_video(input_video, output_video)
