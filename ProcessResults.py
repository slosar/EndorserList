#!/usr/bin/env python

import sys, csv

if len(sys.argv)!=2:
    print ("Specify csv file on command line.")
    sys.exit(1)

fname=sys.argv[1]

fields={}
outputs={}
spamlist=open('results/spamlist.txt','w')
bibtex=open('results/bibtex.bib','w')
comments=open('results/comments.txt','w')

with open(fname) as csvfile:
    spamreader = csv.reader(csvfile)
    for i,row in enumerate(spamreader):
        if i==0:
            for j,name in enumerate(row):
                fields[name.split()[0]]=j
            continue
        endorsing=row[fields['Which']]
        elist=[]
        for word in endorsing.split():
            if "@" in word and 'anze' not in word:
                elist.append(word.replace(',',''))
            elif "Features" in word:
                elist.append('FEAT')
            elif "Modified" in word:
                elist.append('DE')
        for pap in elist:
            if pap not in outputs:
                outputs[pap]=open('results/endorser_'+pap,'w')
            outputs[pap].write (row[fields['Surname']]+" || " + row[fields['Latex']]+" || "+row[fields['LaTeX']]+"\n")
        if 'OK' in row[fields['Decadal']]:
            spamlist.write(row[fields['Name']]+" " +row[fields['Surname']]+" <"+row[fields['Email']]+'>,\n')
        if len(row[fields['Citation']])>1:
            bibtex.write("\n\n%% %s %s %s \n"%(row[fields['Name']],row[fields['Surname']],row[fields['Email']]))
            for line in row[fields['Citation']].split('\n'):
                if (("@article" in line) or
                    ("@ARTICLE" in line) or
                    ("=" in line) or
                    ('\",' in line) or
                    ("}" in line)):
                    bibtex.write(line+"\n")
                else:
                    bibtex.write("%% "+line+"\n")
        if len(row[fields['Anything']])>1:
            comments.write("\n\n From: %s %s %s \n"%(row[fields['Name']],row[fields['Surname']],row[fields['Email']]))
            comments.write(row[fields['Anything']]+"\n")



for name, f in outputs.items():
    f.close()
spamlist.close()
bibtex.close()
comments.close()


    
