# The code the blind reader ran, in order (2026-11-17, purpose-code, 255 rounds).

# ---- run 1 ----
s=open('/work/bits.txt').read().strip()
print(len(s), s.count('1'), s.count('0'))
print(s[:2000])
n=len(s)
def fac(n):
    return [d for d in range(1,int(n**.5)+1) if n%d==0]
print(fac(n))
import re
from collections import Counter
runs=Counter(len(m.group()) for m in re.finditer('1+',s)); print(sorted(runs.items()))
runs=Counter(len(m.group()) for m in re.finditer('0+',s)); print(sorted(runs.items()))

# ---- run 2 ----
s=open('/work/bits.txt').read().strip()
i=s.find('0000000000000001'); print(i,(len(s)-i)%16,(len(s)-i)//16)
# find best offset
for h in range(165,180):
    if (len(s)-h)%16==0: print('h',h)
w=[int(s[j:j+16],2) for j in range(172 if (len(s)-172)%16==0 else i,len(s)-15,16)]
print(len(w))
from collections import Counter
c=Counter(w); print(len(c)); print(sorted(c.items(),key=lambda x:-x[1])[:80])
print(w[:400])
print(w[-300:])

# ---- run 3 ----
s=open('/work/bits.txt').read().strip()
body=s[172:]
w=[int(body[j:j+16],2) for j in range(0,len(body)-15,16)]
# find end of well-formed
print(s[-400:])
def name(x):
    if x<256: return str(x)
    return "%s%d"%("?ABCDEFGHIJKLMNOPQRSTUVWXYZ"[x>>8] if (x>>8)<27 else 'Z%d_'%(x>>8), x&255)
# parse
i=12+256
print(w[12+255], w[12+256])
stmts=[];depth=0;cur=[];pos=[]
j=i
while j<len(w):
    x=w[j]
    if x==256:
        if depth==0: start=j
        depth+=1;cur.append('(')
    elif x==257:
        depth-=1;cur.append(')')
        if depth==0:
            stmts.append(' '.join(cur).replace('( ','(').replace(' )',')'));pos.append(start);cur=[]
    else:
        if depth==0: print('toplevel stray',j,x)
        cur.append(name(x))
    j+=1
print(len(stmts),depth,cur[:20])
import pickle;pickle.dump((stmts,pos,w),open('/work/st.pkl','wb'))
from collections import Counter
cats=Counter(x>>8 for x in w[i:]);print(cats)
for k,(st,p) in enumerate(zip(stmts,pos)):
    if k<330: print(k,p,st)

# ---- run 4 ----
import pickle
stmts,pos,w=pickle.load(open('/work/st.pkl','rb'))
import re
m={'B1':'=','B2':'!=','B3':'<','B4':'>','B5':'<=','B6':'>=','B7':'+','B8':'*','B9':'num','B10':'-','B11':'neg','B12':'/','C1':'T','C2':'F','B13':'not','B14':'and','B15':'or','B16':'list','B17':'len','B18':'nth','B19':'count','B20':'all','B21':'ex','C3':'N','C4':'Q','C5':'R','B22':'=>','B23':'^','C6':'i','D1':'x','D2':'y','D3':'z'}
def nice(st): return re.sub(r'[A-Z]\d+',lambda g:m.get(g.group(),g.group()),st)
out=[nice(s) for s in stmts]
pickle.dump(out,open('/work/out.pkl','wb'))
for k in range(330,520): print(k,pos[k],out[k])

# ---- run 5 ----
s=open('/work/bits.txt').read().strip()
t=s[-200:]
print(t); print(s[:172]==s[-172:][::-1], s[:172])

# ---- run 6 ----
import pickle
stmts,pos,w=pickle.load(open('/work/st.pkl','rb'))
out=pickle.load(open('/work/out.pkl','rb'))
s=open('/work/bits.txt').read().strip()
print(s[:172]==s[-172:])
for k in range(520,702): print(k,pos[k],out[k])

# ---- run 7 ----
import pickle
stmts,pos,w=pickle.load(open('/work/st.pkl','rb'))
C,D='C','D'
pay={(C,C):3,(C,D):0,(D,C):5,(D,D):1}
def allc(h):return C
def alld(h):return D
def tft(h):return C if not h else h[-1][1]
def stft(h):return D if not h else h[-1][1]
def grim(h):return C if all(x[1]!=D for x in h) else D
def pav(h):return C if not h or h[-1][0]==h[-1][1] else D
S={'C21 allC':allc,'C22 allD':alld,'C23 TFT':tft,'C24 susTFT':stft,'C25 grim':grim,'C26 pavlov':pav}
def score(a,b,n=255):
    ha=[];hb=[];t=0
    for _ in range(n):
        x=a(ha);y=b(hb);ha.append((x,y));hb.append((y,x));t+=pay[(x,y)]
    return t
for n,f in S.items():
    tot=sum(score(f,g) for g in S.values()); print(n,tot,divmod(tot,256),[score(f,g) for g in S.values()])
print(score(tft,alld,4))
# section sizes
T=len(w)-12-256-10
b=[0,158,203,274,294,322,362,393,451,493,561,573,584,603,641,702]
for a,c in zip(b,b[1:]):
    e=pos[c] if c<702 else 12114
    print(a,c-1,e-pos[a],round(100*(e-pos[a])/(12114-268),1))
print(sum(1 for x in stmts if x.startswith('(B36')))
