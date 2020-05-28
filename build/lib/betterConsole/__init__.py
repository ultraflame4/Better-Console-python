'''
# Better Console Created By ultraflame4
'''

import PySimpleGUIQt as psg
import time
import traceback
import inspect
import json

v = "0.0.3"
github=" https://github.com/ultraflame4/Better-Console-python"

psg.LOOK_AND_FEEL_TABLE['BtrConsole'] = {'BACKGROUND': '#fafafa',
                                        'TEXT': '#000000',
                                        'INPUT': '#e3e3e3',
                                        'TEXT_INPUT': '#000000',
                                        'SCROLL': '#c7e78b',
                                        'BUTTON': ('black', '#dedede'),
                                        'PROGRESS': ('#01826B', '#D0D0D0'),
                                        'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
                                        }


class BetterConsoleError(Exception):
    pass

class inputHistoryHandler:
    def __init__(self,win):
        self.win=win
        self.history=[]
        self.c=0
    def add(self,string:str):
        self.history.append(string)
        self.history=list(dict.fromkeys(self.history))
    def inputsController(self,events,inp):
        t=0
        if events == 'special 16777235':
            self.c+=1
            t=1
        elif events == 'special 16777237':
            self.c-=1
            t=1

        if t==1:
            t=0
            try:
                self.win['-In-'].Update(self.history[self.c])
            except IndexError:
                if self.c <0:
                    self.c=len(self.history)-1
                else:
                    self.c=0-len(self.history)

class toggleButton:
    def __init__(self):
        # 0-> normal 1-> pressed -1-> disabled
        self.state=0
        self.colors={-1:"#f5f5f5",0:"#dedede",1:"#ebebeb"}
        self.log=''

    def update(self,button):
        button.Update(button_color=('black', self.colors[self.state]))

    def loop(self,events,button):
        if events == button.ButtonText and self.state>-1:
            if self.state!=1:
                self.state=1
                self.update(button)
            else:
                self.state=0
                self.update(button)
        if self.state==-1:
            self.update(button)
            button.disabled=True


class FilterButtonsController:
    def __init__(self):
        self.Norm=toggleButton()
        self.Debug=toggleButton()
        self.Info=toggleButton()
        self.Warn=toggleButton()
        self.Err=toggleButton()
        self.Crict=toggleButton()

    def loop(self,events,win,updatec):
        self.Norm.loop(events,win["Normal"])
        self.Debug.loop(events,win["Debug"])
        self.Info.loop(events,win["Info"])
        self.Warn.loop(events,win["Warning"])
        self.Err.loop(events,win["Error"])
        self.Crict.loop(events,win["Critical"])

    def _start(self,win):
        self.Norm.update(win["Normal"])
        self.Debug.update(win["Debug"])
        self.Info.update(win["Info"])
        self.Warn.update(win["Warning"])
        self.Err.update(win["Error"])
        self.Crict.update(win["Critical"])



class defaultCommands:
    def ping(self):
        return "pong"
    def _return(self,*args):
        return ' '.join(args)


class CommandsHandler:
    def __init__(self):
        self.defaults=defaultCommands()
        self.commandDict={"ping":self.defaults.ping,"return":self.defaults._return}

    def addCommands(self,commands:dict):
        """eg1.{"command name":Function_to_run}
            eg2. {"command name":Function_to_run,"command2 name":Function_2_to_run}"""

        self.commandDict={**self.commandDict,**commands}

    def execute(self,command,*args,**kwargs):
        try:r=self.commandDict[command](*args,*kwargs)
        except KeyError: raise BetterConsoleError("That Command Does Not Exist")
        else:return r

    def raw_execute(self,input_string):
        paraList =input_string.split(' ')
        command = paraList[0];paraList.pop(0);paraList=[i for i in paraList if i]
        try:
            argString="".join(paraList)
            args = dict(e.split('=') for e in argString.split(', '))
        except ValueError:
            args=paraList
        else: args={}
        try:
            return self.execute(command,*args)
        except:
            var = traceback.format_exc()
            return var.replace('\n',' | ')

    def check(self,command):
        if command.split(' ')[0] in self.commandDict:
            return True
        else: return False



class BetterConsole:
    def __init__(self,ConsoleWinName="Default Name"):
        psg.theme("BtrConsole")
        print(f"Better Console by ultraflame42 [Version-{v}]\nGithub:{github}\n")
        layout=[
            [psg.Text("Filters:",size=(17,0.7)),psg.Button("Normal",size=(17,0.7)),psg.Button("Debug",size=(17,0.7)),psg.Button("Info",size=(17,0.7)),psg.Button("Warning",size=(17,0.7)),psg.Button("Error",size=(17,0.7)),psg.Button("Critical",size=(17,0.7))],
            [psg.Multiline(size=(130,40), key='-Out-')],
            [psg.Button(">>>",size=(4,1),bind_return_key=True),psg.Input(size=(125.6,1),do_not_clear=False,key="-In-")]
        ]
        self.win=psg.Window(f" {ConsoleWinName} - [Better Console <version: {v}> by ultraflame42 ]",layout,return_keyboard_events=True,)

        self.consoleOutputText=''
        self.GlobalLineCounter=0
        self.inputHistoryHandler = inputHistoryHandler(self.win)
        self.FilterButtonController=FilterButtonsController()
        self.commandHandler=CommandsHandler()

        print("Finished Initialization. Please wait... Better Console window will show up shortly...")
        self.win.read(timeout=10)
        self.FilterButtonController._start(self.win)

    def inputProcessor(self,input_string):
        self.win['-In-'].Update('')
        self.printc('>>> '+input_string)
        if self.commandHandler.check(input_string):
            r=self.commandHandler.raw_execute(input_string)
            self.printc('> '+str(r))
        pass
    def stringEncoder(self,string,mode=0):
        # Encodes and add data to the string and returns it
        # {'c':<mode *rfr to pt.1>,'l':<line>}][
        #pt.1 stores the type of string it is, eg, debug,warning,normal
        # modes:
        # o -> none normal string
        # 1 -debug 2-> info 3-> warning 4-> critical 5-> error
        #
        metadata={'c':mode,'l':self.GlobalLineCounter}
        self.GlobalLineCounter+=1
        return str(metadata)+']['+string

    def rmvMetaData(self,string):
        s=string.split('][')
        s.pop(0)
        return ''.join(s)

    def getMetaData(self,string):
        return json.loads(string.split('][')[0].replace("'",'"'))

    def toFilter(self,c):
        lvl=c
        if lvl==0:
            return bool(self.FilterButtonController.Norm.state)
        if lvl==1:
            return bool(self.FilterButtonController.Debug.state)
        if lvl==2:
            return bool(self.FilterButtonController.Info.state)
        if lvl==3:
            return bool(self.FilterButtonController.Warn.state)
        if lvl==4:
            return bool(self.FilterButtonController.Crict.state)
        if lvl==5:
            return bool(self.FilterButtonController.Err.state)

    def printc(self,string,mode=0):
        self.consoleOutputText=self.consoleOutputText+"\n"+self.stringEncoder(string.replace('\n'," | "),mode)
        self.updateConsole()
    def updateConsole(self):
        add=""
        # Filter and rmvMetaData
        for x in self.consoleOutputText.split('\n'):
            if x != '':
                data=self.getMetaData(x)

                new=self.rmvMetaData(x)
                if not self.toFilter(data['c']):
                    add=add+new+'\n'

        self.win['-Out-'].Update(add,autoscroll=True)
        self.win['-Out-'].print(' ')
        pass

    def print(self,msg,*args):
        nstring = f"{msg}" + ' '.join(args)
        nstring.replace("\n",' | ')
        self.printc(nstring,0)


    def debug(self,msg,*args):
        ins=inspect.stack()
        func=ins[1].function
        file=ins[1].filename
        lineno=ins[1].lineno
        nstring = f"[file: {file}, line{lineno}] {func} # DEBUG: {msg}" + ' '.join(args)
        nstring.replace("\n",' | ')
        self.printc(nstring,1)

    def info(self,msg,*args):
        ins=inspect.stack()
        func=ins[1].function
        file=ins[1].filename
        lineno=ins[1].lineno
        nstring = f"[file: {file}, line{lineno}] {func} # INFO: {msg}" + ' '.join(args)
        nstring.replace("\n",' | ')
        self.printc(nstring,2)

    def warn(self,msg,*args):
        ins=inspect.stack()
        func=ins[1].function
        file=ins[1].filename
        lineno=ins[1].lineno
        nstring = f"[file: {file}, line{lineno}] {func} # WARNING: {msg}" + ' '.join(args)
        nstring.replace("\n",' | ')
        self.printc(nstring,3)

    def crit(self,msg,*args):
        ins=inspect.stack()
        func=ins[1].function
        file=ins[1].filename
        lineno=ins[1].lineno
        nstring = f"[file: {file}, line{lineno}] {func} # CRITICAL: {msg}" + ' '.join(args)
        nstring.replace("\n",' | ')
        self.printc(nstring,4)

    def error(self,msg,*args):
        ins=inspect.stack()
        func=ins[1].function
        file=ins[1].filename
        lineno=ins[1].lineno
        nstring = f"[file: {file}, line{lineno}] {func} # ERROR: {msg}" + ' '.join(args)
        nstring.replace("\n",' | ')
        self.printc(nstring,5)

    def loop(self):
        '''Include this function in your main loop! Warning: Only recommended to execute once every loop'''
        event, values = self.win.read(timeout=10)
        if event in (None, 'Cancel'):
            exit()
        if event in (None,'>>>'):
            self.updateConsole()
            self.inputProcessor(values["-In-"])
            self.inputHistoryHandler.add(values['-In-'])

        self.inputHistoryHandler.inputsController(event,values['-In-'])
        self.FilterButtonController.loop(event,self.win,self.updateConsole)

        if  event not in (None,'__TIMEOUT__'):
            self.updateConsole()
            self.win["-In-"].SetFocus()
