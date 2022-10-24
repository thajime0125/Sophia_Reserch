import math
import cv2

## 動画を開始ミリ秒～終了ミリ秒までカットする
## 
def trim_video(src_filename, dst_filename, start_seconds, end_seconds):
    ## FPS、フレーム数・開始終了フレーム番号取得
    videoCapture = cv2.VideoCapture(src_filename)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    totalFrames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    startFrameIndex = math.ceil(fps * start_seconds)
    stopFrameIndex = math.ceil(fps * end_seconds)
    if(startFrameIndex < 0): 
        startFrameIndex = 0
    if(stopFrameIndex >= totalFrames):
        stopFrameIndex = totalFrames-1
    videoCapture.set(cv2.CAP_PROP_POS_FRAMES, startFrameIndex)
    frameIndex = startFrameIndex
    
    ## 開始～終了地点までフレーム分割
    imgArr = []
    while(frameIndex <= stopFrameIndex):
        _,img = videoCapture.read()
        imgArr.append(img)
        frameIndex += 1
        
    ## 分割フレームをmp4動画に再構成
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    video = None
    tmpVideosrc_filename = dst_filename
    for img in imgArr:
        if(video is None):
            h,w,_ = img.shape
            video = cv2.VideoWriter(tmpVideosrc_filename, fourcc, 20.0, (w,h))
        video.write(img)
    video.release()
    

# if __name__ == "__main__":
#     ## こういう風に使う
#     trim_video(
#         "/path/to/target.mp4",
#         "/path/to/dest.mp4",
#         3200   ## => 3.2秒から
#         12800  ## => 12.8秒まで
#     )