#!/usr/bin/python3

import os
import pickle
from pathlib import Path

server_data = {
        "5053": {
            "name" : "瑪拉頓",
            "userlist" : ["1396448", "1254127", "1284707", "1506151","1217075","1033941", "1510869", "1516388", "994406", "1644080", "1100596", "1679238", "1592486", "459700", "1932774", "1780465", "1966705", "1274742", "2021903", "1471157", "1932774", "2046272", "1160081", "1783050", "613972", "1557013", "2076848", "1849379", "1741209", "1684006", "1110635", "2032618", "1580093", "1558031", "1995218", "1108651", "1041090", "1450686", "2061123", "1101547", "1208223", "1067363", "1439087", "1333185", "431198", "1519927", "1742519", "738386", "1777132", "345037", "1889992", "2026353", "1045968", "1179032", "1783050", "1447379", "1752135", "854230", "963427", "849154", "1565957", "1020303", "2170057", "1604940", "1850649", "2156681", "2153457", "1521093", "2145924", "1148152", "2143431", "1590024", "1693368", "1327704", "1122232", "2121080", "1828629", "1194654", "1048134", "2004536", "1668522", "1747024", "1702866", "2161031", "2130700", "1458866", "478554", "1443886", "1932334", "142541", "1899025", "713907", "2273649", "2218780", "2183058", "1713087", "1119328", "595996"],
            "guildlist": ["無與倫比的自由", "QAQ", "老兄村", "One Piece", "CTR", "末日天使", "Pallas", "淘金(G)團", "Nemesis", "啾尼爾", "SoF", "我只會心疼哥哥", "黑手別黑本阿會長說我們只收歐洲人不收非洲人", "自由殿堂", "IMBA", "信董爽歪歪", "黑玫瑰", "糕餅舖", "輪迴夢境", "镶金玫瑰", "傲雪紛飛", "Boom", "遠征", "小迷宮", "低治傷歐拉歐拉團", "迷霧中的野花", "深淵", "低治傷歐拉歐拉主團", "黑手別黑本阿會長說我們只收歐洲人不收非洲人二團", "萬窮殿", "腹肌真是大GG", "濕速車車", "時溯旅人", "Avec le soleil ☀ ", "欸波波", "大B團", "TW - No offensive names.", "Koi", "朝花夕拾", "甘寧周罵渡假村", "Impact", "肥腸", "Silver Dawn", "Lycoris", "IKEA of Avalon", "在被告身旁不堪一擊", "亞斯塔洛特", "幸運女神事務所", "雲裡霧裡", "我只會心疼哥哥", "不想放手", "下午團", "What's Up", "朝花夕拾初心團", "倚竹醉酒笑紅塵", "看到路上有人拿棍子不要以為不是要打你", "胖鳥的野團記錄檔", "驅魔麵館", "可不可經典再現", "自由二團", "B爺團", "暖光", "劍與魔法重返4團", "老戰友", "TW - 不要 冒犯性 名稱.", "SSR Angerforge", "深瞳之森", "爲你寫詩", "The One", "老鳥深夜食堂", "wisdomangel", "千帆公会", "無上流沙", "米奇不妙屋", "好久不見", "龍王山遠征軍", "Blue Wings（亞服）", "DiamondForce", "老干部局机关二食堂（台服）", "青云小筑", "又见花开", "Crane dream （CD）", "北凉"]
            },
        "5052": {
            "name" : "伊弗斯",
            "userlist" : ["1231180", "973644", "690499"],
            "guildlist": ["極限鐵盒六團", "Legend of Defiler", " 壞寶寶聯盟我只信好牧", "軍師 聯盟", " Remix", " Destiny Breaker", "i have a dream", " 撿到槍一團", "樹蛙娛樂", "咖波與他的快樂夥伴", "吃瓜真香", "邊境小鎮", "艾歐尼亞天空-伊弗斯", "古老神話", "Avengers", "TW 野團", "Rely EX", "肥羊王G團", "Dawang Gaming", "寂寞謳歌", "二萬二良心企業", "提里斯法守護者", "薄荷葉", "WCL LOGS", "Island of Greed", "「粗」「四」wow30cm.tw", "神羅天征", "Merry Meet Merry Part", "Source of Chaos", "極限鐵盒6團", "浪團", "Look at me", "極限鐵盒_1團", "Rely金團", "Source of Chaos 2團", "極限鐵盒2團", "食我", "部落瘋狗", "細雨紛飛", "微醺沙發", "艾彩", "鹹魚集合體", "IFC2", "神羅二團", "無料案内所", "有禮貌", "清風醉花亭", "ForSaken", "Eternity", "泡奶戰神休閒團", "歐維士布萊克", "Pantheon", "珠光寶氣", "Breath of Horde", "Aurora", "NO MERCY", "Nomad", "JOKER-G", "Meteora", "姨爹姨爹蹦蹦", "加拿大楓葉國", "Gossiping", "Fight Club", "走不近", "123進組", "Exodus", "Cum down", "Rbae Style", "Dark Tranquillity", "大小黑鵰同萌會", "國際貓毛盜採組織", "進輪車業", "納茲格寧姆的鋼鐵部落G團", "香城", "龍貓團", "Endless Memory", "索爾的一棟城堡", "咕咕雞團", "Devil May Cry", "【極限鐵盒】4團", "唷唷", "化物語", "巫妖抬價小隊", "爸爸去哪兒", "Dark-H", "天涯海閤", "Slackers", "AllYouCanEat", "無料案内所", "Meteora", "昂比利克斯", "咖波與他的快樂夥伴", "歐維士布萊克", "未眠人", "今天先這樣", "雁渡寒潭", "Noobs Int", "大雷瓜棚", "G United int", "Old School", "深藏功与名", "Fairy Town", "咕咕保護協會", "S A分会", "光華白鐵廠", "万焰公会", "Keahoarl-777", "New School", "咩咩財團", "王牌飛行員", "我们唱歌很好听", "TreeNewBee", "貓貓在角落", "WELL.台服", "多喝開水", "Aurora Forever", "Rest In Peace", "Reborn", "关羽台服g团", "晴天亚服", "黎明之光", "Wind Rose", "NukeG团-伊弗斯", "禿頭萌妹團（台服）", "marsh", "NEED", "金字塔", "超越周四团", "单刀", "金陵世家 霜月团", "小浣熊", "直到魔兽的尽头", "阿斯加德", "纵横"],
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

