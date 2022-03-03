# cmd
A bash clone with some working functionalities. You cannot access the real files on the system. It creates a virtual directory structure which cannot read, write, delete or update the real files on the system. You can do these operations with the files and directories which are inside my cmd only.  
Works on both Linux and Windows.

## Stable Commands:
### Bash like Commands
ls  
cd  
pwd  
mkdir  
rmdir  
mv  
cp  
clear  
exit
### My Commands:
cmdtxt  
savecmd  
loadcmd  
cote

## Commands (Not working properly):
sudo  
userdel  
useradd  
su  

## My Commands Usage:
#### cmdtxt
Prints how program is storing the data.
#### savecmd
Saves the cmd data as a json file
#### loadcmd
Loads the cmd data from the json file
#### cote
Like VIM editor and NANO editor, I created a text editor COTE (Command Only Text Editor).
It is not as powerful as vim and nano but can be used inside my cmd to edit text.
## cote commands:
q = Quit  
a = Append  
e = Edit  
r = Read  
c = Change  
del = Delete  
s = Save
### q
Quit the cote.
### a
Append the multiline text entered by the user.
Executing 'a' will start listening the user inputs.
To exit append mode '?qa' is used.
### e
Edit whole text.
### r
Print the text of the file with line numbers. Line numbers starts from 0.
### c
Edit the particular line. It requires a line number as parameter.
Can be used as 'c 5' to edit line number 6 (as line number starts from 0).
### del
Delete the range of lines.
###### Syntax
del [start-end] 
This will delete the lines from index number start to end (both inclusive).
### s
This will save all of the changes. To check wheather the file is saved or not see the color of the last arrow of '>>>' which is present in every line of COTE like the arrows of python interactive mode. If its color is red the changes are not saved and if it is white then all changes are saved  in the file.
