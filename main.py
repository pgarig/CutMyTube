import PySimpleGUI as sg
import youtube_dl
import subprocess
import os
from shutil import copyfile

sg.theme('DarkAmber')

radio_choices = ['Video', 'Audio']
layout = [  
            [sg.Text('Video URL', font=(10), size=(15, 1), auto_size_text=False), sg.InputText(default_text="https://www.youtube.com/watch?v=", font=(10))],
            [sg.Text('Start of video', font=(10), size=(15, 1), auto_size_text=False), sg.InputText(default_text="00:00:00", size=(9, 1), font=(10))],
            [sg.Text('End of video', font=(10), size=(15, 1), auto_size_text=False), sg.InputText(default_text="00:00:05", size=(9, 1), font=(10))],
            [sg.Radio('Video', 'type', default=True, font=(10)), sg.Radio('Audio', 'type', font=(10))],
            [sg.Radio('With re-encoding', 'reencoding', default=True, font=(10)), sg.Radio('Without re-encoding', 'reencoding', font=(10))],
            [sg.Button('Download', key = 'download', size=(61, 1), font=(20))]
        ]

window = sg.Window('CutMyTub', layout, icon='icon.ico')


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    
    try:
        os.remove("video.mp4")
    except:
        pass
    try:
        os.remove("audio.mp3")
    except:
        pass


    if values[6] == True:
        reEncoding = '-c copy'
    else:
        reEncoding = ''


    if values[3] == True:
        
        command = 'youtube-dl --merge-output-format mp4 --output "video.mp4" ' \
                    '' + values[0]
        subprocess.call(command.split(), shell=False)

        print("Terminé youtube")

        command = 'ffmpeg -i #video.mp4#.mp4 -ss '+values[1]+' -to '+values[2]+' '+reEncoding+' video.mp4'
        subprocess.call(command, shell=False)

        try:
            os.remove("#video.mp4#.mp4")
        except:
            print('supression impossible')
    else:
        
        command = 'youtube-dl --quiet --extract-audio --audio-format mp3 --output "audio.mp3" ' \
                    '' + values[0]
        subprocess.call(command.split(), shell=False)

        command = 'ffmpeg -i #audio.mp3 -ss '+values[1]+' -to '+values[2]+' '+reEncoding+' audio.mp3'
        subprocess.call(command, shell=False)

        try:
            os.remove("#audio.mp3")
        except:
            pass


window.close()