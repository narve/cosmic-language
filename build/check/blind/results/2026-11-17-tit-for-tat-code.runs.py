# The code the blind reader ran, in order (2026-11-17, last-statement-code, after the reorder).

# ---- run 1 ----
s=open('/work/bits.txt').read().strip()
n=len(s);print(n)
print(s[:600]);print(s[-300:])
def f(n):
    return [d for d in range(2,n) if n%d==0]
print(f(n)[:40])
import re
from collections import Counter
runs=Counter(len(m.group()) for m in re.finditer('1+',s));print(sorted(runs.items()))
runs=Counter(len(m.group()) for m in re.finditer('0+',s));print(sorted(runs.items()))

# ---- run 2 ----
s=open('/work/bits.txt').read().strip()
h=s.find('0'*8); print(h)
pre=s[:h]; print(pre, len(pre)); 
t=s.rfind('1011011101111101111111'); print(t, len(s)-t, s[t:]==pre)
body=s[h:t]; print(len(body), len(body)%16, len(body)%8)
w=[int(body[i:i+16],2) for i in range(0,len(body),16)]
print(len(w)); print(w[:300])
from collections import Counter
c=Counter(w); print(len(c)); print(c.most_common(60))
print(w[-200:])

# ---- run 3 ----
s=open('/work/bits.txt').read().strip()
body=s[172:189212]
w=[int(body[i:i+16],2) for i in range(0,len(body),16)]
def name(x):
    hi,lo=x>>8,x&255
    return str(lo) if hi==0 else "%s%d"%("?PFCVKQRSTU"[hi],lo)
# top-level statements
st=[];d=0;cur=[];start=None;pos=[]
for i,x in enumerate(w):
    if d==0 and x!=256 and x!=257:
        st.append(('raw',i,i,name(x)));continue
    if x==256:
        if d==0:start=i;cur=[]
        d+=1;cur.append('(')
    elif x==257:
        d-=1;cur.append(')')
        if d==0: st.append(('S',start,i,' '.join(cur).replace('( ','(').replace(' )',')')))
    else:cur.append(name(x))
print(len(st),d)
import pickle;pickle.dump((w,st),open('/work/st.pkl','wb'))
from collections import Counter
print(sorted(Counter(x>>8 for x in w).items()))
prev=None
out=[]
for k,(t,a,b,txt) in enumerate(st):
    if t=='raw': continue
    out.append("%d [%d-%d] %s"%(k,a,b,txt))
open('/work/out.txt','w').write('\n'.join(out))
print(len(out))
# print those first occurrence of each head op
seen=Counter()
for l in out:
    key=l.split('] ')[1].split()[0]
    seen[key]+=1
    if seen[key]<=4: print(l[:300])

# ---- run 4 ----
t=open('/work/out.txt').read()
print(t[:19500])

# ---- run 5 ----
import pickle
w,st=pickle.load(open('/work/st.pkl','rb'))
print([ (a,x) for t,a,b,x in st if t=='raw'][:15], [ (a,x) for t,a,b,x in st if t=='raw'][-5:])
print(len(open('/work/out.txt').read()))

# ---- run 6 ----
t=open('/work/out.txt').read()
i=t.find('712 [6514')
print(t[i:i+17000])

# ---- run 7 ----
import pickle
w,st=pickle.load(open('/work/st.pkl','rb'))
print([hex(x) for x in w[11769:11815]]); print(172+16*11769,172+16*11815, 172+16*len(w))
# depth check: do statements ever fail to balance / any raw words after 268?
print([s for s in st if s[0]=='raw' and s[1]>=268])
C,D='C','D'
pay={(C,C):3,(C,D):0,(D,C):5,(D,D):1}
S={'21':lambda h:C,'22':lambda h:D,'23':lambda h:C if not h else h[-1][1],'24':lambda h:D if not h else h[-1][1],
'25':lambda h:C if all(p[1]!=D for p in h) else D,'26':lambda h:C if not h or h[-1][0]==h[-1][1] else D}
def score(a,b,n):
    ha=[];hb=[];t=0
    for _ in range(n):
        x=S[a](ha);y=S[b](hb);ha.append((x,y));hb.append((y,x));t+=pay[x,y]
    return t
for a in S: print(a,sum(score(a,b,10) for b in S),[score(a,b,10) for b in S])
