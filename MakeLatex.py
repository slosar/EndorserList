#!/usr/bin/env python
import sys
if len(sys.argv)!=2:
    print ("Specify endorser file on command line.")
    sys.exit(1)

fname=sys.argv[1]


def processline(line):
    sname,name,inst=line.split("||")
    sname=sname.replace(" ","")
    inst=inst.replace("\n","")
    inst=inst.replace(",", " ")
    #print ("X",inst,inst.split("\\"),"Y")
    insts=["\\"+x.replace(" ","") for x in inst.split("\\")[1:]] ## this is robust against spaces, commas other bullshit
    return (sname,name,insts)

entries=sorted(map(processline, open(fname).readlines()))

instdir={}
icount=0
instlist=""
for sname,lname,insts in entries:
    line=lname+"^{"
    for i,inst in enumerate(insts):
        if i>0:
            line+=","
        if inst not in instdir:
            icount+=1
            instdir[inst]=icount
            instlist+="$^%i$ %s \\\\\n"%(icount,inst)
        line+=str(instdir[inst])
    line+="}, "
    print (line)

print ("\n\n%%% \n\n",instlist)





