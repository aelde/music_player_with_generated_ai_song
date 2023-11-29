from tkinter import *
import pygame
from PIL import Image, ImageTk
from tkinter import filedialog
import os

root = Tk()
root.title('Music Player')
root.geometry("500x400")

pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = ''
paused = False

def load_song():
    directory = filedialog.askdirectory()
    if directory:
        root.deiconify = directory
    
        for song in os.listdir(root.deiconify):
            name, ext = os.path.splitext(song)
            if ext == '.mp3':
                songs.append(song)
                songlist.insert(END, song)
        
        songlist.select_set(0)
        global current_song
        current_song = songs[songlist.curselection()[0]]
        play_music()

def play_music(): 
    global paused, current_song
    if not paused:
        pygame.mixer.music.load(os.path.join(root.deiconify, current_song))
        pygame.mixer.music.play(loops=0)
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    global paused
    paused = True
    pygame.mixer.music.pause()

def next_music():
    global current_song, paused
    selected_index = songlist.curselection()
    if selected_index:
        songlist.select_clear(selected_index[0])
        next_index = (selected_index[0] + 1) % len(songs)
        songlist.select_set(next_index)
        current_song = songs[next_index]
        play_music()

def prev_music():
    global current_song, paused
    selected_index = songlist.curselection()
    if selected_index:
        songlist.select_clear(selected_index[0])
        prev_index = (selected_index[0] - 1) % len(songs)
        songlist.select_set(prev_index)
        current_song = songs[prev_index]
        play_music()

organize_menu = Menu(menubar, tearoff=0)
organize_menu.add_command(label="Open", command=load_song)
menubar.add_cascade(label="File", menu=organize_menu)

songlist = Listbox(root, bg="black", fg="white", width=100, height=20, selectbackground="gray", selectforeground="black")
songlist.pack(pady=0)

# Load button images
play_btnimg = Image.open("play.png")
pause_btnimg = Image.open("pause.png")
next_btnimg = Image.open("next.png")
prev_btnimg = Image.open("prev.png")

# Resize function
def resize_image(image, width, height):
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(resized_image)

# Define the desired width and height for the button image
button_width = 50
button_height = 50

# Resize images
play_img = resize_image(play_btnimg, button_width, button_height)
pause_img = resize_image(pause_btnimg, button_width, button_height)
next_img = resize_image(next_btnimg, button_width, button_height)
prev_img = resize_image(prev_btnimg, button_width, button_height)

controlsframe = Frame(root)
controlsframe.pack()

# Create buttons with resized images
prev_bt = Button(controlsframe, image=prev_img, borderwidth=0, command=prev_music)
play_bt = Button(controlsframe, image=play_img, borderwidth=0, command=play_music)
pause_bt = Button(controlsframe, image=pause_img, borderwidth=0, command=pause_music)
next_bt = Button(controlsframe, image=next_img, borderwidth=0, command=next_music)

prev_bt.grid(row=0, column=0, padx=10)
play_bt.grid(row=0, column=1, padx=10)
pause_bt.grid(row=0, column=2, padx=10)
next_bt.grid(row=0, column=3, padx=10)

root.mainloop()
