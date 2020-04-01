from datetime import datetime
import sqlite3
import sys,time

con=sqlite3.Connection('chatBot_Database')
cur=con.cursor()
cur.execute("create table if not exists contacts(phNo varchar2(15) primary key, name varchar2(25) not null)")
cur.execute("create table if not exists alarms(dateTime varchar2(20) primary key)")
cur.execute("create table if not exists notes(dateTime varchar2(25) not null,txt varchar2(150))")

def Print(s):
    for letter in s:
        sys.stdout.write(letter)
        time.sleep(.04)

def myMain(key):

    def ExecHi():
        Print("Hi! How can i help you.")
        print
        pass
    
    def ExecDate():
        Print("today date : "+datetime.today().strftime('%d-%m-%Y'))
        print
        pass
    
    def ExecTime():
        Print("current time : "+datetime.today().strftime('%H:%M'))
        print
        pass
    
    def ExecDateTime():
        Print("current date and time : "+datetime.today().strftime('%d-%m-%Y %H:%M'))
        print
        pass

    def ExecSaveContact():
        Print("Enter name : ")
        input_name=raw_input()
        Print("Enter number : ")
        input_number=raw_input()
        if(len(input_name)!=0 and len(input_number)!=0):
            try:
                cur.execute("insert into contacts values(?,?)",(input_number,input_name))
                con.commit()
                Print("Contact Added")
                print
            except:
                Print("Already exists")
                print
        else:
            Print("Invalid contact")
            print
        pass

    def ExecShowContact():
        cur.execute("select * from contacts")
        temp=cur.fetchall()
        if(len(temp)!=0):
            print("Phone          Name")
            for i in temp:
                for j in i:
                    print(j+"    "),
                print
        else:
            Print("----Empty----")
            print
        pass

    def ExecSetAlarm():
        Print("Enter date(dd-mm-yyyy) : ")
        input_date=raw_input()
        Print("Enter time(hh:mm) : ")
        input_time=raw_input()
        temp1=input_date.split('-')
        temp2=input_time.split(':')
        if(len(input_date)!=0 and len(input_time)!=0 and len(temp1)==3 and len(temp2)==2):
            try:
                cur.execute("insert into alarms values(?)",(input_time+"      "+input_date,))
                con.commit()
                Print("Alarm set successfully")
                print
            except:
                Print("Alarm already exists")
                print
        else:
            Print("Something invalid")
            print
        pass

    def ExecShowAlarm():
        cur.execute("select * from alarms")
        temp=cur.fetchall()
        if(len(temp)!=0):
            print("Time       Date")
            for i in temp:
                for j in i:
                    print(j)
                print
        else:
            Print("----empty----")
            print
        pass

    def ExecMakeNotes():
        Print("Enter text : ")
        input_txt=raw_input()
        if(len(input_txt)!=0):
            cur.execute("insert into notes values(?,?)",(datetime.today().strftime('%d-%m-%Y  %H:%M')+" : ",input_txt))
            con.commit()
            Print("Note added")
            print
        else:
            Print("Invalid text")
            print
        pass

    def ExecShowNotes():
        cur.execute("select * from notes")
        temp=cur.fetchall()
        if(len(temp)!=0):
            for i in temp:
                for j in i:
                    print(j+"  "),
                print
                print
        else:
            Print("----empty----")
            print
        pass

    def ExecCall():
        Print("enter contact name : ")
        input_name=raw_input()
        if(len(input_name)!=0):
            cur.execute("select phNo from contacts where name = (?)",(input_name,))
            temp=cur.fetchall()
            if(len(temp)!=0):
                Print("calling to "+temp[0][0]+" ...")
                print
            else:
                Print("contact not found")
                print
        else:
            Print("invalid name")
            print
        pass
    
    def ExecExit():
        sys.exit(0)
        pass
    
    locals()['Exec' + key]()

class Object:
    def __repr__(self):
        return '<%s>' % getattr(self, '__name__', self.__class__.__name__)
    def is_alive(self):
        return hasattr(self, 'alive') and self.alive
    def display(self, canvas, x, y, width, height):
        pass

class Agent(object):
    def __init__(self):
        def program(percept):
            return input('Percept=%s; action? ' % percept)
        self.program = program
        self.alive = True


class TableDrivenAgent(Agent):

    
    def __init__(self, table):
        
        Agent.__init__(self)
        percepts = []

        def program(percept):
            
            percepts.append(percept)

            action = table.get(tuple(percepts))

            return action

        self.program = program

class ReflexVacuumAgent(Agent):
    def __init__(self):
        Agent.__init__(self)
        def program(status):
            if (status== 'hi' or status=='hello' or status=='hii'): return myMain('Hi')
            elif  (status== 'date' or status=='show date' or status=='what is current date' or status=='show current date'): return myMain('Date')
            elif (status == 'time' or status=='show time' or status=='show current time' or status=='what is time'): return myMain('Time')
            elif (status=='date time' or status=='show date with time' or status=='show date and time'):  return myMain('DateTime')
            elif (status=='save contact' or status=='add contact'): return myMain('SaveContact')
            elif(status=='contact' or status=='show contact'): return myMain('ShowContact')
            elif(status=='set alarm' or status=='new alarm' or status=='save alarm' or status=='add alarm'): return myMain('SetAlarm')
            elif (status == 'alarm' or status=='show alarm'): return myMain('ShowAlarm')
            elif (status == 'make note' or status=='create note'): return myMain('make note')
            elif (status == 'note'  or status=='show note'): return myMain('ShowNotes')
            elif (status == 'call' or status=='make a call'): return myMain('Call')
            
        self.program = program



def TableDrivenVacuumAgent():
    table = {
            "exit":"Exit",
            "hi":"Hi",
            "hello":"Hi",
            "date time":"DateTime",
            "date":"Date",
            "time":"Time",
            "save contact":"SaveContact",
            "add contact":"SaveContact",
            "contact":"ShowContact",
            "set alarm":"SetAlarm",
            "new alarm":"SetAlarm",
            "save alarm":"SetAlarm",
            "add alarm":"setAlarm",
            "alarm":"ShowAlarm",
            "make note":"make notemake notemake note",
            "note":"ShowNotes",
            "call":"Call",
            }



    return TableDrivenAgent(table)



class Environment:
    def __init__(self,):
        self.objects = []; self.agents = []
    object_classes = []
    def percept(self, agent):
        query = str(raw_input('You:'))
        return self.execute_action(agent,query)
    def execute_action(self, agent, query):
        return agent.program(query)




if __name__ == "__main__":
    while(1):
        env = Environment()
        rvAgent = ReflexVacuumAgent()
        env.percept(rvAgent)
