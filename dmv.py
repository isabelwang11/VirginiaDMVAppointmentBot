from requests_html import AsyncHTMLSession
from datetime import datetime
# import itertools
# import asyncio
import time
import random
from pydub import AudioSegment
from pydub.playback import play
import urllib.request
import urllib.parse

def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.txtlocal.com/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

asession = AsyncHTMLSession()

sites = {
    "Tyson's Corner": "https://vadmvappointments.as.me/schedule.php?calendarID=5019953",
    "Sterling": "https://vadmvappointments.as.me/schedule.php?calendarID=4344351",
    "Manassas Satellite Location": "https://vadmvappointments.as.me/schedule.php?calendarID=4175271",
    "Franconia": "https://vadmvappointments.as.me/schedule.php?calendarID=4539136",
    "Woodbridge": "https://vadmvappointments.as.me/schedule.php?calendarID=4150702"
    # "Covington": "https://vadmvappointments.as.me/schedule.php?calendarID=4766422" # Used for testing
}

before_date = datetime(year=2021, month=8, day=15)

async def get_site(location, url):
    r = await asession.get(url)
    await r.html.arender(sleep=10)
    calendar = r.html.find(".calendar", first=True)

    try:
        active_days = calendar.find(".activeday")
        if active_days:
            for active in active_days:
                current = datetime.strptime(active.attrs['day'], '%Y-%m-%d')
                print(location, '-', datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S'))
                if True or current < before_date:
                    loc = location + '-' + datetime.strptime(active.attrs['day'], '%Y-%m-%d').strftime('%B %d, %Y')
                    song = AudioSegment.from_wav("beep-7.wav")
                    play(song)
                    resp = sendSMS('NmM2NzczNzU0YTMyNGM3YTc2NDI0YzMzNGU3NDU1Njc=', '5716853811', 'Isabel\'s DMV Appointment Availability Bot', loc)
                    print(resp)
                else:
                    print('\t', location, '- No appointments before', before_date.strftime('%B %d, %Y'))
                    break
        else:
            print('\t', location, '- No appointments at this location.')
    except:
        print(location, "- Can't find calendar element.")

while True:
    print("Running Cycle -", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # asession.loop.run_until_complete(asyncio.gather(*[get_site(loc, url) for loc, url in sites.items()]))
    # time.sleep(random.randint(180, 420))
    for loc, url in sites.items():
        try:
            asession.loop.run_until_complete(get_site(loc,url))
        except:
            print('Oopsie Woopsie! Uwu We made a fucky wucky!! A wittle fucko boingo! The code monkeys at our headquarters are working VEWY HAWD to fix this!')
            time.sleep(random.randint(180,420)/len(sites))