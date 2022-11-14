import moviepy.editor as mp


def trim_video(src_filename, dst_filename, start_frame, end_frame):

    start_time = start_frame // 30
    end_time = end_frame // 30
    final_clip = mp.VideoFileClip(src_filename).subclip(start_time, end_time)
    final_clip.write_videofile(
        dst_filename,
        codec='libx264', 
        audio_codec='aac', 
        temp_audiofile='temp-audio.m4a', 
        remove_temp=True
    )

if __name__ == "__main__":

    trim_video(
        "data/kochi_gameonly.mp4",
        "data/kochi_game_trim.mp4", 
        32340,
        33600
    )

