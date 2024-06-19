from colorama import Fore, Style, init
import datetime
from rich.console import Console

style = Console()

init()

class colors:
    green = f"{Fore.LIGHTGREEN_EX}"
    red = f"{Fore.LIGHTRED_EX}"
    darkred = f"{Fore.RED}"
    yellow = f"{Fore.LIGHTYELLOW_EX}"
    magenta = f"{Fore.LIGHTMAGENTA_EX}"
    cyan = f"{Fore.LIGHTCYAN_EX}"
    black = f"{Fore.LIGHTBLACK_EX}"
    white = f"{Fore.LIGHTWHITE_EX}"
    blue = f"{Fore.LIGHTBLUE_EX}"
    reset = f"{Style.RESET_ALL}"
    
class time:
    time = datetime.datetime.now()
    hour_time = time.hour
    hour_time1 = time.minute
    hour_time2 = time.second

    data_time = f"{colors.green}[{colors.black}{hour_time:02}:{hour_time1:02}:{hour_time2:02}{colors.green}]{colors.reset}"
class banners:
    p = "═"*100
    x = "═"*20
    w = "╔"
    l = "╗"
    c = "╚"
    y = "╝"
    now = datetime.datetime.now()
    day = now.strftime("%A")
    
    
    banner = f"""\n
\t\t\t\t{colors.cyan}╔═╗┌┬┐┬ ┬┌─┐┌─┐┬┌─┐ {colors.black} ╔═╗┬─┐┌─┐ ┬┌─┐┌─┐┌┬┐
\t\t\t\t{colors.cyan}║╣  │ ├─┤│ │├─┘│├─┤ {colors.black} ╠═╝├┬┘│ │ │├┤ │   │ 
\t\t\t\t{colors.cyan}╚═╝ ┴ ┴ ┴└─┘┴  ┴┴ ┴ {colors.black} ╩  ┴└─└─┘└┘└─┘└─┘ ┴ {colors.cyan}{day}{colors.reset}\n
{colors.white}{w}{p}{l}\n
\tAUTHOR\t\t={colors.magenta} ClaySec{colors.white}
\tTEAM\t\t= {colors.magenta}SundaXploiter{colors.white}
\tGITHUB\t\t={colors.magenta} https://github.com/1llsion/{colors.white}
\tVERSION\t\t={colors.cyan} 1.0.12{colors.white}
\tDESCRIPTION\t= {colors.magenta}Tools For Pentesting Web Application{colors.white}
\tNOTE\t\t= {colors.black}KALAU MAU RECODE IJIN DULU NGAB / AUTHOR JANGAN DI\n\t\t\t  GANTI NGACA ANJING KALAU GK PUNYA SKILL JANGAN RECODE{colors.reset}\n
{colors.white}{c}{p}{y}{colors.reset}\n
    """
    def menu():
        menu_list = [
        "shell finder", 
        "wordpress brute force", 
        "md5hash", 
        "wordpress analyze", 
        "laravel auto get env", 
        "DDOS", 
        "sitemap generator", 
        "port scanner"
        ]

        severity_list = [
            f"[ info   ]", 
            f"[ normal ]", 
            f"[ info   ]", 
            f"[ any    ]", 
            f"[ normal ]", 
            f"[ high   ]", 
            f"[ info   ]", 
            f"[ info   ]"
        ]

        descriptions_list = [
            "Find potential shells on a server.",
            "Perform brute force attacks on WordPress sites to identify weak credentials.",
            "Generate and analyze MD5 hashes for integrity checks.",
            "Analyze WordPress installations for common vulnerabilities.",
            "Automatically retrieve environment variables in Laravel applications.",
            "Simulate Distributed Denial of Service attacks for testing purposes.",
            "Generate sitemaps for websites to improve SEO.",
            "Scan network ports to identify open services."
        ]
        p2 = "═"*129
        print(f"{colors.white}╔{p2}╗")
        print("║ {:<30} {:<17} {:<78} ║".format("Menu", "Severity", "Description"))
        print(f"╠{p2}╣")
        for menu, severity, description in zip(menu_list, severity_list, descriptions_list):
            print("║ {:<30} {:<17} {:<78} ║".format(menu, severity, description))
        print(f"╚{p2}╝")
