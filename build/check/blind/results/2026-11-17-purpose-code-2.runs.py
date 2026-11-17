# The code the blind reader ran, in order (2026-11-17, purpose-code, second run).

# ---- run 1 ----
s=open('/work/bits.txt').read().strip()
print(len(s), s.count('1'), s.count('0'))
print(s[:600])
print(s[-300:])
n=len(s)
f=[d for d in range(1,2000) if n%d==0]
print(f)
import re
from collections import Counter
runs=Counter(len(m.group()) for m in re.finditer('1+',s))
print(sorted(runs.items()))
runs=Counter(len(m.group()) for m in re.finditer('0+',s))
print(sorted(runs.items()))

# ---- run 2 ----
s=open('/work/bits.txt').read().strip()
h=s.index('0'*15)
print(h, s[:h])
# trailer
import re
t=len(s)-171
print(s[t-40:t], s[t:]==s[:171])
body=s[171:t]
print(len(body), len(body)%16, len(body)%8)
for w in (8,16):
    ws=[int(body[i:i+w],2) for i in range(0,len(body)-w+1,w)]
    from collections import Counter
    c=Counter(ws); print(w,len(ws),len(c)); print(c.most_common(60))
ws=[int(body[i:i+16],2) for i in range(0,len(body),16)]
print(ws[:400])

# ---- run 3 ----
s=open('/work/bits.txt').read().strip()
body=s[172:]
print(len(body)%8)
b=[int(body[i:i+8],2) for i in range(0,len(body)-7,8)]
print(b[:60]); print(b[250:900]); print(b[-80:])

# ---- run 4 ----
s=open('/work/bits.txt').read().strip()
body=s[172:-172]
print(len(body)%16, s[-172:]=='0'+s[:171])
t=[(int(body[i:i+8],2),int(body[i+8:i+16],2)) for i in range(0,len(body),16)]
from collections import Counter
print(Counter(a for a,b in t))
for k in range(1,6): print(k, sorted(Counter(b for a,b in t if a==k).items()))
import pickle; pickle.dump(t,open('/work/t.pkl','wb'))
# first appearance of each class>=1 token
seen={}
for i,x in enumerate(t):
    if x[0]>=1 and x not in seen: seen[x]=i
print(sorted(seen.items(), key=lambda kv:kv[1]))

# ---- run 5 ----
import pickle
t=pickle.load(open('/work/t.pkl','rb'))
pre={2:'W',3:'N',4:'v',5:'E',6:'F',7:'G',8:'H',9:'J'}
out=[];depth=0;line=[];lines=[];start=0
for i,(a,b) in enumerate(t):
    if a==1 and b==0:
        if depth==0: start=i
        depth+=1; line.append('(')
    elif a==1 and b==1:
        depth-=1; line.append(')')
        if depth==0:
            lines.append((start,' '.join(line).replace('( ','(').replace(' )',')'))); line=[]
    elif a==0: 
        line.append(str(b))
        if depth==0: lines.append((i,line[0])); line=[]
    else: line.append(pre[a]+str(b))
print(len(lines), depth)
pickle.dump(lines,open('/work/lines.pkl','wb'))
open('/work/out.txt','w').write('\n'.join(f'{i} {l}' for i,l in lines))
txt=open('/work/out.txt').read()
print(len(txt))
L=txt.split('\n')
print('\n'.join(L[268:268+330]))

# ---- run 6 ----
L=open('/work/out.txt').read().split('\n')
import re
i0=[k for k,l in enumerate(L) if l.startswith('4314 ')][0]
print('\n'.join(L[i0+1:i0+300]))

# ---- run 7 ----
L=open('/work/out.txt').read().split('\n')
i0=[k for k,l in enumerate(L) if l.startswith('10256 ')][0]
print('\n'.join(L[i0+1:]))

# ---- run 8 ----
C,D='C','D'
pay={(C,C):3,(C,D):0,(D,C):5,(D,D):1}
S={21:lambda h:C,22:lambda h:D,23:lambda h:C if not h else h[-1][1],24:lambda h:D if not h else h[-1][1],
25:lambda h:C if all(x[1]!=D for x in h) else D,26:lambda h:C if not h or h[-1][0]==h[-1][1] else D}
def score(a,b,n):
    ha=[];hb=[];t=0
    for _ in range(n):
        x=S[a](ha);y=S[b](hb);ha.append((x,y));hb.append((y,x));t+=pay[(x,y)]
    return t
claims={(23,23):2*256+241,(22,22):251,(23,22):250,(22,23):255,(21,22):0,(22,21):4*256+231,(26,22):125,(22,26):2*256+243,(23,24):2*256+113,(24,23):2*256+118,(25,24):254,(24,25):254}
print(all(score(a,b,251)==v for (a,b),v in claims.items()))
tot={a:sum(score(a,b,251) for b in S) for a in S}; print(tot)
print({23:15*256+47,21:14*256+178,26:14*256+56,25:13*256+188,22:11*256+206,24:10*256+84})
# physics checks
k=8.617333e-5; E21=13.605693*0.75
print(E21*(256+46)/2**17/k, E21*(256+47)/2**17/k)
TP=1.416784e32; print(156/2**106*TP,157/2**106*TP)
# section sizes
bounds=[('counting/number literals',0,268),('arith & numbers',268,1717),('logic, lists, quantifiers, number sets, exp/complex',1717,4888),('fold/map/mean/probability',4888,5592),('quote/type/eval',5592,6691),('physics',6691,9933),('chemistry/molecules',9933,10445),('game',10445,12102)]
for n,a,b in bounds: print(n,b-a,round((b-a)/12102*100,1))

# ---- run 9 ----
s=open('/work/bits.txt').read().strip()
print(s[:172]==s[-172:], [len(x) for x in s[:172].split('0')], (len(s)-344)/16)
import pickle
t=pickle.load(open('/work/t.pkl','rb'))
print(t[:14], t[12:16], t[266:270])
L=open('/work/out.txt').read().split('\n')
print(sum(1 for l in L if '(W36' in l), len(L)-268)
