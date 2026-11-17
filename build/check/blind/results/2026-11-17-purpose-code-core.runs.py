# The code the blind reader ran, in order (2026-11-17, purpose-code, core message only).

# ---- run 1 ----
s=open('/work/bits.txt').read().strip()
print(len(s), s.count('1'), s.count('0'))
print(s[:600])
n=len(s)
def f(n):
    return [d for d in range(2,int(n**.5)+1) if n%d==0]
print(f(n))
import re,collections
runs=collections.Counter(len(m.group()) for m in re.finditer('1+',s))
print(sorted(runs.items()))
runs=collections.Counter(len(m.group()) for m in re.finditer('0+',s))
print(sorted(runs.items()))

# ---- run 2 ----
s=open('/work/bits.txt').read().strip()
i=s.find('0'*8); print(i)
for off in range(165,180):
    r=s[off:]
    if len(r)%16==0: print('off',off,len(r)//16)
# find end unary as well
print(s[-400:])

# ---- run 3 ----
s=open('/work/bits.txt').read().strip()
b=s[172:-172]
print(len(b)/16)
w=[int(b[i:i+16],2) for i in range(0,len(b),16)]
import collections
c=collections.Counter(w)
print(len(c)); print(sorted(c.items()))
print(w[:400])
by=[int(b[i:i+8],2) for i in range(0,len(b),8)]
print(sorted(collections.Counter(by).items()))

# ---- run 4 ----
s=open('/work/bits.txt').read().strip()
b=s[172:-172]
w=[int(b[i:i+16],2) for i in range(0,len(b),16)]
def tok(x):
    h,l=x>>8,x&255
    if h==0: return str(l)
    if x==256: return '('
    if x==257: return ')'
    return 'ABCDE'[h-2]+str(l)
# find start of bracketed part
i=w.index(256)
print(w[:i][:15], i)
out=[];depth=0;cur=[]
lines=[]
for x in w[i:]:
    cur.append(tok(x))
    if x==256: depth+=1
    if x==257:
        depth-=1
        if depth==0: lines.append(' '.join(cur)); cur=[]
print(len(lines), cur)
open('/work/lines.txt','w').write('\n'.join(lines))
for k,l in enumerate(lines[:330]): print(k,l)

# ---- run 5 ----
L=open('/work/lines.txt').read().split('\n')
for k,l in enumerate(L[319:],319): print(k,l)

# ---- run 6 ----

from fractions import Fraction as F
import itertools, random, operator, functools
L=open('/work/lines.txt').read().split('\n')
def parse(toks):
    t=toks.pop(0)
    if t=='(':
        r=[]
        while toks[0]!=')': r.append(parse(toks))
        toks.pop(0); return r
    return t
C,D='B18','B19'
NAT=[0,1,2,3,4,5,7,9,16,100,255,256,1000]
RAT=[F(0),F(1),F(-1),F(1,2),F(2,3),F(-7,3),F(5),F(22,7),F(-100),F(1,1000)]
random.seed(1)
def rh():
    return tuple((random.choice([C,D]),random.choice([C,D])) for _ in range(random.randint(0,6)))
HIST=[()]+[rh() for _ in range(40)]
STR=('B21','B22','B23','B24','B25','B26')
def dom(d,env):
    if d=='B3': return NAT
    if d=='B4': return RAT
    if d=='B20': return HIST
    return ev(d,env)
def strat(n,h):
    if n=='B21': return (C,)
    if n=='B22': return (D,)
    if n=='B23': return (C,) if not h else (h[-1][1],)
    if n=='B24': return (D,) if not h else (h[-1][1],)
    if n=='B25': return (C,) if all(x[1]!=D for x in h) else (D,)
    if n=='B26': return (C,) if not h or h[-1][0]==h[-1][1] else (D,)
    if n=='B27': return (C,) if not h or h[-1][1]==C else (C,D,D)
    if n=='B28': return (C,D)
PAY={(C,C):3,(C,D):0,(D,C):5,(D,D):1}
def play(a,b,n):
    h=();g=()
    for _ in range(n):
        x=strat(a,h)[0]; y=strat(b,g)[0]
        h+=((x,y),); g+=((y,x),)
    return h
def chain(op,v): return all(op(a,b) for a,b in zip(v,v[1:]))
def ev(e,env):
    if isinstance(e,str):
        if e in env: return env[e]
        if e[0]=='A' and False: pass
        if e=='B1': return True
        if e=='B2': return False
        if e=='B29': return STR
        if e[0] in 'AB': return e
        return F(int(e))
    op=e[0]; a=e[1:]
    if op in('A20','A21'):
        vals=[ev(a[2],{**env,a[0]:x}) for x in dom(a[1],env)]
        return all(vals) if op=='A20' else any(vals)
    if op=='A24': return tuple(ev(a[2],{**env,a[0]:x}) for x in dom(a[1],env))
    if op=='A22': return (not ev(a[0],env)) or ev(a[1],env)
    if op=='A29': return ev(a[1],env) if ev(a[0],env) else ev(a[2],env)
    if op=='A23':
        o=a[0]; v=ev(a[1],env)
        if o=='A7': return sum(v)
        if o=='A8': return functools.reduce(operator.mul,v)
        if o=='A3': return chain(operator.lt,v)
        raise Exception(o)
    v=[ev(x,env) for x in a]
    if op=='A1': return chain(operator.eq,v)
    if op=='A2': return v[0]!=v[1]
    if op=='A3': return chain(operator.lt,v)
    if op=='A4': return chain(operator.gt,v)
    if op=='A5': return chain(operator.le,v)
    if op=='A6': return chain(operator.ge,v)
    if op=='A7': return sum(v)
    if op=='A8': return functools.reduce(operator.mul,v)
    if op=='A9': return functools.reduce(lambda x,y:x*256+y,v)
    if op=='A10': return v[0]-v[1]
    if op=='A11': return -v[0]
    if op=='A12': return F(v[0])/v[1]
    if op=='A13': return not v[0]
    if op=='A14': return all(v)
    if op=='A15': return any(v)
    if op=='A16': return tuple(v)
    if op=='A17': return len(v[0])
    if op=='A18': return v[0][int(v[1])-1]
    if op=='A19': return v[1].count(v[0])
    if op=='A25': return F(sum(v[0]))/len(v[0])
    if op=='A26': return F(v[1].count(v[0]),len(v[1]))
    if op=='A27': return tuple(itertools.product(v[0],v[1]))
    if op=='A28': return v[0][1:]
    if op=='A64': return PAY[(v[0],v[1])]
    if op=='A65': return strat(v[0],v[1])
    if op=='A66': return play(v[0],v[1],int(v[2]))
    if op=='A67': return sum(PAY[x] for x in play(v[0],v[1],int(v[2])))
    raise Exception(op)
bad=[]
for k,l in enumerate(L):
    try:
        r=ev(parse(l.split()),{})
    except Exception as ex: r='ERR %r'%ex
    if r is not True: bad.append((k,r,l))
for b in bad: print(b)
print(len(bad))
tot={s:sum(sum(PAY[x] for x in play(s,t,255)) for t in STR) for s in STR}
print(tot)
# sizes
import bisect
n=[len(l.split()) for l in L]
def share(a,b): return sum(n[a:b]), round(100*sum(n[a:b])/5976,1)
for a,b in [(0,158),(158,186),(186,203),(203,274),(274,281),(281,319),(319,380)]: print(a,b,share(a,b))
print(268/5976)

# ---- run 7 ----

C,D='C','D'
import random
random.seed(2)
def pav(h): return C if not h or h[-1][0]==h[-1][1] else D
def gtft(h): return (C,) if not h or h[-1][1]==C else (C,D,D)
ok=True
for _ in range(2000):
    h=tuple((random.choice([C,D]),random.choice([C,D])) for _ in range(random.randint(0,6)))
    # stmts 334/335 (lazy and): nonempty & last own==last other -> C ; != -> D
    if len(h)>0 and h[-1][0]==h[-1][1]: ok&= pav(h)==C
    if len(h)>0 and h[-1][0]!=h[-1][1]: ok&= pav(h)==D
    if len(h)>0 and h[-1][1]==C: ok&= gtft(h)==(C,)
    if len(h)>0 and h[-1][1]==D: ok&= gtft(h)==(C,D,D)
print(ok)
L=open('/work/lines.txt').read().split('\n')
print(sum(len(l.split()) for l in L)+268, len(L))
