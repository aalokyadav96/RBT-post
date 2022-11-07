import requests
from bs4 import BeautifulSoup
import subprocess
from flask import Flask, request, render_template

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/new', methods=['POST'])
def hello_world():
    if request.method == 'POST':
        urlstr = request.form['url']
    soup = BeautifulSoup(requests.get(urlstr).content, "html.parser")
    count = 1
    dcount = 0
    countd = 1
    with open('subtitles.srt','w',encoding='utf-8') as the_file:
        for tr in soup.find_all('tr')[1:]:
            tds = tr.find_all('td')
            if tds[3].text != "" :
                print(tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[4].text)
                duration = "00:00:" + str(dcount).zfill(2) + ",000 --> 00:00:" + str(countd).zfill(2) + ",000"
                strng =str(count) + "\n" + duration + "\n" + "<i><b>Departure Time</b> : </i>" + tds[1].text.replace("\n", "") + "\n" + "<i><b>Route</b>       : </i>" +  tds[2].text.replace("\n", "") + "\n" + "<i><b>Via</b>            : </i>" + tds[3].text.replace("\n", "") + "\n" + "<i><b>Bus Type</b> : </i>"  + tds[4].text.replace("\n", "") + "\n"+ "No : "+str(count) + "\n\n"
                the_file.write(strng)
                count = count + 1
                countd = countd + 1
                dcount = dcount + 1
#print(soup.prettify())
    dr = dcount*1
    frmto = soup.find("h1", {"class":"post-title"}).text
    dura = "color=c=white:s=1920x1080:d="+ str(dr)
    print("Duration : ",dura)
    fl = frmto.replace(" ", "_").replace("\n", "") + ".mp4"
    filename = "static/" + fl
    imgfile = "videos/" + frmto.replace(" ", "_").replace("\n", "") + ".mp4"
    print(filename)
    draw = "subtitles=subtitles.srt:force_style='FontName=Calibri,PrimaryColour=&H00000000,Outline=0,MarginV=30,Alignment=0,Fontsize=36,MarginL=28,MarginR=24', drawbox=x=0:y=0:w=1920:h=1080:t=18:color=black@0.75,drawbox=:x=0:y=0:w=1920:h=1080:t=16:color=yellow, drawtext=fontfile=Tahoma:fontsize=150:fontcolor=black@0.15:x=(w-text_w)/2:y=(h-text_h)/2:text='Roadways Bus Time',drawtext=fontfile=Tahoma:fontsize=80:box=1:boxborderw=20:boxcolor=yellow@0.75:bordercolor=black:fontcolor=black:x=(w-text_w)/2:y=28:text='"+ str(frmto)+"'"
    subprocess.call(['ffmpeg', '-y', '-f', 'lavfi', '-i', dura, '-vf', draw, filename])
    drt = "drawtext=fontfile=Calibri:fontsize=120:fontcolor=black:x=(w-text_w)/2:y=(h-text_h)/2:text='" + frmto + "'"
    thmb = "thumb/" + fl
    subprocess.call(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=size=1920x1080:duration=1:rate=25:color=white', '-vf',drt , thmb])

    with open('list.txt','w',encoding='utf-8') as my_file:
        stcfile = "file '"+filename+"'"
        thmbfile = "file '"+thmb+"'"
        my_file.write(thmbfile+"\n")
        my_file.write(stcfile+"\n")
        my_file.write("file 'warning.mp4'")

    subprocess.call(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy',  imgfile])

    return render_template('done.html',url=urlstr, header=frmto, filename=fl)
#ffmpeg -y -f lavfi -i color=c=white:s=1920x1080:d=10 -vf "subtitles=subtitles.srt: force_style='FontName=Calibri,PrimaryColour=&H00000000,Outline=0,MarginV=120,Alignment=0,Fontsize=30,MarginL=28,MarginR=24', drawbox=x=0:y=0:w=1920:h=1080:t=18:color=black@0.75, drawbox=:x=0:y=0:w=1920:h=1080:t=16:color=yellow, drawtext=fontfile=Breezesans:fontsize=80:box=1:boxborderw=10:boxcolor=yellow@0.75:bordercolor=black: fontcolor=black:x=(w-text_w)/2:y=28:text='Narnaul to Rewari TimeTable'" output.mp4