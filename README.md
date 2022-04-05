This is the script to crawl the player data on [[WCL TW region](https://tw.classic.warcraftlogs.com/)] for World of Warcraft classic TBC, should also works with other regions.

You can find this UI [[WCLRanks on CurseForge](https://curseforge.com/wow/addons/wclranks/)].

# Prerequisite
These scripts run on Ubuntu Jammy(22.04) server, so all commands and scripts all run under Ubuntu Linux server.

Not sure how many packages need to be installed, I try to list them all. Please file bugs or send me pull-request to complement the list.

    sudo apt install git python3 python3-tqdm python3-requests

# Start
## WCLRanks
First of all you have to clone the UI part from my repo, [[WCLRanks](https://github.com/acelan/WCLRanks)], to another name, and then delete the `Data` folder and commit the change.

Setup your own project on CurseForge and push the code to github or somewhere else. And then add the source tree in `Manage Project -> Source` and select `Automatic Packaging -> Package tagged commits`(you may want to do this after all have been set).

## API key
Create you own client API key from [[here](https://classic.warcraftlogs.com/api/clients/)], and put the client id and secret in `config.py`.

    client_id = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    client_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

## Reports you want to check regularly
Edit `server/gen_list.py` and add the server id, server name, and the user id and/or guild name which you want to retrive reports from.

Ex.
```python
    server_data = {
        "SERVER_ID": {
            "name" : "SERVER_NAME",
            "userlist" : ["USER1_ID", "USER2_ID", "USER3_ID"],
            "guildlist": ["GUILD1_NAME", "GUILD2_NAME", "GUILD3_NAME"]
        },
        "5053": {	# an real example
            "name" : "瑪拉頓",
            "userlist" : ["1396448", "1254127", "1284707", "1506151","1217075","1033941", "1510869", "1516388", "994406", "1644080", "1100596", "1679238", "1592486", "459700"],
            "guildlist": ["無與倫比的自由", "QAQ", "老兄村", "One Piece", "CTR", "末日天使", "Pallas", "淘金(G)團", "Nemesis", "啾尼爾", "SoF", "我只會心疼哥哥", " 黑手別黑本阿會長說我們只>收歐洲人不收非洲人", " 自由殿堂", "IMBA", "信董爽歪歪", "黑玫瑰", "糕餅舖", "輪迴夢境", "镶金玫瑰", "傲雪紛飛"]
        },
    }
```
Run `gen_list.py` after the user and guild list have been set, it generates directories to contains the info of the servers. You need to run this script everytime you add/modify the userlist and/or guildlist.

## Run the crawler
Just run `wcl_ant.py`, it generates `Data` directory and put all the data there.

Be aware of the rate limit and the points you spent while retriving data. You can check it from the bottom of the [[profile](https://classic.warcraftlogs.com/profile)] page.

You may consider to [[subscribe](https://www.patreon.com/warcraftlogs)] warcraftlogs for $2 per month to get 10 times of the points if your region includes too many servers to retrive all the data in one day.

## Bump the version
Make sure the `WCLRanks` directory is properly set to `WCLRanks_path` and TOC filename set to `WCLRanks_toc` in the file `bump_version.py`, and then run `bump_version.py`, it copies `Data` to `WCLRanks` folder, bumps UI version in TOC file, and do git commit and tag to the repo.

## Update TOC file
The toc file, `WCLRanks.toc`, for `WCLRanks` is in this project, make the eodification on the `WCLRanks.toc` in this repo if you want to update the TOC info.

`bump_version.py` updates the version in `WCLRanks.toc` and copy it to `WCLRanks` directory.

Be aware of that you need to change the `WCLRanks` folder name and TOC filename to your project name and make sure the new folder name is written in `WCLRanks_path` and `WCLRanks_toc` in `bump_version.py` file.

## Final step
Confirmed you have no issue running `wcl_ant.py` and `bump_version.py`, then you can put them into cron job and run them at regular time.

Ex.
```
0 2 * * * (cd /home/acelan/wow/wcl_ant; ./wcl_ant.py > wcl_ant.log)
0 14 * * * (cd /home/acelan/wow/wcl_ant; ./bump_version.py >> wcl_ant.log)
```
And if you didn't setup "Automatic Packaging" yet, now it's the time.
