# detection
Detecting Human Presence in Video

The Model is successfuuly tested and run on local Ubuntu 14.04.

What required to run this repo ?
   (1)OpenCV 3
   (2)Python 2.7

How to run this Repo ?
 
  Step -1
     I have used YOLO network for detecting human presence in video. So you need to first clone the YOLO repo.
     
     mkdir YOLO
     cd YOLO
     git clone https://github.com/pjreddie/darknet
     cd darknet
     make
     
  Step -2
  
     See the attached timestamps file which have timestamps of all frames of given video. Put that file into /YOLO/darknet       directory
  
  Step -3
  
     Input Video -  https://drive.google.com/file/d/0B2vPCVjlmUOsa2otcnJMbmtKRFE/view?usp=sharing
     Download and Rename the video as videoplayback
     Run detection.py file attached above by firing command -  
     
     python detection.py    on your shell.
     
     
    Your Detection Model will start running. Detection timestamps (when person is detected in video) will be stored in output.txt file in
    /YOLO/darknet/ directory. I have attached a sample output.txt generated on my machhine.
    
    

