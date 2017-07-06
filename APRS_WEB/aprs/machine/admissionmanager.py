import collections
from admissions_classifier import createClassifier
import pickle
import dill
import os
import time
import copy


universityNotDone={
    # not done yet - change this comment when they are done



    # 66: 'University of Oregon', Problem?
}

universityTest={
10: 'Columbia University',
55: 'University of Rochester',

}


universityFiles={


    #DONEEE



    58: 'University of California -Santa Cruz',
    60: 'Northeastern University',
    59: 'Vanderbilt University',
    51: 'University of Florida',
    52: 'Indiana University Bloomington',
    53: 'Rensselaer Polytechnic Institute',
    54: 'University of Pittsburgh',

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
    74: 'New York University',
    76: 'University of Delaware',
    77: 'University of Maryland Baltimore County',
    78: 'University of Nebraska Lincoln',
    80: 'University of Texas at Dallas',
    81: 'Washington State University',
    82: 'Brandeis Uinversity',
    83: 'Clemson University',
    85: 'Florida State University',
    86: 'George Washington University',
    87: 'University of Connecticut',
    88: 'University of Kansas',
    89: 'University of New Mexico',
    91: 'Bringham Young University',
    92: 'Drexel University',
    93: 'Kansas State University',
    94: 'New Jersey Institute of Technology',
    96: 'University of Central Florida ',
    97: 'University of Georgia',
    98: 'University of Kentucky',
    99: 'University of Texas at Arlington',

    100: 'Worcester Polytechnic Institute',


}


universityCreateFiles={

10: 'Columbia University',
55: 'University of Rochester',

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
        self.admitfilename= dirpath+ str(id)+'A.csv' #admitfilename
        self.rejectfilename= dirpath+str(id)+'R.csv' #reject file name
        self.admissionslistfilename =str(id)+'L.csv'  #filename of the pickle file that stores the admissions list that was generated post
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
        print 'hello'
        createClassifier(self)
        print 'HELLLO'
        if self.svm_classifier_comp!=None:
            sampleobservation = [160, 168, 328, 110, 70, 12, 2, 1]
            print 'We have an svm classifier , lets predict a sample '+str(sampleobservation)

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

                print 'Heyy'
                auniversity=University(i)

                loca = str(i)+'O.p'
                fo= open(loca,'wb')

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
print 'CHICKKKY PICKKYYY'


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
            '''
            f = open('universityobjects.p', 'wb')
            pickle.dump(universityobjects, f, -1)
            f.close()
            '''


def inference_manager(sample,name):

        #for inferencing
        '''
        f = open('universityobjects.p', 'rb')
        universityobjects = pickle.load(f)
        f.close()
        '''
        global af
        #global dirpath

        af = open(dirpath+str(name)+'_Report.txt','w')

        # TEST A PROFILE in sample
        #sample = [168, 158, 326, 110, 75, 0, 2, 1]
        mywrite('Profile Report')
        mywrite(name)
        mywrite('Profile '+str(sample))



        for i in universityTest:
            try:
                print 'is it here1'

                fo = open(dirpath+str(i)+'O.p','rb')

                print 'is it here2'

                #auniversity = universityobjects[i]
                print 'before load'
                #auniversity = pickle.load(fo)
                auniversity = dill.load(fo)
                print 'after load'
                fo.close()
                #print
                mywrite('\n')
                #print auniversity.id

                #print auniversity.name
                mywrite(auniversity.name)
                #print auniversity.admitfilename
                #print auniversity.rejectfilename
                #print auniversity.svm_classifier_filename
                #print 'Prediction for profile '+str(sample)
                #print 'Svm prediction '+str(auniversity.svm_classifier_comp.predict(sample))
                mywrite('SVM prediction '+str(auniversity.svm_classifier_comp.predict(sample)))

                #print 'SVM score '+str(auniversity.svm_classifier_comp_score)
                #print 'Data size '+str(len(auniversity.list.profile1))

                #print 'Decision Tree Prediction '+str(auniversity.dt_classifier_comp.predict(sample))
                #print 'Decision Tree Score '+str(auniversity.dt_comp_score)
                mywrite('Decision Tree Prediction '+str(auniversity.dt_classifier_comp.predict(sample)))

                #print 'KNN Prediction '+str( auniversity.knn_classifier_comp.predict(sample))
                #print 'KNN Score '+str(auniversity.knn_comp_score)
                mywrite('KNN Prediction '+str( auniversity.knn_classifier_comp.predict(sample)))
                #print
            except Exception as e:
                print e
                print str(i)+' '+str(universityTest[i])+' object file not found'


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




#here calling the classifiers
#createAllClassifiers(universityobjects)

if __name__=='__main__':
    create_manager()
    sample,name =createProfile()

    inference_manager(sample,name)
    #print os.path.dirname(__file__)