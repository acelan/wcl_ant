#!/usr/bin/python3

import os
import pickle
from pathlib import Path

server_data = {
        "5053": {
            "name" : "瑪拉頓",
            "userlist" : ["1396448", "1254127", "1284707", "1506151","1217075","1033941", "1510869", "1516388", "994406", "1644080", "1100596", "1679238", "1592486", "459700"],
            "guildlist": ["無與倫比的自由", "QAQ", "老兄村", "One Piece", "CTR", "末日天使", "Pallas", "淘金(G)團", "Nemesis", "啾尼爾", "SoF", "我只會心疼哥哥", "黑手別黑本阿會長說我們只收歐洲人不收非洲人", "自由殿堂", "IMBA", "信董爽歪歪", "黑玫瑰", "糕餅舖", "輪迴夢境", "镶金玫瑰", "傲雪紛飛", "Boom", "遠征", "小迷宮", "低治傷歐拉歐拉團", "迷霧中的野花", "深淵", "低治傷歐拉歐拉主團", "黑手別黑本阿會長說我們只收歐洲人不收非洲人二團", "萬窮殿", "腹肌真是大GG", "濕速車車", "時溯旅人", "Avec le soleil ☀ ", "欸波波"]
            },
        "5052": {
            "name" : "伊弗斯",
            "userlist" : [],
            "guildlist": ["極限鐵盒六團", "Legend of Defiler", " 壞寶寶聯盟我只信好牧", "軍師 聯盟", " Remix", " Destiny Breaker", "i have a dream", " 撿到槍一團", "樹蛙娛樂", "咖波與他的快樂夥伴", "吃瓜真香", "邊境小鎮", "艾歐尼亞天空-伊弗斯", "古老神話", "Avengers", "TW 野團", "Rely EX", "肥羊王G團", "Dawang Gaming", "寂寞謳歌", "二萬二良心企業", "提里斯法守護者", "薄荷葉", "WCL LOGS", "Island of Greed", "「粗」「四」wow30cm.tw", "神羅天征", "Merry Meet Merry Part", "Source of Chaos", "極限鐵盒6團", "浪團", "Look at me", "極限鐵盒_1團", "Rely金團", "Source of Chaos 2團", "極限鐵盒2團", "食我", "部落瘋狗", "細雨紛飛", "微醺沙發", "艾彩", "鹹魚集合體", "IFC2", "神羅二團", "無料案内所", "有禮貌", "清風醉花亭", "ForSaken", "Eternity", "泡奶戰神休閒團", "歐維士布萊克", "Pantheon", "珠光寶氣", "Breath of Horde", "Aurora", "NO MERCY", "Nomad", "JOKER-G", "Meteora", "姨爹姨爹蹦蹦", "加拿大楓葉國", "Gossiping", "Fight Club", "走不近", "123進組", "Exodus", "Cum down", "Rbae Style", "Dark Tranquillity", "大小黑鵰同萌會"],
            },
        }

for server in server_data:
    if not os.path.isdir(server):
        os.mkdir(server)

    pickle.dump(server_data[server]["name"], open('%s/name.pkl' % server, 'wb'))
    if server_data[server]["userlist"]:
        Path(server).mkdir(parents=True, exist_ok=True)
        pickle.dump(server_data[server]["userlist"], open('%s/userlist.pkl' % server, 'wb'))
        print(pickle.load(open('%s/userlist.pkl' % server, 'rb')))
    if server_data[server]["guildlist"]:
        Path(server).mkdir(parents=True, exist_ok=True)
        pickle.dump(server_data[server]["guildlist"], open('%s/guildlist.pkl' % server, 'wb'))
        print(pickle.load(open('%s/guildlist.pkl' % server, 'rb')))

