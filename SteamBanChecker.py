import asyncio
import aiohttp
import re
import requests
from time import time

while True:
    userinput = input("Provide a Steam Account Identifier:")
    timeout = input("Timeout (in sec):")
    API_key = ""
    bans = []
    regex = r"(?:(?<=Reason)|(?<=Důvod))<\/\w*>[\s|.]*<.*>(.*)<"

    SBPages = ['https://www.skial.com/sourcebans/index.php?p=banlist',               #tf2
             'https://sappho.io/bans/index.php?p=banlist',                           #tf2
             'https://bans.blackwonder.tf/index.php?p=banlist',                      #tf2, 401 error due to "maintenance" per discord
             'https://triggerhappygamers.com/sourcebans/index.php?p=banlist',        #tf2
             'https://firepoweredgaming.com/sourcebanspp/index.php?p=banlist',       #tf2
             'https://bans.flux.tf/index.php?p=banlist',                             #tf2, 500 error due to sourcebans++ error per discord
             'https://bans.wonderland.tf/index.php?p=banlist',                       #tf2, 403s due to cloudflare, to be removed soon?
             'https://lazypurple.com/sourcebans/index.php?p=banlist',                #tf2
             'http://disc-ff.site.nfoservers.com/sourcebanstf2/index.php?p=banlist', #tf2
             'https://sg-gaming.net/bans/index.php?p=banlist',                       #tf2
             'http://tf2swapshop.com/sourcebans/index.php?p=banlist',                #tf2
             'https://bans.scrap.tf/index.php?p=banlist',                            #tf2
             'https://bans.panda-community.com/index.php?p=banlist',                 #tf2
             'http://www.thefurrypound.org/sourcebans/index.php?p=banlist',         
             'https://www.tf2-oreon.fr/sourceban/index.php?p=banlist',              
             'https://sb.ugc-gaming.net/index.php?p=banlist',                        #tf2, 403s on datacenter ips
             'https://www.theville.org/sourcebans/index.php?p=banlist',             
             'https://looscommunity.xyz/sourcebans/index.php?p=banlist',            
             'https://cedapug.com/sourcebans/index.php?p=banlist',                  
             'https://banlist.gamesites.cz/tf2/index.php?p=banlist',                
             'https://www.lazyneer.com/SourceBans/index.php?p=banlist',             
             'https://www.the-vaticancity.com/sourcebans/index.php?p=banlist',      
             'https://bans.tf2maps.net/index.php?p=banlist',                        
             'https://sirplease.gg/index.php?p=banlist',                             #l4d2
             'https://astramania.ro/sban2/index.php?p=banlist',                      #csgo
             'https://bans.tf2trade.com/index.php?p=banlist',                       
             'https://bans.nide.gg/index.php?p=banlist',                             #css
             'https://bachuruservas.lt/sb/index.php?p=banlist',                      #csgo
             'https://snksrv.com/bans/index.php?p=banlist',                          #csgo
             'https://ban.hellz.fr/index.php?p=banlist',                             #css
             'https://hellclan.co.uk/sourcebans/index.php?p=banlist',                #css 
             'http://94.249.194.218/sb/index.php?p=banlist',                         #css
             'https://gunserver.ru/sourcebans/index.php?p=banlist',                  #css
             'https://pong.setti.info/sourcebans/index.php?p=banlist',               #css&csgo
             'https://sourcebans.dreamfire.fr/index.php?p=banlist',                  #css
             'https://spectre.gg/bans/index.php?p=banlist',                          
             'https://sourcebans.ghostcap.com/index.php?p=banlist',                 
             'https://7-mau.com/server/index.php?p=banlist',                        
             'https://www.banlist.madgames.eu/index.php?p=banlist',                 
    #         'https://bans.starserv.net/index.php?p=banlist',                       #broken
             'http://www.game-server.sk/sourcebans/index.php?p=banlist',            
             'https://www.weallplay.eu/sourcebans/index.php?p=banlist',             
             'https://www.mestrogaming.net/secureplay/index.php?p=banlist',         
             'https://sourcebans.acekill.pl/index.php?p=banlist',                   
    #         'https://klonken.com/bans/index.php',                                  #custom search function, broken
             'https://magyarhns.hu/sourcebans/index.php?p=banlist',                  
             'https://bans.powerfps.com/index.php?p=banlist',                        
             'https://pwnzone.net/sourcebans/index.php?p=banlist',                   
             'https://banlist.games-town.eu/index.php?p=banlist',                    
             'https://bans.tfrag.dk/index.php?p=banlist',                            
             'https://sameteem.com/sourcebans/index.php?p=banlist',                  #csgo
             'https://bans.csiservers.com/index.php?p=banlist',                      #gmod
             'https://sourcebans.gflclan.com/index.php?p=banlist',                   #tf2, css, gmod, csgo
             'http://bans.harpoongaming.com/index.php?p=banlist',
             'https://bans.tf2ro.com/index.php?p=banlist',
             'https://bans.otaku.tf/bans'
             ]

    def translate_to_id64(identifier):
        vanityurl_pattern = r"id\/(\S{2,32})\/?"
        steamid2_pattern = r"^STEAM_[0-5]:[0-1]:\d+$"
        steamid3_pattern = r"^\[U:1:(\d+)\]$"
        id64_pattern = r"(765\d{14})"

        if re.search(vanityurl_pattern, identifier):
            vanity = re.search(vanityurl_pattern, identifier).group(1)
            response = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={API_key}&vanityurl={vanity}", timeout=int(timeout))
            if response.status_code == 403:
                print("Please provide a valid SteamAPI key in the script for resolving CustomURLs")
                return
            elif response.json()['response']['success'] == 1:
                steamid64 = response.json()['response']['steamid']
                print(steamid64)
                return steamid64
            else:
                print(f"SteamAPI Error: {response.json['response']['message']}")
                return
        elif re.search(steamid2_pattern, identifier):
            steamid2_parts = identifier.split(":")
            steamid64 = ((int(steamid2_parts[2]) * 2) + int(steamid2_parts[1])) + 76561197960265728
            return steamid64
        elif re.search(steamid3_pattern, identifier):
            id = re.search(steamid3_pattern, identifier).group(1)
            steamid64 = int(id) + 76561197960265728
            return steamid64
        elif re.search(id64_pattern, identifier):
            steamid64 = re.search(id64_pattern, identifier).group(1)
            return steamid64
        else:
            print("Input is not a valid Steam identifier.")
            return

    def id64_to_steamid2(id64):
        steamid = []
        subid = int(id64) - 76561197960265728
        if subid % 2 == 0:
            steamid.append('0:')
        else:
            steamid.append('1:')
        steamid.append(str(subid//2))
        return ''.join(steamid)

    def id64_to_steamid3(id64):
        steamid = []
        steamid.append('[U:1:')
        subid = int(id64) - 76561197960265728
        steamid.append(str(subid)+']')
        return ''.join(steamid)

    ID64 = translate_to_id64(userinput)

    async def fetch_bans(website, session):
        domain = re.search('^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n]+)', website).group(1)
        if domain == 'skial.com':
            url = website + '&advType=steam&advSearch=' + id64_to_steamid3(ID64)
        else:
            url = website + '&advType=steam&advSearch=' + id64_to_steamid2(ID64)
        responsestart = time()
        try:
            async with session.get(url, timeout=int(timeout)) as response:
                html = await response.text()
                if response.status > 200:
                    print(f'{domain} returned code {response.status}')
                    return None
                matches = re.findall(regex, html)
                for reason in matches:
                    if reason != "":
                        print(f'{domain} - {reason}')
                        bans.append(f"{domain} - {reason}")
        except asyncio.TimeoutError:
            print(f"Timeout while fetching {domain}")
            return None
        except Exception as e:
            print(f'Error while fetching {domain}: {e}')
            return None

    async def main(websites):
        start = time()
        session = aiohttp.ClientSession()
        ret = await asyncio.gather(*[fetch_bans(website, session) for website in websites])
#        print(f"{len(bans)} entries in the banlist!")
        await session.close()
        print(f"Finished scanning. Took {time()-start} seconds.")

    asyncio.run(main(SBPages))