import numpy as np
import cv2
import os
import subprocess

count = 0
cnt = 0
found = False
frame_no = 0;
global t_start 
t_start = 0.0
global t_end 
t_end = 0.0

def check():
        datafile = file('/home/hiren/YOLO/darknet/output')
        found = False
        for line in datafile:
            if 'person' in line:
                found = True
                break
        return found

cap = cv2.VideoCapture('videoplayback')
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()


while(1):
    ret, frame = cap.read()
    frame_no = frame_no+1;
    cframe = frame
    cv2.imshow('oimage',cframe)
    cv2.imwrite('/home/hiren/YOLO/darknet/data/snap.jpg', frame)
    cframe = frame
    size = frame.size
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    nzCount = cv2.countNonZero(fgmask);
    dFactor = 33000
    zCount  = size - nzCount


    if count > 2 and count < 150 and found == True:           ### Person is Detecetd in this set of frames ##
	count = count + 1
        continue


    if  nzCount > dFactor:   
	print "Something Detected"                                ### Checking The Density of White Pixels in Binary Image ###
	count = count+1
	
	os.chdir('/home/hiren/YOLO/darknet') 	             ### Something Detected in frame so run your network algorithm on that frame ###
	os.system('./darknet detect cfg/yolo.cfg yolo.weights data/snap.jpg > output')

	found = check()
	
	if found:
		print "Person Detected in Frame"            ### Capture timestamps as the person is detected in frame ###
		if count == 1:
	        	print "Save Start Time" 
			f_no = str(frame_no)
			t_start = subprocess.check_output("awk 'NR == n' n=" + f_no + " /home/hiren/YOLO/darknet/timestamps",shell=True)
			t_start = float(t_start)
			t_start = int(t_start)
		else:
			print "Save End Time"
			if count > 149:
				i = 0	
				while(i < 40):
					ret, frame = cap.read()
					i = i+1
					frame_no = frame_no + 1
					count = count + 1
					
			f_no = str(frame_no)
			t_end = subprocess.check_output("awk 'NR == n' n=" + f_no + " /home/hiren/YOLO/darknet/timestamps",shell=True)
			t_end = float(t_end)
			t_end = int(t_end)
	else:
		if count > 149:
			print "No person detected with count > 149"
			print "Finding End Time For Frame" + str(frame_no)
        		f_no = str(frame_no)
        		t_end = subprocess.check_output("awk 'NR == n' n=" + f_no + " /home/hiren/YOLO/darknet/timestamps",shell=True)
        		t_end = float(t_end)
        		t_end = int(t_end)
        		#t_end = os.system("awk 'NR == n' n=" + f_no + " /home/hiren/YOLO/darknet/timestamps") 
        		print "Write staring and ending time to files output.txt"
        		t_start = '{}:{}'.format(*divmod(t_start, 60))
        		t_end = '{}:{}'.format(*divmod(t_end, 60))
        		os.system("echo "+t_start+"-"+t_end+" >> /home/hiren/YOLO/darknet/output.txt")
			count = 0
			
		else:
			print "No Person Detected"
			i = 0
			while(i<40):
				ret, frame = cap.read()
                                i = i+1
                                frame_no = frame_no + 1
				
			count = 0

    else:
	print "Nothing Detected"
	if count != 0:
		if count > 149:
			print "Finding End Time For Frame" + str(frame_no)
        		f_no = str(frame_no)
        		t_end = subprocess.check_output("awk 'NR == n' n=" + f_no + " /home/hiren/YOLO/darknet/timestamps",shell=True)
        		t_end = float(t_end)
        		t_end = int(t_end)
        		print "Write staring and ending time to files output.txt"
        		t_start = '{}:{}'.format(*divmod(t_start, 60))
        		t_end = '{}:{}'.format(*divmod(t_end, 60))
        		os.system("echo "+t_start+"-"+t_end+" >> /home/hiren/YOLO/darknet/output.txt")
			count = 0
		else:
			count = 0

    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cv2.imshow('oimage',cframe)
cap.release()
cv2.destroyAllWindows()

