# The code the blind reader ran, in order (2026-11-17, purpose-code, 255 rounds).

# ---- run 1 ----
s=open('/work/bits.txt').read().strip()
print(len(s), s.count('1'), s.count('0'))
print(s[:2000])
n=len(s)
def f(n):
    return [d for d in range(2,n) if n%d==0]
print(f(n)[:50])
import re
runs=re.findall(r'0+|1+',s)
from collections import Counter
print(Counter(len(r) for r in runs if r[0]=='1').most_common(20))
print(Counter(len(r) for r in runs if r[0]=='0').most_common(20))

# ---- run 2 ----
s=open('/work/bits.txt').read().strip()
i=s.index('0'*15)
print(i, (len(s)-i)%16, (len(s)-i)//16)
pre=s[:i]; print([len(x) for x in pre.split('0')])
# figure alignment
for off in range(i-2,i+3):
    w=[int(s[off+k*16:off+k*16+16],2) for k in range(60)]
    print(off,w)

# ---- run 3 ----
s=open('/work/bits.txt').read().strip()
w=[int(s[172+k*16:172+k*16+16],2) for k in range(12124)]
print(s[172+12124*16:])
from collections import Counter
c=Counter(w); print(len(c)); print(sorted(c.items())[:400])
print(sorted(c.items())[400:])
print(w[:700])

# ---- run 4 ----
s=open('/work/bits.txt').read().strip()
w=[int(s[172+k*16:172+k*16+16],2) for k in range(12124)]
def name(x):
    if x<256: return str(x)
    h,l=x>>8,x&255
    return "ABCDEFGHIJKLMNOP"[h]+str(l) if h<16 else "?%d"%x
# parse
i=12+256
out=[];depth=0;cur=[];start=i
stmts=[]
while i<len(w):
    x=w[i]
    if x==256: 
        if depth==0: start=i
        depth+=1;cur.append('(')
    elif x==257:
        depth-=1;cur.append(')')
        if depth==0:
            stmts.append((start," ".join(cur).replace('( ','(').replace(' )',')')));cur=[]
    else:
        cur.append(name(x))
        if depth==0:
            stmts.append((i,"RAW "+cur[0]));cur=[]
    i+=1
print(len(stmts),depth,cur)
import pickle;pickle.dump(stmts,open('/work/st.pkl','wb'))
for a,b in stmts[:330]: print(a,b)

# ---- run 5 ----
import pickle
st=pickle.load(open('/work/st.pkl','rb'))
for a,b in st[330:]: print(a,b)

# ---- run 6 ----
s=open('/work/bits.txt').read().strip()
tail=s[172+12114*16:]
print(len(tail)); print(tail); print(s[:172])
print(tail==s[:172][::-1], [i for i,c in enumerate(tail) if c=='0'], [i for i,c in enumerate(tail[::-1]) if c=='0'])
pay={('C','C'):3,('C','D'):0,('D','C'):5,('D','D'):1}
S={'allC':lambda h:'C','allD':lambda h:'D','TFT':lambda h:'C' if not h else h[-1][1],'STFT':lambda h:'D' if not h else h[-1][1],
'grim':lambda h:'C' if all(x[1]=='C' for x in h) else 'D','pav':lambda h:'C' if not h or h[-1][0]==h[-1][1] else 'D'}
def score(a,b,n):
    ha=[];hb=[];t=0
    for _ in range(n):
        x=S[a](ha);y=S[b](hb);ha.append((x,y));hb.append((y,x));t+=pay[x,y]
    return t
for a in S:
    print(a,{b:score(a,b,255) for b in S},sum(score(a,b,255) for b in S))
print([ (a*256+b) for a,b in [(2,253),(1,3),(4,251),(2,255),(2,123),(2,128),(1,2),(15,109),(14,238),(14,113),(13,244),(11,254),(10,125)]])
# section sizes
import pickle
st=pickle.load(open('/work/st.pkl','rb'))
b=[0,12,268,1717,2000,2262,4228,4888,5211,5592,6691,10445,12114,12124]
print([(b[i],round(100*(b[i+1]-b[i])/12124,1)) for i in range(len(b)-1)])
print(sum(1 for a,x in st if x.startswith('(C36')), len(st))
