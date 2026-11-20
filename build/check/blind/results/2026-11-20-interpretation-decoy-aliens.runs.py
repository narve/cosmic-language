# The code the blind reader ran, in order (2026-11-20, interpretation, decoy message (Kepler-1647, invented senders), Opus).
# Received: the decoy repeated 5 times, cut inside the first and last copy, every bit inverted, as /work/received.bin.

# ---- run 1 ----

import os
d=open('/work/received.bin','rb').read()
print(len(d),len(d)*8)
print(d[:64].hex())
from collections import Counter
print(Counter(d).most_common(10))
os.listdir('/work')

# ---- run 2 ----

import numpy as np
b=np.unpackbits(np.frombuffer(d,dtype=np.uint8))
print(b.mean())
n=len(b)
def fac(n):
    f=[];p=2
    while p*p<=n:
        while n%p==0:f.append(p);n//=p
        p+=1
    if n>1:f.append(p)
    return f
print(fac(n))
s=''.join(map(str,b[:600]));print(s)
# runs
z=np.where(b==0)[0]
gaps=np.diff(z);print(Counter(gaps).most_common(20))

# ---- run 3 ----

from collections import Counter
d=open('/work/received.bin','rb').read()
b=''.join(format(x,'08b') for x in d)
open('/work/bits.txt','w').write(b)
n=len(b)
print(b.count('1')/n)
def fac(n):
    f=[];p=2
    while p*p<=n:
        while n%p==0:f.append(p);n//=p
        p+=1
    if n>1:f.append(p)
    return f
print(fac(n))
print(b[:800])
import re
print(Counter(len(m) for m in re.findall('0+',b)).most_common(10))
print(Counter(len(m) for m in re.findall('1+',b)).most_common(20))

# ---- run 4 ----

b=open('/work/bits.txt').read()
N=200000
x=[1 if c=='1' else 0 for c in b[:N]]
import math
res=[]
for lag in range(1,200):
    s=sum(1 for i in range(N-lag) if x[i]==x[i+lag])
    res.append((s/(N-lag),lag))
print(sorted(res,reverse=True)[:20])

# ---- run 5 ----

for off in range(8):
    print(off, b[off::8].count('0')/ (len(b)//8))
d=open('/work/received.bin','rb').read()
print(Counter(d).most_common(40))
print(len(Counter(d)))

# ---- run 6 ----

from collections import Counter
b=open('/work/bits.txt').read()
for off in range(8):
    print(off, b[off::8].count('0')/ (len(b)//8))
d=open('/work/received.bin','rb').read()
print([(format(k,'08b'),v) for k,v in Counter(d).most_common(40)])
print(len(Counter(d)))

# ---- run 7 ----

from collections import Counter
b=open('/work/bits.txt').read()
W=20000
for i in range(0,len(b),W):
    seg=b[i:i+W]
    c=Counter(seg[j:j+8] for j in range(0,len(seg)-7,8))
    print(i, round(seg.count('1')/len(seg),3), c.most_common(4))

# ---- run 8 ----

b=open('/work/bits.txt').read()
for st in [1000,100000,300000]:
    pat=b[st:st+300]
    pos=[];i=-1
    while True:
        i=b.find(pat,i+1)
        if i<0:break
        pos.append(i)
    print(st,pos,[pos[k+1]-pos[k] for k in range(len(pos)-1)])

# ---- run 9 ----

b=open('/work/bits.txt').read()
P=359422
n=len(b)
diff=[i for i in range(n-P) if b[i]!=b[i+P]]
print(len(diff), diff[:50])
print(n-3*P, n/P)
def fac(n):
    f=[];p=2
    while p*p<=n:
        while n%p==0:f.append(p);n//=p
        p+=1
    if n>1:f.append(p)
    return f
print(fac(P))

# ---- run 10 ----

P=359422
def fac(n):
    f=[];p=2
    while p*p<=n:
        while n%p==0:
            f.append(p);n//=p
        p+=1
    if n>1:f.append(n)
    return f
print(fac(P), fac(1339312), fac(261046))

# ---- run 11 ----

import re
b=open('/work/bits.txt').read()
P=359422
c=b[:P]
open('/work/cycle.txt','w').write(c)
# longest runs
for ch in '01':
    runs=sorted(((m.end()-m.start(),m.start()) for m in re.finditer(ch+'+',c+c)),reverse=True)[:10]
    print(ch,runs)

# ---- run 12 ----

c=open('/work/cycle.txt').read()
s=c[74700:75300]
import re
print([ (m.group()[0],len(m.group())) for m in re.finditer('0+|1+',c[74000:75300])])

# ---- run 13 ----

c=open('/work/cycle.txt').read()
P=len(c)
z=set(i for i,ch in enumerate(c) if ch=='0')
zl=sorted(z)
import random
random.seed(1)
samp=random.sample(zl,20000)
res=[]
for lag in range(9,3000):
    s=sum(1 for i in samp if (i+lag)%P in z)
    res.append((s,lag))
res.sort(reverse=True);print(res[:30])

# ---- run 14 ----

c=open('/work/cycle.txt').read()
W=144
for r in range(500,540):
    print(c[r*W:(r+1)*W].replace('1','.').replace('0','#'))

# ---- run 15 ----

c=open('/work/cycle.txt').read()
from collections import Counter
import re
def phase(lo,hi):
    return Counter(m.start()%8 for m in re.finditer('(?=01111111 0)'.replace(' ',''),c[lo:hi]) if True)
for lo in range(0,len(c),20000):
    print(lo, Counter((m.start()+lo)%8 for m in re.finditer('(?=011111110)',c[lo:lo+20000])).most_common(3))

# ---- run 16 ----

c=open('/work/cycle.txt').read()
import re
ms=[(m.start()+1+7, m.start()%8) for m in re.finditer('(?=011111110)',c[70000:80000])]
# print positions of the terminal zero with phase
last7=max(p for p,ph in ms if ph==7); first5=min(p for p,ph in ms if ph==5 and p>last7-100)
print(last7+70000, first5+70000)
print([(p+70000,ph) for p,ph in ms if 74800<p+70000<76500])

# ---- run 17 ----

c=open('/work/cycle.txt').read()
S=75008
m=c[S:]+c[:S]
open('/work/msg.txt','w').write(m)
print(m[:1600])

# ---- run 18 ----

m=open('/work/msg.txt').read()
p=m.find('1'*16)
print(p)
seg=m[p:p+600]
for w in (8,15,16):
  for off in range(w):
    vals=[int(''.join('1' if ch=='0' else '0' for ch in seg[i:i+w]),2) for i in range(off,len(seg)-w,w)]
    print(w,off,vals[:20])

# ---- run 19 ----

m=open('/work/msg.txt').read()
inv=lambda s:int(''.join('1' if ch=='0' else '0' for ch in s),2)
st=174
vals=[inv(m[i:i+16]) for i in range(st,len(m)-15,16)]
print(len(vals))
print(vals[:400])

# ---- run 20 ----

m=open('/work/msg.txt').read()
print(m[:174])
print((len(m)-174)%16, (len(m)-174)//16)
inv=lambda s:int(''.join('1' if ch=='0' else '0' for ch in s),2)
vals=[inv(m[i:i+16]) for i in range(174,len(m),16)]
import json;json.dump(vals,open('/work/vals.json','w'))
from collections import Counter
C=Counter(vals)
print(len(C))
big=sorted(k for k in C if k>=256)
print([(k,hex(k),C[k]) for k in big])
print(vals[-40:])

# ---- run 21 ----

import json
vals=json.load(open('/work/vals.json'))
def name(v):
    if v<256: return str(v)
    hb,lb=v>>8,v&255
    return f"{'?ABCDEFGHI'[hb]}{lb}"
# parse
def parse(vals):
    stack=[[]];pre=[]
    for i,v in enumerate(vals):
        if v==256: stack.append([])
        elif v==257:
            e=stack.pop(); stack[-1].append(e)
        else: stack[-1].append(name(v))
    assert len(stack)==1
    return stack[0]
top=parse(vals)
print(len(top))
def s(e):
    return '('+' '.join(s(x) for x in e)+')' if isinstance(e,list) else e
out=[s(e) for e in top]
open('/work/top.txt','w').write('\n'.join(out))
print(sum(1 for e in top if not isinstance(e,list)))
for i,l in enumerate(out[:200]): print(i,l)

# ---- run 22 ----

out=open('/work/top.txt').read().split('\n')
for i in range(200,420): print(i,out[i][:260])

# ---- run 23 ----

out=open('/work/top.txt').read().split('\n')
for i in range(420,640): print(i,out[i][:300])

# ---- run 24 ----

out=open('/work/top.txt').read().split('\n')
for i in range(640,840): print(i,out[i][:330])

# ---- run 25 ----

out=open('/work/top.txt').read().split('\n')
for i in range(840,1040): print(i,out[i][:330])

# ---- run 26 ----

out=open('/work/top.txt').read().split('\n')
for i in range(1040,1246): print(i,out[i][:400])

# ---- run 27 ----

import json
vals=json.load(open('/work/vals.json'))
out=open('/work/top.txt').read().split('\n')
def name(v):
    hb,lb=v>>8,v&255
    return f"{'?ABCDEFGHI'[hb]}{lb}"
# map token index -> top-level statement index
stmt=[];depth=0;k=0
for v in vals:
    stmt.append(k)
    if v==256: depth+=1
    elif v==257:
        depth-=1
        if depth==0:k+=1
    elif depth==0: k+=1
first={};cnt={}
for i,v in enumerate(vals):
    if v>=512:
        first.setdefault(v,stmt[i]); cnt[v]=cnt.get(v,0)+1
missing=[]
for hb in range(2,10):
    ks=sorted(v for v in first if v>>8==hb)
    print(hb, len(ks), [ (name(v),first[v],cnt[v]) for v in ks])
    full=set(range(ks[0],ks[-1]+1))-set(ks); print(' gaps',[name(x) for x in sorted(full)])
nums=sorted(set(v for v in vals if v<256));print(nums)

# ---- run 28 ----

code = r'''
import json, math, itertools
from fractions import Fraction as Fr
vals=json.load(open('/work/vals.json'))
def parse(vals):
    stack=[[]]
    for v in vals:
        if v==256: stack.append([])
        elif v==257:
            e=stack.pop(); stack[-1].append(e)
        else: stack[-1].append(v)
    return stack[0]
top=parse(vals)
def nm(v):
    if isinstance(v,list): return '('+' '.join(nm(x) for x in v)+')'
    if v<256: return str(v)
    return f"{'?ABCDEFGHI'[v>>8]}{v&255}"
B=lambda k:0x200+k; C=lambda k:0x300+k; D=lambda k:0x400+k
class Unk(Exception): pass
TRUE,FALSE=('C',1),('C',2)
COOP,DEF=('C',5),('C',6)
I=complex(0,1)
def isnum(x): return isinstance(x,(int,Fr,float,complex)) and not isinstance(x,bool)
def eq(a,b):
    if isnum(a) and isnum(b):
        return abs(complex(a)-complex(b))<1e-9*(1+abs(complex(a)))
    if isinstance(a,tuple) and isinstance(b,tuple) and a[:1]==('L',) and b[:1]==('L',):
        return len(a)==len(b) and all(eq(x,y) for x,y in zip(a[1:],b[1:]))
    return a==b
def L(*xs): return ('L',)+tuple(xs)
def items(l):
    if not (isinstance(l,tuple) and l[0]=='L'): raise Unk('notlist')
    return list(l[1:])
def cost(a,b):
    return {(COOP,COOP):3,(DEF,DEF):5,(COOP,DEF):7,(DEF,COOP):2}[(a,b)]
def strat(s,h):
    h=items(h)
    last=items(h[-1]) if h else None
    if s==C(9): return L(COOP)
    if s==C(10): return L(DEF)
    if s==C(11): return L(COOP) if not h else L(last[1])
    if s==C(12): return L(DEF) if not h else L(last[1])
    if s==C(13): return L(COOP) if all(items(p)[1]==COOP for p in h) else L(DEF)
    if s==C(14): return L(COOP) if not h else (L(COOP) if last[0]==last[1] else L(DEF))
    if s==C(15): return L(COOP) if not h or last[1]==COOP else L(COOP,DEF,DEF)
    if s==C(16): return L(COOP,DEF)
    raise Unk('strat')
def play(s1,s2,n):
    h1=[];h2=[]
    for _ in range(n):
        a=items(strat(s1,L(*h1)))[0]; b=items(strat(s2,L(*h2)))[0]
        h1.append(L(a,b)); h2.append(L(b,a))
    return L(*h1)
SAMPLES={C(3):list(range(0,12))+[255,256,1000],
         C(4):[Fr(n,d) for n in range(-6,7) for d in (1,2,3,7)],
         C(18):[Fr(n,d) for n in range(-6,7) for d in (1,2,3)]+[math.sqrt(2),-math.pi,0.37],
         C(20):[complex(a,b) for a in (-2,0,1,0.5) for b in (-1,0,2,0.3)],
         C(7):[COOP,DEF],
         C(17):[C(9),C(10),C(11),C(12),C(13),C(14)],
         }
def unitvecs():
    import random
    r=random.Random(5); out=[L(1,0,0),L(0,1,0),L(0,0,1)]
    for _ in range(10):
        v=[r.gauss(0,1) for _ in range(3)]; n=math.sqrt(sum(x*x for x in v)); out.append(L(*[x/n for x in v]))
    return out
def vecs():
    import random
    r=random.Random(7); return [L(*[r.randint(-3,3) for _ in range(3)]) for _ in range(8)]
def hists():
    out=[L()]
    for n in (1,2,3):
        for combo in itertools.product([COOP,DEF],repeat=2*n):
            out.append(L(*[L(combo[2*i],combo[2*i+1]) for i in range(n)]))
    return out
SAMPLES[C(23)]=vecs(); SAMPLES[C(24)]=unitvecs(); SAMPLES[C(8)]=hists()
CONST={C(1):TRUE,C(2):FALSE,C(19):I,C(21):math.e,C(22):math.pi}
def domain(d,env):
    if isinstance(d,int) and d in SAMPLES: return SAMPLES[d]
    v=ev(d,env)
    return items(v)
def truth(x):
    if x==TRUE: return True
    if x==FALSE: return False
    raise Unk('nonbool')
def B_(b): return TRUE if b else FALSE
def num(x):
    if isnum(x): return x
    raise Unk('nonnum')
def mul(a,b):
    if isinstance(a,float) or isinstance(b,float) or isinstance(a,complex) or isinstance(b,complex): return complex(a)*complex(b) if (isinstance(a,complex) or isinstance(b,complex)) else a*b
    return a*b
def power(a,b):
    if isinstance(b,int) and not isinstance(a,(complex,)) and b>=0: return a**b
    if isinstance(a,Fr) and isinstance(b,int): return a**b
    return complex(a)**complex(b)
def simp(x):
    if isinstance(x,complex) and abs(x.imag)<1e-12: x=x.real
    if isinstance(x,Fr) and x.denominator==1: return int(x)
    return x
def ev(e,env):
    if isinstance(e,int):
        if e<256: return e
        if e in env: return env[e]
        if e in CONST: return CONST[e]
        if e in (C(5),C(6)): return ('C',e-0x300)
        if e>>8==3 and C(9)<=e<=C(16): return e
        if e>>8==2: return ('OP',e)
        if e==C(7): return L(COOP,DEF)
        if e==C(17): return L(*SAMPLES[C(17)])
        if e==C(26): return L(*[('Q',x) for x in top])
        raise Unk(nm(e))
    op=e[0]; a=e[1:]
    if not isinstance(op,int): raise Unk('applyexpr')
    k=op-0x200
    if k==20 or k==21:
        var,dom,body=a
        res=[truth(ev(body,{**env,var:x})) for x in domain(dom,env)]
        return B_(all(res) if k==20 else any(res))
    if k==24:
        var,dom,body=a
        return L(*[ev(body,{**env,var:x}) for x in domain(dom,env)])
    if k==41:
        var,dom,body=a
        xs=domain(dom,env)
        if dom==C(24): raise Unk('sphere-avg')
        return sum(num(ev(body,{**env,var:x})) for x in xs)/len(xs)
    if k==44:
        var,val,body=a
        return ev(body,{**env,var:ev(val,env)})
    if k==29:
        c=truth(ev(a[0],env)); return ev(a[1] if c else a[2],env)
    if k==22:
        p=truth(ev(a[0],env));
        return TRUE if not p else B_(truth(ev(a[1],env)))
    if k==42: return ('Q',a[0])
    args=[ev(x,env) for x in a]
    if k==1: return B_(all(eq(args[0],x) for x in args[1:]))
    if k==2: return B_(not eq(args[0],args[1]))
    if k in (3,4,5,6):
        f={3:lambda x,y:x<y,4:lambda x,y:x>y,5:lambda x,y:x<=y+1e-12,6:lambda x,y:x>=y-1e-12}[k]
        xs=[num(x) for x in args]
        if any(isinstance(x,complex) for x in xs): xs=[x.real if abs(x.imag)<1e-12 else (_ for _ in ()).throw(Unk('cmp complex')) for x in xs]
        return B_(all(f(xs[i],xs[i+1]) for i in range(len(xs)-1)))
    if k==7:
        s=0
        for x in args: s=s+num(x)
        return simp(s)
    if k==8:
        s=1
        for x in args: s=mul(s,num(x))
        return simp(s)
    if k==9:
        s=0
        for x in args: s=s*256+x
        return s
    if k==10: return simp(num(args[0])-num(args[1]))
    if k==11: return simp(-num(args[0]))
    if k==12:
        x,y=num(args[0]),num(args[1])
        if isinstance(x,int) and isinstance(y,int): return simp(Fr(x,y))
        return simp(x/y)
    if k==13: return B_(not truth(args[0]))
    if k==14: return B_(all(truth(x) for x in args))
    if k==15: return B_(any(truth(x) for x in args))
    if k==16: return L(*args)
    if k==17: return len(items(args[0]))
    if k==18: return items(args[0])[args[1]-1]
    if k==19: return sum(1 for x in items(args[1]) if eq(x,args[0]))
    if k==23:
        f=args[0]; xs=items(args[1])
        if f==('OP',B(7)): return simp(sum(xs))
        if f==('OP',B(8)):
            s=1
            for x in xs: s*=x
            return s
        if f==('OP',B(3)): return B_(all(xs[i]<xs[i+1] for i in range(len(xs)-1)))
        raise Unk('fold')
    if k==25:
        xs=items(args[0]); return simp(Fr(sum(xs))/len(xs)) if all(isinstance(x,(int,Fr)) for x in xs) else sum(xs)/len(xs)
    if k==26:
        xs=items(args[1]); return simp(Fr(sum(1 for x in xs if eq(x,args[0])),len(xs)))
    if k==27: return L(*[L(x,y) for x in items(args[0]) for y in items(args[1])])
    if k==28: return L(*items(args[0])[1:])
    if k==30: return cost(args[0],args[1])
    if k==31: return strat(args[0],args[1])
    if k==32: return play(args[0],args[1],args[2])
    if k==33:
        h=items(play(args[0],args[1],args[2])); return sum(cost(*items(p)) for p in h)
    if k==34: return simp(power(num(args[0]),num(args[1])))
    if k==35: return abs(num(args[0]))
    if k==36:
        import cmath; return simp(cmath.exp(complex(num(args[0]))))
    if k==37: return simp(sum(mul(x,y) for x,y in zip(items(args[0]),items(args[1]))))
    if k==38:
        import cmath; return simp(cmath.cos(complex(num(args[0]))))
    if k==39:
        u,v=items(args[0]),items(args[1]); d=sum(x*y for x,y in zip(u,v)); nu=math.sqrt(sum(x*x for x in u)); nv=math.sqrt(sum(x*x for x in v))
        return math.acos(max(-1,min(1,d/nu/nv)))
    if k==40:
        x,y=items(args[0]),items(args[1])
        return L(*[simp(x[1]*y[2]-x[2]*y[1]),simp(x[2]*y[0]-x[0]*y[2]),simp(x[0]*y[1]-x[1]*y[0])])
    raise Unk('op'+nm(op))
'''
open('/work/evalr.py','w').write(code)
print('ok')

# ---- run 29 ----

exec(open('/work/evalr.py').read())
from collections import Counter
res=Counter(); bad=[]; unk=Counter()
for i,e in enumerate(top):
    if not isinstance(e,list): continue
    try:
        r=ev(e,{})
        if r==TRUE: res['T']+=1
        elif r==FALSE: res['F']+=1; bad.append(i)
        else: res['nonbool']+=1; bad.append((i,'nb',r))
    except Unk as x: res['unk']+=1; unk[str(x)]+=1
    except Exception as x: res['err']+=1; bad.append((i,'err',repr(x)[:80]))
print(res); print(unk.most_common(30))
for b in bad[:40]: print(b, nm(top[b if isinstance(b,int) else b[0]])[:200])

# ---- run 30 ----

import sys,time
t=time.time()
exec(open('/work/evalr.py').read())
print('loaded',len(top),time.time()-t,flush=True)
for i in range(21,40):
    print(i,ev(top[i],{}),flush=True)

# ---- run 31 ----

import signal,time
exec(open('/work/evalr.py').read())
class TO(Exception): pass
def h(s,f): raise TO()
signal.signal(signal.SIGALRM,h)
from collections import Counter
res=Counter(); bad=[]; unk=Counter(); slow=[]
T0=time.time()
for i,e in enumerate(top):
    if not isinstance(e,list): continue
    if time.time()-T0>100: print('stopped at',i); break
    signal.alarm(2)
    try:
        r=ev(e,{})
        if r==TRUE: res['T']+=1
        elif r==FALSE: res['F']+=1; bad.append(i)
        else: res['nonbool']+=1; bad.append((i,'nb'))
    except Unk as x: res['unk']+=1; unk[str(x)]+=1
    except TO: res['timeout']+=1; slow.append(i)
    except Exception as x: res['err']+=1; bad.append((i,'err',repr(x)[:80]))
    finally: signal.alarm(0)
print(res); print(unk.most_common(40)); print('slow',slow)
for b in bad[:40]: print(b, nm(top[b if isinstance(b,int) else b[0]])[:200])

# ---- run 32 ----

exec(open('/work/evalr.py').read())
S={9:'AllC',10:'AllD',11:'TFT',12:'STFT',13:'Grim',14:'Pavlov'}
def tot(a,b,n): return sum(cost(*items(p)) for p in items(play(C(a),C(b),n)))
print('TFT v AllD 4:',tot(11,10,4))
for i in (394,395,396,397,398,399,400,401,402,403,404,405):
    e=top[i]; print(i, nm(e), ev(e,{}))
for a in (11,13,9,14,10,12):
    print(S[a], sum(tot(a,b,255) for b in S), divmod(sum(tot(a,b,255) for b in S),256))
for i in (386,387,388,389,390,391,392,393,1243,1244,1245,356,357,358,359,353,354,355):
    print(i, ev(top[i],{}))

# ---- run 33 ----

exec(open('/work/evalr.py').read())
msg=top  # top-level items
def find(expr): return sum(1 for x in msg if x==expr)
print([msg[k-1] for k in (1,2,4,12,13,21)], nm(msg[21]))
for i in range(610,620):
    e=top[i]; q=e[1][1][1]; n=e[2]; print(i,nm(q),'claimed',n,'actual',find(q))
# 639/640 etc
print(nm(top[635])); print(nm(top[637]))

# ---- run 34 ----

import math
me=9.1093837e-31; mp=1.67262192e-27; mn=1.67492750e-27; e=1.602176634e-19
hbar=1.054571817e-34; c=2.99792458e8; G=6.67430e-11; kB=1.380649e-23; k=8.9875517923e9
lP=math.sqrt(hbar*G/c**3); tP=math.sqrt(hbar*G/c**5); mP=math.sqrt(hbar*c/G); TP=math.sqrt(hbar*c**5/G/kB**2)
Ry=13.605693*e*(1/(1+me/mp)) # reduced-mass hydrogen
E21=Ry*(1-1/4)
def chk(name,val,lo,hi): print(f"{name:45s} {val:.6g}  in [{lo:.6g},{hi:.6g}]  {'OK' if lo<val<hi else 'NO'}")
chk('mp/me',mp/me,7*256+44,7*256+45)
chk('mn/me',mn/me,7*256+46,7*256+47)
chk('mn/mp',mn/mp,1+2**-11,1+2**-9)
chk('alpha (k e^2/hbar c)',k*e*e/(hbar*c),1/138,1/137)
chk('Coulomb/grav p-e',k*e*e/(G*mp*me),2**130,2**131)
chk('G mp^2/(hbar c) ',G*mp**2/(hbar*c),0,1)
chk('mp/mP',mp/mP,2**-64,2**-63)
chk('me/mP',me/mP,2**-75,2**-74)
E21cm=h21=6.62607015e-34*1420.405751e6
chk('E(21cm)/E(H 2->1)',E21cm/E21,2**-21,2**-20)
chk('1/(f21 tP)',1/(1420.405751e6*tP),2**113,2**114)
chk('lambda21/lP',c/1420.405751e6/lP,2**113,2**114)
chk('E21/(me c^2)',E21/(me*c*c),2**-16,2**-15)
chk('photon(2->1)/(E2-E1)',1,1-2**-11,1)  # trivial
chk('tau_n/tP',878.4/tP,2**153,2**154)
chk('t1/2 C14 / t1/2 H3',5730/12.32,2**8,2**9)
chk('mK0/me',497.611/0.51099895,3*256+205,3*256+207)
d=3.32e-3; chk('K_L e+/e- ratio',(1+d)/(1-d),1+2**-8,1+2**-7)
chk('Ttp H2/H2O',13.8033/273.16,103/2048,105/2048)
chk('Ttp Ne/H2O',24.5561/273.16,736/8192,737/8192)
chk('Ttp Ar/H2O',83.8058/273.16,1256/4096,1257/4096)
chk('k Ttp(H2O)/(E2-E1)',kB*273.16/E21,302/2**17,303/2**17)
chk('Ttp(H2O)/T_Planck',273.16/TP,156/2**106,157/2**106)
pP=mP/(lP*tP**2)
chk('ptp(H2O)/p_Planck',611.657/pP,203/2**376,204/2**376)
chk('ptp H2/H2O',7041/611.657,11,12)
chk('ptp Ne/H2O',43368/611.657,141/2,143/2)
chk('ptp Ar/H2O',68890/611.657,112,113)
chk('m(He4)/4m(H1)',4.002602/(4*1.00782503),1-2**-7,1-2**-8)
chk('T_CMB/Ttp',2.7255/273.16,163/2**14,164/2**14)
chk('DNA rise/lP',0.34e-9/lP,2**83,2**85)
chk('DNA pitch/lP',3.4e-9/lP,2**87,2**88)
chk('bp per turn 2pi/twist',10.5,8,13)
chk('Sun mass / mp',1.98847e30/mp,7*2**187,2**190)
chk('Sun R / lP',6.957e8/lP,2**145,2**146)
chk('Sun T/Ttp',5772/273.16,16,32)
chk('Sun L/(c^5/G)',3.828e26/(c**5/G),2**-85,2**-83)
chk('SgrA* mass/mp',4.15e6*1.98847e30/mp,2**211,2**212)
chk('R0 (8.2kpc)/lP',8.2e3*3.0857e16/lP,2**183,2**184)
chk('galactic yr (230Myr)/tP',230e6*3.156e7/tP,2**196,2**197)
chk('v_sun 230km/s / c',230e3/c,2**-11,9*2**-13)

# ---- run 35 ----

import math, itertools
hbar=1.054571817e-34; c=2.99792458e8; G=6.67430e-11; kB=1.380649e-23; mp=1.67262192e-27
lP=math.sqrt(hbar*G/c**3); tP=math.sqrt(hbar*G/c**5)
Msun=1.98847e30; Rsun=6.957e8; Lsun=3.828e26; AU=1.496e11; yr=3.156e7
sig=math.pi**2*kB**4/(60*hbar**3*c**2)
print('sigma',sig)
M1=(7*2**187*mp, 2**190*mp); M2=(2**189*mp,2**190*mp)
print('star M/Msun',[x/Msun for x in M1],'R/Rsun',[2**145*lP/Rsun,2**146*lP/Rsun],'T',[16*273.16,32*273.16])
L=(2**-85*c**5/G, 2**-83*c**5/G); print('L/Lsun',[x/Lsun for x in L])
# consistency: L=4pi R^2 sig T^4: find R,T within bounds giving L within bounds
ok=[]
for R in [2**145*lP*(1+i/20) for i in range(21)]:
    for T in [16*273.16*(1+j/20) for j in range(21)]:
        Lx=4*math.pi*R*R*sig*T**4
        if L[0]<Lx<L[1]: ok.append((R/Rsun,T))
print('consistent star combos',len(ok), ok[:3], ok[-3:])
print('companion M/Msun',[x/Msun for x in M2],'R/Rsun',[2**144*lP/Rsun,2**145*lP/Rsun])
a=(2**149*lP,2**150*lP); P=(2**163*tP,2**164*tP)
print('binary a AU',[x/AU for x in a],'P days',[x/86400 for x in P])
# Kepler: P^2 = 4pi^2 a^3/(G M) -> required M
Mreq=[4*math.pi**2*aa**3/(G*PP**2)/Msun for aa in a for PP in P]
print('binary Kepler Mtot range Msun',min(Mreq),max(Mreq),' allowed',(M1[0]+M2[0])/Msun,(M1[1]+M2[1])/Msun)
ap=(2**154*lP,2**155*lP); Pp=(2**170*tP,2**171*tP)
print('planet a AU',[x/AU for x in ap],'P yr',[x/yr for x in Pp], 'R/Rjup',[2**141*lP/7.1492e7,2**142*lP/7.1492e7],'Mmax/Mjup',2**182*mp/1.898e27)
Mreq=[4*math.pi**2*aa**3/(G*PP**2)/Msun for aa in ap for PP in Pp]
print('planet Kepler Mtot range',min(Mreq),max(Mreq))
d=(2**183*lP,2**184*lP); Pg=(2**196*tP,2**197*tP); Mb=(2**211*mp,2**212*mp)
print('BH Msun',[x/Msun for x in Mb],'d kpc',[x/3.0857e19 for x in d],'P Myr',[x/yr/1e6 for x in Pg])
r=[4*math.pi**2*dd**3/(G*MM*PP**2) for dd in d for MM in Mb for PP in Pg]; print('enclosed/BH ratio range',min(r),max(r),'claimed',2**12,2**16)
# beings
print('mass kg',2**96*mp,2**97*mp,'size m',2**117*lP,2**118*lP,'T K',17/16*273.16,9/8*273.16)
print('genome bp',2**32,2**33)
# pulsars
for nm_,lo,hi,dlo,dhi in [('C51',139,140,2**-48,2**-47),('C52',139,141,2**-47,2**-41),('C53',136,137,121*2**-71,149*2**-71),('C54',134,135,111*2**-70,137*2**-70),('C55',143,144,2**-49,2**-48),('C56',144,145,2**-50,2**-49)]:
    print(nm_,'P s',2**lo*tP,2**hi*tP,'Pdot',dlo,dhi)

# ---- run 36 ----

import json
vals=json.load(open('/work/vals.json'))
P=359422; S=75008
startbit=P-S  # message bit index at file bit 0
endbit=(1339312-S)%P  # message bit at file end (exclusive) in last copy
def stmt_at(bit):
    if bit<174: return 'preamble'
    w=(bit-174)//16
    depth=0;k=0
    for i,v in enumerate(vals[:w+1]):
        if i==w: return (w,k)
        if v==256: depth+=1
        elif v==257:
            depth-=1
            if depth==0:k+=1
        elif depth==0:k+=1
print('file starts at message bit',startbit, stmt_at(startbit))
print('file ends at message bit',endbit, stmt_at(endbit))
print('full copies start at file bits',[S+i*P for i in range(4)])
