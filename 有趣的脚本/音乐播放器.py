import pygame
import tkinter as tkr
from tkinter.filedialog import askdirectory
import os

music_player = tkr.Tk()
music_player.title("我的音乐播放器")
music_player.geometry("450x350")
directory = askdirectory()
os.chdir(directory)
song_list = os.listdir()

play_list = tkr.Listbox(music_player, font="Helvetica 12 bold", bg='yellow', selectmode=tkr.SINGLE)
for item in song_list:
    pos = 0
    play_list.insert(pos, item)
    pos += 1
pygame.init()
pygame.mixer.init()


def play():
    """播放"""
    pygame.mixer.music.load(play_list.get(tkr.ACTIVE))
    var.set(play_list.get(tkr.ACTIVE))
    pygame.mixer.music.play()


def stop():
    """停止"""
    pygame.mixer.music.stop()


def pause():
    """暂停"""
    pygame.mixer.music.pause()


def unpause():
    """取消暂停"""
    pygame.mixer.music.unpause()


Button1 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="播放", command=play, bg="blue", fg="white")
Button2 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="停止", command=stop, bg="red", fg="white")
Button3 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="暂停", command=pause, bg="purple", fg="white")
Button4 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="取消暂停", command=unpause, bg="orange", fg="white")

var = tkr.StringVar()
song_title = tkr.Label(music_player, font="Helvetica 12 bold", textvariable=var)

song_title.pack()
Button1.pack(fill="x")
Button2.pack(fill="x")
Button3.pack(fill="x")
Button4.pack(fill="x")
play_list.pack(fill="both", expand="yes")
music_player.mainloop()