import moviepy.editor as mp


def trim_video(src_filename, start_frame, end_frame):

    start_time = start_frame // 30
    end_time = end_frame // 30
    trim_clip = mp.VideoFileClip(src_filename).subclip(start_time, end_time)
    # final_clip.write_videofile(
    #     dst_filename,
    #     codec='libx264', 
    #     audio_codec='aac', 
    #     temp_audiofile='temp-audio.m4a', 
    #     remove_temp=True
    # )
    return trim_clip

def concat_movie(clips, dst_filename):
    final_clip = mp.concatenate_videoclips(clips)
    final_clip.write_videofile(
        dst_filename,
        codec='libx264', 
        audio_codec='aac', 
        temp_audiofile='temp-audio.m4a', 
        remove_temp=True
    )
    return

if __name__ == "__main__":
    highlight_scenes = [33300, 69480, 162420, 172980, 199740, 224280]
    clips = []
    for i in highlight_scenes:
        clips.append(
            trim_video(
                "data/kochi_gameonly.mp4", 
                i-600,
                i+300
                )
            )
    concat_movie(clips, "data/highlight.mp4")

