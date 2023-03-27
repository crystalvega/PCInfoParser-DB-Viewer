from command_runner.elevate import elevate

import Config
import GUI
import MySQL


def main():
    check, Return, mysql = Config.Check()
    if check:
        if MySQL.Connect(mysql[0], mysql[1], mysql[2], mysql[3]) == 0:
            Parsinginfo = MySQL.ParseDB()
            GUI.Start(Parsinginfo)
    else:
        print(Return)

if __name__ == "__main__":
    elevate(main)