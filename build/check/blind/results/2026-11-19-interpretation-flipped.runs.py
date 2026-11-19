# The code the blind reader ran, in order (2026-11-19, interpretation, full message with every bit inverted, Opus).

# ---- run 1 ----
s=open('/work/bits.txt').read().strip()
print(len(s), set(s), s.count('1'))
print(s[:600])
import sympy
print(sympy.factorint(len(s)))

# ---- run 2 ----
s=open('/work/bits.txt').read().strip()
ones=[i for i,c in enumerate(s[:400]) if c=='1']
print(ones[:15])
import re
# factor
n=len(s);f=[];m=n;d=2
while d*d<=m:
    while m%d==0:f.append(d);m//=d
    d+=1
if m>1:f.append(m)
print(f)
# runs structure
runs=[(m.group()[0],len(m.group())) for m in re.finditer(r'0+|1+',s)]
print(len(runs)); print(runs[:40])

# ---- run 3 ----
s=open('/work/bits.txt').read().strip()
h=171  # header end index: zero run ends at 171
print(s[130:200])
r=s[172:]
print(len(r))
inv=''.join('1' if c=='0' else '0' for c in r)
print(inv[:800])
print(inv.count('1')/len(inv))

# ---- run 4 ----
print(len(inv)%16, len(inv)/16)
w=[int(inv[i:i+16],2) for i in range(0,len(inv)-len(inv)%16,16)]
print(w[:200])

# ---- run 5 ----
s=open('/work/bits.txt').read().strip()
r=s[172:]
inv=''.join('1' if c=='0' else '0' for c in r)
open('/work/inv.txt','w').write(inv)
print(len(inv)%16, len(inv)/16)
w=[int(inv[i:i+16],2) for i in range(0,len(inv)-len(inv)%16,16)]
print(w[:300])

# ---- run 6 ----
inv=open('/work/inv.txt').read()
w=[int(inv[i:i+16],2) for i in range(0,len(inv)-len(inv)%16,16)]
print(inv[-40:])
from collections import Counter
c=Counter(x for x in w if x>255)
print(sorted(c.items()))
print(len(w))

# ---- run 7 ----
inv=open('/work/inv.txt').read()
w=[int(inv[i:i+16],2) for i in range(0,len(inv)-len(inv)%16,16)]
def nm(x):
    if x<256: return str(x)
    if x==256: return '['
    if x==257: return ']'
    return f'{chr(ord("A")+(x>>8)-2)}{x&255}'
# locate sentences
start=w.index(256)
print(start)
sents=[];cur=None;outside=[]
for i,x in enumerate(w[start:],start):
    if x==256: cur=[];si=i
    elif x==257: sents.append((si,cur));cur=None
    elif cur is not None: cur.append(x)
    else: outside.append((i,x))
print(len(sents), outside[:50], len(outside))
out=[]
for si,c in sents: out.append(f'{si}: '+' '.join(map(nm,c)))
open('/work/sents.txt','w').write('\n'.join(out))
print('\n'.join(out[:150]))

# ---- run 8 ----
inv=open('/work/inv.txt').read()
w=[int(inv[i:i+16],2) for i in range(0,len(inv)-len(inv)%16,16)]
def nm(x):
    if x<256: return str(x)
    if x==256: return '['
    if x==257: return ']'
    return f'{chr(ord("A")+(x>>8)-2)}{x&255}'
print(' '.join(nm(x) for x in w[268:1300]))

# ---- run 9 ----
code=r'''
inv=open('/work/inv.txt').read()
w=[int(inv[i:i+16],2) for i in range(0,len(inv)-len(inv)%16,16)]
N={}
def nm(x):
    if x<256: return str(x)
    if x in N: return N[x]
    return f'{chr(ord("A")+(x>>8)-2)}{x&255}'
def parse(i):
    # parse expression starting at w[i]==256; return (tree,next)
    assert w[i]==256
    i+=1; t=[]
    while w[i]!=257:
        if w[i]==256:
            sub,i=parse(i); t.append(sub)
        else: t.append(w[i]); i+=1
    return t,i+1
def top(start=268):
    out=[];i=start
    while i<len(w):
        if w[i]==256:
            t,j=parse(i); out.append((i,t)); i=j
        else:
            out.append((i,('RAW',w[i]))); i+=1
    return out
def fmt(t):
    if isinstance(t,tuple): return '<RAW %d>'%t[1]
    if isinstance(t,list): return '('+' '.join(fmt(x) for x in t)+')'
    return nm(t)
'''
open('/work/h.py','w').write(code)
exec(code)
T=top()
print(len(T), [x for x in T if isinstance(x[1],tuple)][:20])
print(w[:268][-20:])

# ---- run 10 ----
exec(open('/work/h.py').read())
T=top()
lines=[f'{k:4d} {i:6d} '+fmt(t) for k,(i,t) in enumerate(T)]
open('/work/stm.txt','w').write('\n'.join(lines))
s=open('/work/bits.txt').read().strip()
print(s[-172:])
print('\n'.join(lines[130:260]))

# ---- run 11 ----
L=open('/work/stm.txt').read().split('\n')
print('\n'.join(l[:220] for l in L[100:130]))
print('\n'.join(l[:220] for l in L[260:420]))

# ---- run 12 ----
L=open('/work/stm.txt').read().split('\n')
print('\n'.join(l[:200] for l in L[420:600]))

# ---- run 13 ----
L=open('/work/stm.txt').read().split('\n')
print('\n'.join(l[:200] for l in L[600:790]))

# ---- run 14 ----
L=open('/work/stm.txt').read().split('\n')
print('\n'.join(l[:230] for l in L[790:1000]))

# ---- run 15 ----
L=open('/work/stm.txt').read().split('\n')
for k in [443,510,543,553,554,555,830,831,987]: print(L[k]);print()

# ---- run 16 ----
exec(open('/work/h.py').read())
from fractions import Fraction as Fr
import itertools, math
s=open('/work/bits.txt').read().strip()
print('trailer==header', s[-172:]==s[:172], s[:172].count('1'))
T=top()
body=w[:19111]
# self reference: B13 = word stream? check index claims
print([body[k-1] for k in (1,2,4,12,13)])
def occ(seq,sub):
    return sum(1 for i in range(len(seq)-len(sub)+1) if seq[i:i+len(sub)]==sub)
for e in [[513,1,1],[513,3,3],[514,0,1],[513,5,5],[513,2,3],[515,3,2],[513,6,6],[515,5,6]]:
    print(e, occ(body,[256]+e+[257]))
# evaluator
class U(Exception):pass
def ev(t,env={}):
    if isinstance(t,int):
        if t<256: return t
        if t in env: return env[t]
        if t==0x301: return True
        if t==0x302: return False
        raise U(t)
    h=t[0]; a=t[1:]
    if h==0x209: # base256
        v=0
        for x in a: v=v*256+ev(x,env)
        return v
    if h==0x240: # let
        e2=dict(env); e2[a[0]]=ev(a[1],env); return ev(a[2],e2)
    if h==0x226 and False: pass
    if h==0x238: return ('Q',repr(a[0]))
    if h==0x229: return ev(a[1],env) if ev(a[0],env) else ev(a[2],env)
    if h in (0x214,0x215,0x222):
        if h==0x214: return all(ev(x,env) for x in a)
        if h==0x215: return any(ev(x,env) for x in a)
        return (not ev(a[0],env)) or ev(a[1],env)
    if h in (0x220,0x221,0x224):
        S=ev(a[1],env)
        if not isinstance(S,list): raise U('set')
        vals=[]
        for x in S:
            e2=dict(env);e2[a[0]]=x; vals.append(ev(a[2],e2))
        return all(vals) if h==0x220 else any(vals) if h==0x221 else vals
    v=[ev(x,env) for x in a]
    if h==0x223:
        op=a[0]; L=v[1]; return ev([op]+L,env) if False else ap(op,L)
    return ap(h,v)
def ap(h,v):
    if h==0x201: return all(x==v[0] for x in v)
    if h==0x202: return v[0]!=v[1]
    if h==0x203: return all(v[i]<v[i+1] for i in range(len(v)-1))
    if h==0x204: return all(v[i]>v[i+1] for i in range(len(v)-1))
    if h==0x205: return all(v[i]<=v[i+1] for i in range(len(v)-1))
    if h==0x206: return all(v[i]>=v[i+1] for i in range(len(v)-1))
    if h==0x207: return sum(v[1:],v[0]) if not isinstance(v[0],list) else None
    if h==0x208: return math.prod(v)
    if h==0x20a: return v[0]-v[1]
    if h==0x20b: return -v[0]
    if h==0x20c: return Fr(v[0])/v[1]
    if h==0x20d: return not v[0]
    if h==0x210: return list(v)
    if h==0x211: return len(v[0])
    if h==0x212: return v[0][v[1]-1]
    if h==0x213: return v[1].count(v[0])
    if h==0x219: return Fr(sum(v[0]))/len(v[0])
    if h==0x21a: return Fr(v[1].count(v[0]),len(v[1]))
    if h==0x21b: return [[x,y] for x in v[0] for y in v[1]]
    if h==0x21c: return v[0][1:]
    if h==0x21e: return Fr(v[0])**v[1]
    if h==0x21f: return abs(v[0])
    if h==0x221: pass
    raise U(h)
ok=bad=un=0;badl=[]
for k,(i,t) in enumerate(T[:989]):
    try:
        r=ev(t)
        if r is True: ok+=1
        else: bad+=1;badl.append((k,r))
    except Exception as e: un+=1
print(ok,bad,un,badl[:20])

# ---- run 17 ----
exec(open('/work/h.py').read())
T=top()
tops=[t for i,t in T[:989]]
B13=list(range(0))+w[:268]+tops   # numbers then statements
print(len(B13), B13[0],B13[1],B13[3],B13[11],B13[12])
for e in [[513,1,1],[513,3,3],[514,0,1],[513,5,5],[513,2,3],[515,3,2],[513,[519,2,2],5],[513,6,6],[515,5,6],[513,[519,3,3],6]]:
    print(e, sum(1 for x in tops if x==e))
# PD: cost matrix, C=B44 D=B45
C,D='C','D'
cost={(C,C):3,(D,D):5,(C,D):7,(D,C):2}
def strat(name,my,op,rng=None):
    if name=='ALLC':return C
    if name=='ALLD':return D
    if name=='TFT':return C if not op else op[-1]
    if name=='STFT':return D if not op else op[-1]
    if name=='GRIM':return D if D in op else C
    if name=='PAV':return C if not op or my[-1]==op[-1] else D
S=['ALLC','ALLD','TFT','STFT','GRIM','PAV']
def play(a,b,n):
    ha,hb=[],[]
    for _ in range(n):
        x=strat(a,ha,hb);y=strat(b,hb,ha);ha.append(x);hb.append(y)
    return sum(cost[(x,y)] for x,y in zip(ha,hb))
print('TFT v ALLC 4', play('TFT','ALLC',4))
pairs=[('TFT','TFT'),('ALLC','ALLC'),('TFT','ALLC'),('ALLC','TFT'),('ALLD','ALLC'),('ALLC','ALLD'),('PAV','ALLC'),('ALLC','PAV'),('TFT','STFT'),('STFT','TFT'),('GRIM','STFT'),('STFT','GRIM')]
print([play(a,b,255) for a,b in pairs])
print([2*256+253,4*256+251,4*256+253,4*256+248,6*256+249,1*256+254,5*256+251,3*256+123,4*256+126,4*256+121,4*256+250,4*256+250])
for a in S: print(a, sum(play(a,b,255) for b in S))
print({'TFT':21*256+111,'GRIM':21*256+235,'ALLD?B48':21*256+238,'PAV':22*256+149,'B49':25*256+95,'STFT':27*256+11})

# ---- run 18 ----
exec(open('/work/h.py').read())
T=top()
first={}
def walk(t,k):
    if isinstance(t,list):
        for x in t: walk(x,k)
    elif isinstance(t,int) and t>257: first.setdefault(t,k)
for k,(i,t) in enumerate(T[:989]): walk(t,k)
print(len(first))
print(' '.join(f'{nm(x)}@{k}' for x,k in sorted(first.items())))
# checks of CMB frame feasibility
import random,math
cnt=0
for _ in range(200000):
    a=random.uniform(.25,.5);c=random.uniform(-1,-.75)
    if a*a+c*c>1: continue
    b=random.choice([1,-1])*math.sqrt(1-a*a-c*c)
    d=random.uniform(.5,1);f=random.uniform(.25,.75)
    if d*d+f*f>=1: continue
    e=math.sqrt(1-d*d-f*f)
    if not(1/8<e<7/8): continue
    if abs(a*d+b*e+c*f)<0.02: cnt+=1
print('feasible samples',cnt)
