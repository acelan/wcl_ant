#!/usr/bin/python

import requests
import json
import time
import os
from tqdm import tqdm
import datetime
import pickle

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

def wcl_query(query):
    api_call_headers = {'Authorization': 'Bearer ' + access_token}
    api_call_response = requests.post(api_url, json={"query": query}, headers=api_call_headers, verify=False)
    return api_call_response.text

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
    partition = 5
    partition_name = "P3.5"
    userdata["PHASE"] = partition_name
    query = "query { characterData { \n"
    if username:
        for name in username:

            metric = "default"
            k_metric = "default"
            g_metric = "default"
            t_metric = "default"
            h_metric = "default"
            if userdata.get(name):
                zones = userdata[name].split("|")
                for zone in zones:
                    if "Restoration" in zone:
                        metric = "hps"
                    elif "Holy" in zone:
                        metric = "hps"
                    elif "Discipline" in zone:
                        metric = "hps"
                    elif "Shadow" in zone:
                        metric = "dps"
                    elif "Retribution" in zone:
                        metric = "dps"
                    elif "Elemental" in zone:
                        metric = "dps"
                    elif "Balance" in zone:
                        metric = "dps"

                    if "K: " in zone:
                        k_metric = metric
                    elif "G: " in zone:
                        g_metric = metric
                    elif "T: " in zone:
                        t_metric = metric
                    elif "H: " in zone:
                        h_metric = metric

            query += "c%s: character(name: \"%s\", serverRegion:\"tw\", serverSlug: \"%s\") { id name " % (idx, name, server_name)
            query += "Karazhan: zoneRankings(zoneID:1007, partition: %s, metric: %s) " % (partition, k_metric)
            query += "ZulAman: zoneRankings(zoneID:1012, partition: %s, metric: %s) " % (partition, k_metric)
            query += "Gruul_Magtheridon: zoneRankings(zoneID:1008, partition: %s, metric: %s) " % (partition, g_metric)
            query += "SSC_TK: zoneRankings(zoneID:1010, partition: %s, metric: %s) " % (partition, t_metric)
            query += "BT_Hyjal: zoneRankings(zoneID:1011, partition: %s, metric: %s) " % (partition, h_metric)
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

    # {"id":60800656,"name":"\u842c\u60e1\u99ac\u723a","server":{"id":5053}}
    username = []
    for key, reports in entries.items():
        if reports["rankedCharacters"]:
            #print("reports = %s" % reports["data"])
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

def best_rank(allstars):
    best = allstars[0]
    for allstar in allstars:
        if best["regionRank"] > allstar["regionRank"]:
            best = allstar
    return best

def update_userdata(server_id, server_name, username):
    len_username = len(username)
    idx = 1
    step = 10
    userdata = read_userdata("server/%s" % server_id) or {}
    while True:
        end = idx + step
        stop = False
        if idx + step >= len_username:
            end = len_username
            stop = True

        print("username(%s) = %s" % (len(username), username[idx:end]))
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
            msg += "\n[\"%s\"] =\"|" % (user["name"])
            list_str = ""
            #print("user = %s" % user)
            if user["Karazhan"] and user["Karazhan"]["allStars"]:
                allstars = best_rank(user["Karazhan"]["allStars"])
                #print("allstars = %s" % allstars)
                percent = allstars["rankPercent"] #(1-allstars["rank"]/allstars["total"])*100
                msg += add_color_code(user["name"], percent)
                list_str += add_color_code(user["name"], percent)
                msg += "K: %s/%0.2f%%B%sD%s(%s)|" % (allstars["points"], percent, allstars["serverRank"], allstars["regionRank"], allstars["spec"])
                list_str += "K: %s/%0.2f%%B%sD%s(%s)|" % (allstars["points"], percent, allstars["serverRank"], allstars["regionRank"], allstars["spec"])
            if user["ZulAman"] and user["ZulAman"]["allStars"]:
                allstars = best_rank(user["ZulAman"]["allStars"])
                #print("allstars = %s" % allstars)
                percent = allstars["rankPercent"] #(1-allstars["rank"]/allstars["total"])*100
                msg += add_color_code(user["name"], percent)
                list_str += add_color_code(user["name"], percent)
                msg += "Z: %s/%0.2f%%B%sD%s(%s)|" % (allstars["points"], percent, allstars["serverRank"], allstars["regionRank"], allstars["spec"])
                list_str += "Z: %s/%0.2f%%B%sD%s(%s)|" % (allstars["points"], percent, allstars["serverRank"], allstars["regionRank"], allstars["spec"])
            if user["Gruul_Magtheridon"] and user["Gruul_Magtheridon"]["allStars"]:
                #allstars = user["Gruul_Magtheridon"]["allStars"][0]
                allstars = best_rank(user["Gruul_Magtheridon"]["allStars"])
                #print("allstars = %s" % allstars)
                percent = allstars["rankPercent"] # (1-allstars["rank"]/allstars["total"])*100
                msg += add_color_code(user["name"], percent)
                list_str += add_color_code(user["name"], percent)
                msg += "G: %s/%0.2f%%B%sD%s(%s)|" % (allstars["points"], ((1-allstars["rank"]/allstars["total"])*100), allstars["serverRank"], allstars["regionRank"], allstars["spec"])
                list_str += "G: %s/%0.2f%%B%sD%s(%s)|" % (allstars["points"], ((1-allstars["rank"]/allstars["total"])*100), allstars["serverRank"], allstars["regionRank"], allstars["spec"])
            if user["SSC_TK"] and user["SSC_TK"]["allStars"]:
                #allstars = user["SSC_TK"]["allStars"][0]
                allstars = best_rank(user["SSC_TK"]["allStars"])
                #print("allstars = %s" % allstars)
                percent = allstars["rankPercent"] # (1-allstars["rank"]/allstars["total"])*100
                msg += add_color_code(user["name"], percent)
                list_str += add_color_code(user["name"], percent)
                msg += "T: %s/%0.2f%%B%sD%s(%s)|" % (allstars["points"], ((1-allstars["rank"]/allstars["total"])*100), allstars["serverRank"], allstars["regionRank"], allstars["spec"])
                list_str += "T: %s/%0.2f%%B%sD%s(%s)|" % (allstars["points"], ((1-allstars["rank"]/allstars["total"])*100), allstars["serverRank"], allstars["regionRank"], allstars["spec"])
            if user["BT_Hyjal"] and user["BT_Hyjal"]["allStars"]:
                #allstars = user["SSC_TK"]["allStars"][0]
                allstars = best_rank(user["BT_Hyjal"]["allStars"])
                #print("allstars = %s" % allstars)
                percent = allstars["rankPercent"] # (1-allstars["rank"]/allstars["total"])*100
                msg += add_color_code(user["name"], percent)
                list_str += add_color_code(user["name"], percent)
                msg += "H: %s/%0.2f%%B%sD%s(%s)|" % (allstars["points"], ((1-allstars["rank"]/allstars["total"])*100), allstars["serverRank"], allstars["regionRank"], allstars["spec"])
                list_str += "H: %s/%0.2f%%B%sD%s(%s)|" % (allstars["points"], ((1-allstars["rank"]/allstars["total"])*100), allstars["serverRank"], allstars["regionRank"], allstars["spec"])
            msg += "\""
            if list_str:
                userdata[user["name"]] = list_str
        msg += "\n"
        print("==========================================")
        print(msg)
        print("==========================================")
        write_userdata("server/%s" % server_id, userdata)

        for i in tqdm(range(450)):
            time.sleep(1)

        if stop:
            break

    return userdata

def write_target(server_name, filename, userdata):
    path = "Data/"

    if not os.path.exists(path):
        os.mkdir(path)

    f = open( path + filename, 'w')
    f.write("if(GetRealmName() == \"%s\")then\nWP_Database = {\n" % server_name)

    for name, stat  in userdata.items():
        f.write("[\"%s\"] = \"%s\",\n" % (name, stat))

    f.write("}\nend")
    f.close()

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
