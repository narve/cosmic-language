# The code the blind reader ran, in order (2026-11-17, purpose-code, core message, losses 2 3 5 7).

# ---- run 1 ----
s=open('/work/bits.txt').read().strip()
print(len(s),s.count('1'),s.count('0'))
print(s[:2000])
n=len(s)
def f(n):
    return [d for d in range(2,n) if n%d==0][:40]
print(f(n))
# autocorrelation
import collections
for lag in range(1,65):
    m=sum(1 for i in range(0,min(n-lag,200000)) if s[i]==s[i+lag])
    print(lag,round(m/min(n-lag,200000),3),end='; ')

# ---- run 2 ----
s=open('/work/bits.txt').read().strip()
i=s.find('0000000000000001')
print(i, s[:i+2])
# find preamble end: unary primes
import re
pre=re.match(r'(1+0)+',s).group(0)
print(len(pre),[len(x) for x in pre.split('0')])
for off in (len(pre)-1,len(pre),len(pre)+1):
    r=s[off:]
    print(off,len(r)%16,[int(r[k:k+16],2) for k in range(0,16*30,16)])

# ---- run 3 ----
s=open('/work/bits.txt').read().strip()
r=s[172:]
w=[int(r[k:k+16],2) for k in range(0,len(r)-15,16)]
print(len(w),len(r)%16, r[-12-32:])
import collections
c=collections.Counter(w)
print(len(c)); print(sorted(c.items())[:50]); print(c.most_common(60))
print(w[:400]); print(w[-200:])

# ---- run 4 ----
s=open('/work/bits.txt').read().strip()
r=s[172:]
t=s[-172:]
print([len(x) for x in t.split('0')])
r=s[172:-172]; print(len(r)%16)
w=[int(r[k:k+16],2) for k in range(0,len(r),16)]
print(len(w))
def name(x):
    if x<256: return str(x)
    if x==256: return '('
    if x==257: return ')'
    return {2:'F',3:'K',4:'v'}.get(x>>8,'?%d_'%(x>>8))+str(x&255)
# split top-level
out=[];d=0;cur=[];pos=[]
start=0
for i,x in enumerate(w):
    if x==256:
        if d==0: start=i
        d+=1
    cur.append(name(x))
    if x==257:
        d-=1
    if d==0:
        out.append((start if cur[0]=='(' else i,' '.join(cur)));cur=[]
print(len(out),d)
open('/work/dec.txt','w').write('\n'.join(f'{a} {b}' for a,b in out))
import collections
print(collections.Counter(x>>8 for x in w))
for a,b in out[:600]: print(a,b)

# ---- run 5 ----
L=open('/work/dec.txt').read().split('\n')
for l in L[600:]: print(l)

# ---- run 6 ----

from fractions import Fraction as Q
import itertools,sys
sys.setrecursionlimit(10000)
s=open('/work/bits.txt').read().strip()
r=s[172:-172]
w=[int(r[k:k+16],2) for k in range(0,len(r),16)]
def parse(i):
    x=w[i]
    if x==256:
        i+=1;l=[]
        while w[i]!=257:
            e,i=parse(i);l.append(e)
        return l,i+1
    if x<256: return x,i+1
    return ({2:'F',3:'K',4:'v'}[x>>8]+str(x&255)),i+1
stm=[];i=0
while i<len(w):
    st=i;e,i=parse(i);stm.append((st,e))
NAT=list(range(0,12))+[255,256,300]
RAT=sorted(set([Q(a,b) for a in range(-6,7) for b in range(1,7)]+[Q(255),Q(1,3),Q(2,3)]))
C,D='K18','K19'
pay={(C,C):3,(D,D):5,(C,D):7,(D,C):2}
STR=['K22','K23','K24','K25','K26','K27']
class Hist(list): pass
def strat(k,h):
    opp=[x[1] for x in h]
    if k=='K22': return [C]
    if k=='K23': return [D]
    if k=='K24': return [C] if not h else [opp[-1]]
    if k=='K25': return [D] if not h else [opp[-1]]
    if k=='K26': return [C] if D not in opp else [D]
    if k=='K27': return [C] if not h or h[-1][0]==h[-1][1] else [D]
    if k=='K28': return [C] if not h or opp[-1]==C else [C,D,D]
    if k=='K29': return [C,D]
import functools
@functools.lru_cache(None)
def play(a,b,n):
    h=[]
    for _ in range(n):
        x=strat(a,h)[0]; y=strat(b,[[q,p] for p,q in h])[0]
        h.append([x,y])
    return h
def hists():
    # sample histories for K21
    out=[[]]
    for n in (1,2,3):
        for m in itertools.product([C,D],repeat=2*n):
            out.append([[m[2*j],m[2*j+1]] for j in range(n)])
    return out
def dom(k):
    return {'K3':NAT,'K4':RAT,'K20':[C,D],'K21':hists(),'K30':STR}[k]
def chain(a,f): return all(f(a[j],a[j+1]) for j in range(len(a)-1))
def ev(e,env):
    if isinstance(e,int): return e
    if isinstance(e,str):
        if e[0]=='v': return env[e]
        if e=='K1': return True
        if e=='K2': return False
        if e=='K20': return [C,D]
        if e=='K30': return STR
        if e in('K3','K4','K21'): return dom(e)
        return e
    h=e[0]; a=e[1:]
    if h in('F20','F21','F24'):
        d=ev(a[1],env)
        g=(ev(a[2],{**env,a[0]:x}) for x in d)
        return all(g) if h=='F20' else any(g) if h=='F21' else list(g)
    if h=='F22': return (not ev(a[0],env)) or ev(a[1],env)
    if h=='F29': return ev(a[1],env) if ev(a[0],env) else ev(a[2],env)
    if h=='F23':
        l=ev(a[1],env); op=a[0]
        if op=='F7': return sum(l)
        if op=='F8':
            p=1
            for x in l:p*=x
            return p
        if op=='F3': return chain(l,lambda x,y:x<y)
    if h=='F14': return all(ev(x,env) for x in a)
    if h=='F15': return any(ev(x,env) for x in a)
    v=[ev(x,env) for x in a]
    if h=='F1': return chain(v,lambda x,y:x==y)
    if h=='F2': return v[0]!=v[1]
    if h=='F3': return chain(v,lambda x,y:x<y)
    if h=='F4': return chain(v,lambda x,y:x>y)
    if h=='F5': return chain(v,lambda x,y:x<=y)
    if h=='F6': return chain(v,lambda x,y:x>=y)
    if h=='F7': return sum(v)
    if h=='F8':
        p=1
        for x in v:p*=x
        return p
    if h=='F9':
        n=0
        for x in v:n=n*256+x
        return n
    if h=='F10': return v[0]-v[1]
    if h=='F11': return -v[0]
    if h=='F12': return Q(v[0])/Q(v[1])
    if h=='F13': return not v[0]
    if h=='F16': return v
    if h=='F17': return len(v[0])
    if h=='F18': return v[0][v[1]-1]
    if h=='F19': return v[1].count(v[0])
    if h=='F25': return Q(sum(v[0]),len(v[0]))
    if h=='F26': return Q(v[1].count(v[0]),len(v[1]))
    if h=='F27': return [[x,y] for x in v[0] for y in v[1]]
    if h=='F28': return v[0][1:]
    if h=='F64': return pay[(v[0],v[1])]
    if h=='F65': return strat(v[0],v[1])
    if h=='F66': return play(v[0],v[1],v[2])
    if h=='F67': return sum(pay[(x,y)] for x,y in play(v[0],v[1],v[2]))
    raise Exception(h)
bad=0
for st,e in stm:
    if isinstance(e,int): continue
    try:
        v=ev(e,{})
    except Exception as ex:
        v='ERR '+repr(ex)
    if v is not True: bad+=1;print(st,v,e)
print('checked',sum(1 for _,e in stm if not isinstance(e,int)),'bad',bad)
for k in STR: print(k, sum(sum(pay[(x,y)] for x,y in play(k,j,255)) for j in STR))

# ---- run 7 ----

from fractions import Fraction as Q
# the four statements, checked with domains closed enough for the claim
N=range(0,40)
# 2680: forall n exists m: m = n+1
print(all(any(m==n+1 for m in range(0,41)) for n in N))
# 3184: every natural is a rational (n = n/1)
print(all(Q(n,1)==n for n in N))
# 3199: forall a,b natural, a/(b+1) is a rational
print(all(isinstance(Q(a,b+1),Q) for a in N for b in N))
# 3387: forall rational x exists rational y: x+y=0
R=[Q(a,b) for a in range(-9,10) for b in range(1,7)]
print(all(any(x+y==0 for y in R) for x in R))
# section sizes in words (of 6114 + 344 preamble/trailer bits)
bounds=[('number list (primes, 0..255)',0),('equality/order',268),('arithmetic + - * / neg, base-256',593),('truth values, logic',1717),('lists',2000),('quantifiers, number sets',2262),('implication',3406),('fold/map/mean/probability/product/tail/if',3504),('game: moves, payoffs',4307),('strategies',4513),('match + score definitions',5181),('worked examples, stochastic',5474),('tournament results',5654),('conclusion',5960),('end',6114)]
for (n,a),(_,b) in zip(bounds,bounds[1:]): print(f'{n:45s} {b-a:5d} words {100*(b-a)/6114:5.1f}%')
