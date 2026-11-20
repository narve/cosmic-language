# The code the blind reader ran, in order (2026-11-20, interpretation, decoy message (Kepler-1647, invented senders with their own hereditary molecule), Opus).
# Received: the decoy repeated 5 times, cut inside the first and last copy, every bit inverted, as /work/received.bin.

# ---- run 1 ----

import os
d=open('/work/received.bin','rb').read()
print(len(d), len(d)*8)
print(d[:64].hex())
from collections import Counter
bits=''.join(f'{b:08b}' for b in d)
print(Counter(bits))
print(bits[:400])
n=len(bits)
import sympy
print(sympy.factorint(n))

# ---- run 2 ----

import re
from collections import Counter
d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
runs=[(m.group()[0],len(m.group())) for m in re.finditer(r'0+|1+',bits)]
print(Counter(r for r in runs if r[0]=='0').most_common(20))
print(Counter(r for r in runs if r[0]=='1').most_common(40))
print(Counter(d).most_common(30))

# ---- run 3 ----

d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
n=len(bits)
for q in [2,4]:
    L=n//q
    parts=[bits[i*L:(i+1)*L] for i in range(q)]
    print(q,L,[sum(a!=b for a,b in zip(parts[0],p)) for p in parts])
# positions of long zero runs
import re
for m in re.finditer(r'0{8,}',bits):
    print(m.start(),len(m.group()))

# ---- run 4 ----

d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
n=len(bits);P=360670
print(n/P, n-3*P)
for k in range(1,4):
    a=bits[:n-k*P]; b=bits[k*P:]
    diff=[i for i in range(len(a)) if a[i]!=b[i]]
    print(k,len(diff),diff[:20])

# ---- run 5 ----

d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
P=360670
print(bits[-40:])
def fac(n):
    f=[];p=2
    while p*p<=n:
        while n%p==0: f.append(p);n//=p
        p+=1
    if n>1:f.append(n)
    return f
print(fac(P))
s=bits[178000:181200]
for i in range(0,len(s),100): print(s[i:i+100].replace('1','.').replace('0','#'))

# ---- run 6 ----

d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
from collections import Counter
import math
for off in range(8):
    c=Counter(bits[i:i+8] for i in range(off,360670,8))
    H=-sum(v/sum(c.values())*math.log2(v/sum(c.values())) for v in c.values())
    print(off,round(H,3),len(c),c.most_common(6))

# ---- run 7 ----

import re
d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
P=360670
for m in re.finditer(r'1{40,}',bits[:P]): print(m.start(),len(m.group()))

# ---- run 8 ----

d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
s=bits[:4000]
for i in range(0,len(s),100): print(s[i:i+100].replace('1','.').replace('0','#'))

# ---- run 9 ----

import re
from collections import Counter
d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
P=360670
s=bits[:P]
for k in [5,6,7]:
    toks=re.split('1{%d,}'%k,s)
    c=Counter(toks)
    print(k,len(c),c.most_common(40))

# ---- run 10 ----

import re
d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
m=''.join('1' if c=='0' else '0' for c in bits)  # marks
open('/work/marks.txt','w').write(m)
s=m[180000:182600]
# show tokens split by gaps>=4 with gap length
out=[];pos=0
for t in re.finditer(r'1[01]*?1(?=0{4,}|$)|1(?=0{4,})',s):
    out.append((t.start()-pos, t.group())); pos=t.end()
print(' '.join(f'[{g}]{t}' for g,t in out))

# ---- run 11 ----

m=open('/work/marks.txt').read()
P=360670
from collections import Counter
import math
def H(s,off,w=8):
    c=Counter(s[i:i+w] for i in range(off,len(s)-w,w))
    t=sum(c.values());return -sum(v/t*math.log2(v/t) for v in c.values())
W=4000
res=[]
for st in range(0,P,W):
    s=m[st:st+W]
    hs=[H(s,o) for o in range(8)]
    b=min(range(8),key=lambda o:hs[o])
    res.append(((st+b)%8, round(hs[b],2), round(sorted(hs)[1],2)))
print(res)

# ---- run 12 ----

m=open('/work/marks.txt').read()
i=m.find('1'+'0'*1+'1'*31,180000)
st=180724+31  # after 31-run
print(m[180600:180760])
s=m[st:st+1400]
for k in range(0,len(s),16): print(st+k, s[k:k+16].replace('0','.').replace('1','#'))

# ---- run 13 ----

m=open('/work/marks.txt').read()
blk=lambda a,b: m[a:b]
# find period of repeating block in 181363..182083
s=m[181203:182100]
for p in range(60,100):
    sim=sum(s[i]==s[i+p] for i in range(len(s)-p))/(len(s)-p)
    if sim>0.9: print(p,sim)

# ---- run 14 ----

m=open('/work/marks.txt').read()
for a in range(181200,182180,80):
    print(a, m[a:a+80].replace('0','.').replace('1','#'))

# ---- run 15 ----

m=open('/work/marks.txt').read()
for a in range(182160,183800,80):
    print(a, m[a:a+80].replace('0','.').replace('1','#'))

# ---- run 16 ----

d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
P=360670
def uart(b,N,stop=1,start=0):
    i=start;out=[];err=0
    while i<len(b)-N-stop:
        if b[i]=='1': i+=1; continue
        data=b[i+1:i+1+N]; st=b[i+1+N:i+1+N+stop]
        if st!='1'*stop: err+=1
        out.append(data); i+=1+N+stop
    return out,err
for N in [5,6,7,8,9]:
    o,e=uart(bits[:P],N)
    print(N,len(o),e)

# ---- run 17 ----

m=open('/work/marks.txt').read()
import re
# tokenise by gaps: print as list of (gap, run-pattern) using gaps >=7 as separators
def tok(s,g=7):
    return [t for t in re.split('0{%d,}'%g,s) if t]
s=m[178000:180760]
print(' '.join(tok(s)))

# ---- run 18 ----

m=open('/work/marks.txt').read()
from collections import Counter
for a in range(178000,184000,400):
    c=Counter(i%8 for i in range(a,a+400) if m[i]=='1')
    print(a, sorted(c.items()))

# ---- run 19 ----

m=open('/work/marks.txt').read()
def bytes_at(a,b,off):
    a=a-((a-off)%8)
    return [int(m[i:i+8],2) for i in range(a,b,8)]
v=bytes_at(181200,182400,4)
print(v)
print(bytes_at(181200,182400,0))

# ---- run 20 ----

m=open('/work/marks.txt').read()
P=360670
W=320
best=[]
for a in range(0,P,W//2):
    sc=[]
    for ph in range(8):
        st=a+((ph-a)%8)
        sc.append(sum(1 for i in range(st,min(a+W,P)-8,8) if int(m[i:i+8],2)<4))
    b=max(range(8),key=lambda p:sc[p]); s2=sorted(sc)[-2]
    best.append((a,b,sc[b],s2))
# summarize changes
prev=None
for a,b,s,s2 in best:
    if b!=prev: print(a,b,s,s2); prev=b

# ---- run 21 ----

m=open('/work/marks.txt').read()
def B(a,b,ph):
    st=a+((ph-a)%8); return [(i,int(m[i:i+8],2)) for i in range(st,b,8)]
print(B(180480,180640,6))
print(m[180590:180770])
print(B(180740,180900,4))

# ---- run 22 ----

m=open('/work/marks.txt').read()
P=360670
s=m[180582:180760]
print(s)
import re
print([len(x) for x in re.findall('1+',s)])
end=180582+s.rfind('1')+1
print(end, m[end:end+20])
# phase 4 bytes start at multiples ≡4 mod 8
for e in range(end,end+10):
    if e%8==4: print('byte start',e); bs=e
U=bs-180582
print('unary-ish length',U,(P-U)%8,(P-U)//8)

# ---- run 23 ----

m=open('/work/marks.txt').read()
P=360670
st=180756
by=bytes(int(m[st+8*i:st+8*i+8],2) for i in range(45062))
open('/work/msg.bin','wb').write(by)
# check consistency with second copy
by2=bytes(int(m[st+P+8*i:st+P+8*i+8],2) for i in range(45062) if st+P+8*i+8<=len(m))
print(len(by2), sum(a!=b for a,b in zip(by,by2)))
from collections import Counter
print(Counter(by).most_common(40))
print(list(by[:300]))

# ---- run 24 ----

by=open('/work/msg.bin','rb').read()
L=list(by)
sep=[1,1,1,0,2]
stm=[];cur=[];i=0
while i<len(L):
    if L[i:i+5]==sep:
        stm.append(cur);cur=[];i+=5
    else: cur.append(L[i]);i+=1
stm.append(cur)
print(len(stm))
for s in stm[:150]: print(s)

# ---- run 25 ----

by=open('/work/msg.bin','rb').read()
L=list(by)
i=0
# find index of first '1,1,0,2,7'
for k in range(len(L)):
    if L[k:k+5]==[1,1,0,2,7]: break
print(k)
print(L[k-200:k+400])

# ---- run 26 ----

by=open('/work/msg.bin','rb').read()
W=[(by[i],by[i+1]) for i in range(0,len(by),2)]
from collections import Counter
c=Counter(t for t,v in W)
print(len(W),c)
for t in sorted(c):
    print(t, sorted(Counter(v for tt,v in W if tt==t).items())[:80])

# ---- run 27 ----

by=open('/work/msg.bin','rb').read()
W=[(by[i],by[i+1]) for i in range(0,len(by),2)]
names={0:'',2:'o',3:'v',4:'a',5:'b',6:'c',7:'d',8:'e',9:'f'}
def tokstr(t,v):
    if t==1: return '(' if v==0 else ')'
    if t==0: return str(v)
    return f'{names[t]}{v}'
toks=[tokstr(*w) for w in W]
# split top level
stmts=[];depth=0;cur=[];pre=[]
for k,tk in enumerate(toks):
    if depth==0 and tk!='(':
        pre.append((len(stmts),tk)); 
        if tk==')': print('unbalanced at',k)
        continue
    cur.append(tk)
    if tk=='(':depth+=1
    elif tk==')':
        depth-=1
        if depth==0: stmts.append(' '.join(cur).replace('( ','(').replace(' )',')'));cur=[]
print(len(stmts), 'top-level non-list tokens:',len(pre), pre[:50])
import pickle; pickle.dump((W,toks,stmts),open('/work/p.pkl','wb'))
for i,s in enumerate(stmts[:120]): print(i,s)

# ---- run 28 ----

import pickle
W,toks,stmts=pickle.load(open('/work/p.pkl','rb'))
for i in range(120,330): print(i,stmts[i][:300])

# ---- run 29 ----

import pickle
W,toks,stmts=pickle.load(open('/work/p.pkl','rb'))
for i in range(330,520): print(i,stmts[i][:260])

# ---- run 30 ----

import pickle
W,toks,stmts=pickle.load(open('/work/p.pkl','rb'))
for i in range(520,700): print(i,stmts[i][:240])

# ---- run 31 ----

import pickle
W,toks,stmts=pickle.load(open('/work/p.pkl','rb'))
for i in range(700,900): print(i,stmts[i][:240])

# ---- run 32 ----

import pickle
W,toks,stmts=pickle.load(open('/work/p.pkl','rb'))
for i in range(900,1060): print(i,stmts[i][:300])

# ---- run 33 ----

import pickle
W,toks,stmts=pickle.load(open('/work/p.pkl','rb'))
for i in range(1060,1226): print(i,stmts[i][:400])

# ---- run 34 ----

import pickle, math
from fractions import Fraction as F
W,toks,stmts=pickle.load(open('/work/p.pkl','rb'))
# build trees
def build(W):
    out=[];stack=[out]
    for t,v in W:
        if t==1 and v==0: n=[]; stack[-1].append(n); stack.append(n)
        elif t==1 and v==1: stack.pop()
        else: stack[-1].append((t,v))
    return out
top=build(W)
trees=[x for x in top if isinstance(x,list)]
print(len(top),len(trees))
pickle.dump((top,trees),open('/work/trees.pkl','wb'))

# ---- run 35 ----


code = r'''
import pickle, math, cmath, itertools
from fractions import Fraction as F
top,trees=pickle.load(open('/work/trees.pkl','rb'))
class Unk(Exception): pass
class Q:  # quoted
    def __init__(s,t): s.t=t
    def __eq__(s,o): return isinstance(o,Q) and key(s.t)==key(o.t)
    def __hash__(s): return hash(key(s.t))
def key(t):
    return tuple(key(x) for x in t) if isinstance(t,list) else t
D,C='D','C'
def histories(maxlen=3):
    pairs=[(a,b) for a in (D,C) for b in (D,C)]
    for n in range(maxlen+1):
        for h in itertools.product(pairs,repeat=n): yield tuple(h)
nums=lambda x: isinstance(x,(int,F,float,complex)) and not isinstance(x,bool)
def rnd(x):
    return x
def strat(s,h):
    # returns list (distribution)
    if s=='v9': return (D,)
    if s=='v10': return (C,)
    if s in('v11','v12'):
        if not h: return (D,) if s=='v11' else (C,)
        return (h[-1][1],)
    if s=='v13':
        return (D,) if sum(1 for r in h if r[1]==C)==0 else (C,)
    if s=='v14':
        if not h: return (D,)
        return (D,) if h[-1][0]==h[-1][1] else (C,)
    if s=='v15':
        if not h: return (D,)
        return (D,) if h[-1][1]==D else (D,C,C)
    if s=='v16': return (D,C)
    raise Unk('strat')
PAY={(D,D):3,(C,C):5,(D,C):7,(C,D):2}
def play(a,b,n):
    ha=[];hb=[]
    for i in range(n):
        x=strat(a,tuple(ha)); y=strat(b,tuple(hb))
        if len(x)>1 or len(y)>1: raise Unk('random')
        ha.append((x[0],y[0])); hb.append((y[0],x[0]))
    return tuple(ha)
SETS={'v3':list(range(0,12)),'v4':list(range(-8,9)),'v18':[F(-7,2),-2,F(-1,3),0,F(1,2),1,2,F(5,2),3],
      'v7':[D,C],'v17':['v9','v10','v11','v12','v13','v14']}
def ev(t,env):
    if isinstance(t,tuple):
        ty,v=t
        if ty==0: return v
        if ty==4: 
            if ('a',v) in env: return env[('a',v)]
            raise Unk('free var')
        if ty==3:
            n='v%d'%v
            if n=='v1': return True
            if n=='v2': return False
            if n=='v5': return D
            if n=='v6': return C
            if n=='v7': return (D,C)
            if n=='v19': return 1j
            if n=='v21': return math.e
            if n=='v22': return math.pi
            if n in ('v9','v10','v11','v12','v13','v14','v15','v16'): return n
            if n=='v17': return tuple(SETS['v17'])
            if n=='v26': return MSG
            if n=='v27': return Q((3,27))
            if n in SETS: return ('SET',n)
            raise Unk(n)
        if ty==2: return ('OP',v)
        raise Unk('type%d'%ty)
    op=t[0]
    if op[0]!=2: raise Unk('head')
    o=op[1]; A=t[1:]
    E=lambda x: ev(x,env)
    if o==42: return Q(A[0])
    if o in (20,21,24,41,44):
        var=A[0]; dom=E(A[1])
        if o==44:
            e2=dict(env); e2[('a',var[1])]=dom; return ev(A[2],e2)
        if isinstance(dom,tuple) and dom and dom[0]=='SET': dom=SETS.get(dom[1]) or (_ for _ in ()).throw(Unk('set '+dom[1]))
        if o==24 and not isinstance(dom,tuple) and dom!=MSG: raise Unk('map')
        if o==41: raise Unk('avg')
        res=[]
        for x in dom:
            e2=dict(env); e2[('a',var[1])]=x
            res.append(ev(A[2],e2))
        if o==20: return all(r is True for r in res)
        if o==21: return any(r is True for r in res)
        if o==24: return tuple(res)
    if o==29:
        c=E(A[0]); return E(A[1]) if c is True else E(A[2])
    if o==22:
        a=E(A[0]); 
        if a is not True: return True
        return E(A[1])
    if o==23:
        f=A[0]; lst=E(A[1])
        return ev([f]+[q(x) for x in lst],env)
    args=[E(a) for a in A]
    if o==1: return all(eq(args[0],x) for x in args[1:])
    if o==2: return not eq(args[0],args[1])
    if o in (3,4,5,6):
        cmp={3:lambda a,b:a<b,4:lambda a,b:a>b,5:lambda a,b:a<=b,6:lambda a,b:a>=b}[o]
        return all(cmp(args[i],args[i+1]) for i in range(len(args)-1))
    if o==7: 
        s=0
        for x in args: s=s+x
        return s
    if o==8:
        s=1
        for x in args: s=s*x
        return s
    if o==9:
        s=0
        for x in args: s=s*256+x
        return s
    if o==10: return args[0]-args[1]
    if o==11: return -args[0]
    if o==12: return F(args[0],args[1]) if all(isinstance(x,(int,F)) for x in args) else args[0]/args[1]
    if o==13: return not args[0]
    if o==14: return all(x is True for x in args)
    if o==15: return any(x is True for x in args)
    if o==16: return tuple(args)
    if o==17: return len(args[0])
    if o==18: return args[0][args[1]-1]
    if o==19: return sum(1 for x in args[1] if eq(x,args[0]))
    if o==25: return F(sum(args[0]),len(args[0])) if all(isinstance(x,(int,F)) for x in args[0]) else sum(args[0])/len(args[0])
    if o==26: return F(sum(1 for x in args[1] if eq(x,args[0])),len(args[1]))
    if o==27: return tuple(tuple(p) for p in itertools.product(*args))
    if o==28: return tuple(args[0][1:])
    if o==30: return PAY[(args[0],args[1])]
    if o==31: return strat(args[0],tuple(args[1]))
    if o==32: return play(args[0],args[1],args[2])
    if o==33: return sum(PAY[r] for r in play(args[0],args[1],args[2]))
    if o==34:
        a,b=args
        if isinstance(a,(int,F)) and isinstance(b,int) and b>=0: return F(a)**b
        return a**b
    if o==35: return abs(args[0])
    if o==36: return cmath.exp(args[0]) if isinstance(args[0],complex) else math.exp(args[0])
    if o==37: return sum(x*y for x,y in zip(args[0],args[1]))
    if o==38: return math.cos(args[0])
    if o==39:
        a,b=args; c=sum(x*y for x,y in zip(a,b))/math.sqrt(sum(x*x for x in a)*sum(x*x for x in b)); return math.acos(max(-1,min(1,c)))
    if o==40:
        a,b=args; return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
    if o==43:
        x=args[0]
        if isinstance(x,Q): t=x.t; return 1 if isinstance(t,list) else t[0]
        if isinstance(x,int): return 0
        raise Unk('kind')
    if o==45:
        x=args[0]
        if isinstance(x,Q): 
            r=ev(x.t,env)
            return r
        return x
    if o==46:
        q0,val=args
        def sub(t):
            if isinstance(t,list): return [sub(y) for y in t]
            if t==(3,27): return unq(val)
            return t
        return Q(sub(q0.t))
    raise Unk('op%d'%o)
def q(x):
    if isinstance(x,Q): return x.t
    if isinstance(x,bool): return (3,1 if x else 2)
    if isinstance(x,int): return (0,x)
    if isinstance(x,tuple) and x and x[0]=='OP': return (2,x[1])
    return ('lit',x)
def unq(v):
    if isinstance(v,Q): return v.t
    return q(v)
def ev_lit(t,env):
    pass
_old=ev
def ev(t,env):
    if isinstance(t,tuple) and t[0]=='lit': return t[1]
    return _old(t,env)
def eq(a,b):
    if isinstance(a,Q) or isinstance(b,Q):
        if isinstance(a,Q) and isinstance(b,Q): return a==b
        x=a if isinstance(b,Q) else b; y=b if isinstance(b,Q) else a
        if isinstance(x,int) and not isinstance(x,bool): return y.t==(0,x)
        return False
    if nums(a) and nums(b): 
        if isinstance(a,(float,complex)) or isinstance(b,(float,complex)): return abs(a-b)<1e-9
        return a==b
    return a==b
MSG=tuple([x[1] if not isinstance(x,list) else Q(x) for x in top])
'''
open('/work/ev.py','w').write(code)
exec(code)
res={}
for i,t in enumerate(trees):
    try:
        r=ev(t,{})
        res[i]=r
    except Unk as e: res[i]=('UNK',str(e))
    except Exception as e: res[i]=('ERR',repr(e))
from collections import Counter
print(Counter(type(r).__name__ if not isinstance(r,tuple) else r[0] for r in res.values()))
print([ (i,r) for i,r in res.items() if r is False])
print([ (i,r) for i,r in res.items() if not isinstance(r,bool) and not (isinstance(r,tuple) and r[0]=='UNK')][:40])

# ---- run 36 ----


src=open('/work/ev.py').read()
src=src.replace("SETS={'v3':list(range(0,12)),'v4':list(range(-8,9)),'v18':[F(-7,2),-2,F(-1,3),0,F(1,2),1,2,F(5,2),3],",
"""import numpy as np
_r=[x for x in np.roots([1,0,1,1]) if abs(x.imag)<1e-12][0].real
SETS={'v3':list(range(0,300)),'v4':sorted(set([F(a,b) for a in range(-9,10) for b in range(1,10)])),
 'v18':sorted(set([F(a,b) for a in range(-9,10) for b in range(1,10)]))+[math.sqrt(2),-math.sqrt(2),(1+math.sqrt(5))/2,(1-math.sqrt(5))/2,_r,3**0.2,math.sqrt(3)],""")
# new quote handling
src+=r'''
def quote(t):
    if isinstance(t,list): return tuple(quote(c) for c in t)
    if t[0]==0: return t[1]
    if t[0]==2: return ('OP',t[1])
    return ('SYM',t)
def unquote(x):
    if isinstance(x,bool): return (3,1 if x else 2)
    if isinstance(x,int): return (0,x)
    if isinstance(x,tuple) and x and x[0]=='OP': return (2,x[1])
    if isinstance(x,tuple) and x and x[0]=='SYM': return x[1]
    if isinstance(x,tuple): return [unquote(c) for c in x]
    return ('lit',x)
_ev2=ev
def ev(t,env):
    if isinstance(t,list) and t and t[0]==(2,42): return quote(t[1])
    if isinstance(t,list) and t and t[0]==(2,43):
        x=ev(t[1],env)
        if isinstance(x,bool): return 3
        if isinstance(x,int): return 0
        if isinstance(x,tuple) and x and x[0]=='OP': return 2
        if isinstance(x,tuple) and x and x[0]=='SYM': return x[1][0]
        if isinstance(x,tuple): return 1
        raise Unk('kind')
    if isinstance(t,list) and t and t[0]==(2,45):
        x=ev(t[1],env); return ev(unquote(x),env)
    if isinstance(t,list) and t and t[0]==(2,46):
        q0=ev(t[1],env); val=ev(t[2],env)
        def sub(x):
            if x==('SYM',(3,27)): return val
            if isinstance(x,tuple) and x and x[0] not in ('OP','SYM'): return tuple(sub(y) for y in x)
            return x
        return sub(q0)
    if isinstance(t,list) and t and t[0]==(2,23):
        f=ev(t[1],env); lst=ev(t[2],env)
        return ev([unquote(f)]+[unquote(x) for x in lst],env)
    return _ev2(t,env)
def eq(a,b):
    if nums(a) and nums(b):
        if isinstance(a,(float,complex)) or isinstance(b,(float,complex)): return abs(a-b)<1e-9
        return a==b
    return a==b
MSG=tuple([x[1] if not isinstance(x,list) else quote(x) for x in top])
'''
open('/work/ev2.py','w').write(src)
exec(src)
res={}
for i,t in enumerate(trees):
    try: res[i]=ev(t,{})
    except Unk as e: res[i]=('UNK',str(e))
    except Exception as e: res[i]=('ERR',repr(e))
from collections import Counter
print(Counter(type(r).__name__ if not isinstance(r,tuple) else r[0] for r in res.values()))
print('FALSE',[ i for i,r in res.items() if r is False])
print([ (i,r) for i,r in res.items() if isinstance(r,tuple) and r[0]=='ERR'][:20])
print(Counter(r[1] for r in res.values() if isinstance(r,tuple) and r[0]=='UNK'))

# ---- run 37 ----


src=open('/work/ev2.py').read() if False else None
import re
src=open('/work/ev.py').read()
src=src.replace("SETS={'v3':list(range(0,12)),'v4':list(range(-8,9)),'v18':[F(-7,2),-2,F(-1,3),0,F(1,2),1,2,F(5,2),3],",
"""def _bis(f,a,b):
    for _ in range(200):
        m=(a+b)/2
        if (f(a)<0)==(f(m)<0): a=m
        else: b=m
    return (a+b)/2
_r=_bis(lambda x:x**3+x+1,-2.0,0.0)
SETS={'v3':list(range(0,300)),'v4':sorted(set([F(a,b) for a in range(-9,10) for b in range(1,10)])),
 'v18':sorted(set([F(a,b) for a in range(-9,10) for b in range(1,10)]))+[math.sqrt(2),-math.sqrt(2),(1+math.sqrt(5))/2,(1-math.sqrt(5))/2,_r,3**0.2,math.sqrt(3)],""")
tail=open('/work/ev2tail.py','w')
src+=r'''
def quote(t):
    if isinstance(t,list): return tuple(quote(c) for c in t)
    if t[0]==0: return t[1]
    if t[0]==2: return ('OP',t[1])
    return ('SYM',t)
def unquote(x):
    if isinstance(x,bool): return (3,1 if x else 2)
    if isinstance(x,int): return (0,x)
    if isinstance(x,tuple) and x and x[0]=='OP': return (2,x[1])
    if isinstance(x,tuple) and x and x[0]=='SYM': return x[1]
    if isinstance(x,tuple): return [unquote(c) for c in x]
    return ('lit',x)
_ev2=ev
def ev(t,env):
    if isinstance(t,list) and t and t[0]==(2,42): return quote(t[1])
    if isinstance(t,list) and t and t[0]==(2,43):
        x=ev(t[1],env)
        if isinstance(x,bool): return 3
        if isinstance(x,int): return 0
        if isinstance(x,tuple) and x and x[0]=='OP': return 2
        if isinstance(x,tuple) and x and x[0]=='SYM': return x[1][0]
        if isinstance(x,tuple): return 1
        raise Unk('kind')
    if isinstance(t,list) and t and t[0]==(2,45):
        x=ev(t[1],env); return ev(unquote(x),env)
    if isinstance(t,list) and t and t[0]==(2,46):
        q0=ev(t[1],env); val=ev(t[2],env)
        def sub(x):
            if x==('SYM',(3,27)): return val
            if isinstance(x,tuple) and x and x[0] not in ('OP','SYM'): return tuple(sub(y) for y in x)
            return x
        return sub(q0)
    if isinstance(t,list) and t and t[0]==(2,23):
        f=ev(t[1],env); lst=ev(t[2],env)
        return ev([unquote(f)]+[unquote(x) for x in lst],env)
    return _ev2(t,env)
def eq(a,b):
    if nums(a) and nums(b):
        if isinstance(a,(float,complex)) or isinstance(b,(float,complex)): return abs(a-b)<1e-9
        return a==b
    return a==b
MSG=tuple([x[1] if not isinstance(x,list) else quote(x) for x in top])
'''
open('/work/ev2.py','w').write(src)
exec(src)
res={}
for i,t in enumerate(trees):
    try: res[i]=ev(t,{})
    except Unk as e: res[i]=('UNK',str(e))
    except Exception as e: res[i]=('ERR',repr(e))
from collections import Counter
print(Counter(type(r).__name__ if not isinstance(r,tuple) else r[0] for r in res.values()))
print('FALSE',[ i for i,r in res.items() if r is False])
print([ (i,r) for i,r in res.items() if isinstance(r,tuple) and r[0]=='ERR'][:20])
print(Counter(r[1] for r in res.values() if isinstance(r,tuple) and r[0]=='UNK'))

# ---- run 38 ----


src=open('/work/ev2.py').read().replace("'v3':list(range(0,300))","'v3':list(range(0,13))+[255,256,1000]")
src=src.replace("sorted(set([F(a,b) for a in range(-9,10) for b in range(1,10)]))","sorted(set([F(a,b) for a in range(-6,7) for b in range(1,7)]))")
open('/work/ev2.py','w').write(src)
import signal
exec(src)
import time
res={}
for i,t in enumerate(trees):
    if i>=600: break
    t0=time.time()
    try: res[i]=ev(t,{})
    except Unk as e: res[i]=('UNK',str(e))
    except Exception as e: res[i]=('ERR',repr(e))
    if time.time()-t0>2: print('slow',i)
from collections import Counter
print(Counter(type(r).__name__ if not isinstance(r,tuple) else r[0] for r in res.values()))
print('FALSE',[ i for i,r in res.items() if r is False])
print([ (i,r) for i,r in res.items() if isinstance(r,tuple) and r[0]=='ERR'][:20])
print(Counter(r[1] for r in res.values() if isinstance(r,tuple) and r[0]=='UNK'))

# ---- run 39 ----


exec(open('/work/ev2.py').read())
import pickle
W,toks,stmts=pickle.load(open('/work/p.pkl','rb'))
res={}
for i in list(range(324,400))+list(range(582,606))+[1223,1224,1225]:
    try: res[i]=ev(trees[i],{})
    except Unk as e: res[i]=('UNK',str(e))
    except Exception as e: res[i]=('ERR',repr(e))
for i,r in res.items(): 
    if r is not True: print(i,r,stmts[i][:120])
# tournament table
S=['v9','v10','v11','v12','v13','v14']
for a in S:
    row=[sum(PAY[r] for r in play(a,b,255)) for b in S]
    print(a,row,sum(row), divmod(sum(row),256))

# ---- run 40 ----


import math
hbar=1.054571817e-34;G=6.67430e-11;c=299792458;kB=1.380649e-23;me=9.1093837e-31;mp=1.67262192e-27;mn=1.67492750e-27
lP=math.sqrt(hbar*G/c**3);tP=lP/c;mP=math.sqrt(hbar*c/G);TP=mP*c**2/kB
eV=1.602176634e-19;alpha=1/137.035999
Ttr=273.16; PP=c**7/(hbar*G**2)
def chk(name,lo,val,hi): print(f"{name:40s} {lo:.6g} < {val:.6g} < {hi:.6g}  {'OK' if lo<val<hi else 'FAIL'}")
chk('mp/me',7*256+44,mp/me,7*256+45)
chk('mn/me',7*256+46,mn/me,7*256+47)
chk('mn/mp',1+2**-11,mn/mp,1+2**-9)
chk('alpha',1/138,alpha,1/137)
ke=8.9875517923e9;e=1.602176634e-19
chk('Fcoul/Fgrav p-e log2',130,math.log2(ke*e*e/(G*mp*me)),131)
chk('mp/mPl log2',-64,math.log2(mp/mP),-63)
chk('me/mPl log2',-75,math.log2(me/mP),-74)
E21=hbar*2*math.pi*1420405751.77; Ely=10.19881*eV
chk('E21cm/Lya log2',-21,math.log2(E21/Ely),-20)
chk('1/(f21 tP) log2',113,math.log2(1/(1420405751.77*tP)),114)
chk('Lya/mec2 log2',-16,math.log2(Ely/(me*c*c)),-15)
chk('tau_n/tP log2',153,math.log2(879.4/tP),154)
chk('t1/2 C14/H3',256,5730/12.32,512)
chk('mK0/me',3*256+205,497.611/0.51099895,3*256+207)
chk('K_L e+/e- ratio',1+2**-8,(1+3.32e-3)/(1-3.32e-3),1+2**-7)
chk('Ttr H2/H2O *2048',103,13.8033/Ttr*2048,105)
chk('Ttr Ne/H2O *8192',2*256+224,24.5561/Ttr*8192,2*256+225)
chk('Ttr Ar/H2O *4096',4*256+232,83.8058/Ttr*4096,4*256+233)
chk('kTtr/Lya *2^17',302,kB*Ttr/Ely*2**17,303)
chk('Ttr/TPl *2^106',156,Ttr/TP*2**106,157)
chk('Ptr water/PPl *2^376',203,611.657/PP*2**376,204)
chk('Ptr H2/water',11,7.041e3/611.657,12)
chk('Ptr Ne/water',70.5,43.37e3/611.657,71.5)
chk('Ptr Ar/water',112,68.89e3/611.657,113)
chk('m He4/(4 mH)',1-2**-7,4.0026032/(4*1.00782503),1-2**-8)
chk('T_CMB/Ttr *2^14',163,2.72548/Ttr*2**14,164)
Msun=1.98892e30;Rsun=6.957e8;Lsun=3.828e26
print('star: M/Msun',7*2**187*mp/Msun,2**190*mp/Msun,' R/Rsun',2**145*lP/Rsun,2**146*lP/Rsun,' T',20*Ttr,25*Ttr,' L/Lsun',2**-85*c**5/G/Lsun,2**-83*c**5/G/Lsun)
print('companion: M',2**189*mp/Msun,2**190*mp/Msun,' R',2**144*lP/Rsun,2**145*lP/Rsun,' T',18*Ttr,24*Ttr,' a AU',2**149*lP/1.496e11,2**150*lP/1.496e11,' P days',2**163*tP/86400,2**164*tP/86400)
MJ=1.898e27;RJ=7.1492e7
print('planet: a AU',2**154*lP/1.496e11,2**155*lP/1.496e11,' P yr',2**170*tP/3.156e7,2**171*tP/3.156e7,' R/RJ',2**141*lP/RJ,2**142*lP/RJ,' M< MJ',2**182*mp/MJ)
print('BH M/Msun',2**211*mp/Msun,2**212*mp/Msun,' dist kpc',2**183*lP/3.086e19,2**184*lP/3.086e19,' period Myr',2**196*tP/3.156e13,2**197*tP/3.156e13)
print('v along v48 km/s',c/2048/1e3,9*c/8192/1e3, ' v47 <',c/8192/1e3,' v49<',c/16384/1e3)
print('species mass kg',2**96*mp,2**97*mp,' size m',2**117*lP,2**118*lP,' T K',17/16*Ttr,9/8*Ttr)
print('helix rise nm',2**83*lP*1e9,2**84*lP*1e9,' pitch nm',2**87*lP*1e9,2**88*lP*1e9, ' genome bp',2**33,2**34)
for nm,(a,b) in {'v51':(139,140),'v53':(136,137),'v54':(134,135),'v55':(143,144),'v56':(144,145)}.items(): print(nm,'P s',2**a*tP,2**b*tP)
print('v52 P s',11*2**136*tP,5*2**138*tP)
print('Pdots v51',2**-48,2**-47,' v52',3*2**-48,9*2**-45,' v53',121*2**-71,149*2**-71,' v54',111*2**-70,137*2**-70,' v55',2**-49,2**-48,' v56',2**-50,2**-49)

# ---- run 41 ----


import pickle
W,toks,stmts=pickle.load(open('/work/p.pkl','rb'))
P=360670; ub=174
# message coordinate: unary block at 0..173, bytes from 174
def msgpos(filepos): return (filepos-180582)%P
for fp in [0,1421302,1421327]:
    mp_=msgpos(fp); 
    if mp_<ub: print(fp,'unary',mp_)
    else:
        b=(mp_-ub)//8; w=b//2
        # which statement: count top-level
        print(fp,'byte',b,'word',w)
# statement index by word
d=0;si=-1;start=[];idx=0
top_index=[]
cnt=0
for k,(t,v) in enumerate(W):
    if t==1 and v==0:
        if d==0: cnt+=1
        d+=1
    elif t==1 and v==1: d-=1
    top_index.append(cnt-1)
for w in [ (msgpos(0)-ub)//16, (msgpos(1421302)-ub)//16]:
    print(w, 'statement',top_index[w]-21 if top_index[w]>=0 else None)
# decode the 3 erroneous bits in each version
bits=''.join(f'{b:08b}' for b in open('/work/received.bin','rb').read())
m=''.join('1' if c=='0' else '0' for c in bits)
for base in [1421302-P, 1421302]:
    s0=base-((msgpos(base)-ub)%16)
    print([ (int(m[s0+16*k:s0+16*k+8],2),int(m[s0+16*k+8:s0+16*k+16],2)) for k in range(-3,2) if s0+16*k+16<=len(m)])
print(len(bits)-1421302, bits[-30:])

# ---- run 42 ----


import pickle
W,toks,stmts=pickle.load(open('/work/p.pkl','rb'))
first={};cnt={}
for i,s in enumerate(stmts):
    for tk in s.replace('(',' ').replace(')',' ').split():
        if tk[0].isalpha():
            cnt[tk]=cnt.get(tk,0)+1
            first.setdefault(tk,i)
pre={'o':2,'v':3,'a':4,'b':5,'c':6,'d':7,'e':8,'f':9}
out=[]
for k in sorted(first,key=lambda x:(pre[x[0]],int(x[1:]))):
    t=pre[k[0]];v=int(k[1:])
    out.append(f"{k}=[{t:02x} {v:02x}] first#{first[k]} n={cnt[k]}")
print('; '.join(out))
