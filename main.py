import cv2 as cv
import numpy as np
import module as m
import time
import csv
import xlrd
import xlwt
from xlwt import Workbook
import PILasOPENCV as Image
import PILasOPENCV as ImageDraw
import PILasOPENCV as ImageFont

#write Excel
wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')

#read Excel
read = xlrd.open_workbook("Hasil Pertanyaan.xls")
sheet = read.sheet_by_index(0)
sheet.cell_value(0,0)
sheet1.write(0, 0, "Pertanyaan")
sheet1.write(0, 1, "Jawaban")

# Variables
COUNTER = 0
CLOSED_EYES_FRAME = 3
cameraID = 0
delay = 0
delay1 = 0
videoPath = "Video/Your Eyes Independently_Trim5.mp4"
# variables for frame rate.
FRAME_COUNTER = 0
START_TIME = time.time()
FPS = 0
i = 1
n = 0
kanan = 0
kiri = 0
layak = 0
coorX = 950 - len(sheet.cell_value(i-0, 0)*14)
coorX1 = 950 - len(sheet.cell_value(i, 0)*14)

# creating camera object
camera = cv.VideoCapture(0, cv.CAP_DSHOW)
camera.set(3,1080)
camera.set(4,720)
#camera.set(15, 0.1)

img_1 = cv.imread('Background.png')
img_2 = cv.imread('MainMenuStretched.png')
img_1 = cv.putText(img_1, (sheet.cell_value(i, 0)), (950 - len(sheet.cell_value(i, 0)*14), 300), m.fonts, 1.5, m.WHITE, 2)
img_1 = cv.putText(img_1, (sheet.cell_value(i, 1)), (200, 610), m.fonts, 2, m.WHITE, 2)
img_1 = cv.putText(img_1, (sheet.cell_value(i, 2)), (1625, 610), m.fonts, 2, m.WHITE, 2)

while True:
    cv.imshow('Main Menu', img_2)
    kunci = cv.waitKey(1)
    if (kunci == ord(' ')):
        cv.destroyWindow('Main Menu')
        while True:
            FRAME_COUNTER += 1
            # getting frame from camera
            ret, frame = camera.read()
            if ret == False:
                break

            # converting frame into Gry image.
            grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            height, width = grayFrame.shape
            circleCenter = (int(width/2), 50)
            # calling the face detector funciton
            image, face = m.faceDetector(frame, grayFrame)
            if face is not None:

                # calling landmarks detector funciton.
                image, PointList = m.faceLandmakDetector(frame, grayFrame, face, False)
                # print(PointList)

                cv.putText(frame, f'FPS: {round(FPS,1)}',
                           (460, 20), m.fonts, 0.7, m.WHITE, 2)
                RightEyePoint = PointList[36:42]
                LeftEyePoint = PointList[42:48]
                mask, pos, color = m.EyeTracking(frame, grayFrame, RightEyePoint)
                maskleft, leftPos, leftColor = m.EyeTracking(
                    frame, grayFrame, LeftEyePoint)


                # draw background as line where we put text.

                cv.line(image, (30, 90), (100, 90), color[0], 30)
                cv.line(image, (25, 50), (135, 50), m.WHITE, 30)
                cv.line(image, (int(width-150), 50), (int(width-45), 50), m.WHITE, 30)
                cv.line(image, (int(width-140), 90),
                        (int(width-60), 90), leftColor[0], 30)


                # writing text on above line
                cv.putText(image, f'{pos}', (35, 95), m.fonts, 0.6, color[1], 2)
                cv.putText(image, f'{leftPos}', (int(width-140), 95),
                           m.fonts, 0.6, leftColor[1], 2)
                cv.putText(image, f'Right Eye', (35, 55), m.fonts, 0.6, color[1], 2)
                cv.putText(image, f'Left Eye', (int(width-145), 55),
                           m.fonts, 0.6, leftColor[1], 2)

                for n in range(sheet.nrows):
                    with open('Hasil Pertanyaan 2.xls', 'a', newline="") as file:
                        wb.save('Hasil Pertanyaan 2.xls')
                        cv.imshow('UI', img_1)
                        if f'{leftPos}' == 'Pilihan 1' or f'{leftPos}' == 'Pilihan 1' and f'{pos}' == 'Pilihan 1':
                            delay += 0.015
                            delay1 += 0.015
                            kiri += 0.015
                            if delay > 5:
                                if i == 1:
                                    sheet1.write(i,0, (sheet.cell_value(i, 0)))
                                    sheet1.write(i,1, (sheet.cell_value(i, 1)))
                                    i+=1
                                img_1 = cv.imread('Left.png') #hasil kiri ditampilkan
                                img_1 = cv.putText(img_1, (sheet.cell_value(i-1, 0)), (950 - len(sheet.cell_value(i-1, 0)*14), 300), m.fonts, 1.5, m.WHITE, 2)
                                img_1 = cv.putText(img_1, (sheet.cell_value(i, 1)), (200, 610), m.fonts, 2, m.WHITE, 2)
                                img_1 = cv.putText(img_1, (sheet.cell_value(i, 2)), (1625,610), m.fonts, 2, m.WHITE, 2)
                                sheet1.write(i,0, (sheet.cell_value(i, 0)))
                                sheet1.write(i,1, (sheet.cell_value(i, 1)))
                                delay = 0
                                print(i)
                                if i == 1:
                                    img_1 = cv.imread('Left.png') #hasil kiri ditampilkan
                                    img_1 = cv.putText(img_1, (sheet.cell_value(i, 0)), (950 - len(sheet.cell_value(i, 0)*14), 300), m.fonts, 3, m.WHITE, 2)
                                    img_1 = cv.putText(img_1, (sheet.cell_value(i, 1)), (200, 610), m.fonts, 2, m.WHITE, 2)
                                    img_1 = cv.putText(img_1, (sheet.cell_value(i, 2)), (1625, 610), m.fonts, 2, m.WHITE, 2)
                            if delay1 > 7:
                                if i == 2:
                                    img_1 = cv.putText(img_1, (sheet.cell_value(i-1, 0)), (950 - len(sheet.cell_value(i, 0)*14), 300), m.fonts, 1.5, m.WHITE, 2)
                                    coorX = 0
                                    coorX1 = 0
                                print(sheet.cell_value(i, 0) + " = " + sheet.cell_value(i, 1))
                                img_1 = cv.imread('Background.png') #hasil kiri ditampilkan
                                img_1 = cv.putText(img_1, (sheet.cell_value(i, 0)), (950 - len(sheet.cell_value(i, 0)*14), 300), m.fonts, 1.5, m.WHITE, 2)
                                img_1 = cv.putText(img_1, (sheet.cell_value(i, 1)), (200, 610), m.fonts, 2, m.WHITE, 2)
                                img_1 = cv.putText(img_1, (sheet.cell_value(i, 2)), (1625, 610), m.fonts, 2, m.WHITE, 2)
                                delay = 0
                                delay1 = 0
                                print(i)
                                i+=1
                        if f'{leftPos}' == 'Pilihan 2' or f'{leftPos}' == 'Pilihan 2' and f'{pos}' == 'Pilihan 2':
                            delay += 0.015
                            delay1 += 0.015
                            kanan += 0.015
                            if delay > 5.0:
                                if i == 1:
                                    sheet1.write(i,0, (sheet.cell_value(i, 0)))
                                    sheet1.write(i,1, (sheet.cell_value(i, 1)))
                                    i+=1
                                img_1 = cv.imread('Right.png') #hasil kanan ditampilkan
                                img_1 = cv.putText(img_1, (sheet.cell_value(i-1, 0)), (950 - len(sheet.cell_value(i-1, 0)*14), 300), m.fonts, 1.5, m.WHITE, 2)
                                img_1 = cv.putText(img_1, (sheet.cell_value(i, 1)), (200, 610), m.fonts, 2, m.WHITE, 2)
                                img_1 = cv.putText(img_1, (sheet.cell_value(i, 2)), (1625, 610), m.fonts, 2, m.WHITE, 2)
                                sheet1.write(i,0, (sheet.cell_value(i, 0))) #pertanyaan
                                sheet1.write(i,1, (sheet.cell_value(i, 2))) #jawaban
                                if i == 1:
                                    img_1 = cv.imread('Right.png') #hasil kanan ditampilkan
                                    img_1 = cv.putText(img_1, (sheet.cell_value(i, 0)), (950 - len(sheet.cell_value(i, 0)*14), 300), m.fonts, 3, m.WHITE, 2)
                                    img_1 = cv.putText(img_1, (sheet.cell_value(i, 1)), (200, 610), m.fonts, 2, m.WHITE, 2)
                                    img_1 = cv.putText(img_1, (sheet.cell_value(i, 2)), (1625, 610), m.fonts, 2, m.WHITE, 2)
                                delay = 0
                                layak+=1
                                print(i)
                            if delay1 > 7:
                                print(sheet.cell_value(i, 0) + " = " + sheet.cell_value(i, 2))
                                img_1 = cv.imread('Background.png')
                                img_1 = cv.putText(img_1, (sheet.cell_value(i, 0)), (950 - len(sheet.cell_value(i, 0)*14), 300), m.fonts, 1.5, m.WHITE, 2)
                                img_1 = cv.putText(img_1, (sheet.cell_value(i, 1)), (200, 610), m.fonts, 2, m.WHITE, 2)
                                img_1 = cv.putText(img_1, (sheet.cell_value(i, 2)), (1625, 610), m.fonts, 2, m.WHITE, 2)
                                delay = 0
                                delay1 = 0
                                print(i)
                                i+=1
                        if i == (sheet.nrows):
                            break
            if i == (sheet.nrows):
                print(layak)
                if layak > 5:
                    print("Anda layak untuk vaksin")
                    img_1 = cv.imread('Hasil.png')
                    img_1 = cv.putText(img_1, "ANDA LAYAK UNTUK VAKSIN", (300, 500), m.fonts, 3, m.WHITE, 2)
                    cv.imshow('UI', img_1)
                if layak <= 5:
                    print("Anda tidak layak untuk vaksin")
                    img_1 = cv.imread('Hasil.png')
                    img_1 = cv.putText(img_1, "ANDA TIDAK LAYAK UNTUK VAKSIN", (200, 500), m.fonts, 3, m.WHITE, 2)
                    cv.imshow('UI', img_1)
                    delay+=0.01
                key3 = cv.waitKey(1)
                if (key3 == ord('r')):
                    i = 0
                    layak = 0
                    cv.destroyWindow('Frame')
                    cv.destroyWindow('UI')
                    break

            key2 = cv.waitKey(1)
            if (key2 == ord('r')):
                i = 0
            # showing the frame on the screen
            cv.imshow('Frame', image)

            # calculating the seconds
            SECONDS = time.time() - START_TIME
            # calculating the frame rate
            FPS = FRAME_COUNTER/SECONDS

            key = cv.waitKey(1)

            if (key == ord('q')):
                cv.destroyWindow('Frame')
                cv.destroyWindow('UI')
                break
            if delay == 4:
                cv.destroyWindow('Frame')
                cv.destroyWindow('UI')
                break
# closing the camera
camera.release()
# Recoder.release()
# closing  all the windows
cv.destroyAllWindows()
