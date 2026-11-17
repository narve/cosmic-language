# The code the blind reader ran, in order (2026-11-17, purpose-code).

# ---- run 1 ----
s=open('/work/bits.txt').read().strip()
n=len(s);print(n,s.count('1'))
print(s[:600])
print([d for d in range(1,2000) if n%d==0])
import re,collections
runs=collections.Counter(len(m.group()) for m in re.finditer('1+',s));print(sorted(runs.items()))
runs=collections.Counter(len(m.group()) for m in re.finditer('0+',s));print(sorted(runs.items()))

# ---- run 2 ----
s=open('/work/bits.txt').read().strip()
i=s.index('0'*15);print(i, (len(s)-i)%16, (len(s)-i)//16)
print(s[-400:])
b=s[i:]
w=[int(b[k:k+16],2) for k in range(0,len(b)-15,16)]
import collections
c=collections.Counter(w);print(len(c));print(sorted(c.items())[:300])
print(w[:400])

# ---- run 3 ----
s=open('/work/bits.txt').read().strip()
i=172
b=s[i:]
w=[int(b[k:k+16],2) for k in range(0,len(b)-15,16)]
print(w[-30:], max(w))
def tok(x):
    if x<256: return str(x)
    if x==256: return '('
    if x==257: return ')'
    return 'S%d'%(x-512)
# split into top-level statements
st=[];d=0;cur=[]
pos=[]
for k,x in enumerate(w[12+257:]):
    if x==256:
        if d==0: start=k
        d+=1
    cur.append(tok(x))
    if x==257:
        d-=1
        if d==0: st.append(' '.join(cur));pos.append(start);cur=[]
print(len(st),cur[:50])
open('/work/st.txt','w').write('\n'.join(f'{p} {t}' for p,t in zip(pos,st)))
for k in range(0,700): print(k,st[k])

# ---- run 4 ----
s=open('/work/bits.txt').read().strip()
b=s[172:]
w=[int(b[k:k+16],2) for k in range(0,len(b)-15,16)]
body=w[12+256:]
names={1:'=',2:'!=',3:'<',4:'>',5:'<=',6:'>=',7:'+',8:'*',9:'B256',10:'-',11:'neg',12:'/',13:'not',14:'and',15:'or',16:'list',17:'len',18:'nth',19:'count',20:'forall',21:'exists',22:'implies',23:'pow',24:'abs',25:'exp',26:'fold',27:'map',28:'mean',29:'prob',30:'cross',31:'quote',32:'kind',33:'rest',34:'if',35:'eval',36:'PHYS',37:'mass',38:'charge',257:'T',258:'F',259:'N',260:'Z?',261:'R',262:'i',263:'C',264:'e',265:'pi',266:'EXPR'}
def tok(x):
    if x<256: return str(x)
    if x==256: return '('
    if x==257: return ')'
    x-=512
    if x in names: return names[x]
    if 513<=x<600: return 'xyzuvwabcd'[x-513] if x-513<10 else 'v%d'%x
    return 'S%d'%x
st=[];d=0;cur=[];pos=[]
for k,x in enumerate(body):
    if x==256:
        if d==0: start=k
        d+=1
    cur.append(tok(x))
    if x==257:
        d-=1
        if d==0: st.append(' '.join(cur).replace('( ','(').replace(' )',')'));pos.append(start);cur=[]
print(len(st),cur, len(body))
import pickle;pickle.dump((st,pos),open('/work/st.pkl','wb'))
# first-appearance of each symbol
seen={}
for k,x in enumerate(body):
    if x>512 and x not in seen: seen[x]=k
print([(tok(x),k) for x,k in seen.items()])
for k in range(640,len(st)):
    if pos[k]>3900: print(pos[k],st[k])

# ---- run 5 ----
import pickle
st,pos=pickle.load(open('/work/st.pkl','rb'))
for k in range(len(st)):
    if 6280<pos[k]<8600: print(pos[k],st[k])

# ---- run 6 ----
import pickle
st,pos=pickle.load(open('/work/st.pkl','rb'))
for k in range(len(st)):
    if 8550<pos[k]<10020: print(pos[k],st[k])

# ---- run 7 ----
s=open('/work/bits.txt').read().strip()
print(s[:172]==s[-172:], s[:172][::-1]==s[-172:], s[-172:])
C,D='C','D'
pay={(C,C):3,(C,D):0,(D,C):5,(D,D):1}
# history x = list of (own, other)
S={'ALLC':lambda h:C,'ALLD':lambda h:D,
'TFT':lambda h:C if not h else h[-1][1],
'STFT':lambda h:D if not h else h[-1][1],
'GRIM':lambda h:C if all(o==C for _,o in h) else D,
'PAV':lambda h:C if not h or h[-1][0]==h[-1][1] else D}
def score(a,b,n):
    ha=[];hb=[];t=0
    for _ in range(n):
        x=S[a](ha);y=S[b](hb);ha.append((x,y));hb.append((y,x));t+=pay[x,y]
    return t
for a,b in [('TFT','TFT'),('ALLD','ALLD'),('TFT','ALLD'),('ALLD','TFT'),('ALLC','ALLD'),('ALLD','ALLC'),('PAV','ALLD'),('ALLD','PAV'),('TFT','STFT'),('STFT','TFT'),('GRIM','STFT'),('STFT','GRIM')]:
    print(a,b,score(a,b,10))
for a in S: print(a,sum(score(a,b,10) for b in S))
print(score('TFT','ALLD',4))
# sizes
b=[1,1451,2010,3341,4492,5196,6292,9430,9708,9934,11547]
print([round((b[i+1]-b[i])/11546*100,1) for i in range(len(b)-1)])
