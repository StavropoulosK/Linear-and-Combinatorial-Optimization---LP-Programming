import os
dirname = os.path.dirname(__file__)
import pymprog


# Finnish-Swedish alphabet
alphabet = "abcdefghijklmnopqrstuvwxyzåäö"

def getFrequencyOfLetters(text):

    # Convert text to lowercase
    text = text.lower()

    letter_frequency = [0] * 29

    totalChars=0

    for char in text:
        if char in alphabet:
            totalChars +=1
            position = alphabet.find(char)
            letter_frequency[position] += 1

    for i in range(len(letter_frequency)):
        letter_frequency[i]=letter_frequency[i]/totalChars

    return letter_frequency

def getAvgWordLength(text):
    #https://stackoverflow.com/questions/12761510/python-how-can-i-calculate-the-average-word-length-in-a-sentence-using-the-spl

    filtered = ''.join(filter(lambda x: x not in '".,;!-', text))
    words = [word for word in filtered.split() if word]
    avg = sum(map(len, words))/len(words)
    return avg

# Gia kathe keimeno o pinakas F periexei ena dianisma me 30 times. 29 einai i sixntotita kathe gramatos kai 1 to meso megethos ton lekseon
# Sinolika periexei 18 keimena. Epomenos periexei 18 dianismata 30 stoixeion to kathena
# ta f1..f9 einai keimena me filandika kai ta s1..s9 me souidika. Ta prota 6 keimena apo kathe glosa xrisimopoiountai gia training kai ta 
# ipolia 3 gia testing.

F=[]

paths=['f1','f2','f3','f4','f5','f6','f7','f8','f9','s1','s2','s3','s4','s5','s6','s7','s8','s9']

def getParameters():

    i=0

    for i in range(len(paths)):
        filename=os.path.join(dirname,'texts/'+paths[i]+'.txt')
        text=''
        with open(filename, 'r', encoding="utf-8") as file:
            text = file.read().replace('\n', '')

        letter_freq = getFrequencyOfLetters(text)
        avgLength= getAvgWordLength(text)
        fi= letter_freq + [avgLength]
        F.append(fi)
          

getParameters()


def solve_first_norm():
    # min ∑ (ui1+ui2)    i=1..30
    # ∑ (ui1 fid -ui2 fid) +b  >=1   i=1..30     για κάθε φιλανδικό κείμενο d
    # ∑ (ui1 fid -ui2 fid) +b <= -1  i=1..30     για κάθε σουηδικό κείμενο d
    # ui1, ui2 ≥0, b ∈R
    # Iparxoun 61 metablites apofasis. u1_1 u1_2, u2_1 u2_2, u3_1 u3_2, u4_1 u4_2 ..., u30_1 u30_2, b

    c= [1] * 60 + [0]   # to b den emfanizetai stin antikeimeniki sinartisi

    Ag=[]
    bg=[1] * 6

    Al=[]
    bl=[-1] * 6

    for i in range(6):
        # filandika keimena
        f_greater=F[i]  
        u=[]
        for i in range(len(f_greater)):         #to f_greater einai mia grami kathe fora me ta xaraktiristika fid ton filandikon keimenon
            elem=f_greater[i]
            u.append(elem)                      # elem=fid ,   -elem=-fid
            u.append(-elem)
        u.append(1)             # to b exei sintelesti 1
        Ag.append(u) 

    for i in range(6):
        # souidika keimena
        f_lesser= F[i+9]
        u=[]
        for i in range(len(f_lesser)):         #to f_lesser einai mia grami kathe fora me ta xaraktiristika fid ton souidikon keimenon
            elem=f_lesser[i]
            u.append(elem)
            u.append(-elem)
        u.append(1)             # to b exei sintelesti 1
        Al.append(u) 

    model=pymprog.model('first norm')

    x=model.var('ui',60,kind=float)
    x += model.var('b',1,kind=float,bounds=(None,None))

    m1,n1= len(Ag), len(Ag[0])
    m2,n2= len(Al), len(Al[0])
    y={}

    for i in range(m1):

        y[i]= sum(Ag[i][j]*x[j] for j in range(n1)) >= bg[i]

    for i in range(m2):
        y[i+m1] = sum(Al[i][j] *x[j] for j in range(n2))<=bl[i]

    n=n1
    model.minimize(sum(c[i]*x[i] for i in range(n)))

    model.solve()
    #print('z=',model.vobj())

    coeff=[]
    for j in range(n):
        #print(x[j].primal)
        coeff.append(x[j].primal)
    
    return coeff

def solve_inf_norm():
    # norma apeiro

    # min x    i=1..30
    # ∑ (ui1 fid -ui2 fid) +b  >=1   i=1..30     για κάθε φιλανδικό κείμενο d
    # ∑ (ui1 fid -ui2 fid) +b <= -1  i=1..30     για κάθε σουηδικό κείμενο d
    # ui1+ui2-x <= 0      i=1..30
    # ui1, ui2,x ≥0, b ∈R
    # Iparxoun 62 metablites apofasis. u1_1 u1_2, u2_1 u2_2, u3_1 u3_2, u4_1 u4_2 ..., u30_1 u30_2, b, x

    c= [0] * 60 + [0] +[1]   # stin antikeimeniki sinartisi emfanizetai mono to x.

    Ag=[]
    bg=[1] * 6

    Al=[]
    bl=[-1] * 6 + [0] *30       # 30 periorismoi logo tou ui1+ui2-x <= 0

    for i in range(6):
        # filandika keimena
        f_greater=F[i]  
        u=[]
        for i in range(len(f_greater)):         #to f_greater einai mia grami kathe fora me ta xaraktiristika fid ton filandikon keimenon
            elem=f_greater[i]
            u.append(elem)
            u.append(-elem)
        u.append(1)             # to b exei sintelesti 1
        u.append(0)             # to x exei sintelesti 0

        Ag.append(u) 

    for i in range(6):
        # souidika keimena
        f_lesser= F[i+9]
        u=[]
        for i in range(len(f_lesser)):         #to f_lesser einai mia grami kathe fora me ta xaraktiristika fid ton souidikon keimenon
            elem=f_lesser[i]
            u.append(elem)
            u.append(-elem)
        u.append(1)             # to b exei sintelesti 1
        u.append(0)             # to x exei sintelesti 0

        Al.append(u) 
    
    for i in range(30):
        # u1_1+u1_2-x<=0,  u2_1+u2_2-x<=0,..., u30_1+u30_2-x<=0
        u=[0]*60+[0]+[-1]      # b=0, x=-1
        u[2*i]=1
        u[2*i+1]=1
        Al.append(u) 

    
    model=pymprog.model('infinity norm')

    x=model.var('ui',60,kind=float)
    x += model.var('b',1,kind=float,bounds=(None,None))
    x += model.var('x',1,kind=float)


    m1,n1= len(Ag), len(Ag[0])
    m2,n2= len(Al), len(Al[0])
    y={}

    for i in range(m1):

        y[i]= sum(Ag[i][j]*x[j] for j in range(n1)) >= bg[i]

    for i in range(m2):
        y[i+m1] = sum(Al[i][j] *x[j] for j in range(n2))<=bl[i]

    n=n1
    model.minimize(sum(c[i]*x[i] for i in range(n)))

    model.solve()
    #print('z=',model.vobj())

    coeff=[]
    for j in range(n):
        #print(x[j].primal)
        coeff.append(x[j].primal)
    
    return coeff

def evaluate(coeff):
    # coeff einai oi sintelestes ton u1_1 u1_2, u2_1 u2_2, u3_1 u3_2, u4_1 u4_2 ..., u30_1 u30_2, b   (kai tou x stin periptosi tis normas apiro)
    # g(fd) = sum [(ui1-ui2)*fid] + b    i=1..30
    # gia ena kainourgio keimeno ipologizoume to dianisma fid (30 stoixion) kai an i timi g(fd) einai >=1 tote to keimeno aniki
    # sta filandika. An g(fd)<=-1 tote aniki sta souidika. An -1<=g(fd) <=1  tote den imaste sigouroi ala antistoixoume to keimeno
    # stin katigoria pou briskete plisiestera  g(fd)>=0  ->  filandika,  g(fd) <=0 ->souidika

    # San evaluation data tha xrisimopoiisoume 3 filandika kai 3 souidika keimena.
    # ta f7,f8,f9 kai s7,s8,s9

    f7_params=F[6]
    f8_params=F[7]
    f9_params=F[8]

    s7_params=F[15]
    s8_params=F[16]
    s9_params=F[17]

    testSet=[f7_params,f8_params,f9_params,s7_params,s8_params,s9_params]
    file_name=['f7.txt','f8.txt','f9.txt','s7.txt','s8.txt','s9.txt']
    for i in range(len(testSet)):
        fi=testSet[i]

        g_value=0

        for j in range(30): 
            g_value +=  (coeff[j*2]-coeff[j*2+1])*fi[j]

        g_value += coeff[60]   #prosthetoume to bias b

        response=''

        if(g_value>=1):response='Finnish'
        elif(g_value>=0): response='Finnish probably'
        elif(g_value<=-1): response='Swedish'            
        elif(g_value<=0): response='Swedish probably'   

        print("file name=%s g(fd)=%.2f, result: %s " % (file_name[i],g_value,response))


print('\n\n Objective function with norm 1 \n\n')
coeff_first_norm=solve_first_norm()
evaluate(coeff_first_norm)


print('\n\n Objective function with norm infinity \n\n')

coeff_inf_norm=solve_inf_norm()
evaluate(coeff_inf_norm)

