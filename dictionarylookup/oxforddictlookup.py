#!/usr/bin/python3
import tkinter as tk
import requests

from pageparser import ParsePageContent

def GetMeanings(entryText):
    url = 'https://www.lexico.com/en/definition/{}'.format(entryText)
    page = requests.get(url)
    meanings = ParsePageContent(page.content)
    return meanings

def UpdateLabel(label, entryText, meanings):
    if meanings is None:
        label['text'] = 'No search result found for "{}"'.format(entryText)
        return

    message = ''
    sep = ''
    for ipos, info in enumerate(meanings):
        # Iterate over meanings for each part of speech
        message += sep
        sep = '\n\n'
        message += FormatMessageForPartOfSpeech(info)

    label['text'] = message
    return

def FormatMessageForPartOfSpeech(info):
    assert 'partOfSpeech' in info
    assert 'meanings' in info
    
    message = '{}'.format(info['partOfSpeech'].capitalize())
    numMeanings = len(info['meanings'])
    for imeaning in range(1, numMeanings + 1):
        message += '\n'
        message += '    {}. {}'.format(imeaning, info['meanings'][imeaning]['main'])
    return message

root = tk.Tk()

canvas = tk.Canvas(root, height=480, width=640)
canvas.pack()

frame = tk.Frame(root, bg='#ffffff', border=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=37)
entry.place(relwidth=0.65, relheight=1.0)
entry.focus() # focus on this entry

infobox = tk.Frame(root, bg='#ffffff', border=10)
infobox.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')
infolabel = tk.Label(infobox, anchor='nw', justify='left')
infolabel.place(relwidth=1.0, relheight=1.0)

onClick = lambda: UpdateLabel(infolabel, entry.get(), GetMeanings(entry.get()))
button = tk.Button(frame, text='Go!', command=onClick)
button.place(relwidth=0.35, relheight=1.0, relx=0.65)

onEnter = lambda event: UpdateLabel(infolabel, entry.get(), GetMeanings(entry.get()))
root.bind('<Return>', onEnter)

def onCtrlQ(root, event):
    root.destroy()
root.bind('<Control-q>', lambda event: onCtrlQ(root, event))

root.mainloop()
