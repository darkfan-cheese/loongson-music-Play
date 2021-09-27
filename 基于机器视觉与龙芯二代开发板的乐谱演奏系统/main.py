import cv2 as cv
import data
import Play


data = data.Music()
play = Play.Play()
play.get()
# print(play.files)
play.play(data.song[0])




