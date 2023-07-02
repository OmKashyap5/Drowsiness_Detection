video_capture=cv2.VideoCapture(0)
if(video_capture.isOpened()):
    #This loop runs for the time the vehicle is on. It can beforcefully shut by pressing 'q' or any command as possible. The manufacturer
    #can apply the optimal condition
    while(True):
        start_time=time.time()
        end_time=start_time+0.7
        open=0
        closed=0
        #This loop runs via function for 0.7 second as it is equal to twice the average required for human to blink. If the eye is closed for more than
        #time person is possibly drowsie.
        while(time.time()<end_time):
            ret,frame=video_capture.read()
            if(ret==True):
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)   # Convert the frame to grayscale as model is trained on gray scale images
                faces=face.detectMultiScale(gray)             # Detect faces
                for (x,y,w,h) in faces:                       # Iterate over the detected faces
                    roi_gray=gray[y:y+h,x:x+w]                # Get the region of interest containing the face in gray scale image
                    roi_color=frame[y:y+h,x:x+w]              # Get the region of interest containing the face in colored image
                    eyes=eye.detectMultiScale(roi_gray)       # Detect eyes in the ROI
                    for (a,b,c,d) in eyes:                    #Iterate over the detected faces
                        eye_roi_gray=roi_gray[b:b+d,a:a+c]    # Get the region of interest containing the eye in grey scale image
                        eye_roi_color=roi_color[b:b+d,a:a+c]  # Get the region of interest containing the eye in colored image
                        eye_image=eye_roi_gray.copy()         #Creating an image out of the eye_roi_grey for further process
                        #Processing the image according to requirments of the model
                        resized_frame=cv2.resize(eye_image,(65,65))
                        normalized_frame=resized_frame/255.0
                        flattened_frame=normalized_frame.flatten()
                        #Predicting eyes condition open or closed
                        predictions=model.predict(flattened_frame)
                        if(predictions==0):
                            closed=closed+1
                        elif(predictions==1):
                            open=open+1
        if(open>=1.05*closed):
            print("Normal")               # Normal.No action required
        elif(open>=0.3*closed):
            print("notification")         #Insert a code to issue a notificatio or confirmation prompt
        elif(open<3*closed):
            print("alarm")                #Insert a code to ring an alarm

        #The above choosen value are custom and calculated by self estimation.
        #This can be changed according to users preference
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    print("Camera is closed. Try giving other camera index in videocapture")
video_capture.release()