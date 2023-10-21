from roboflowoak import RoboflowOak
from numpy import mean
import cv2
import time
import numpy as np

width = 640
height = 640
dim = (width, height)
size = (width, height)

# font
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
org = (25, 25)
fontScale = 1
color = (255, 0, 0)
thickness = 1

fpsArray = []
averageFPS = 0

pixel_ratio_array = []
averagePR = 0

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (640, 640))

if __name__ == '__main__':
    # instantiating an object (rf) with the RoboflowOak module
    # API Key: https://docs.roboflow.com/rest-api#obtaining-your-api-key
    rf = RoboflowOak(model="MODEL-AI", confidence=0.4, overlap=0.3,
    version="1", api_key="API-KEY", rgb=True,
    depth=False, device=None, blocking=True)
    # Running our model and displaying the video output with detections
    while True:
        t0 = time.time()
        # The rf.detect() function runs the model inference
        result, frame, raw_frame, depth = rf.detect()

        # print(result)

        predictions = result["predictions"]

        # print(predictions)

        for object in predictions:
            
            # print(object.json())
            object_JSON = object.json()

            object_class = str(object_JSON['class'])
            object_class_text_size = cv2.getTextSize(object_class, font, fontScale, thickness)
            print("CLASS: " + object_class)
            object_confidence = str(round(object_JSON['confidence']*100 , 2)) + "%"
            print("CONFIDENCE: " + object_confidence)

            # pull bbox coordinate points
            x0 = object_JSON['x'] - object_JSON['width'] / 2
            y0 = object_JSON['y'] - object_JSON['height'] / 2
            x1 = object_JSON['x'] + object_JSON['width'] / 2
            y1 = object_JSON['y'] + object_JSON['height'] / 2
            box = (x0, y0, x1, y1)
            # print("Bounding Box Cordinates:" + str(box))

            ## THIS IS WHERE THE PIXEL RATIO IS CREATED ##
            if object_class == "Soda":
            
                soda_inches = 4.83

                soda_height = object_JSON['height']

                pixel_to_inches = soda_height / soda_inches
                pixel_ratio_array.append(pixel_to_inches)
                # print(pixel_to_inches)

                object_Inches = soda_height / averagePR

                print("SODA INCHES: " + str(object_Inches))

                inches_ORG = (int(x0), int(y0-10))

                frame = cv2.putText(frame, 'Inches: ' + str(object_Inches)[:4], inches_ORG, font, fontScale, (255,255,255), thickness, cv2.LINE_AA)

            if object_class == "Figure":

                figure_height = object_JSON['height']

                object_Inches = figure_height / averagePR

                print("FIGURE INCHES: " + str(object_Inches))

                inches_ORG = (int(x0), int(y0-10))

                frame = cv2.putText(frame, 'Inches: ' + str(object_Inches)[:4], inches_ORG, font, fontScale, (255,255,255), thickness, cv2.LINE_AA) 

            if object_class == "Water":

                water_height = object_JSON['height']

                object_Inches = water_height / averagePR

                print("WATER INCHES: " + str(object_Inches))

                inches_ORG = (int(x0), int(y0-10))

                frame = cv2.putText(frame, 'Inches: ' + str(object_Inches)[:4], inches_ORG, font, fontScale, (255,255,255), thickness, cv2.LINE_AA)   
        
        # timing: for benchmarking purposes
        t = time.time()-t0
       

        # setting parameters for depth calculation
        # max_depth = np.amax(depth)
        # print("DEPTH: " + str(max_depth))

        # resize image
        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

        fpsArray.append(1/t)
        averageFPS = mean(fpsArray)
        averagePR = mean(pixel_ratio_array)

        print("FPS: ", 1/t)
        print("PREDICTIONS: ", [p.json() for p in predictions])
        print("PIXEL RATIO: " + str(averagePR) + "\n")

        resized = cv2.putText(resized, 'FPS: ' + str(averageFPS)[:4], org, font, fontScale, color, thickness, cv2.LINE_AA)

        del fpsArray[:-180]
        del pixel_ratio_array[:-180]

        cv2.imshow("frame", resized)

        out.write(resized)
    
        # how to close the OAK inference window / stop inference: CTRL+q or CTRL+c
        if cv2.waitKey(1) == ord('q'):
            break