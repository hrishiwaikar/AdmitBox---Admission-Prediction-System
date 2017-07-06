# -*- coding: utf-8 -*-
"""
Created on Fri Sep 02 23:49:16 2016

@author: Jack
"""

import csv
import pandas as pd


class AdmissionProfile():
    
    profile1=[]
    profile2=[]
    atorpoint=None
    profile3=[]
    profile4=[]
    profile1target=[]
    profile2target=[]
    profile3target=[]
    profile4target=[]
    colleges=[]
    extendedprofile1 = []
    extendedtarget1=[]
    originalp1=[]
    originaltarget1=[]

    
    def __init__(self,admitfile,rejectfile):
        print 'Preprocessing Admit file...'
        self.preprocessprofiles(admitfile,'admit')
        print 'Done'
        print 'Preprocessing Reject file...'
        self.preprocessprofiles(rejectfile,'reject')
        print 'Done'

        print 'Streamlining Data'
        self.streamline()
        print 'Done'

        self.originalp1=list(self.profile1)
        self.originaltarget1=list(self.profile1target)

        self.profile1=self.extendedprofile1
        self.profile1target=self.extendedtarget1
     
    
    
    def profiletype(self,type1,type2):
        dif=type1-type2
        if dif==0:
            if type1==1:
                return 1
            elif type1==2:
                return 4
        elif dif==-1:
            return 2
        elif dif==1:
            return 3
    
    def createcollegecsv(self):
        mydf=pd.DataFrame(self.colleges)
        mydf.to_csv('collegelist.csv',index=False,header=False)


    def streamline(self):

        extendedprofile=[]
        admitprofile = []
        rejectprofile = []

        # create admit and reject list

        for i, profile in enumerate(self.profile1):
            if self.profile1target[i] == 'admit':
                admitprofile.append(profile)
            else:
                rejectprofile.append(profile)

        self.streamline_admit(admitprofile)
        self.streamline_rejects(rejectprofile)
        '''
        for i,profile in enumerate(self.profile1):
            print str(i)+' '+str(profile)+' '+str(self.profile1target[i])
        '''



    def streamline_admit(self,admitprofile):
        extendedadmitprofile=[]
        extendedtargetprofile1=[]

        highestagg=0
        highestquant=0
        highestverb=0
        highestwork=0

        highestprofile=None

        averagequant=0
        averageverb=0
        averagegre = 0
        averageagg=0
        averagework=0

        totalquant=0
        otalverb=0
        totalgre=0
        totalwork=0
        totalagg=0
        totaltoefl=0
        #calculate averages




        #calculate average and highests

        for i,profile in enumerate(admitprofile):

            #print str(i) + ' ' + str(admitprofile[i]) + ' admit'

            #all about agg
            if admitprofile[i][4]>highestagg:
                highestagg=admitprofile[i][4]
                highestprofile=admitprofile[i]

            totalagg=totalagg+admitprofile[i][4]

            #all about gre
            if admitprofile[i][0]>highestquant:
                highestquant=admitprofile[i][0]

            if admitprofile[i][1]>highestverb:
                highestverb=admitprofile[i][1]

            totalquant=totalquant+admitprofile[i][0]
            totalverb=totalverb+admitprofile[i][1]
            #print 'highestquant '+str(highestquant)
            #print 'highestverb '+str(highestverb)
            totaltoefl=totaltoefl+admitprofile[i][3]
            totalwork=totalwork+admitprofile[i][5]

            #work
            if admitprofile[i][5]>highestwork:
                highestwork=admitprofile[i][5]

            #print 'highestwork '+str(highestwork)




        totalcount=float(len(admitprofile))
        averageagg=totalagg/totalcount
        #print averageagg

        averagequant=int(totalquant/totalcount)
        #print averagequant

        averageverb=int(totalverb/totalcount)
        #print averageverb

        averagegre=int(averagequant+averageverb)
        #print averagegre

        averagetoefl=int(totaltoefl/totalcount)
        #print averagetoefl

        averagework=int(totalwork/totalcount)
        #print averagework

        #add profiles

        self.extendedprofile1=list(self.profile1)
        self.extendedtarget1=list(self.profile1target)

        #FOr highest profile
        #Highest profile by agg: keep the agg same , improve other aspects and admit them
        #print 'Highest Profile'
        #print highestprofile
        addcount=int(0.7*totalcount)
        if addcount<10:
            addcount=15
        #improve gre scores and add 20%profiles profiles:
        upperprofiles=[]
        newquant = highestprofile[0]
        newverb=highestprofile[1]
        newwork=averagework
        betterpaper=highestprofile[6]
        betteragg=highestprofile[4]
        bettertoefl=highestprofile[3]
        #print 'New Profiles'
        for i in range(addcount):
            newp= []
            newquant = newquant + 1
            if newquant>170:
                newquant=165
            newp.append(newquant)

            newverb=newverb+1
            if newverb>170:
                newverb=160
            newp.append(newverb)

            newgre=newquant+newverb
            newp.append(newgre)


            newp.append(highestprofile[3])

            if betteragg<87:
                betteragg = betteragg + 2
            else:
                betteragg=averageagg+2


            newp.append(betteragg)


            if newwork<60:
                newwork=newwork+3
            newp.append(newwork)

            if betterpaper>3:
                betterpaper=2
            else:
                betterpaper=betterpaper+1

            newp.append(betterpaper)

            newp.append(1)

            #print newp
            self.extendedprofile1.append(newp)
            self.extendedtarget1.append('admit')

        #for i, profile in enumerate(self.extendedprofile1):
            #print str(i) + ' ' + str(profile) + ' ' + str(self.extendedtarget1[i])


    def streamline_rejects(self,rejectprofile):

            #print '\nReject Streamlining\n'

            lowestprofile=[]

            lowestagg=90
            lowestgre=340
            lowestquant=170
            lowestverb=170
            lowestwork=30

            averagequant = 0
            averageverb = 0
            averagegre = 0
            averageagg = 0
            averagework = 0


            totalquant=0
            totalverb=0
            totalgre=0
            totalwork=0
            totalagg=0
            totaltoefl=0
            #calculate averages



            for i,profile in enumerate(rejectprofile):

                #print str(i) + ' ' + str(rejectprofile[i]) + ' reject'
                # all about agg
                if rejectprofile[i][4] <lowestagg and rejectprofile[i][4]>45:
                    lowestagg = rejectprofile[i][4]
                    lowestprofile= rejectprofile[i]

                totalagg = totalagg + rejectprofile[i][4]



                # all about gre
                if rejectprofile[i][0] < lowestquant:
                    lowestquant = rejectprofile[i][0]

                if rejectprofile[i][1] < lowestverb:
                    lowestverb= rejectprofile[i][1]

                totalquant = totalquant + rejectprofile[i][0]
                totalverb = totalverb + rejectprofile[i][1]

                totaltoefl=totaltoefl+rejectprofile[i][3]

                totalwork=totalwork+rejectprofile[i][5]



            rejectlen=len(rejectprofile)
            #print 'lowestagg ' + str(lowestagg)

            #print 'lquant ' + str(lowestquant)
            #print 'lverb ' + str(lowestverb)
            lowestgre=lowestquant+lowestverb

            averagequant=int(totalquant/float(rejectlen))
            #print averagequant
            averageverb=int(totalverb/float(rejectlen))
            #print averageverb

            averagetoefl=int(totaltoefl/float(rejectlen))
            #print averagetoefl

            averagegre=averagequant+averageverb
            #print averagegre
            averagework=int(totalwork/float(rejectlen))
            averageagg=int(totalagg/float(rejectlen))
            #print averagework
            #print averageagg


            #print 'lgre'+str(lowestgre)
            #print lowestprofile

            #For lower profiles :
            #CREATE lower profiles below lowest and mark them rejected
            addcount=int(0.6*len(rejectprofile))

            if addcount<20:
                addcount=20

            newverb=lowestprofile[0]
            newquant=lowestprofile[1]
            newgre=lowestprofile[2]
            newtoefl=lowestprofile[3]
            newagg=lowestprofile[4]
            newwork=0
            newpaper=0
            newbranch=0


            for i in range(addcount):
                newp=[]

                if newquant > 140:
                    newquant = newquant - 3
                else:
                    newquant = averagequant

                newp.append(newquant)

                if newverb>138:
                    newverb=newverb-3
                else:
                    newverb=averageverb

                newp.append(newverb)


                newgre=newverb+newquant
                newp.append(newgre)

                if newtoefl > 78:
                    newtoefl = newtoefl - 5
                else:
                    newtoefl = averagetoefl
                newp.append(newtoefl)

                if newagg>48:
                    newagg=newagg-2
                else:
                    newagg=averageagg

                newp.append(newagg)

                if newwork>0:
                    newwork=newwork-2
                else:
                    newwork=averagework
                newp.append(newwork)
                #append paper =0
                newp.append(0)

                if newbranch==0:
                    newbranch=1
                else:
                    newbranch=0

                newp.append(newbranch)
                #print 'newp '+str(newp)

                self.extendedprofile1.append(newp)
                self.extendedtarget1.append('reject')












    def preprocessprofiles(self,filename,admissionstatus):


        with open(filename) as f:

            reader=csv.reader(f)
            header_row=next(reader)
            #print(header_row)
            
            incomplete=[]

               
            for no,row in enumerate(reader):
                
                #print row[11]

                if '(Spring 2017)' or '(Fall 2017)' or 'Fall(2016)' in row[11]:
                    #print str(no)+' '+row[11]

                    #extract GRE Scores
                    if 'Quant' in row[3]:
                        #print row[3]
                        quantlines=row[3].split('Quant: ')
                        quantline=quantlines[1]
                        quantscore=int(quantline[:3])
                        verballines=row[3].split('Verbal: ')
                        verballine=verballines[1]
                        verbalscore=int(verballine[:3])
                        total=quantscore+verbalscore
                        #print no,quantscore,verbalscore,total
                    else:
                        if no not in incomplete:
                           incomplete.append(no)


                    #extract TOEFL/IELTS Score
                    #print no,row[4]
                    if 'N.A.' in row[4]:
                        if no not in incomplete:
                            incomplete.append(no)
                    elif 'TOEFL' in row[4]:
                        toefllines=row[4].split('TOEFL\n')
                        toeflscore=int(toefllines[1])
                        #print 'TOEFL',no,toefllines
                        type2=1
                        languagetestscore=toeflscore
                    elif 'IELTS' in row[4]:
                        ieltslines=row[4].split('IELTS\n')
                        ieltsscore=float(ieltslines[1])
                        type2=2
                        languagetestscore=ieltsscore
                        #print 'IELTS',no,ieltsscore
                    else:
                        #print 'Something Else'
                        #print no,'toefl',row[4]
                        if no not in incomplete:
                            incomplete.append(no)

                    #print row[5]
                    #extract UG Score in percentage or CGPA
                    if '%' in row[5]:
                        percentageline=row[5].split('%')
                        scoreline=percentageline[0].split('\n')
                        ugpercentage=float(scoreline[1])
                        type1=1
                        academicscore=ugpercentage
                        #print no,ugpercentage
                    elif 'CGPA' in row[5]:
                        cgpaline=row[5].split('UG Score\n')
                        cgpa=float(cgpaline[1].split('CGPA')[0])
                        #print cgpa
                        type1=2
                        academicscore=cgpa
                    else :
                        #print '\nSomething Else'
                        #print no,'Academicscore',row[5]
                        if no not in incomplete:
                            incomplete.append(no)

                    #extract work experience in months
                    #print row[6]
                    if 'NA' in row[6]:
                        workexp=0
                    elif 'month' in row[6]:
                        workline=row[6].split('Work Exp.\n')
                        workexp=int(workline[1].split(' month')[0])
                    #print no,workexp
                    else:
                        #print '\nSomething elseee'
                        #print no,'workexp',row[6]
                        if no not in incomplete:
                            incomplete.append(no)
                            #print 'appended '+str(no)


                    #extract info on paper published
                    #print row[7]
                    if 'None' in row[7]:
                        paperscore=0
                    elif 'National' in row[7]:
                        paperscore=2
                    elif 'International' in row[7]:
                        paperscore=3
                    elif 'Local' in row[7]:
                        paperscore=1
                    else:
                        paperscore=0

                    #extract OriginalBranch and College/University name
                    #print row[10]



                    if 'NA' in row[10]:
                        if no not in incomplete:
                            incomplete.append(no)
                    else:
                        #print no,row[10]
                        backgroundline=row[10].split(' from ')
                        if len(backgroundline)>1:
                            branch=backgroundline[0].split('Undergrad:\n\n')[1]

                            institute=backgroundline[1]

                            if 'Computer' in branch:
                                branchscore=1
                            else :
                                branchscore=0

                            if institute not in self.colleges:
                                self.colleges.append(institute)

                            #print no,backgroundline[1]

                    #profile type:
                    # 11=> % toefl profile 1
                    # 12=> % ielts profile 2
                    # 21=3> cgpa toefl profile 3
                    # 22=> cgpa ielts profile 4

                    #profile =['quantscore','verbalscore','totalscore','toefl/ielts','percentage/cgpa',
                    # 'workexp','paperscore','originalbranch','university','admissionstatus']

                    if no not in incomplete:
                         profile=[]
                         #profile.extend([quantscore,verbalscore,total,languagetestscore,academicscore,
                         #                  workexp,paperscore,branchscore,institute])
                         profile.extend([quantscore,verbalscore,total,languagetestscore,academicscore,
                                           workexp,paperscore,branchscore])
                         #print profile

                         ptype=self.profiletype(type1,type2)
                         if ptype==1:
                            #profile1=[]
                            self.profile1.append(profile)
                            self.profile1target.append(admissionstatus)
                         elif ptype==2:
                            self.profile2.append(profile)
                            self.profile2target.append(admissionstatus)
                         elif ptype==3:
                            self.profile3.append(profile)
                            self.profile3target.append(admissionstatus)
                         elif ptype==4:
                            self.profile4.append(profile)
                            self.profile4target.append(admissionstatus)





#for a,college in enumerate(colleges):
    #print '\n'+str(a)+" "+college






 ### San Jose

'''
print 'Columbia'
print
m=AdmissionProfile('10A.csv','10R.csv')
#print m.profile1
#print m.profile1target


for i,k in enumerate(m.profile1):
    print str(i)+' '+ str(m.profile1[i])+' '+str(m.profile1target[i])

print
print
for i,k in enumerate(m.originalp1):
    print str(i)+ ' '+ str(m.originalp1[i])+' '+str(m.originaltarget1[i])

'''