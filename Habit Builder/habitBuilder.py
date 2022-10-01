import PySimpleGUI as sg
from datetime import datetime, date
from pathlib import Path

format = "%m/%d/%Y"

#IMPORTANT: EDIT THE NAMES AND POINTS OF YOUR HABITS, AND REMOVE OR EVEN ADD A NEW HABIT!
#ADJUST THE POINTS SUBTRACTED DEPENDING ON HOW HARD YOU WANT TO BE ON YOURSELF
habits = [('Habit 1', -2), ('Habit 2', -6), ('Habit 3', -1)]
POINTS_ADDED_PER_DAY = 1

habitButtons = [sg.B(x[0], expand_x=True) for x in habits]
habitKeys = [x[0] for x in habits]



#get current date
today = date.today()
today = list(str(today).split("-"))
today = today[1] + "/" + today[2] + '/' + today[0]


#get recorded info: [score,failed habit date, current date, highest streak]
file_path = 'Score_Keeper.txt'
if file_path:
    file = Path(file_path)
else:
    print("Score keeper not found")
    exit()
data = file.read_text().split(',')
if len(data)  == 1: data = [0,today,today,0]
data[0] = int(data[0])

#add points and update streak
currDate = datetime.strptime(today, format)
mostRecentDate = datetime.strptime(data[2], format)
failedHabitDate = datetime.strptime(data[1], format)        #streak = currDate-fhd      #added score = currDate-mrd
streak = (currDate - failedHabitDate).days
if streak > int(data[3]): data[3] = streak
data[0] += (currDate - mostRecentDate).days * POINTS_ADDED_PER_DAY     #add score
data[2] = today


sg.theme('LightBrown13')
layout = [
    [sg.T("Click the corresponding button whenever you are inconsistent with your habit", expand_x=True, font="Young 10", justification='center')],
    habitButtons,
    [sg.T(today, justification='center', key="-DATE-", expand_x=True, font="Young 15")],
    [sg.VPush()],
    [sg.T(data[0],key='-SCORE-', expand_x=True, expand_y=True, justification="center", font="Young 50")],
    [sg.VP()],
    [sg.T("Current Streak: "), sg.T(streak, key='-STREAK-')],
    [sg.T("Highest Streak: "), sg.T(data[3])]
]



window = sg.Window("Papaya Score", layout, size=(500,300), return_keyboard_events=True)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:break

    if event in habitKeys:
        data[0] += habits[habitKeys.index(event)][1]
        data[1] = today

    window['-SCORE-'].update(data[0])


data = [str(x) for x in data]
if file_path:
    file = Path(file_path)
    file.write_text(",".join(data))



