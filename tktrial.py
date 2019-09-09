import mysql.connector as sql
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from tkinter import *
import plotly as py
from datetime import datetime
import tkinter.filedialog
from tkinter.ttk import *
import os
import time
import pandas as pd
def start():
    cnxn=sql.connect(user='root',password='')
    cursor=cnxn.cursor(buffered=True)
    cursor.execute('create database stats')
    cursor.execute('use stats')
    cursor.execute('create table files(file varchar(30),user varchar(30),constraint file_pk primary key(file))')
    cursor.execute("create table users(user varchar(30),name varchar(60),year varchar(1) check(year>'0' and year<'5'),constraint user_pk primary key(user))")
    cursor.execute("create table entries(file varchar(30),date date,t0 time,t100 time)")
    cursor.execute('create table greens(gid integer,cno integer,bc float)')
    cursor.execute('alter table files add constraint file_user_fk foreign key(user) references users(user)')
    cursor.execute('create table buildings(bname varchar(30),bid integer,cno integer,bc float)')
    cursor.execute('create table buildings1(bname varchar(30),bid integer,cno integer,bc float,updown integer)')
    campus=[12.83788,80.15521,12.84363,80.14977,12.8458,80.15305,12.84412,80.15905]
    for i in range(len(campus)):
        cursor.execute("insert into buildings values('campus',100,"+str(i+1)+","+str(campus[i])+")")
    cnxn.commit()
    cnxn.close()
    move6()
def total_time_spent():
    enterdb()
    exit1()
    cursor.execute('select bid,bname from buildings group by bid')
    bname=dict(cursor.fetchall())
    for i in bname.keys():
        Label(root,text=str(i)+":"+str(bname[i])).grid()
    Label(root,text='enter building id:').grid()
    global ebid
    ebid=Entry()
    ebid.grid()
    Label(root,text='enter year').grid()
    global eyear
    eyear=Entry()
    eyear.grid()
    Button(root,text='Submit',command=leave).grid()
def leave():
    bid=ebid.get()
    year=eyear.get()
    cursor.execute('select sum(t'+bid+") from entries natural join files where user in (select user from users where year='"+year+"')")
    k=str(cursor.fetchall())
    #cursor.execute("select*from  where year='"+year+"'")
    if k!='[(None,)]':
        k=int((k)[11:-5:])
        #k=k/len(a)
        k=((k%100)%60)+(100*(((k%100)//60)+((k%10000)//100)%60))+(10000*((k//10000)+((k%10000)//100)//60))
        #k=(str(k))[:-4:]+':'+(str(k))[-4:-2:]+':'+(str(k))[-2::]
    else:
        k=0
    Label(root,text=(str(k)+" hhmmss")).grid()
    Button(root,text="OK",command=move6).grid()
def userno1():
    userno=euserno.get()
    exit1()
    a=dbs()
    cursor.execute('use '+a[int(userno)])
    cursor.execute('show tables')
    b=cursor.fetchall()
    global dates
    dates={}
    for i in range (len(b)):
        b[i]=str(b[i])[2:-3:]
        dates[str(i)]=b[i]
        lab=Label(root,text=(i,':',b[i]))
        lab.grid()
    l1=Label(root,text="Select date")
    l1.grid()
    global edate
    edate=Entry()
    edate.grid()
    Label(root,text="Initial time (hhmmss)").grid()
    global eti1
    eti1=Entry(root)
    eti1.grid(column=0,row=i+4)
    Label(root,text="Final time (hhmmss)").grid(row=i+5)
    global etf1
    etf1=Entry(root)
    etf1.grid(row=i+6,column=0)
    Button(root,text="Submit",command=process).grid()
def process():
    date=edate.get()
    ti=str(eti1.get())
    tf=str(etf1.get())
    exit1()
    cursor.execute('select location_id,sum(wait) from '+dates[date]+" where time>'"+ti+"' and time <'"+tf+"' and wait>0 group by location_id")
    k=(cursor.fetchall())
    ###print(k)
    cursor.execute('use stats')
    cursor.execute('select bid,bname from buildings group by bid')
    bname=dict(cursor.fetchall())
    print(bname)
    Label(root,text=len(k)).grid()
    for i in range(len(k)):
        k[i]=list(k[i])
        k[i][1]=str(k[i][1])
        Label(root,text=(bname[(k[i][0])]+' : '+str(float(k[i][1])/60)+" minutes")).grid()
    Button(root,text='OK',command=move6).grid()
def login():
    ##print(e1.get(),e2.get())
    enterdb1(e1.get(),e2.get())
    a=dbs()
    exit1()
    for i in range(len(a)):
        Label(root,text=(i,':',a[i])).grid()
    global euserno
    euserno=Entry()
    Label(root,text="Select user").grid()
    euserno.grid()
    Button(root,text="Submit",command=userno1).grid()
    
def time_at_location_user():
    exit1()
    Label(root,text="Enter Admin Username:").grid()
    global e1
    e1=Entry(root)
    e1.grid()
    Label(root,text="Enter Password:").grid()
    global e2
    e2=Entry(root)
    e2.grid()
    Button(root,text="Submit",command=login).grid()
def heatmap():    
    root.destroy()
    enterdb()
    cursor.execute('use stats')
    cursor.execute('select bid from buildings group by bid')
    bid=cursor.fetchall()
    cursor.execute('select bname from buildings group by bid')
    bname=cursor.fetchall()
    a=dbs()
    for n in a:
        cursor.execute('use '+n)
        cursor.execute('show tables')
        b=cursor.fetchall()
        dates={}
        ##print(b)
        for m in range (len(b)):
            b[m]=str(b[m])[2:-3:]
            cursor.execute("select hour(time) from "+b[m]+" group by hour(time)")
            a=cursor.fetchall()
            ###print(a)
            data=[]
            hour=0
            #cursor.execute('select bid from buildings')
            #bid=cursor.fetchall()
            #bname=['b block','cblock','ab2','ab1','a block','vmart','admin','pathway','unmarked']
            for i in range(len(a)):
                a[i]=int(str(a[i])[1:-2:])
                hour=a[i]
                data.append([])
                for j in range(len(bid)):
        #                ##print(j,len(data),data)
                    print(bid[j])
                    print("select sum(time) from "+b[m]+" where location_id="+str(bid[j])[2:-3:]+" and time>='"+str(hour)+":00:00' and time <'"+str(hour+1)+":00:00'")
                    cursor.execute("select sum(time) from "+b[m]+" where location_id='"+str(bid[j])[1:-2:]+"' and time>='"+str(hour)+":00:00' and time <'"+str(hour+1)+":00:00'")
                    k=str(cursor.fetchone())                            
                    print(k)
                    if k!='(None,)':
                        k=int((k)[10:-4:])
                        k=((k%100)%60)+(100*(((k%100)//60)+((k%10000)//100)%60))+(10000*((k//10000)+((k%10000)//100)//60))
                    else:
                        k=0
                    data[i].append(k)
            ###print(data)
            #for i in a:
             #   dic[str(i)[1:-2:]]+=1
          #  ##print(str(i)[1:-2:],dic[str(i)[1:-2:]])
            ax=( sns.heatmap(data,yticklabels=a,xticklabels=bname))
            sns.color_palette("Blues")
            ###print(len(ax),i)
            ax.set_title(n+"_"+b[m])
            plt.show()
    create()
    move6()
def initiat():
    root.geometry=("500x500")
    root.resizeable=(0,0)
    root.title("Welcome to Been There")
    root.lift()
    Label(root,text="Choose the function you wish to use").grid(row=1,column=1)
    cnxn=sql.connect(user='root',password='')
    cursor=cnxn.cursor(buffered=True)
    cursor.execute('show databases')
    a=list(cursor.fetchall())
    ###print(a)
    b=0
    for i in a:
        i=str(i)
        q='stats'
        ###print(i[2:-3],q)
        if i[2:-3]==q:
            Label(root,text="Database has been initiated already.Please make sure that campus co-ordinates are properly introduced in code.").grid(row=2,column=1)
            b=1
    if b!=1:
        Button(root,text='Start',command=start).grid(row=1,column=15)
    else:
        Button(root,text="New File",command=run).grid(row=2+b,column=1)
        Button(root, text="HeatMap",command=heatmap).grid(row=3+b,column=1)
        Button(root,text="Locate user",command=time_at_location_user).grid(row=4+b,column=1)
        Button(root,text="Time spent at a place",command=total_time_spent).grid(row=5+b,column=1)
        Button(root,text='Add Building',command=login2).grid(row=6+b,column=1)
        Button(root,text="Add green area",command=login4).grid(row=7+b,column=1)
        Button(root,text="Most happening Places",command=mosthap).grid(row=8+b,column=1)
        Button(root,text="Average Outing",command=avgout).grid(row=9+b,column=1)
        Button(root,text="Track User",command=track).grid(row=10+b,column=1)
        Button(root,text="Crowd Analysis",command=crowd).grid(row=11+b,column=1)
        Button(root,text="Weekend Outing stats",command=weekend).grid(row=12+b,column=1)
    root.mainloop()
def area(x1, y1, x2, y2, x3, y3):
    return abs(((x1 * (y2 - y3))+ (x2 * (y3 - y1)) + (x3 * (y1 - y2))) / 2.0) 
def check( j,x1, y1, x2, y2, x3,y3,x, y):  
    A = area(x1, y1, x2, y2, x3, y3)
    A1= area(x, y, x1, y1, x2, y2) 
    A2 = area(x, y, x2, y2, x3, y3) 
    A3 = area(x, y, x3, y3, x1,y1)
    #print(A1,A2,A3,A)
    if((abs(A1 + A2 + A3 -A))<0.0000001):
        return(j)
    else:
        return(0)
def area1(c,x,y):
    #print("1"+str(c))
    a=0
    for i in range(len(c)):
        c[i]=int(c[i])
    for i in range(3,len(c)-4,2):
        a=check(1,c[1],c[2],c[i],c[i+1],c[i+2],c[i+3],x,y)
        if a==1:
            return(c[0])
            break
    return(a)
def area2(c,ud,x,y):
    x=0
    for i in range(1,len(c)-2,2):
        print(c,x,y,ud[str(c[0])])
        if ud[str(c[0])][i]==((x-c[i])(y-c[i+1])-(c[i]-c[i+2])(c[i+1]-c[i+3]))*((0-c[i])(0-c[i+1])-(c[i]-c[i+2])(c[i+1]-c[i+3])):
            print('hi')
            x+=1
    if x==len(ud[str(c[0])]):
        return(c[0])
    return(0)
def fileread():
    #root.withdraw() #use to hide tkinter window
    currdir = os.getcwd()
    global file
    file = tkinter.filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a file')
    ###print(file)
    file=(file.split('/'))[len(file.split('/'))-1]
    dataset=pd.read_csv(file)
    root.lift()
    global data
    data=dataset.iloc[1:,0:3].values
    cursor.execute('use stats')
    cursor.execute('select user from users')
    a=cursor.fetchall()
    b=0
    for i in a:
        k=((str(i))[2:-3:])
        if file[:8:] ==k:
            cursor.execute("insert into files values('"+file+"','"+file[:8:]+"')")
            b=1
            break
    exit1()
        
    if b==1:
        cursor.execute('create database if not exists '+file[:8:]+'')
        addtodb()
        addstats()
        bargraph()
        cnxn.commit()
        cnxn.close()
        move6()

    if b!=1:
        ##print("h1")
        root.title("hi")
        l1=Label(root,text='enter name:')
        l1.grid()
        ##print("h1")
        global e1
        e1=Entry(root)
        e1.grid()
        l2=Label(root,text='Enter year:')
        l2.grid()
        global e2
        e2=Entry(root)
        e2.grid()
        b=Button(root,text="Submit",command=move)
        b.grid()
        ##print("h1")
def move():
    name=e1.get()
    year=e2.get()
    exit1()
        
    cursor.execute("insert into users values('"+file[:8:]+"','"+name+"','"+year+"')")
    cursor.execute("insert into files values('"+file+"','"+file[:8:]+"')")
    cursor.execute('create database if not exists '+file[:8:]+'')
    addtodb()
    addstats()
    bargraph()
    cnxn.commit()
    cnxn.close()
    move6()
def addtodb():
    #campus=[100,12.83788,80.15521,12.84363,80.14977,12.8458,80.15305,12.84412,80.15905]
    cursor.execute('use stats')
    #cordinate=pd.read_csv('vit_coordinates.csv')
    #cord=cordinate.iloc[0:,0:10].values
    cursor.execute('select bid,bname,bc from buildings order by bid desc')
    c=cursor.fetchall()
    cord=[]
    for i in c:
        #print(i)
        if [i[0]] in cord:
            q=0
        else:
            cord.append([i[0]])
    for i in range(len (cord)):
        for j in c:
            if j[0]==cord[i][0]:
                cord[i].append(float(j[2]))
    cursor.execute('select bid,bname,bc,updown from buildings1 order by bid desc')
    c1=cursor.fetchall()
    cord1=[]
    ud={}
    for i in c1:
        #print(i)
        if [i[0]] in cord:
            q=0
        else:
            cord1.append(str([i[0]]))
            ud[str(i[0])]=[]
    for i in range(len (cord)):
        for j in c1:
            if j[0]==cord[i][0]:
                cord1[i].append(float(j[2]))
                ud[str(j[0])].append(int(j[3]))
    ##print(cord[0])
    x=0
    global buildings
    buildings=["outside campus"]
    for j in range (len(c)):
        if str(c[j]) not in buildings:
            buildings.append(str(c[j]))
    for j in range (len(c1)):
        if str(c[j]) not in buildings:
            buildings.append(str(c[j]))
                     
    ##print("hi")
    exit1()
    root.title("progress")
    l=Label(root,text="Please wait, This may take a few minutes depending on the size of input file")
    l.grid()
    progress_var = DoubleVar()
    bar=Progressbar(root,variable=progress_var,maximum=len(data))
    bar.grid()
    c=0
    cursor.execute('use '+file[0:8:])
    for i in range(1,len(data)):
        if(str(data[i][0][0:4:]+data[i][0][5:7:]+data[i][0][8:10]) in totalwaitdates):
            x=0
        else:
            totalwaitdates.append(str(data[i][0][0:4:]+data[i][0][5:7:]+data[i][0][8:10]))
            totalwait[data[i][0][0:4:]+data[i][0][5:7:]+data[i][0][8:10]]={'0':s,'100':s}
            for j in range(len(cord)):
                totalwait[data[i][0][:4:]+data[i][0][5:7:]+data[i][0][8:10]][str(cord[j][0])]=s
        cursor.execute('CREATE TABLE if not exists d'+data[i][0][0:4:]+data[i][0][5:7:]+data[i][0][8:10]+' (time time,latitude real,longitude real,location_id int,wait time,constraint time_pk primary key(time))')
        s2=data[i][0][11:19:]
        s1=data[i-1][0][11:19:]
        FMT = '%H:%M:%S'
        wait = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
        data[i][1]=float(data[i][1])
        data[i][2]=float(data[i][2])
        if abs(data[i][1]-data[i-1][1])<0.0001 and abs(data[i][2]-data[i-1][2])<0.00001 and c<5 and x!=0 and x!=100:
            cursor.execute("insert into d"+data[i][0][0:4:]+data[i][0][5:7:]+data[i-1][0][8:10]+" values (%s,%s,%s,%s,%s)",((data[i][0][11::]),(data[i][1]),(data[i][2]),(x),(wait)))
            c+=1
            totalwait[data[i][0][0:4:]+data[i][0][5:7:]+data[i][0][8:10]][str(x)]+=wait
            continue
        x=0
        x=area1(cord[0],data[i][1],data[i][2])
        if x==100:
            for j in range(1,len(cord)):
                x=area1(cord[j],data[i][1],data[i][2])
                if x!=0:
                    break
            if x==0:
                for j in range(len(cord2)):
                    x=area2(cord1[j],ud[cord1[j][0]],data[i][1],data[i][2])
                    if x!=0:
                        break
            if x==0:
                cursor.execute("insert into d"+data[i][0][0:4:]+data[i][0][5:7:]+data[i-1][0][8:10]+" values (%s,%s,%s,%s,%s)",((data[i][0][11::]),(data[i][1]),(data[i][2]),(100),(wait)))
            else:
                cursor.execute("insert into d"+data[i][0][0:4:]+data[i][0][5:7:]+data[i-1][0][8:10]+" values (%s,%s,%s,%s,%s)",((data[i][0][11::]),(data[i][1]),(data[i][2]),(x),(wait)))
        else:
            cursor.execute("insert into d"+data[i][0][0:4:]+data[i][0][5:7:]+data[i-1][0][8:10]+" values (%s,%s,%s,%s,%s)",((data[i][0][11::]),(data[i][1]),(data[i][2]),(0),(wait)))
        totalwait[data[i][0][0:4:]+data[i][0][5:7:]+data[i][0][8:10]][str(x)]+=wait
        progress_var.set(i)
        time.sleep(0.02)
        root.update_idletasks()
        root.after(1,addtodb)    
def addstats(): 
    #print("HI")
    cursor.execute('use stats')
    cursor.execute('select bid from buildings')
    bids=cursor.fetchall()
    #a='create table entries (file varchar(30),date date'
    #for j in bids:
      #  a+=','
        #a+='t'
      #  a+=str(j)[2:-3:]
        #a+=' time'
        ###print(a)
    #a+=")"
    ###print(a)
   # cursor.execute(a)
    for i in totalwait.keys():
        a="insert into entries values('"
        a+=file
        a+="','"
        a+=i
        #print(i)
        for j in range (len(totalwait[i].keys())):
            #print(j)
            a+="','"
            a+=str(totalwait[i][list(totalwait[i].keys())[j]])[11::]
            ##print(a)
        a+="')"
        #print(a)
        cursor.execute(a)
    cnxn.commit()
    #for i in totalwait.keys():
      #      cursor.execute('insert into entries values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',((file),(i),(totalwait[i]['1']),(totalwait[i]['2']),(totalwait[i]['3']),(totalwait[i]['4']),(totalwait[i]['5']),(totalwait[i]['6']),(totalwait[i]['7']),(totalwait[i]['11']),(totalwait[i]['100']),(totalwait[i]['0'])))
def bargraph():
    root.destroy()
    cursor.execute('use stats')
    #print(totalwaitdates)
    for j in totalwaitdates:
        for i in totalwait[j].keys():
            cursor.execute("select t"+i+" from entries where date='"+j+"' and file='"+file+"'")
            k=cursor.fetchone()
            #print(k,i,j,file)
            if str(k)=="(datetime.timedelta(0),)":
                k=0
            else:
                k=int(str(k)[28:-3:])
                k=((k%100)%60)+(100*(((k%100)//60)+((k%10000)//100)%60))+(10000*((k//10000)+((k%10000)//100)//60))
            totalwait[j][i]=k
        #print(buildings)
        #print(totalwait[j].keys())
        plt.bar(totalwait[j].keys(),totalwait[j].values(),color=['red' ,'blue'],width=0.8)
        plt.show()
    create()
    move6()
def run():
    exit1()
        
    global totalwaitdates
    totalwaitdates=[]
    global totalwait
    totalwait={}
    global s
    s="00:00:00"
    s=datetime.strptime(s,'%H:%M:%S')
    enterdb()
    global data1
    fileread()

def enterbuilding():
    enterdb1(e1.get(),e2.get())
    n=int(e3.get())
    exit1()
    Label(root,text="Enter building name").grid()
    global ebname
    ebname=Entry(root)
    ebname.grid()
    global ebc
    ebc=[]
    print(var.get())
    if str(var.get())=='Convex':
        for i in range(0,(n*2)-1,2):
            Label(root,text="Enter Latitude and Longiude of corner "+str(i+1)+":").grid()
            ebc.append(Entry(root))
            ebc[i].grid(column=0,row=3+i)
            ebc.append(Entry(root))
            ebc[i+1].grid(column=1,row=3+i)
        global bs
        bs=Button(root,text="Submit",command=eb1)
        bs.grid()
        root.mainloop()
    else:
        global var1
        var1=[]
        Label(root,text='Select Up if origin and polygon are on the different sides of line else Down').grid()
        for i in range(0,(n*2)-1,2):
            Label(root,text="Enter Latitude and Longiude of corner "+str(i+1)+":").grid()
            ebc.append(Entry(root))
            ebc[i].grid(column=0,row=5+i)
            ebc.append(Entry(root))
            ebc[i+1].grid(column=1,row=5+i)
            var1.append(StringVar(root))
            var1[int(i/2)].set('up')
            d1=OptionMenu(root,var1[int(i/2)],'up','down')
            d1.grid(row=5+i,column=2)
        bs=Button(root,text="Submit",command=eb2)
        bs.grid()
        root.mainloop()
def eb1():
    bname=ebname.get()
    cursor.execute('select bid from buildings group by bid')
    bid=cursor.fetchall()
    if str(bid)=='None':
        bid=0
    else:
        bid=len(bid)
    cursor.execute('select bid from buildings1 group by bid')
    bid1=cursor.fetchall()
    if str(bid1)=='None':
        bid1=0
    else:
        bid1=len(bid1)
    bid=bid+bid1
    bc=[]
    cursor.execute('use stats')
    for i in range(0,len(ebc)):
        cursor.execute("insert into buildings values(%s,%s,%s,%s)",((bname),(str(bid)),(i+1),(ebc[i].get())))
    cursor.execute("alter table entries add column (t"+str(bid)+" time)")
    cnxn.commit()
    move6()
def eb2():
    bname=ebname.get()
    cursor.execute('select bid from buildings group by bid')
    bid=cursor.fetchall()
    if str(bid)=='None':
        bid=0
    else:
        bid=len(bid)
    cursor.execute('select bid from buildings1 group by bid')
    bid1=cursor.fetchall()
    if str(bid1)=='None':
        bid1=0
    else:
        bid1=len(bid1)
    bid=bid+bid1
    cursor.execute('use stats')
    for i in range(0,len(ebc)):
        print(ebc[i].get())
        if(var1[i].get()=='up'):
            cursor.execute("insert into buildings1 values(%s,%s,%s,%s)",((bname),(str(bid)),(i+1),(ebc[i].get()),(-1)))
        else:
            cursor.execute("insert into buildings1 values(%s,%s,%s,%s)",((bname),(str(bid)),(i+1),(ebc[i].get()),(1)))
    cursor.execute("alter table entries add column (t"+str(bid)+" time)")
    cnxn.commit()
    move6()
def login2():
    exit1()
    Label(root,text="Enter Admin Username:").grid()
    global e1
    e1=Entry(root)
    e1.grid()
    Label(root,text="Enter Password:").grid()
    global e2
    e2=Entry(root)
    e2.grid()
    Label(root,text='Enter convex or concave Buildings').grid()
    global var
    var=StringVar(root)
    var.set('convex')
    d=OptionMenu(root,var,'Convex','Concave')
    d.grid()
    Label(root,text='Enter Number of Co-ordinates').grid()
    global e3
    e3=Entry(root)
    e3.grid()
    b1=Button(root,text="Submit",command=enterbuilding)
    b1.grid()
def mosthap():
    enterdb()
    cursor.execute("select bid from buildings where bid<>100 group by bid")
    bid=cursor.fetchall()
    exit1()
    bid=list(bid)
    root.title("Most Happening Places")
    for k1 in range(4):
        cursor.execute("select bname from buildings where bid<>100 order by bid")
        bname=cursor.fetchall()
        a1=[]
        a3=[]
        Label(root,text=("For Year="+str(k1+1))).grid()
        for i in bid:
            cursor.execute("select (sum(t"+str(i)[1:-2:]+")) from entries natural join files natural join users where year="+str(k1+1))
            b=cursor.fetchall()
            b=str(b)
            ###print(i,b)
            ###print(b[1:12:])
            if str(b)!="[(None,)]":
                k=int(b[11:-5:])
                a1.append(k)
                k=((k%100)%60)+(100*(((k%100)//60)+((k%10000)//100)%60))+(10000*((k//10000)+((k%10000)//100)//60))
                ###print(k)
                if(k==0):
                    k='000000'
                #k=((k//3600)*10000)+(((k%3600)//60)*100)+(k%60)
                a3.append(str(k))
                ###print(b1,b2)
            #a2.append(str(i)[2:-3:])
            else:
                k=0
                a1.append(k)
                a3.append('000000')
        j=0
        while(a1!=[]):
            j+=1
            i=a1.index(max(a1))
            ###print(i,bname,str(bname[i])[2:-3:])
            Label(root,text=(str(j)+" : "+str(bname[i])[2:-3:]+" => "+a3[i][:2:]+":"+a3[i][2:4:]+":"+a3[i][4:6:])).grid()
            a1.pop(i)
            bname.pop(i)
            a3.pop(i)
    b=Button(root,text="Ok",command=move6)
    b.grid()
def avgout():
    enterdb()
    a1=[]
    a3=[]
    exit1()
    root.title("Average Outing Time")
    for i in range(4):
        cursor.execute("select sum(t0) from entries natural join files natural join users where year='"+str(i+1)+"'")
        b=cursor.fetchall()
        cursor.execute("select sum(coun) from (select count(distinct(date)) as coun from entries natural join files natural join users where year='"+str(i+1)+"' group by user) as t")
        a=cursor.fetchall()
        if str(a)!="[(None,)]":
            #print(a)
            a=int(str(a)[11:-5:])
            cursor.execute("select (sum(t0)) from entries natural join files natural join users where year="+str(i+1))
            b=cursor.fetchall()
            #print(b)###print(i,b)
                ###print(b[1:12:])
            ##print(str(b))
            if str(b)!="[(None,)]":
                b=str(b)[2:-3:]
                k=int(b[9:-2:])
                k=((k%100)%60)+(100*(((k%100)//60)+((k%10000)//100)%60))+(10000*((k//10000)+((k%10000)//100)//60))
                    ###print(k)
                    #k=((k//3600)*10000)+(((k%3600)//60)*100)+(k%60)
                    ###print(b1,b2)
                #a2.append(str(i)[2:-3:])
            else:
                k=0
                a1.append(k)
                a3.append('000000')
            Label(root,text=("Year :"+str(i+1)+"=> "+str(round(k/(a*60)))+" minutes")).grid()
        else:
            Label(root,text=("Year :"+str(i+1)+"=> 0 minutes")).grid()
    b=Button(root,text="Ok",command=move6)
    b.grid()
def track():
    exit1()
    Label(root,text="Enter Admin Username:").grid()
    global e1
    e1=Entry(root)
    e1.grid()
    Label(root,text="Enter Password:").grid()
    global e2
    e2=Entry(root)
    e2.grid()
    b1=Button(root,text="Submit",command=login3)
    b1.grid()
def login3():
    enterdb1(e1.get(),e2.get())
    exit1()
    a=dbs()
    for i in range (len(a)):
        Label(root,text=str(i)+" : "+a[i]).grid()
    global euserno
    euserno=Entry(root)
    Label(root,text="Select user").grid()
    euserno.grid()
    b3=Button(root,text="Submit",command=userno2)
    b3.grid()
def userno2():
    userno=int(euserno.get())
    a=dbs()
    cursor.execute('use '+a[userno])
    cursor.execute('show tables')
    b=cursor.fetchall()
    global dates
    dates={}
    exit1()
    for i in range (len(b)):
        b[i]=str(b[i])[2:-3:]
        dates[str(i)]=b[i]
        Label(root,text=(i,':',b[i])).grid()
    Label(root,text="Select date").grid()
    global edate
    edate=Entry(root)
    edate.grid()
    Label(root,text="Initial time (hhmmss)").grid()
    global eti1
    eti1=Entry(root)
    eti1.grid(column=0,row=i+4)
    Label(root,text="final time (hhmmss)").grid()
    global etf1
    etf1=Entry(root)
    etf1.grid(row=i+6,column=0)
    b1=Button(root,text="Submit",command=process2)
    b1.grid()
def process2():
    date=edate.get()
    ti=str(eti1.get())
    tf=str(etf1.get())
    root.destroy()
    cursor.execute('select latitude,longitude from '+dates[date]+" where time>'"+ti+"' and time <'"+tf+"' and wait>0 order by time")
    k=(cursor.fetchall())
    cursor.execute('use stats')
    cursor.execute('use stats')
    #cordinate=pd.read_csv('vit_coordinates.csv')
    #cord=cordinate.iloc[0:,0:10].values
    cursor.execute('select bid,bname,bc from buildings order by bid,cno')
    c=cursor.fetchall()
    cord=[]
    for i in c:
        #print(i)
        if [i[0]] in cord:
            q=0
        else:
            cord.append([i[0]])
    for i in range(len (cord)):
        for j in c:
            if j[0]==cord[i][0]:
                cord[i].append(float(j[2]))
    for i in range (len(cord)):
        bc=[[],[]]
        print(cord[i])
        if(cord[i][0]!=100):
            for j in range(1,len(cord[i]),2):
                bc[0].append(cord[i][j])
                bc[1].append(cord[i][j+1])
            bc[0].append(cord[i][1])
            bc[1].append(cord[i][2])
            print(bc)
            plt.fill(bc[1],bc[0],'r')
    cursor.execute('select bid,bname,bc from buildings1 order by bid,cno')
    c=cursor.fetchall()
    cord=[]
    for i in c:
        #print(i)
        if [i[0]] in cord:
            q=0
        else:
            cord.append([i[0]])
    for i in range(len (cord)):
        for j in c:
            if j[0]==cord[i][0]:
                cord[i].append(float(j[2]))
    for i in range (len(cord)):
        bc=[[],[]]
        print(cord[i])
        if(cord[i][0]!=100):
            for j in range(1,len(cord[i]),2):
                bc[0].append(cord[i][j])
                bc[1].append(cord[i][j+1])
            bc[0].append(cord[i][1])
            bc[1].append(cord[i][2])
            print(bc)
            plt.fill(bc[1],bc[0],'r')
    cursor.execute('select gid,cno,bc from greens order by gid,cno')
    c=cursor.fetchall()
    cord=[]
    for i in c:
        #print(i)
        if [i[0]] in cord:
            q=0
        else:
            cord.append([i[0]])
    for i in range(len (cord)):
        for j in c:
            if j[0]==cord[i][0]:
                cord[i].append(float(j[2]))
    for i in range (len(cord)):
        bc=[[],[]]
        print(cord[i])
        if(cord[i][0]!=100):
            for j in range(1,len(cord[i]),2):
                bc[0].append(cord[i][j])
                bc[1].append(cord[i][j+1])
            bc[0].append(cord[i][1])
            bc[1].append(cord[i][2])
            print(bc)
            plt.fill(bc[1],bc[0],'g')
#    cursor.execute('select bc1,bc2,bc3,bc4,bc5,bc6,bc7,bc8 from greens where bid<>100 order')
  #  bids=cursor.fetchall()
    #bids=list(bids)
#    bc=[[],[]]
  #  for i in range (len(bids)):
    #    bc[0].append([float(bids[i][0]),float(bids[i][2]),float(bids[i][4]),float(bids[i][6]),float(bids[i][0])])
      #  bc[1].append([float(bids[i][1]),float(bids[i][3]),float(bids[i][5]),float(bids[i][7]),float(bids[i][1])])
        #plt.fill(bc[1][i],bc[0][i],'g')
    ##print(k)
    a=[[],[]]
    #plt.plot(float(k[0][1]),float(k[0][0]),'b')
    for i in range(1,len(k)-1):
        a[0].append(float(k[i][0]))
        a[1].append(float(k[i][1]))
    ###print(k)
    ##print(a[0],a[1])
    plt.plot(a[1],a[0],)
    #plt.plot(float(k[len(k)-1][1]),float(k[len(k)-1][0]),'b')
    #plt.xlim([80.149,80.159])
    #plt.ylim([12.837,12.845])
    plt.show()
    create()
    initiat()
def crowd():
    enterdb()
    exit1()
    Label(root,text="Enter the date in YYYYMMDD format").grid()
    global edate
    edate=Entry(root)
    edate.grid()
    b=Button(root,text='Submit',command=move4)
    b.grid()
def move4():
    datetl=edate.get()
    a=dbs()
    cursor.execute('select bid from buildings group by bid order by bid ')
    ebid=cursor.fetchall()
    cursor.execute('select bname from buildings group by bid order by bid')
    ebname=cursor.fetchall()
    ebid=list(ebid)
    for i in range(len(ebid)):
        ebid[i]=str(ebid[i])
        ebname[i]=str(ebname[i])
    ebname=list(ebname)
    exit1()
    root.title("Crowd")
    for lid in ebid:
        k=lid
        lid=str(lid)[1:-2:]
        count=0
        for i in a:
             cursor.execute('use '+i)
             cursor.execute('show tables')
             b=cursor.fetchall()
             b=list(b)
             for j in b:
                 if str(j)=="('d"+datetl+"',)":
                     ##print(str(j)[2:-2])
                     w="select location_id from "+str(j)[2:-3:]+" where location_id="+lid
                     ##print(w)
                     cursor.execute(w)
                     lid1=cursor.fetchall()
                     if str(lid1)!="[]":
                         count+=1
        x=ebid.index(k)
        Label(root,text=("Building: "+ebname[x][2:-3:]+"\nStudents present: "+str(count))).grid()
    b=Button(root,text="Ok",command=move6)
    b.grid()
def weekend():
    enterdb()
    exit1()
    Label(root,text="Enter the date in YYYY-MM-DD format").grid()
    global edate
    edate=Entry(root)
    edate.grid()
    global b
    b=Button(root,text='Submit',command=move5)
    b.grid()
def move5():
    datetl=edate.get()
    exit1()
    x=0
    cursor.execute("select dayofweek('"+datetl+"')")
    datetl1=str(cursor.fetchall())
    #print(str(datetl1)[2:-3:])
    a=dbs()
    if str(datetl1)[2:-3:]=='1' or  str(datetl1)[2:-3:]=='7':
        for i in a:
             cursor.execute('use '+i)
             cursor.execute('show tables')
             b1=cursor.fetchall()
             b1=list(b1)
             for j in b1:
                 ##print(datetl)
                 ##print(j,"[('d"+datetl[0:4:]+datetl[5:7:]+datetl[8::]+"',)]")
                 if str(j)=="('d"+datetl[0:4:]+datetl[5:7:]+datetl[8::]+"',)":
                     ##print(str(j)[2:-2])
                     w="select location_id from "+str(j)[2:-3:]+" where location_id=0"
                     ##print(w)
                     cursor.execute(w)
                     lid1=cursor.fetchall()
                     if str(lid1)!="[]":
                         Label(root,text=("user "+i)).grid()
                         x=1
        if x!=0:
            Button(root,text="Ok",command=move6).grid()
        else:
            Label(root,text='No Outnigs on this day recorded').grid()
            Button(root,text='Retry',command=move7).grid()
            Button(root,text='exit',command=move6).grid()
    else:
        Label(root,text='Either Date format is wrong or given date is not a weekend').grid()
        Button(root,text='Retry',command=move7).grid()
        Button(root,text='exit',command=move6).grid()
def login4():
    exit1()
    Label(root,text="Enter Admin Username:").grid()
    global e1
    e1=Entry(root)
    e1.grid()
    Label(root,text="Enter Password:").grid()
    global e2
    e2=Entry(root)
    e2.grid()
    Label(root,text="enter the number of co-ordinates").grid()
    global e3
    e3=Entry(root)
    e3.grid()
    Button(root,text="Submit",command=addgreen).grid()

def addgreen():
    enterdb1(e1.get(),e2.get())
    cursor.execute('use stats')
    n=int(e3.get())
    exit1()
    global ebc
    ebc=[]
    for i in range(0,2*n,2):
        Label(root,text="Enter Latitude and Longiude of corner "+str((i/2)+1)+":").grid()
        ebc.append(Entry(root))
        ebc[i].grid(column=0,row=i+2)
        ebc.append(Entry(root))
        ebc[i+1].grid(column=1,row=i+2)
    global bs
    bs=Button(root,text="Submit",command=eb2)
    bs.grid()
    root.mainloop()
def eb2():
    bc=[]
    cursor.execute('select gid from greens group by gid')
    bid=cursor.fetchall()
    if str(bid)=='None':
        bid=0
    else:
        bid=len(bid)
    for i in range (len(ebc)):
        bc.append(ebc[i].get())
        cursor.execute("insert into greens values("+str(bid+1)+","+str(i+1)+","+bc[i]+")")
    ###print(bname,bid,bc1,bc2,bc3,bc4,bc5,bc6,bc7,bc8)
    cnxn.commit()
    #cursor.execute("insert into greens values(%s,%s,%s,%s,%s,%s,%s,%s)",((bc1),(bc2),(bc3),(bc4),(bc5),(bc6),(bc7),(bc8)))
    move6()    
def move6():
    exit1()
    initiat()
def move7():
    exit1()
    weekend()
def enterdb():
    global cnxn
    cnxn=sql.connect(user='root',password='',database='stats')
    global cursor
    cursor=cnxn.cursor(buffered=True)
def enterdb1(username,password):
    global cnxn
    cnxn=sql.connect(user=username,password=password,database='stats')
    global cursor
    cursor=cnxn.cursor(buffered=True)
def exit1():
    for i in root.grid_slaves():
        i.destroy()
def create():
    global root
    root=Tk()
    root.lift()
def dbs():
    cursor.execute('select user from users')
    a=cursor.fetchall()
    for i in range(len(a)):
        a[i]=str(a[i])[2:-3:]
    return(a)
create()
initiat()
root.mainloop()
