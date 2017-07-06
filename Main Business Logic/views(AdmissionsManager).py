
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.





import collections
from .machine.admissions_classifier import createClassifier
import pickle
import dill
import os
import time
import copy


universityNotDone={
    # not done yet - change this comment when they are done


    #86: 'George Washington University',

#01 : 'Carnegie Mellon University',
#02 : 'Massachusetts Institute of Technology',
#03 : 'Stanford University',
#04 : 'University of California- Berkeley',

#06 : 'Cornell University',
#07 : 'University of Washington',
#08 : 'Princeton University',
#09 : 'Georgia Institute of Technology',
#10 : 'University of Texas- Austin',
#11 : 'California Institute of Technology',

#14 : 'University of Michigan- Ann Arbor',
#15 : 'Columbia University',
16 : 'University of California- San Diego',
#17 : 'University of Maryland- College Park',
#18 : 'Harvard University',
#19 : 'University of Pennsylvania',
#20 : 'Brown University',
#21 : 'Purdue University- West Lafayette',
#22 : 'Rice University',
23 : 'University of Southern California',
#24 : 'Yale University',
#25 : 'Duke University',
26 : 'University of Massachusetts- Amherst',
#27 : 'University of North Carolina- Chapel Hill',
#28 : 'John Hopkins University',
29 : 'New York University',
#30 : 'Pennsylvania State University- University Park',
31 : 'University of California- Irvine',
#32 : 'University of Minnesota- Twin Cities',
#33 : 'University of Virginia',
#34 : 'Northwestern University',

#37 : 'University of California- Davis',
#38 : 'University of California- Santa Barbara',
#39 : 'University of Chicago',
#40 : 'Darthmouth College',

#43 : 'University of Arizona',


#46 : 'Virginia Tech',
#47 : 'Washington University in St. Louis',

#49 : 'Boston University',
50 : 'North Carolina State University',



    #93: 'Kansas State University',


    #98: 'University of Kentucky',
    99: 'University of Texas at Arlington',

    #100: 'Worcester Polytechnic Institute',

    # 66: 'University of Oregon', Problem?


    120:'California State University, Fullerton',




}

universityTest={
05 : 'University of Illinois- Urbana Champaign',
10: 'Columbia University',

12 : 'University of Wisconsin- Madison',
13 : 'University of California- Los Angeles',
35 : 'Ohio State University',
36 : 'Rutgers, the State University of New Jersey',

41 : 'Stony Brook University- SUNY',
42 : 'Texas A&M University- College Station',
44 : 'University of Colorado- Boulder',
45 : 'University of Utah',
48 : 'Arizona State University',
51: 'University of Florida',
    52: 'Indiana University Bloomington',

53: 'Rensselaer Polytechnic Institute',
#54: 'University of Pittsburgh',

55: 'University of Rochester',
58: 'University of California -Santa Cruz',
59: 'Vanderbilt University',


60: 'Northeastern University',


61: 'University of Illonois Chicago',

62: 'University of Notre Dame',
63: 'Iowa State',


    64: 'SUNY Buffalo',
    65: 'University of Iowa',
    67: 'George Mason University',
    68: 'Oregon State University',
    69: 'Syracuse University',
    70: 'Case Western University',

    72: 'Colorado State University',
#74: 'New York University',
    76: 'University of Delaware',
    77: 'University of Maryland Baltimore County',
    78: 'University of Nebraska Lincoln',
    80: 'University of Texas at Dallas',
81: 'Washington State University',

    82: 'Brandeis Uinversity',
83: 'Clemson University',
    85: 'Florida State University',
    87: 'University of Connecticut',
    #88: 'University of Kansas',
    #89: 'University of New Mexico',

    91: 'Bringham Young University',



    92: 'Drexel University',
94: 'New Jersey Institute of Technology',
96: 'University of Central Florida ',
    97: 'University of Georgia',
    110: 'SUNY Binghamton'



}


universityFiles={


    #DONEEE





}


universityCreateFiles={

    105: 'Texas A&M Kingsville',


}



af = None
dirpath = '/home/hrishikesh/Django_Projects/APRS_WEB/aprs/machine/'
create = True
dict_exist = False



class University :
    allName=None
    def __init__(self,id):
        self.id=id
        self.name = universityCreateFiles[id]
        self.list = None
        self.admitfilename= dirpath+str(id)+'A.csv' #admitfilename
        self.rejectfilename= dirpath+str(id)+'R.csv' #reject file name
        self.admissionslistfilename =dirpath+str(id)+'L.csv'  #filename of the pickle file that stores the admissions list that was generated post
                                     #preprocessing
        self.svm_classifier_filename =dirpath+str(id)+'_SVM_C.p'  #name of pickle file in which classifier will be saved
        self.svm_classifier_comp = None    #some classifier -now SVC
        self.svm_classifier_comp_score=None   # it's score when it was created
        #self.svm_classifier_plt = None
        self.dt_classifier_comp=None
        self.dt_comp_score = None
        self.knn_classifier_comp = None
        self.knn_comp_score =None
        self.myLocation = dirpath+str(id)+'O.p'
        self.createmyClassifier()


    def createmyClassifier(self):
        # in this function we will create the classifier for this university by calling admission_classifier's
        # createClassifier
        print 'Object instantiated , preproccessing and creating classifiers for the university'
        createClassifier(self)

        if self.svm_classifier_comp!=None:
            sampleobservation = [160, 168, 328, 110, 70, 12, 2, 1]
            print '\nTesting a created classifier : Lets predict a sample '+str(sampleobservation)

            print self.svm_classifier_comp.predict(sampleobservation)

        #save the classifier as a pickle file
        '''
        f = open(self.svm_classifier_filename,'wb')
        pickle.dump(self.svm_classifier_comp,f,-1)
        f.close()
        '''

    def predict(self,profile):
        return self.svm_classifier_comp.predict(profile)


def mywrite(text):
    af.write('\n')
    af.write(str(text))


#THis dictionary is supposed to store all  the objects of universities
#universityobjects = {}
uni_object=None


def createUniversityObjects(universityobjects):

    #universityobjects_old = dict(universityobjects)
    #create and add each university object to the universityobjects dictiionary
    for i in universityCreateFiles:
        try:

            if i not in universityFiles:


                '''
                global dict_exist
                if dict_exist==True:
                    f = open('universityobjects.p', 'rb')  # open and retrieve the existing university objects
                    universityobjects = pickle.load(f)
                    f.close()
                '''

                print '\n\nCreating University object for '+str(universityCreateFiles[i])
                auniversity=University(i)

                loca = dirpath+str(i)+'O.p'
                fo= open(loca,'wb')
                print '\nPickling and dumping '+str(auniversity.name)+' object at location '+str(loca)
                #pickle.dump(auniversity,fo,-1)
                dill.dump(auniversity,fo)
                fo.close()


                #universityobjects[i] =auniversity
                #else:
                #del universityobjects[i]
                #auniversity = University(i)
                #universityobjects[i] = auniversity
                '''
                f = open('universityobjects.p', 'wb')
                pickle.dump(universityobjects, f, -1)
                f.close()
                if dict_exist==False:
                    dict_exist=True

                '''
        except :
            print 'Hello'





    #make university objects ordered dictionary
    #universityobjects=collections.OrderedDict(universityobjects)

    #f.close()
    #display the university objects

    return universityobjects





####################PROGRAM STARTS HERE###################################################################

#first make the university files ordered incase it isnt
universityFiles=collections.OrderedDict(universityFiles)


def create_manager():
    if create:
        if dict_exist == True:
            print 'dic does exist'
            f = open('universityobjects.p', 'rb')  #open and retrieve the existing university objects
            universityobjects = pickle.load(f)
            f.close()
            # add the new item s added in the universityFIle to the unviersityobjects dictionary
            # and resave it

        else: #if university objects file is being created first time
            universityobjects={}

        if universityobjects!=None:

            universityobjects = createUniversityObjects(universityobjects)





def inference_manager(sample,name):
        global universityTest
        universityTest = collections.OrderedDict(sorted(universityTest.items()))  #for inferencing
        '''
        f = open('universityobjects.p', 'rb')
        universityobjects = pickle.load(f)
        f.close()
        '''
        global af
        global dirpath
        #dirpath = '/home/hrishikesh/Django_Projects/APRS_WEB/aprs/machine/'
        #af = open(dirpath+str(name)+'_Report.txt','w')

        af = open(dirpath+ str(name) + '_Report.txt', 'w')

        # TEST A PROFILE in sample
        #sample = [168, 158, 326, 110, 75, 0, 2, 1]
        mywrite('Profile Report')
        mywrite(name)
        mywrite('Profile '+str(sample))

        inferencelist =[]


        for i in universityTest:
            universityinfo = []
            try:
                print '\n\n '+str(i)+' '+str(universityTest[i])
                print
                print
                loca = dirpath+str(i)+'O.p'
                fo = open(loca,'rb')
                print 'Loading university object from location '+str(loca)


                #auniversity = universityobjects[i]

                #auniversity = pickle.load(fo)
                auniversity = dill.load(fo)

                fo.close()
                #print
                mywrite('\n')
                #print auniversity.id

                #print auniversity.name
                mywrite(auniversity.name)
                universityinfo.append(auniversity.name)
                #print auniversity.admitfilename
                #print auniversity.rejectfilename
                #print auniversity.svm_classifier_filename
                #print 'Prediction for profile '+str(sample)
                svm_prediction = auniversity.svm_classifier_comp.predict(sample)
                #print 'Svm prediction '+str(svm_prediction)
                mywrite('SVM prediction '+str(svm_prediction))
                universityinfo.append(svm_prediction)
                #print 'SVM score '+str(auniversity.svm_classifier_comp_score)
                #print 'Data size '+str(len(auniversity.list.profile1))

                decision_prediction = auniversity.dt_classifier_comp.predict(sample)
                #print 'Decision Tree Prediction '+str(decision_prediction)
                #print 'Decision Tree Score '+str(auniversity.dt_comp_score)
                mywrite('Decision Tree Prediction '+str(decision_prediction))
                universityinfo.append(decision_prediction)

                knn_prediction =  auniversity.knn_classifier_comp.predict(sample)
                #print 'KNN Prediction '+str(knn_prediction)
                #print 'KNN Score '+str(auniversity.knn_comp_score)
                mywrite('KNN Prediction '+str(knn_prediction))
                #print
                universityinfo.append(knn_prediction)

                inferencelist.append(universityinfo)

            except Exception as e:
                print e
                print str(i)+' '+str(universityTest[i])+' object file not found'

        return inferencelist
            #for j,p in enumerate(auniversity[i].list.profile1):
                #print str(p)+' '+str(auniversity.list.profile1target[j])




def createProfile():
    print
    print 'Enter Profile '
    name = raw_input('Name : ')
    gre_quant =int(raw_input('GRE Qunat : '))
    gre_verb = int(raw_input('GRE Verb :  '))
    gre_total = gre_quant+gre_verb
    toefl = int(raw_input('TOEFL : '))
    agg  = int(raw_input('Percentage : '))
    workexp = int(raw_input('Work Exp : '))
    paper_score  = int(raw_input('Paper Score (International=3,National=2,Local=1,Notwritten=0)  :'))
    branchscore=int(raw_input('Branch is Comp (Yes=1 ,No =0): '))

    sample =[gre_quant,gre_verb,gre_total,toefl,agg,workexp,paper_score,branchscore]

    return sample,name














def home(request):
    #create_manager()

    return render(request,'aprs/home.html')

def landpage(request):
    name = request.POST['name']
    email = request.POST['email']
    greQuant = int(request.POST['greQuant'])
    greVerbal = int(request.POST['greVerbal'])
    toefl = int(request.POST['toefl'])
    uAgg = int(request.POST['uAgg'])
    workexp = int(request.POST['workexp'])
    paper_score = int(request.POST['paper_score'])
    branch = int(request.POST['branch'])

    print name
    print email
    print greQuant
    print greVerbal
    print toefl
    print uAgg
    print workexp
    print branch
    print paper_score


    total = greQuant + greVerbal
    #sample = [gre_quant, gre_verb, gre_total, toefl, agg, workexp, paper_score, branchscore]
    sample = [greQuant,greVerbal,total,toefl,uAgg,workexp,paper_score,branch]
    #create_manager()
    inferencelist =inference_manager(sample,name)
    inferencelist=inference_manager(sample,name)

    if branch==1:
        branchname = 'Computer Science'
    else:
        branchname = 'Other'

    context ={
        'inferencelist':inferencelist,
        'name':name,
        'greQuant':greQuant,
        'greVerbal':greVerbal,
        'total':total,
        'toefl':toefl,
        'uAgg':uAgg,
        'workexp':workexp,
        'branchname':branchname,

    }


    return render(request,'aprs/random_landpage.html',context)


