'''
function: multi_tracking demo
date: 2018-5-29
author: antengda
description: allow you to select tow objects to track
'''
import cv2 
import sys
import time

def multi_tracking(filepath):
    
    #create multitracker construct
    multi_tracker = cv2.MultiTracker_create()
    tracker_type = 'CSRT'
    
    cap = cv2.VideoCapture(filepath)
    ok, frame = cap.read()

    bbox1 = cv2.selectROI('tracking',frame)
    bbox2 = cv2.selectROI('tracking',frame)

    if ok:
        print('read the first frame,allow you to select four objects to track')

    multi_tracker.add(cv2.TrackerCSRT_create(),frame,tuple(bbox1))
    multi_tracker.add(cv2.TrackerCSRT_create(),frame,tuple(bbox2))
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            print('failed to read a frame')
            break

        #start to count
        start = cv2.getTickCount()
        
        #multi_tracker update per frame
        ok,bboxes = multi_tracker.update(frame)
        
        #calculate fps
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - start)

        #drawing boxes
        if ok:
            for i in range(bboxes.shape[0]):
                p1 = (int(bboxes[i][0]), int(bboxes[i][1]))
                p2 = (int(bboxes[i][0] + bboxes[i][2]), int(bboxes[i][1] + bboxes[i][3]))
                cv2.rectangle(frame, p1, p2, (255,0,255), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2) 
        
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 :
             break   

if __name__ == '__main__':
    multi_tracking('/media/antengda/2617D55455123745/video/multi_face.avi')