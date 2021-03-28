from aiohttp import web
import requests
import datetime

from data_base import session, User, Event

def check_dates(param_start, param_end):
    date_time = {
        "start" : None,
        "end" : None,
        "result" : ""
    }
    if ((param_start == None)|(param_end == None)):
        date_time['result'] = "Enter start & end datetime of period"
        return date_time
    try:
        date_time["start"] = datetime.datetime.strptime(param_start, '%Y-%m-%d %H:%M:%S')
        date_time["end"] = datetime.datetime.strptime(param_end, '%Y-%m-%d %H:%M:%S')
    except:
        date_time['result'] = "wrong datetime format, should be %Y-%m-%d %H:%M:%S"
        return date_time
    if (date_time["end"] < date_time["start"]):
        date_time['result'] = "end datetime should be higher than start datetime"
    return date_time

async def method_A(request):
    param_ip = request.rel_url.query.get('ip')
    param_start = request.rel_url.query.get('start')
    param_end = request.rel_url.query.get('end')
    user = session.query(User).filter(User.ip_address == param_ip).first()
    result = ""
    if (user == None):
        result = "IP is not found"
    else:
        date_time = check_dates(param_start, param_end)
        result = date_time['result']
        if (result == ""):
            events = session.query(Event).filter((Event.my_time > date_time["start"])&(Event.my_time < date_time["end"])&(Event.user_id == user.id)).all()
            for event in events:
                result += user.username + " " + user.ip_address + " " + event.my_type + " " + event.my_time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
    if (result == ""):
        result = "нету событий по IP в заданном периоде"
    return web.Response(text=str(result))

async def method_B(request):
    param_start = request.rel_url.query.get('start')
    param_end = request.rel_url.query.get('end')
    date_time = check_dates(param_start, param_end)
    result = date_time['result']
    if (result == ""):
        events = session.query(Event).filter((Event.my_time > date_time["start"])&(Event.my_time < date_time["end"])).all()
        for event in events:
            result += session.query(User).get(event.user_id).username + " " + session.query(User).get(event.user_id).ip_address + " " + event.my_type + " " + event.my_time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
    if (result == ""):
        result = "нету событий в заданном периоде"
    return web.Response(text=str(result))