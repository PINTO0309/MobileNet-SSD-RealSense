import cv2, time

width  = 640
height = 480
fps = ""
framecount = 0
elapsedTime = 0

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FPS, 180)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
#cv2.namedWindow('FPS', cv2.WINDOW_AUTOSIZE)

while True:
    t1 = time.perf_counter()
    ret, frame = cap.read()
    #cv2.putText(frame, fps, (width-180,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)
    #cv2.imshow('FPS', frame)
    #if cv2.waitKey(1)&0xFF == ord('q'):
    #    break
    t2 = time.perf_counter()
    framecount += 1
    if framecount >= 30:
        fps = "(Playback) {:.1f} FPS".format(framecount/elapsedTime)
        print("fps = ", str(fps))
        framecount = 0
        elapsedTime = 0
    elapsedTime += t2-t1
cap.release()
cv2.destroyAllWindows()

