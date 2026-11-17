# The code the blind reader ran, in order (2026-11-17, last-statement-code).

# ---- run 1 ----
s=open('/work/bits.txt').read().strip()
print(len(s))
print(s[:600])
print(s[-300:])
n=len(s)
print([d for d in range(1,200) if n%d==0])
import collections
for k in (2,3,4,5,6,7,8,9,10,12,16):
    c=collections.Counter(s[i:i+k] for i in range(0,n-k+1,k))
    print(k,len(c),c.most_common(6))

# ---- run 2 ----
s=open('/work/bits.txt').read().strip()
import re,collections
m=re.match(r'(1+0)+1+',s); pre=m.group(0); print(len(pre),[len(x) for x in pre.split('0')])
# trailer
i=s.rfind('00'); 
t=s[::-1]; m2=re.match(r'(1+0)+1+',t); print(len(m2.group(0)),[len(x) for x in m2.group(0).split('0')])
body=s[len(pre):len(s)-len(m2.group(0))]
print(len(body),len(body)%16,len(body)%8)
w=[int(body[i:i+16],2) for i in range(0,len(body),16)]
print(len(w)); print(w[:200])
c=collections.Counter(w); print(len(c)); print(sorted(c.items())[:300])

# ---- run 3 ----
s=open('/work/bits.txt').read().strip()
body=s[172:-172]
w=[int(body[i:i+16],2) for i in range(0,len(body),16)]
print(len(w))
def tok(x):
    if x==256: return '('
    if x==257: return ')'
    if x>=512: return 'S%d'%(x-512)
    return str(x)
# split top-level
out=[];depth=0;cur=[];starts=[]
top=[]
for i,x in enumerate(w):
    if depth==0 and x!=256: top.append((i,x))
    if x==256:
        if depth==0: st=i
        depth+=1
    cur.append(tok(x))
    if x==257:
        depth-=1
        if depth==0: out.append((st,i,' '.join(cur)));cur=[]
    elif depth==0: cur=[]
print(len(out),depth,len(top),top[:20],top[-5:])
import collections
print(collections.Counter(len(o[2].split()) for o in out).most_common(10))
for o in out[:150]: print(o[0],o[2])

# ---- run 4 ----
s=open('/work/bits.txt').read().strip()
body=s[172:-172]
w=[int(body[i:i+16],2) for i in range(0,len(body),16)]
def tok(x):
    if x==256: return '('
    if x==257: return ')'
    if x>=512: return 'S%d'%(x-512)
    return str(x)
out=[];depth=0;cur=[]
for i,x in enumerate(w):
    if x==256:
        if depth==0: st=i
        depth+=1
    cur.append(tok(x))
    if x==257:
        depth-=1
        if depth==0: out.append((st,i,' '.join(cur)));cur=[]
    elif depth==0: cur=[]
import pickle; pickle.dump(out,open('/work/out.pkl','wb'))
print(out[-1], len(w))
for o in out[-12:]: print(o[0],o[1],o[2]);print()
for o in out[150:330]: print(o[0],o[2])

# ---- run 5 ----
import pickle
out=pickle.load(open('/work/out.pkl','rb'))
for o in out[330:]:
    t=o[2]
    print(o[0],t if len(t)<420 else t[:420]+' ...')

# ---- run 6 ----
import pickle
out=pickle.load(open('/work/out.pkl','rb'))
for o in out:
    if o[0]>=10500: print(o[0],o[1],o[2])
print([ (o[0],o[2]) for o in out if 'S283' in o[2]][:3])
print(len(out), 172+11326*16, 172+11372*16)
import re,collections
c=collections.Counter()
for o in out:
    for t in set(re.findall(r'S(?:65|66|67|283)\b',o[2])): c[t]+=1
print(c)
