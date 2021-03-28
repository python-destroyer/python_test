import datetime

from data_base import session, User, Event
from data_base import LOCAL_DIR

def ping(IP):
    #Returns True if host responds to a ping request
    import subprocess, platform
    # Ping parameters as function of OS
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + IP
    # need_sh = False if  platform.system().lower()=="windows" else True
    need_sh = platform.system().lower()!="windows"
    # Ping
    return subprocess.call(args, shell=need_sh) == 0

def get_ip_names(file_path): #check if new IPs or changed names present in txt file
    with open(file_path) as f:
        lines = f.readlines()
        for line in lines:
            val = line.split()
            if (len(val) == 2):
                user_by_ip = session.query(User).filter(User.ip_address == val[1]).first()
                if (user_by_ip == None): #check if user is already present in database
                    #add new users to database
                    user = User(username = val[0], ip_address = val[1], state = ping(val[1]))
                    session.add(user)
                    session.commit()
                elif (user_by_ip.username != val[0]): #check if present user have changed username
                    #update user's username
                    user_by_ip.username = val[0]
                    session.commit()

def ping_IPs():
    get_ip_names(str(LOCAL_DIR) + "/ip_names.txt") #update database from txt file
    all_users = session.query(User).all()
    for user in all_users:  #ping all ip addresses from database
        if (ping(user.ip_address) != user.state):   #check if user state has changed
            if (user.state):
                #exit event
                event = Event(my_type = 'IP вышел из сети', my_time = datetime.datetime.now(), user_id = user.id)
                session.add(event)
                session.commit()
            else:
                #enter event
                event = Event(my_type = 'IP вошел в сеть', my_time = datetime.datetime.now(), user_id = user.id)
                session.add(event)
                session.commit()
            user.state = not user.state    #update user state
            session.commit()