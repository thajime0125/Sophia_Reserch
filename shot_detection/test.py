import cv2
import numpy as np

INFILE = "camera.mp4" # movie file
THRESH = 55.55679398148148 # threshold 

ESC_KEY = 27     # Escキー
INTERVAL= 1      # 待ち時間

WINNAME = "test"
cv2.namedWindow(WINNAME)

class MovieIter(object): #動画のフレームを返すイテレータ
    def __init__(self, moviefile, size=None, inter_method=cv2.INTER_AREA):
        #TODO: check if moviefile exists
        self.org = cv2.VideoCapture(moviefile)
        self.framecnt = 0
        self.size = size #frame size
        self.inter_method = inter_method
    def __iter__(self):
        return self
    def __next__(self):
        self.end_flg, self.frame = self.org.read()
        if not self.end_flg: # end of the movie
            raise StopIteration()
        self.framecnt+=1
        if self.size: # resize when size is specified
            self.frame = cv2.resize(self.frame, self.size, interpolation=self.inter_method)
        return self.frame
    def __del__(self): # anyway it works without destructor 
        self.org.release()

def MSE(pic): # mean square error
    return np.mean(np.square(pic))
    
def MAE(pic): # mean absolute error
    return np.mean(np.abs(pic))

def main():
    picsize = (64, 36)
    
    frame_cnt = 0
    frame_ultima = np.zeros((*picsize[::-1], 3)) # create empty image
    
    for frame in MovieIter(INFILE, None):
        frame_penult = frame_ultima
        frame_ultima = cv2.resize(frame, picsize, interpolation=cv2.INTER_AREA) #指定サイズに縮小
        
        cv2.imshow(WINNAME, frame)
        key = cv2.waitKey(1) # quit when esc-key pressed
        if key == ESC_KEY:
            break
        
        #差分画像作成
        diff = frame_ultima.astype(np.int) - frame_penult.astype(np.int)
        
        if MAE(diff)>=THRESH: #閾値よりMAEが大きい場合、カットと判定
            print("Cut detected!: frame {}".format(frame_cnt))
        
        frame_cnt+=1
    

if __name__ == "__main__":
    main()