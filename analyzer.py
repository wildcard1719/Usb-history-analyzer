import sys
import subprocess
from datetime import datetime, timedelta


try:
    import Evtx.Evtx as evtx

except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-evtx"])
    import Evtx.Evtx as evtx

try:
    path = sys.argv[1]

except:
    path = "C:\Windows\System32\winevt\Logs\Microsoft-Windows-StorageSpaces-Driver%4Operational.evtx"

if "help" in path:
    print("analyzer.py [.evtx file path]")
    exit()

event_id = []
event_time = []
event_media = []

first = []

count_model = []


ii = 0
flag = 0
time_ = ""
dayup = 0

with evtx.Evtx(path) as file:
    records = file.records()
    for record in records:
        ii += 1
        id_ = record.xml().split('\n')[8]
        id_ = id_[id_.index("D>")+2 : id_.index("</")]
        event_id.append(id_)

        model = record.xml().split('\n')[19]
        model = model[model.index('">') + 2: model.index('</')]
        
        serial = record.xml().split('\n')[20]
        serial = serial[serial.index('">') + 2: serial.index('</')]

        maker = record.xml().split('\n')[18]
        maker = maker[maker.index('">') + 2: maker.index('</')]
        
        media = serial + "!@#$" + maker + "!@#$" + model
        event_media.append(media)
        
        if media not in first:
            first.append(media)
        
        time = record.xml().split('\n')[7].split()
        time = time[1][time[1].index('"')+1:] + " " + time[2][:time[1].index('"')-1]
        time = time.split('.')[0]
        dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        time = dt + timedelta(hours=9)
        event_time.append(time)

for i in range(len(event_time)):
    print("--------------------------------------------")
    print('['+str(event_time[i])+']')
    print("TimelineID :" + event_id[i])
    print("Serial Number: " + event_media[i].split('!@#$')[0])
    print("Manufacturer: " + event_media[i].split('!@#$')[1])
    print("Model: " + event_media[i].split('!@#$')[2])
    print()


print("----------Total-" + str(ii) +"----------")

for i in range(len(first)):
    count_model.append(event_media.count(first[i]))


for i in range(len(first)):
    space = " " * (25 - len(first[i].split('!@#$')[0]))
    space2 = " " * (25 - len(first[i].split('!@#$')[1]))
    space3 = " " * (18 - len(first[i].split('!@#$')[2]))
    print("Serial Number:" + str(first[i].split('!@#$')[0]) + space + "Manufacturer:" + first[i].split('!@#$')[1] + space2 +  "Model:" + str(first[i].split('!@#$')[2]) + space3 + "(" + str(count_model[i]) + " times mount)")

with open("Report.txt", 'w') as report:
    report.write("\n\n\n")
    for i in range(len(event_time)):
        report.write("--------------------------------------------\n")
        report.write('[' + str(event_time[i]) + ']\n')
        report.write("TimelineID :" + event_id[i] + "\n")
        report.write("Serial Number: " + event_media[i].split('!@#$')[0] + "\n")
        report.write("Manufacturer: " + event_media[i].split('!@#$')[1] + "\n")
        report.write("Model: " + event_media[i].split('!@#$')[2] + "\n\n")
        for i in range(len(first)):
            count_model.append(event_media.count(first[i]))
    report.write("----------Total-" + str(ii) + "----------\n")
    for i in range(len(first)):
        space = " " * (25 - len(first[i].split('!@#$')[0]))
        space2 = " " * (25 - len(first[i].split('!@#$')[1]))
        space3 = " " * (18 - len(first[i].split('!@#$')[2]))
        report.write("Serial Number:" + str(first[i].split('!@#$')[0]) + space + "Manufacturer:" + first[i].split('!@#$')[1] + space2 + "Model:" + str(first[i].split('!@#$')[2]) + space3 + "(" + str(count_model[i]) + " times mount)\n")

print("\n>>>This result is recorded in report.txt")
