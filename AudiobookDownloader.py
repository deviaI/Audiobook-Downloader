# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 10:07:56 2021

@author: Lukas Knöppel
"""

import requests
import time
from bs4 import BeautifulSoup
import numpy as np
import tkinter as tk
import pickle

def read():
    name = entry_name.get()
    url = entry_url.get()
    path = entry_path.get()


    if len(path) == 0:
        try:
            path = pickle.load(open("DefaultPath.p", "rb"))
        except FileNotFoundError:
            path = ""
    else:
        path = path.replace(path[2], "//")
        if path[-1] != "//":
           path = path + "//"
        print(path)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    ty = '.mp3'
    i = 1
    td = []
    site = url.split(".")[0]
    site = site.split("//")[1]
    if site == "bookaudio":
        Text = "Downloading" + name
        label2 = tk.Label(text = Text)
        label3 = tk.Label()
        label4 = tk.Label()
        label2.pack()
        label3.pack()
        label4.pack()
        for results in soup.findAll('li', attrs = {'class':'track'}):
            number = results.text.split('.')[0]
        for results in soup.findAll('li', attrs = {'class':'track'}):
            tic = time.time()
            Text= 'Downloading ' + name + ' File Nr.' + str(i) + ' of ' + number + '  ...'
            label3["text"] = Text
            url = ''
            url = results.get('data-url')
            url = 'https:' + url
            fName = path + name + str(i) + ty
            r = requests.get(url, allow_redirects=True)
            open(fName, 'wb').write(r.content)
            i = i+1
            toc = time.time()
            td.append(toc-tic)
            eta = ((int(number)-i)*np.mean(td))
            Text = "Estimated time to completion:  %02d:%02d:%02d" %(int(np.floor(eta/3600)), int(np.floor(eta-3600*np.floor(eta/3600.0))/60), int(eta-60*np.floor(eta/60.0)))
            label4["text"] = Text
            window.update()
    elif site == "fulllengthaudiobooks" or site== "hdaudiobooks":
        Text = "Downloading" + name
        label2 = tk.Label(text = Text)
        label3 = tk.Label()
        label4 = tk.Label()
        label2.pack()
        label3.pack()
        label4.pack()
        results = soup.findAll("audio", attrs = {"class":"wp-audio-shortcode"})
        tag = results[-1].attrs["id"]
        number = tag.split("-")[2]
        for result in results:
            tic = time.time()
            Text= 'Downloading ' + name + ' File Nr.' + str(i) + ' of ' + number + '  ...'
            label3["text"] = Text
            url = result.text
            fName = path + name + str(i) + ty
            r = requests.get(url, allow_redirects=True)
            open(fName, 'wb').write(r.content)
            i = i+1
            toc = time.time()
            td.append(toc-tic)
            eta = ((int(number)-i)*np.mean(td))
            Text = "Estimated time to completion:  %02d:%02d:%02d" %(int(np.floor(eta/3600)), int(np.floor(eta-3600*np.floor(eta/3600.0))/60), int(eta-60*np.floor(eta/60.0)))
            label4["text"] = Text
            window.update()
    else:
        Text = "Invalid Site"
        label2 = tk.Label(text = Text)
        label2.pack()
        window.update()
    clear()

def clear():
    entry_name.delete(0, tk.END)
    entry_url.delete(0, tk.END)
    entry_path.delete(0, tk.END)
    window.destroy()

def default():
    path = entry_path.get()
    path = path.replace(path[2], "//")
    if path[-1] != "//":
           path = path + "//"
    pickle.dump(path, open("DefaultPath.p", "wb"))

# Create a new window with the title "Address Entry Form"
window = tk.Tk()
window.title("AudiobookDownloader")

string = tk.StringVar()
# Create a new frame `frm_form` to contain the Label
# and Entry widgets for entering address information
frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
# Pack the frame into the window
frm_form.pack()

# List of field labels
labels = [
    "Name of Audiobook:",
    "URL of Audiobook:",
    "Download Path:"
]

# Loop over the list of field labels
# Create a Label widget with the text from the labels list
label = tk.Label(master=frm_form, text=labels[0])
# Create an Entry widget
entry_name = tk.Entry(master=frm_form, width=50)
# Use the grid geometry manager to place the Label and
# Entry widgets in the row whose index is idx
label.grid(row=0, column=0, sticky="e")
entry_name.grid(row=0, column=1)

label = tk.Label(master=frm_form, text=labels[1])
# Create an Entry widget
entry_url = tk.Entry(master=frm_form, width=50)
# Use the grid geometry manager to place the Label and
# Entry widgets in the row whose index is idx
label.grid(row=1, column=0, sticky="e")
entry_url.grid(row=1, column=1)

label = tk.Label(master=frm_form, text=labels[2])
# Create an Entry widget
entry_path = tk.Entry(master=frm_form, width=50)
# Use the grid geometry manager to place the Label and
# Entry widgets in the row whose index is idx
label.grid(row=2, column=0, sticky="e")
entry_path.grid(row=2, column=1)

# Create a new frame `frm_buttons` to contain the
# Submit and Clear buttons. This frame fills the
# whole window in the horizontal direction and has
# 5 pixels of horizontal and vertical padding.
frm_buttons = tk.Frame()
frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

# Create the "Submit" button and pack it to the
# right side of `frm_buttons`
btn_submit = tk.Button(master=frm_buttons, text="Submit", command=read)
btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

# Create the "Clear" button and pack it to the
# right side of `frm_buttons`
btn_clear = tk.Button(master=frm_buttons, text="Quit", command=clear)
btn_clear.pack(side=tk.RIGHT, ipadx=10)


btn_def = tk.Button(master=frm_buttons, text="Set Path as Default", command=default)
btn_def.pack(side=tk.RIGHT, ipadx=10)

# Start the application
window.mainloop()



