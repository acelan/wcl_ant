#!/usr/bin/python3.10

import requests
import json
import time
import os
import socket
from tqdm import tqdm
import datetime
import pickle
import psutil

from config import client_id, client_secret

requests.packages.urllib3.disable_warnings()

authorize_url = "https://www.warcraftlogs.com/oauth/authorize"
token_url = "https://www.warcraftlogs.com/oauth/token"
api_url = "https://tw.classic.warcraftlogs.com/api/v2/client"

data = {'grant_type': 'client_credentials'}
access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

# we can now use the access_token as much as we want to access protected resources.
tokens = json.loads(access_token_response.text)
access_token = tokens['access_token']
#print("access token: %s" % access_token)

servers = [f for f in os.listdir('server') if not os.path.isfile(os.path.join("server", f))]
zones = ["1023", "1027", "1033"]

bosses = {
            "1023": [1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1082],
            "1027": [1205, 1204, 1197, 1206, 1200, 1185, 1203],
            "1033": [1292, 1294, 1295, 1296, 1297, 1298, 1291, 1299],
}

def get_spec_id(class_id, spec):
    classes = {
        1:{
            'specs':{
                'Blood':{'id':'1','name':'Blood','slug':'Blood','icon':'Interface/AddOns/WCLRanks/Icons/classes:%w:%h:0:0:256:512:36:72:144:180'},
                'Frost':{'id':'2','name':'Frost','slug':'Frost','icon':'Interface/AddOns/WCLRanks/Icons/classes:%w:%h:0:0:256:512:72:108:144:180'},
                'Unholy':{'id':'3','name':'Unholy','slug':'Unholy','icon':'Interface/AddOns/WCLRanks/Icons/classes:%w:%h:0:0:256:512:108:144:144:180'},
                'Lichborne':{'id':'4','name':'Lichborne','slug':'Lichborne','icon':'Interface/AddOns/WCLRanks/Icons/classes:%w:%h:0:0:256:512:72:108:144:180'},
                'Runeblade':{'id':'5','name':'Runeblade','slug':'Runeblade','icon':'Interface/AddOns/WCLRanks/Icons/classes:%w:%h:0:0:256:512:36:72:144:180'},
                'BloodDPS':{'id':'6','name':'Blood','slug':'Blood','icon':'Interface/AddOns/WCLRanks/Icons/classes:%w:%h:0:0:256:512:36:72:144:180'}
            }
        },
        2:{
            'specs':{
                'Balance':{'id':'1','name':'Balance','slug':'Balance','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:36:72:36:72'},
                'Feral':{'id':'2','name':'Feral','slug':'Feral','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:72:108:36:72'},
                'Guardian':{'id':'3','name':'Guardian','slug':'Guardian','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:108:144:36:72'},
                'Restoration':{'id':'4','name':'Restoration','slug':'Restoration','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:144:180:36:72'},
                'Warden':{'id':'5','name':'Warden','slug':'Warden','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:180:216:36:72'}
            }
        },
		3:{
            'specs':{
                'BeastMastery':{'id':'1','name':'Beast Mastery','slug':'BeastMastery','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:36:72:72:108'},
                'Marksmanship':{'id':'2','name':'Marksmanship','slug':'Marksmanship','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:72:108:72:108'},
                'Survival':{'id':'3','name':'Survival','slug':'Survival','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:108:144:72:108'}
            }
        },
        4:{
            'specs':{
                'Arcane':{'id':'1','name':'Arcane','slug':'Arcane','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:36:72:108:144'},
                'Fire':{'id':'2','name':'Fire','slug':'Fire','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:72:108:108:144'},
                'Frost':{'id':'3','name':'Frost','slug':'Frost','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:108:144:108:144'}
            }
        },
        6:{
            'specs':{
                'Holy':{'id':'1','name':'Holy','slug':'Holy','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:36:72:180:216'},
                'Protection':{'id':'2','name':'Protection','slug':'Protection','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:72:108:180:216'},
                'Retribution':{'id':'3','name':'Retribution','slug':'Retribution','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:108:144:180:216'},
                'Justicar':{'id':'4','name':'Justicar','slug':'Justicar','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:144:180:180:216'}
            }
        },
        7:{
            'specs':{
                'Discipline':{'id':'1','name':'Discipline','slug':'Discipline','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:36:72:216:252'},
                'Holy':{'id':'2','name':'Holy','slug':'Holy','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:72:108:216:252'},
                'Shadow':{'id':'3','name':'Shadow','slug':'Shadow','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:108:144:216:252'}
            }
        },
        8:{
             'specs':{
                 'Assassination':{'id':'1','name':'Assassination','slug':'Assassination','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:36:72:252:288'},
                 'Combat':{'id':'2','name':'Combat','slug':'Combat','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:72:108:252:288'},
                 'Subtlety':{'id':'3','name':'Subtlety','slug':'Subtlety','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:108:144:252:288'}
            }
        },
        9:{
            'specs':{
                 'Elemental':{'id':'1','name':'Elemental','slug':'Elemental','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:36:72:288:324'},
                 'Enhancement':{'id':'2','name':'Enhancement','slug':'Enhancement','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:72:108:288:324'},
                 'Restoration':{'id':'3','name':'Restoration','slug':'Restoration','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:108:144:288:324'}
            }
        },
        10:{
            'specs':{
                 'Affliction':{'id':'1','name':'Affliction','slug':'Affliction','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:36:72:324:360'},
                 'Demonology':{'id':'2','name':'Demonology','slug':'Demonology','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:72:108:324:360'},
                 'Destruction':{'id':'3','name':'Destruction','slug':'Destruction','icon':'Interface/AddOns/LogTracker/Icons/classes:%w:%h:0:0:256:512:108:144:324:360'}
            }
        },
        11:{
            'specs':{
                'Arms':{'id':'1','name':'Arms','slug':'Arms','icon':'Interface/AddOns/WCLRanks/Icons/classes:%w:%h:0:0:256:512:36:72:360:396'},
                'Fury':{'id':'2','name':'Fury','slug':'Fury','icon':'Interface/AddOns/WCLRanks/Icons/classes:%w:%h:0:0:256:512:72:108:360:396'},
                'Protection':{'id':'3','name':'Protection','slug':'Protection','icon':'Interface/AddOns/WCLRanks/Icons/classes:%w:%h:0:0:256:512:108:144:360:396'},
                'Gladiator':{'id':'4','name':'Gladiator','slug':'Gladiator','icon':'Interface/AddOns/WCLRanks/Icons/classes:%w:%h:0:0:256:512:144:180:360:396'},
                'Champion':{'id':'5','name':'Champion','slug':'Champion','icon':'Interface/AddOns/WCLRanks/Icons/classes:%w:%h:0:0:256:512:180:216:360:396'}
            },
        },
    }
    spec_id = '0'
    try:
        spec_id = classes[class_id]['specs'][spec]['id']
    except:
        print("Can't get spec id - %s %s" % (class_id, spec))
    return spec_id

def wcl_query(query):
    max_retries = 5
    retry_delay = 10

    for attempt in range(max_retries):
        try:
            api_call_headers = {'Authorization': 'Bearer ' + access_token}
            api_call_response = requests.post(api_url, json={"query": query}, headers=api_call_headers, verify=False, timeout=30)

            # Handle API rate limiting (429)
            try:
                response_data = json.loads(api_call_response.text)
                if "status" not in response_data or response_data["status"] != 429:
                    return api_call_response.text
                else:
                    print("Unexpected output: %s" % api_call_response.text)
                    print("Got 429, let's take a longer sleep")
                    time.sleep(3600)
            except json.JSONDecodeError:
                print("not json format \"%s\"" % api_call_response.text)
                # If not a valid JSON and not a 429 error, return the response
                if api_call_response.status_code != 429:
                    return api_call_response.text
                time.sleep(3600)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout,
                requests.exceptions.RequestException, socket.gaierror) as e:
            # Handle connection errors with exponential backoff
            if attempt < max_retries - 1:  # Don't sleep on the last attempt
                sleep_time = retry_delay * (2 ** attempt)  # Exponential backoff
                print(f"Connection error: {str(e)}. Retrying in {sleep_time} seconds... (Attempt {attempt+1}/{max_retries})")
                time.sleep(sleep_time)
            else:
                print(f"Failed after {max_retries} attempts: {str(e)}")
                raise  # Re-raise the last exception if all retries failed

    return api_call_response.text

def query_points():
    query = "query {rateLimitData {limitPerHour, pointsSpentThisHour, pointsResetIn}}"
    result = wcl_query(query)
    try:
        points = json.loads(result)["data"]["rateLimitData"]
    except:
        print(json.loads(result))
    return points

def gen_query_report(report_code):
    idx = 1
    query = "query { reportData { \n"
    if report_code:
        for code in report_code:
            query += "r%s: report(code: \"%s\") {rankedCharacters { id name server { id }}} \n" % (idx, code)
            idx += 1

    query += "}}"
    return query

def gen_query_code(server_name, users, guilds, starttime):
    idx = 1
    query = "query { reportData { \n"
    if users:
        for user in users:
            query += "u%s: reports(userID: %s, startTime: %s) { data { code }} \n" % (idx, user, starttime)
            idx += 1

    if guilds:
        for guild in guilds:
            query += "g%s: reports(guildName: \"%s\",  guildServerSlug: \"%s\", guildServerRegion: \"tw\", startTime: %s) { data { code }} \n" % (idx, guild, server_name, starttime)
            idx += 1

    query += "}}"
    return query

def gen_query_user(server_name, username, userdata):
    idx = 1
    partition = 4
    partition_name = "P4"
    userdata["PHASE"] = partition_name
    query = "query { characterData { \n"
    if username:
        for name in username:
            query += "c%s: character(name: \"%s\", serverRegion:\"tw\", serverSlug: \"%s\") { id name classID " % (idx, name, server_name)
            for zone in zones:
                for size in ["10", "25"]:
                    query += "D%s: zoneRankings(zoneID: %s, size: %s, partition: %s)," % (zone + "_" + size, zone, size, partition)
            query += "} \n"
            idx += 1

    query += "}}"
    return query

def query_code(server_name, userlist, guildlist, starttime):
    query = gen_query_code(server_name, userlist, guildlist, starttime)
    result = wcl_query(query)
    try:
        entries = json.loads(result)["data"]["reportData"]
        #print("entries = %s" % entries)
    except:
        print("ERROR!!! %s" % result)

    report_code = []
    for key, reports in entries.items():
        if reports and reports["data"]:
            #print("reports = %s" % reports["data"])
            for report in reports["data"]:
                #print("report = %s" % (report["code"]))
                report_code.append(report["code"])

    return report_code

def write_username(username):
    with open("username.txt", 'w') as file_handler:
        for item in username:
            file_handler.write("{}\n".format(item))

def read_username():
    with open("username.txt", "w+") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines

def query_username(report_code):
    query = gen_query_report(report_code)
    result = wcl_query(query)
    try:
        entries = json.loads(result)["data"]["reportData"]
        #print("entries = %s" % entries)
    except:
        print("ERROR!!! %s" % result)

    username = []
    for key, reports in entries.items():
        if reports and "rankedCharacters" in reports and reports["rankedCharacters"]:
            for report in reports["rankedCharacters"]:
                if report["name"] not in username:
                    username.append(report["name"])

    return username

def add_color_code(name, percent):
    if percent == 100 or name in my_name:
        return "A"
    elif percent >= 99:
        return "S"
    elif percent >= 95:
        return "L"
    elif percent >= 85:
        return "N"
    elif percent >= 75:
        return "E"
    elif percent >= 50:
        return "R"
    elif percent >= 25:
        return "U"
    return "C"

def parse_rankings(class_id, zone, rankings):
    ranking_str = ""
    total = 0
    killed = 0
    for boss_id in bosses[zone]:
        total = total + 1
        for ranking in rankings:
            points = 0.0
            rank = 0
            region_rank = 0
            server_rank = 0
            rank_percent = 0.0
            spec = "N"
            spec_id = 0
            if boss_id == ranking["encounter"]["id"]:
                # when doing mindcontrol in NAXX Instructor Razuvious, "total" value is 0 with no ranks
                if ranking["totalKills"] != 0 and ranking["allStars"] and ranking["allStars"]["total"] != 0:
                    killed = killed + 1
                    points = float(ranking["allStars"]["points"])
                    rank = ranking["allStars"]["rank"]
                    region_rank = ranking["allStars"]["regionRank"]
                    server_rank = ranking["allStars"]["serverRank"]
                    rank_percent = float(ranking["allStars"]["rankPercent"])
                    spec = ranking["spec"]
                    spec_id = get_spec_id(class_id, spec)
                    if spec_id == '0':
                        continue

                if ranking_str:
                    ranking_str += '|'
                ranking_str += "%s,%0.2f,%0.2f,%s,%s,%s" % (spec_id, points, rank_percent, server_rank, region_rank, rank)
                break

    return total, killed, ranking_str

def write_userdata(filepath, data):
    with open('%s/userdata.txt' % filepath, 'w') as file:
        file.write(json.dumps(data, ensure_ascii=False)) # use `json.loads` to do the reverse

def read_userdata(filepath):
    if not os.path.exists("%s/userdata.txt" % filepath):
        return False

    with open("%s/userdata.txt" % filepath) as file:
        userdata = file.read()
        #print("read data: %s" % userdata)
        return json.loads(userdata)

def write_target(server_name, filename, userdata):
    path = "Data/"

    if not os.path.exists(path):
        os.mkdir(path)

    f = open( path + filename, 'w')
    f.write("if GetRealmName() ~= \"%s\" then return end\nWP_Database = {\n" % server_name)

    for name, stat  in userdata.items():
        f.write("[\"%s\"] = \"%s\",\n" % (name, stat))

    f.write("}\n")
    f.close()

def update_userdata(server_id, server_name, username):
    len_username = len(username)
    idx = 1
    step = 40
    userdata = read_userdata("server/%s" % server_id) or {}
    while True:
        points = query_points() # requires 23 points
        print("\nRate Limit: %s points / hour, Points Spent: %s Points, Reset In: %s minutes\n" % (points["limitPerHour"], points["pointsSpentThisHour"], int(points["pointsResetIn"]/60)))
        if int(points["limitPerHour"]) - int(points["pointsSpentThisHour"]) < 500:
            print("Run out of points, time to sleep for %s seconds" % points["pointsResetIn"])
            for i in tqdm(range(int(points["pointsResetIn"]) + 10)):
                time.sleep(1)

        end = idx + step
        stop = False
        if idx + step >= len_username:
            end = len_username
            stop = True

        print("username(%s) = %s" % (len(username), username[idx:end]))
        if len_username == 0:
            print("No new report!!")
            return userdata

        print("\n\nget user data from %s to %s/%s" % (idx, end - 1, len_username))

        query = gen_query_user(server_name, username[idx:end], userdata)
        idx += step
        print("query = %s" % query)
        result = wcl_query(query)
        result = result.replace("Noclasssetforthischaracter.ClicktheUpdatebuttonintheupperrighttoestablishaclass.", "")
        result = result.replace("No class set for this character. Click the Update button in the upper right to establish a class.", "")
        try:
            user_data = json.loads(result)["data"]["characterData"]
        except:
            print("########################### Exceed the limit, sleep 1 hour #####################################")
            time.sleep(3600)
            result = wcl_query(query)
            result = result.replace("Noclasssetforthischaracter.ClicktheUpdatebuttonintheupperrighttoestablishaclass.", "")
            result = result.replace("No class set for this character. Click the Update button in the upper right to establish a class.", "")
            user_data = json.loads(result)["data"]["characterData"]

        msg = ""
        for key, user in user_data.items():
            # the player may not have raid data, the report could be for 5-man instance
            if not user:
                continue

            #print("user = %s" % user)
            try:
                class_id = user["classID"]
                if class_id == 0:
                    for classs in classes:
                        if spec in classes[classs]['specs']:
                            # found possible class
                            if class_id == 0:
                                class_id = classs
                # can't determinate the class
                if class_id == 0:
                    print(f"The class_id is 0, and spec = {spec}: {user}")
                    continue
            except:
                print("============ Error ============")
                print(f"{user}")
                continue

            list_str = ""
            msg += "\n[\"%s\"] =\"" % (user["name"])
            for zone in zones:
                for size in ["10", "25"]:
                    zone_str = ""
                    zone_name = 'D' + zone + '_' + size
                    if zone_name in user and "allStars" in user[zone_name]:
                        for allstar in user[zone_name]["allStars"]:
                            spec = allstar["spec"]
                            spec_id = get_spec_id(class_id, spec)
                            if spec_id == '0':
                                print("Error: %s %s %s %s" % (user["name"], class_id, spec, zone_name))
                                continue
                            points = round(float(allstar["points"]), 2)
                            rank = allstar["rank"]
                            region_rank = allstar["regionRank"]
                            server_rank = allstar["serverRank"]
                            rank_percent = round(float(allstar["rankPercent"]), 2)
                            color = add_color_code(user["name"], rank_percent)

                            if zone_str:
                                zone_str += ","
                            zone_str += "{'%s',%s,%0.2f,%0.2f,%s,%s,%s}" % (color, spec_id, points, rank_percent, server_rank, region_rank, rank)

                        total, killed, ranking_str = parse_rankings(class_id, zone, user[zone_name]["rankings"])
                        # print("total = %s, killed = %s, ranking_str = %s" % (total, killed, ranking_str))
                        if zone_str and killed != 0:
                            list_str += "['%s']={%s,%s,{%s},'%s'}," % (zone_name[1:], total, killed, zone_str, ranking_str)

            if list_str:
                now = int(datetime.datetime.now().timestamp())
                userdata[user["name"]] = "{%s, %s, {%s}}" % (class_id, now, list_str)

                msg += userdata[user["name"]]
            write_target(server_name, "%s.lua" % server_id, userdata)
        msg += "\n"
        print("==========================================")
        print(msg)
        print("==========================================")
        write_userdata("server/%s" % server_id, userdata)

        if stop:
            break

        # to fix 429 error, sleep 10 seconds every round
        time.sleep(10)

    return userdata

def ant_run(server_id, server_name, userlist, guildlist, starttime):
    report_code = query_code(server_name, userlist, guildlist, starttime)
    with open("report_code.txt", 'w') as file_handler:
        for item in report_code:
            file_handler.write("{}\n".format(item))

    username = query_username(report_code)
    write_username(username)

    userdata = update_userdata(server_id, server_name, username)

    write_target(server_name, "%s.lua" % server_id, userdata)

def update_xml():
    content = "<Ui xmlns=\"http://www.blizzard.com/wow/ui/\">\n"
    for server_lua in [f for f in os.listdir('Data') if f.endswith(".lua")]:
        content = content + "<Script file=\"%s\" />\n" % server_lua
    content = content + "</Ui>\n"

    f = open("Data/WCLRanks.xml", 'w')
    f.write(content)
    f.close()

def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    return listOfProcessObjects;

listOfProcessIds = findProcessIdByName('wcl_ant.py')
if len(listOfProcessIds) > 1:
    exit(-1)

for server_id in servers:
    server_name = pickle.load(open('server/%s/name.pkl' % server_id, 'rb'))
    userlist = []
    if os.path.isfile('server/%s/userlist.pkl' % server_id):
        userlist = pickle.load(open('server/%s/userlist.pkl' % server_id, 'rb'))
    guildlist = []
    if os.path.isfile('server/%s/guildlist.pkl' % server_id):
        guildlist = pickle.load(open('server/%s/guildlist.pkl' % server_id, 'rb'))
    print("server = %s" % server_id)
    print("name = %s" % server_name)
    print("userlist = %s" % userlist)
    print("guildlist = %s" % guildlist)

    #date_time = datetime.datetime(2021, 9, 1, 0, 0)
    date_time = datetime.date.today() - datetime.timedelta(days=2) # check everyday, but retrive reports from 2 days ago
    starttime = time.mktime(date_time.timetuple()) * 1000

    ant_run(server_id, server_name, userlist, guildlist, starttime)

    update_xml()
