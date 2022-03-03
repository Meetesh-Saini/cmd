import os
from colorama import Fore, Back, Style
import readline
import json
import sys

try:

    pwd = "/home/sandbox"
    dirs = {"sandbox":{"base":{},"bin":{}}}
    path_dict = {}
    users = {"sandbox":"admin"}
    logged = "sandbox"
    
    # add dir path to pwd
    def add_dir(dirname):
        global pwd
        pwd += '/'+dirname
    # remove dir path from pwd
    def back_dir():
        global pwd
        if pwd != "/home":
            pwd = '/'.join(pwd.split('/')[:-1])
    # get the dict of current directory
    def path(fullpath="",parent=False):
        global path_dict
        dir_path = ""
        if not fullpath:
            fullpath = pwd
        if parent:
            for i in range(len(fullpath.split("/"))-3):
                dir_path += f"['{fullpath.split('/')[i+2]}']"
        else:
            for i in range(len(fullpath.split("/"))-2):
                dir_path += f"['{fullpath.split('/')[i+2]}']"
        exec(f"global path_dict; path_dict = dirs{dir_path}")
        return path_dict
    # returns current working directory
    def cwd():
        return pwd.split('/')[-1]
    def err(message):
        fixed = "mash: "
        print(Fore.RED+fixed+Style.RESET_ALL+message)
    def editable_input(txt=""):
        readline.set_startup_hook(lambda: readline.insert_text(txt))
        try:
            return input()
        finally:
            readline.set_startup_hook()


    while True:
        # getting command
        command = input(Fore.GREEN+Style.BRIGHT+f"[{pwd}]{Fore.BLUE} >"+Style.RESET_ALL).strip()
    
        if command=='exit':
            quit()
        elif command == "ls":
            print(Fore.GREEN+f"{Fore.BLUE}".join(f'{Style.RESET_ALL}\t{Fore.GREEN}'.join(path().keys()).split("*"))+Style.RESET_ALL)
        elif command == "pwd":
            print(pwd+'/')
        elif command == "cd" or command.startswith("cd "):
            com = command.split()
            if len(com) == 1:
                pwd = "/home/"+logged
            elif com[1].strip() == '..':
                back_dir()
            elif com[1].strip() == '.':
                pass
            else:
                if com[1].strip() in path():
                    if pwd != "/home":
                        add_dir(com[1].strip())
                    else:
                        err("use su to change user") if com[1].strip() != logged else add_dir(com[1].strip())
                else:
                    err("no such directory exists")
        elif command == "mkdir" or command.startswith("mkdir "):
            com = command.split()
            if len(com)!=1:
                com = com[1].strip()
                if '*' not in com:
                    if com not in path():
                        if pwd != "/home":
                            path()[com] = {}
                        else:
                            err("cannot create user directory, use useradd <username>")
                    else:
                        err("directory already exists")
                else:
                    err("directory name must not contain *")
            else:
                err("directory name is empty.")
        elif command == "rmdir" or command.startswith("rmdir "):
            com = command.split()
            if len(com)!=1:
                com =com[1].strip()
                if pwd!="/home":
                    if com in path():
                        path().pop(com)
                    else:
                        err("directory doesn't exists")
                else:
                    err("cannot remove user directory, remove user by sudo userdel <username>")
            else:
                err("directory name is empty.")
    
        elif command == "sudo" or command.startswith("sudo "):
            if users[logged] == input("password: "+Fore.LIGHTBLACK_EX+Back.LIGHTBLACK_EX+Style.BRIGHT).strip():
                print(Style.RESET_ALL+"Verified user.")
                # com = command.split()[1:]
                # if com[0].strip() == "userdel":
                #     if com[1].strip() == logged:
                #         err("change user first.")
                #     else:
                #         users.pop(com[1].strip())
                #         dirs.pop(com[1].strip())
                # elif com[0].strip() == "useradd":
                #     err("useradd do not require sudo")
            else:
                print(Style.RESET_ALL+"Incorrect password.")
        elif command.startswith("useradd"):
            com = command.split()[1].strip()
            if com not in users:
                users[com] = input("set password: "+Fore.LIGHTBLACK_EX+Back.LIGHTBLACK_EX+Style.BRIGHT).strip()
                print(Style.RESET_ALL+"user created successfully.")
                dirs[com] = {}
            else:
                err("user already exists")
        elif command.startswith("su "):
            com = command.split()[1].strip()
            if users[com] == input("password: "+Fore.LIGHTBLACK_EX+Back.LIGHTBLACK_EX+Style.BRIGHT).strip():
                print(Style.RESET_ALL+"Verified user.")
                pwd = "/home/"+com
                logged = com
            else:
                print(Style.RESET_ALL+"Incorrect password.")
        elif command == "userdel" or command.startswith("userdel "):
            com = command.split()
            if len(com)!=1:
                if com[1].strip() == logged:
                    err("change user first.")
                else:
                    if users[com[1].strip()] == input("password: "+Fore.LIGHTBLACK_EX+Back.LIGHTBLACK_EX+Style.BRIGHT).strip():
                        print(Style.RESET_ALL+"Verified user.")
                        users.pop(com[1].strip())
                        dirs.pop(com[1].strip())
                    else:
                        err("Incorrect password")
            else:
                err("username is empty")
        # Commands Only Text Editor
        elif command == "cote" or command.startswith("cote "):
            com = command.split()
            if len(com)!=1:
                com = com[1].strip()
                print(Fore.WHITE+Back.BLACK+Style.BRIGHT+'\t'+com+'\t'+Style.RESET_ALL)
                saved = False
                if "*"+com in path():
                    txt = path()["*"+com]
                    saved = True
                else:
                    txt = []
                while True:
                    if saved:
                        cote = input(">>>").strip()
                    else:
                        cote = input(f">>{Fore.RED}>{Style.RESET_ALL}").strip()
                    if cote=="q":
                        if not saved:
                            if input("Do you want to save? (any/n)") != "n":
                                path()["*"+com] = txt
                        break
                    elif cote=="a":
                        lines = []
                        while True:
                            editor = input()
                            editor = '\n'.join(editor.split("\n"))
                            if editor == "?qa":
                                if len(lines) != 0:
                                    saved = False
                                break
                            else:
                                lines.append(editor)
                        txt.extend(lines)
                    elif cote.startswith("c "):
                        cote = cote.split()
                        if len(cote)!=1:
                            line_no = int(cote[1].strip())
                            ch_txt = editable_input(txt[line_no])   #input()
                            if txt[line_no] != ch_txt:
                                saved = False
                                txt[line_no] = ch_txt
                    elif cote == "r":
                        pr_txt = [f"{Style.BRIGHT}{i}{Style.RESET_ALL} {txt[i]}" for i in range(len(txt))]
                        print('\n'.join(pr_txt))
                    elif cote.startswith("del "):
                        cote = cote.split()
                        if len(cote)!=0:
                            cote = cote[1].split("-")
                            start = cote[0].strip()[1:].strip()
                            end = cote[1].strip()[:-1].strip()
                            txt = txt[:int(start)]+txt[int(end)+1:]
                        saved = False
                    elif cote=="e":
                        ch_txt = editable_input('\n'.join(txt))   #input()
                        if txt != ch_txt.split('\n'):
                            saved = False
                            txt = ch_txt.split('\n')
                    elif cote=="s":
                        path()["*"+com] = txt
                        saved = True
    
            else:
                err("invalid filename")
        elif command == "mv" or command.startswith("mv "):
            com = command.split()
            if len(com) != 0:
                from_path = com[1].strip()
                to_path = com[2].strip()
                if from_path[-1] == '/' and to_path[-1] == '/':
                    from_path = from_path[:-1]
                    to_path = to_path[:-1]
                    path(to_path,True)[to_path.split("/")[-1]] = path(from_path)
                    path(from_path,True).pop(from_path.split("/")[-1])
                else:
                    if to_path.split("/")[-1] != '' or from_path.split("/")[-1] != '':
                        from_path = from_path.split("/")
                        from_path[-1] = "*"+from_path[-1]
                        from_path = "/".join(from_path)
                        to_path = to_path.split("/")
                        to_path[-1] = "*"+to_path[-1]
                        to_path = "/".join(to_path)
                        path(to_path,True)[to_path.split("/")[-1]] = path(from_path)
                        path(from_path,True).pop(from_path.split("/")[-1])
                    else:
                        err("file name is empty")
        elif command == "cp" or command.startswith("cp "):
            # com = command.split()
            # if len(com) != 0:
            #     from_path = com[1].strip()
            #     to_path = com[2].strip()
            #     path(to_path,True)[to_path.split("/")[-1]] = path(from_path)
            com = command.split()
            if len(com) != 0:
                from_path = com[1].strip()
                to_path = com[2].strip()
                if from_path[-1] == '/' and to_path[-1] == '/':
                    from_path = from_path[:-1]
                    to_path = to_path[:-1]
                    path(to_path,True)[to_path.split("/")[-1]] = path(from_path)
                else:
                    if to_path.split("/")[-1] != '' or from_path.split("/")[-1] != '':
                        from_path = from_path.split("/")
                        from_path[-1] = "*"+from_path[-1]
                        from_path = "/".join(from_path)
                        to_path = to_path.split("/")
                        to_path[-1] = "*"+to_path[-1]
                        to_path = "/".join(to_path)
                        path(to_path,True)[to_path.split("/")[-1]] = path(from_path)
                    else:
                        err("file name is empty")
        elif command == "cmdtxt":
            print(dirs)
        elif command == "savecmd":
            print(Fore.RED+Style.BRIGHT+"CAUTION:"+Style.RESET_ALL+"this will store the text file on the system to save the session.")
            fullpath = input("Enter full path to save cmd file (.json):")
            if os.path.isfile(fullpath):
                err("the file exsits, change file path or file name.")
            elif fullpath.strip()[-5:].lower()!=".json":
                err("file extension should be .json")
            else:
                with open(fullpath,"w") as f:
                    json.dump(dirs,f)
                print(Fore.GREEN+"saved session file successfully to "+fullpath+Style.RESET_ALL)
        elif command == "loadcmd":
            print(Fore.RED+Style.BRIGHT+"CAUTION:"+Style.RESET_ALL+"this will load the text file from the system to load the session and will remove the exisiting session, it is recommended to save session first before loading.")
            fullpath = input("Enter full path of cmd file:")
            if fullpath.strip()[-5:].lower()!=".json":
                err("file extension should be .json")
            elif os.path.isfile(fullpath):
                with open(fullpath,"r") as f:
                    dirs = json.load(f)
                    print(type(dirs))
                print(Fore.GREEN+"session loaded successfully using file "+fullpath+Style.RESET_ALL)
            else:
                err("file do not exists.")
        elif command == "clear":
            os.system("clear")
        elif command=='':
            pass
        else:
            err("command not found")

except KeyboardInterrupt:
    print()
    err("Signing off...")
    sys.exit()
except:
    print(f"{Fore.BLUE+Style.BRIGHT+Back.BLACK}\n\nIgnore if you have pressed CTRL+D\n{Style.RESET_ALL}")
    print(Fore.RED+Back.WHITE+'*'*50+Back.BLACK+Style.BRIGHT+"\nThis broke the code.\nAn error occured please let me know on github what command you executed. So that I can resolve that bug.\n"+Style.NORMAL+Fore.RED+Back.WHITE+'*'*50+Style.RESET_ALL)