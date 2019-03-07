#!/usr/bin/env python
import sys
if len(sys.argv)<2:
    print ("Specify endorser file on command line.")
    sys.exit(1)

fname=sys.argv[1]

first_authors=sys.argv[2:]

def processline(line):
    sname,name,inst=line.split("||")
    sname=sname.split()[-1].upper() ## de la Macorra and such, upper for people who didn't capitalize
    name=name.replace('"','')
    inst=inst.replace("\n","")
    inst=inst.replace(",", " ")
    inst=inst.replace("'", " ")
    #print ("X",inst,inst.split("\\"),"Y")
    insts=["\\"+x.replace(" ","") for x in inst.split("\\")[1:]] ## this is robust against spaces, commas other bullshit
    return (sname.split()[-1],name,insts)

entries=[]
fentries={}
for entry in map(processline, open(fname).readlines()):
    if entry[0] in first_authors:
        fentries[entry[0]]=entry
    else:
        entries.append(entry)
        
entries.sort() 
# the others migth be in wrong order
fentries=[fentries[n] for n in first_authors]


instdir={}
icount=0
instlist=""
lastline=""
for sname,lname,insts in fentries+entries:
    line=lname.strip()+"$^{"
    for i,inst in enumerate(insts):
        if i>0:
            line+=","
        if inst not in instdir:
            icount+=1
            instdir[inst]=icount
            instlist+="$^{%i}$ %s \\\\\n"%(icount,inst)
        line+=str(instdir[inst])
    line+="}$, "
    if lastline!=line: ## fix repeated entries.
        print (line)
    lastline=line

print ("\n\n%%% \n\n",instlist)





