import re, hashlib, os, shutil
from pydub import AudioSegment

#Using a dictionary because hashmaps give O(1) for lookup
char_to_code = {
    'a' : '.-',
    'b' : '-...',
    'c' : '-.-.',
    'd' : '-..',
    'e' : '.',
    'f' : '..-.',
    'g' : '--.',
    'h' : '....',
    'i' : '..',
    'j' : '.---',
    'k' : '-.-',
    'l' : '.-..',
    'm' : '--',
    'n' : '-.',
    'o' : '---',
    'p' : '.--.',
    'q' : '--.-',
    'r' : '.-.',
    's' : '...', 
    't' : '-',
    'u' : '..-', 
    'v' : '...-',
    'w' : '.--',
    'x' : '-..-',
    'y' : '-.--',
    'z' : '--..',
    '1' : '.----',
    '2' : '..---',
    '3' : '...--',
    '4' : '....-',
    '5' : '.....',
    '6' : '-....',
    '7' : '--...',
    '8' : '---..', 
    '9' : '----.',
    '0' : '-----',
    ' ' : '     '
}

#Used to store the file with a unique name, so that they can be searched for to see if they already exist. Used on the web end.


def file_name_generator(message): 
    return hashlib.sha1(message.encode()).hexdigest() + '.wav'


def message_to_morse(message):
    morse = '' 

    for char in message:
        morse += char_to_code[char] + ' '

    return morse

def generate_audio_file(morse):
    dot = AudioSegment.from_wav("dot.wav")
    dash = AudioSegment.from_wav("dash.wav")
    silence = AudioSegment.from_wav("silence.wav")
    new_file = silence * 2 

    for segment in morse:
        if segment == '.':
            new_file += dot

        elif segment == '-':
            new_file += dash

        elif segment == ' ':
            new_file += silence

    new_file += silence * 2

    new_file.export(file_name_generator(morse), format='wav')

def handler(message):
    cleaned   = re.sub(r'[^a-z0-9 ]', '',message.lower())
    print(cleaned)
    morse     = message_to_morse(cleaned)
    file_name = file_name_generator(morse)

    if os.path.isfile('clips/' + file_name):
        print("ALREADY DONE")

    else:
        generate_audio_file(morse)
        shutil.move(file_name, 'clips/'+file_name)


handler('hello')
handler('hell')
handler('Hell;o')
