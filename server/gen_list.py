#!/usr/bin/python3

import os
import pickle
from pathlib import Path

server_data = {
        "5053": {
            "name" : "瑪拉頓",
            "userlist" : ["1396448", "1254127", "1284707", "1506151","1217075","1033941", "1510869", "1516388", "994406", "1644080", "1100596", "1679238", "1592486", "459700", "1932774", "1780465", "1966705", "1274742", "2021903", "1471157", "1932774", "2046272", "1160081", "1783050", "613972", "1557013", "2076848", "1849379", "1741209", "1684006", "1110635", "2032618", "1580093", "1558031", "1995218", "1108651", "1041090", "1450686", "2061123", "1101547", "1208223", "1067363", "1439087", "1333185", "431198", "1519927", "1742519", "738386", "1777132", "345037", "1889992", "2026353", "1045968", "1179032", "1783050", "1447379", "1752135", "854230", "963427", "849154", "1565957", "1020303", "2170057", "1604940", "1850649", "2156681", "2153457", "1521093", "2145924", "1148152", "2143431", "1590024", "1693368", "1327704", "1122232", "2121080", "1828629", "1194654", "1048134", "2004536", "1668522", "1747024", "1702866", "2161031", "2130700", "1458866", "478554", "1443886", "1932334", "142541", "1899025", "713907", "2273649", "2218780", "2183058", "1713087", "1119328", "595996", "173402", "1589541", "978261", "604149", "5992", "2291649", "1159031"],
            "guildlist": ["35好友小號團", "FriendShipClub", "IKEA of Avalon", "Impact", "MyGO!!!!!", "不想放手", "倚竹醉酒笑紅塵", "喵喵叫的小伙伴们", "嘎了給給", "奧斯卡演員", "學長團", "小迷宮", "少少", "幸運女神事務所", "末日天使", "無與倫比的自由", "看到路上有人拿棍子不要以為不是要打你", "老年混子團", "肥腸", "肥腸二團", "膘巴達", "貪婪的冒險者", "餐桌騎士團-小鮮奶", "魔獸爽趴團"],
            },
        "5052": {
            "name" : "伊弗斯",
            "userlist" : ["1231180", "973644", "690499", "1621735", "1022502", "1896889", "973235", "1014893", "1051256", "1965079", "2237696"],
            "guildlist": ["35好友", "Dark Tranquillity", "End", "GGR", "Gladiolus禮拜四五", "O O P S", "Ouroboros", "RL每次都搞", "SSIS-413", "Source of Chaos", "Source of Chaos 2團", "Source of Chaos 週四團", "i have a dream", "一树梨花白", "你有棒子我有故事當我們都在小圈圈", "周防有希粉絲俱樂部", "夜半時光", "安西軍", "醺沙發", "戰士長", "等下要吃什麼", "索爾的一棟城堡", "細雨紛飛", "胖丁金團", "艾歐尼亞天空-伊弗斯", "薄荷葉", "走向共和", "躺著的部落", "辣個男人", "重生之再见伊弗斯", "雙足飛龍菅理員", "韶光", "香草山", "黑暗藝術", "A Star", "Fertty", "Hall of Fame", "Meteora", "Protosss", "Source of Chaos 週日團", "✮PanTheon✮", "✮PanTheon✮Ⅱ", "乂橘子乂", "二萬二良心企業", "你不行的家", "你想證明什麼", "吃瓜真香", "重生之再见伊弗斯", "開心教", "香城", "CurseForge", "END-CN", "IFC1", "Noobs Int", "PUA", "Personal Test", "memory corridor", "天涯海閤", "小喵团 TW", "小鐵經典團", "微醺沙發", "我们都爱点操陈淼圣", "提里斯法守護者", "杀戮", "極限便當盒", "約砲", "薩滿一團", "醬爆的女朋友們", "開心是種選擇", "黑風山觀音禪院", "默"],
            },
        "5205": {
            "name" : "烏蘇雷",
            "userlist" : ["1896889", "486041", "1535244", "2371907", "1052681", "902871", "353477", "2249924", "859477", "642089", "310995"],
            "guildlist": ["Nuke-鸽王争霸", "伊卡洛斯和他的伙伴们", "Dark Tranquillity", "离殇", "P A S", "Meow Boss Gaming", "yseraskyCTM", "The Ran Beach Legion", "Hey Chocolate", "黑手兄弟會", "小喵团台服分舵", "至死不渝", "金陵世家 霜月团", "DrumstickG团", "寒脊山之光", "永 夜 休闲团", "无糖乌苏雷四海为家", "无>糖乌苏雷", "小拳拳幫", "缘起", "鹅城", "誠 諾灬烏蘇雷", "乌鸦团", "千钧一发台服", "颤粟-乌蘇雷", "伊卡洛斯的小伙伴", "LSP驻台办", "为了方便吹逼迫不得已组建的工会", "远征-乌苏雷", "大聪明", "in time", "隨便拉", "marsh", "炎魔之灵", "科语然", "酱爆的女友们"],
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

