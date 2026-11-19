# The code the blind reader ran, in order (2026-11-19, interpretation, Opus). The message was an experiment with
# 11-bit chunks (22-bit tokens; reverted afterwards), repeated 5 times, cut inside the first and last copy, every
# bit inverted, as received.bin.
# stream: message 415930 bits × 5, received bits 129724 to 1786173 (1656449 bits, then 7 random bits to fill 207057 bytes; starts 129724 bits into a repetition, ends 122453 bits into the last), inverted

# ---- run 1 ----
import os,collections
d=open('/work/received.bin','rb').read()
print(len(d),len(d)*8)
bits=''.join(f'{b:08b}' for b in d)
print(bits.count('1'),bits.count('0'))
print(bits[:400])
n=len(bits)
def fac(n): return [i for i in range(2,n) if n%i==0]
print(fac(n)[:40])

# ---- run 2 ----
import re
runs=[len(x) for x in bits.split('0')]
print(len(runs))
print(collections.Counter(runs).most_common(40))
print(runs[:200])

# ---- run 3 ----
import collections
d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
open('/work/bits.txt','w').write(bits)
runs=[len(x) for x in bits.split('0')]
print(len(runs))
print(sorted(collections.Counter(runs).most_common(60)))
print(runs[:300])

# ---- run 4 ----
import numpy as np
b=np.frombuffer(open('/work/bits.txt','rb').read(),dtype=np.uint8)-48
z=1-b
z=z.astype(float)
N=len(z)
f=np.fft.rfft(z-z.mean(),2*N)
ac=np.fft.irfft(f*np.conj(f))[:5000]
top=np.argsort(ac[1:])[::-1][:30]+1
print(sorted(top))
for k in [7,8,9,10,11,12,16,21,22,32,64]: print(k,ac[k]/ac[0])

# ---- run 5 ----
bits=open('/work/bits.txt').read()
zs=[i for i,c in enumerate(bits) if c=='0']
zset=set(zs)
import collections
c=collections.Counter()
sample=zs[:40000]
for i in sample:
    for k in range(1,400):
        if i+k in zset: c[k]+=1
for k,v in sorted(c.items(),key=lambda x:-x[1])[:30]: print(k,v)

# ---- run 6 ----
bits=open('/work/bits.txt').read()
N=len(bits)
W=20000
for s in range(0,N,W*4):
    seg=bits[s:s+W]
    c=[0]*11
    for i,ch in enumerate(seg):
        if ch=='0': c[(s+i)%11]+=1
    print(s,c)

# ---- run 7 ----
bits=open('/work/bits.txt').read()
def dec(start,count):
    out=[]
    for k in range(count):
        w=bits[start+11*k:start+11*k+11]
        out.append(int(''.join('1' if c=='0' else '0' for c in w),2))
    return out
print(bits[:8])
v=dec(8,600)
print(v)

# ---- run 8 ----
bits=open('/work/bits.txt').read()
import collections
ws=[bits[8+11*k:19+11*k] for k in range(7000)]
c=collections.Counter(ws)
for w,n in c.most_common(80): print(w,n)

# ---- run 9 ----
bits=open('/work/bits.txt').read()
s=8
for k in range(300):
    w=bits[s+11*k:s+11*k+11]
    print(w.replace('1','.').replace('0','#'), end='   ' if k%4!=3 else '\n')

# ---- run 10 ----
bits=open('/work/bits.txt').read()
i=bits.find('1'*30)
print(i)
# locate the start of power region: position of word index ~ 330
s=8+11*325
print(bits[s:s+1200].replace('1','.'))

# ---- run 11 ----
bits=open('/work/bits.txt').read()
N=len(bits)
W=1100
phases=[]
for s in range(0,N-W,W):
    best=None
    for p in range(11):
        # words starting at positions ≡p mod 11; score: count words whose first 5 bits are 1 and that contain a zero
        sc=0
        st=s+((p-s)%11)
        for k in range(st,s+W-11,11):
            w=bits[k:k+11]
            if w[:5]=='11111': sc+=1
            if w[-1]=='0': sc+=1
        if best is None or sc>best[0]: best=(sc,p)
    phases.append(best[1])
# compress
out=[];prev=None
for i,p in enumerate(phases):
    if p!=prev: out.append((i*W,p)); prev=p
print(len(out)); print(out[:200])

# ---- run 12 ----
bits=open('/work/bits.txt').read()
for (a,p0,p1) in [(284900,8,6),(701800,6,4),(1117600,4,2),(1533400,2,0)]:
    # find first position where words at phase p0 begin to fail
    for k in range(a-3000+((p0-(a-3000))%11), a+2000, 11):
        w=bits[k:k+11]
        if w[:5]!='11111':
            print(k, bits[k-60:k+80].replace('1','.')); break

# ---- run 13 ----
bits=open('/work/bits.txt').read()
N=len(bits);P=415930
print(P%11, N, N/P)
diff=[i for i in range(N-P) if bits[i]!=bits[i+P]]
print(len(diff), diff[:20], diff[-20:] if diff else None)

# ---- run 14 ----
bits=open('/work/bits.txt').read()
def inv(w): return int(''.join('1' if c=='0' else '0' for c in w),2)
c=698891
# phase 6 words before, phase 4 after
for k in range(c-11*30+((6-(c-330))%11), c+11*5, 11):
    print(k, bits[k:k+11].replace('1','.'), inv(bits[k:k+11]))
print('---')
for k in range(c-11*5+((4-(c-55))%11), c+11*40, 11):
    print(k, bits[k:k+11].replace('1','.'), inv(bits[k:k+11]))

# ---- run 15 ----
bits=open('/work/bits.txt').read()
def inv(w): return int(''.join('1' if c=='0' else '0' for c in w),2)
c=282961
print(c%11, (c-2)%11)
for p in (8,6):
  st=c-110; st+= (p-st)%11
  print('phase',p)
  print(' '.join(str(inv(bits[k:k+11])) for k in range(st,st+330,11)))

# ---- run 16 ----
bits=open('/work/bits.txt').read()
def inv(w): return int(''.join('1' if c=='0' else '0' for c in w),2)
k=282961
bad=[]
while k<300000:
    w=bits[k:k+11]
    if w[:3]!='111': bad.append(k)
    k+=11
print(bad[:20])
b=bad[0]
for p in (8,6):
  st=b-220; st+=(p-st)%11
  print(p,' '.join(str(inv(bits[x:x+11])) for x in range(st,st+440,11)))

# ---- run 17 ----
bits=open('/work/bits.txt').read()
print(bits[286100:286500].replace('1','.'))

# ---- run 18 ----
bits=open('/work/bits.txt').read()
def inv(w): return int(''.join('1' if c=='0' else '0' for c in w),2)
s=286100
seg=bits[s:s+400]
import re
for m in re.finditer('0+',seg): pass
runs=[(m.start()+s,len(m.group())) for m in re.finditer('0+',seg)]
print(runs[:30])
# frame phase 6 after
end=286500
for st in range(286380,286400):
    if st%11==6: print('phase6 start',st); break
print(' '.join(str(inv(bits[x:x+11])) for x in range(286375,286375+11*30,11)))
print(' '.join(str(inv(bits[x:x+11])) for x in range(286377,286377+11*30,11)))

# ---- run 19 ----
bits=open('/work/bits.txt').read()
def inv(w): return int(''.join('1' if c=='0' else '0' for c in w),2)
print(' '.join(str(inv(bits[x:x+11])) for x in range(286380-11*3,286380+11*120,11)))

# ---- run 20 ----
bits=open('/work/bits.txt').read()
def inv(w): return int(''.join('1' if c=='0' else '0' for c in w),2)
P=415930
A=286380; B=286206+P
assert (B-A)%11==0
W=[inv(bits[x:x+11]) for x in range(A,B,11)]
print(len(W))
import pickle; pickle.dump(W,open('/work/W.pkl','wb'))
import collections
c=collections.Counter(W)
print(sorted(c.items()))
print([i for i,w in enumerate(W) if w==255][:50], c[255])

# ---- run 21 ----
import pickle
W=pickle.load(open('/work/W.pkl','rb'))
def show(a,b):
    line=[]
    out=[]
    for i in range(a,b):
        line.append(str(W[i]))
        if W[i]==0:
            out.append(f'{i-len(line)+1:6d}: '+' '.join(line)); line=[]
    out.append(' '.join(line))
    print('\n'.join(out))
show(0,700)

# ---- run 22 ----
import pickle
W=pickle.load(open('/work/W.pkl','rb'))
idx=[i for i,w in enumerate(W) if w==34]
print(idx[:10])
print(' '.join(map(str,W[idx[0]-40:idx[0]+200])))

# ---- run 23 ----
import pickle,collections
W=pickle.load(open('/work/W.pkl','rb'))
chunks=[];cur=[]
for i,w in enumerate(W):
    if w==2 and i>0 and W[i-1]==0 and cur:
        chunks.append(tuple(cur)); cur=[]
    cur.append(w)
chunks.append(tuple(cur))
print(len(chunks))
# shape: replace numbers>2 with N
def shape(c): return ' '.join(str(x) if x<=2 else 'N' for x in c)
sc=collections.Counter(shape(c) for c in chunks)
for s,n in sc.most_common(60): print(n,'|',s)

# ---- run 24 ----
import pickle,collections
W=pickle.load(open('/work/W.pkl','rb'))
st=[];cur=[];starts=[0]
i=0
while i<len(W):
    cur.append(W[i])
    if len(cur)>=4 and cur[-4:]==[1,1,1,0] and i+1<len(W) and W[i+1]==2:
        st.append(cur);cur=[];starts.append(i+1)
    i+=1
st.append(cur)
print(len(st))
pickle.dump((st,starts),open('/work/st.pkl','wb'))
for k in range(60,200): print(k,starts[k],' '.join(map(str,st[k])))

# ---- run 25 ----
import pickle
W=pickle.load(open('/work/W.pkl','rb'))
print(' '.join(map(str,W[-300:])))

# ---- run 26 ----
import pickle,collections
W=pickle.load(open('/work/W.pkl','rb'))
for t in [0,1,2,3,4]:
    c=collections.Counter(W[i+1] for i in range(len(W)-1) if W[i]==t)
    print(t, c.most_common(25))

# ---- run 27 ----
import pickle
st,starts=pickle.load(open('/work/st.pkl','rb'))
for k in range(200,1940,12): 
    s=' '.join(map(str,st[k]))
    print(k,starts[k],s[:200])

# ---- run 28 ----
import pickle,collections
W=pickle.load(open('/work/W.pkl','rb'))
print(len(W)%2)
pairs=[(W[i],W[i+1]) for i in range(0,len(W)-1,2)]
c=collections.Counter(p[0] for p in pairs)
print(sorted(c.items()))
print(collections.Counter(p for p in pairs if p[0]==1))
depth=0;mind=0;hist=[]
for i,p in enumerate(pairs):
    if p==(1,0): depth+=1
    elif p==(1,1): depth-=1
    hist.append(depth); mind=min(mind,depth)
print('final',depth,'min',mind, 'max',max(hist))
print(collections.Counter(hist).most_common(10))

# ---- run 29 ----
import pickle,collections
W=pickle.load(open('/work/W.pkl','rb'))
pairs=[(W[i],W[i+1]) for i in range(0,len(W)-1,2)]
TAG={0:'#',2:'w',3:'c',4:'x',5:'y',6:'z',7:'u',8:'v',9:'t'}
def parse(i):
    # pairs[i]==(1,0)
    assert pairs[i]==(1,0)
    i+=1; out=[]
    while pairs[i]!=(1,1):
        if pairs[i]==(1,0):
            e,i=parse(i); out.append(e)
        else:
            t,v=pairs[i]; out.append(f'{TAG[t]}{v}'); i+=1
    return out,i+1
top=[];i=0
pre=[]
while i<len(pairs):
    if pairs[i]==(1,0):
        e,i=parse(i); top.append(e)
    else:
        pre.append(pairs[i]); top.append(f'{TAG[pairs[i][0]]}{pairs[i][1]}'); i+=1
def s(e): return '('+' '.join(s(x) for x in e)+')' if isinstance(e,list) else e
print(len(top))
heads=collections.Counter(e[0] if isinstance(e,list) else 'atom' for e in top)
print(heads.most_common(50))
pickle.dump(top,open('/work/top.pkl','wb'))
for k,e in enumerate(top[:120]): print(k,s(e))

# ---- run 30 ----
import pickle
top=pickle.load(open('/work/top.pkl','rb'))
def s(e): return '('+' '.join(s(x) for x in e)+')' if isinstance(e,list) else e
for k in range(120,260): print(k,s(top[k])[:170])

# ---- run 31 ----
import pickle
top=pickle.load(open('/work/top.pkl','rb'))
def s(e): return '('+' '.join(s(x) for x in e)+')' if isinstance(e,list) else e
for k in range(260,400): print(k,s(top[k])[:190])

# ---- run 32 ----
import pickle
top=pickle.load(open('/work/top.pkl','rb'))
def s(e): return '('+' '.join(s(x) for x in e)+')' if isinstance(e,list) else e
for k in range(400,520): print(k,s(top[k])[:230])

# ---- run 33 ----
import pickle
top=pickle.load(open('/work/top.pkl','rb'))
def s(e): return '('+' '.join(s(x) for x in e)+')' if isinstance(e,list) else e
for k in range(520,640): print(k,s(top[k])[:260])

# ---- run 34 ----
import pickle
top=pickle.load(open('/work/top.pkl','rb'))
def s(e): return '('+' '.join(s(x) for x in e)+')' if isinstance(e,list) else e
for k in range(640,760): print(k,s(top[k])[:260])

# ---- run 35 ----
import pickle
top=pickle.load(open('/work/top.pkl','rb'))
def s(e): return '('+' '.join(s(x) for x in e)+')' if isinstance(e,list) else e
for k in range(760,880): print(k,s(top[k])[:260])

# ---- run 36 ----
import pickle
top=pickle.load(open('/work/top.pkl','rb'))
def s(e): return '('+' '.join(s(x) for x in e)+')' if isinstance(e,list) else e
for k in range(880,960): print(k,s(top[k])[:400])

# ---- run 37 ----
import pickle
top=pickle.load(open('/work/top.pkl','rb'))
def s(e): return '('+' '.join(s(x) for x in e)+')' if isinstance(e,list) else e
for k in range(960,1023): print(k,s(top[k])[:600])

# ---- run 38 ----
import pickle,sys
from fractions import Fraction as F
sys.setrecursionlimit(10000)
top=pickle.load(open('/work/top.pkl','rb'))
def s(e): return '('+' '.join(s(x) for x in e)+')' if isinstance(e,list) else e
class Unk(Exception): pass
T,Fa='c1','c2'
def B(x): return T if x else Fa
PAY={('c5','c5'):3,('c6','c6'):5,('c5','c6'):7,('c6','c5'):2}
def strat(name,h):
    # h: list of (own,other) as python tuples; returns list of possible moves
    if name=='c9': return ['c5']
    if name=='c10': return ['c6']
    if name=='c11': return ['c5'] if not h else [h[-1][1]]
    if name=='c12': return ['c6'] if not h else [h[-1][1]]
    if name=='c13': return ['c5'] if all(p[1]!='c6' for p in h) else ['c6']
    if name=='c14':
        if not h: return ['c5']
        return ['c5'] if h[-1][0]==h[-1][1] else ['c6']
    if name=='c15':
        if not h: return ['c5']
        return ['c5'] if h[-1][1]=='c5' else ['c5','c6','c6']
    if name=='c16': return ['c5','c6']
    raise Unk(name)
def play(a,b,n):
    ha=[];hb=[]
    for _ in range(n):
        ma=strat(a,ha);mb=strat(b,hb)
        if len(ma)>1 or len(mb)>1: raise Unk('random')
        ha.append((ma[0],mb[0]));hb.append((mb[0],ma[0]))
    return ha
def tolist(h): return [list(p) for p in h]
def ev(e,env):
    if not isinstance(e,list):
        if e[0]=='#': return F(int(e[1:]))
        if e in env: return env[e]
        if e in ('c1','c2','c5','c6') or e in ['c%d'%i for i in range(9,17)]: return e
        if e=='c17': return ['c9','c10','c11','c12','c13','c14']
        if e=='c19': return complex(0,1)
        raise Unk(e)
    h=e[0]; a=e[1:]
    if h in('w20','w21'):
        v=a[0]; S=ev(a[1],env)
        if not isinstance(S,list): raise Unk('set')
        rs=[ev(a[2],{**env,v:x})==T for x in S]
        return B(all(rs) if h=='w20' else any(rs))
    if h=='w24':
        v=a[0]; S=ev(a[1],env)
        if not isinstance(S,list): raise Unk('set')
        return [ev(a[2],{**env,v:x}) for x in S]
    if h=='w44':
        return ev(a[2],{**env,a[0]:ev(a[1],env)})
    if h=='w29':
        c=ev(a[0],env); return ev(a[1] if c==T else a[2],env)
    if h=='w23':
        op=a[0]; L=ev(a[1],env)
        return ev([op]+[('#lit',x) for x in L],env) if False else apply(op,L)
    args=[ev(x,env) for x in a]
    return apply(h,args)
def apply(h,x):
    if h=='w1': return B(all(v==x[0] for v in x))
    if h=='w2': return B(x[0]!=x[1])
    if h=='w3': return B(all(x[i]<x[i+1] for i in range(len(x)-1)))
    if h=='w4': return B(all(x[i]>x[i+1] for i in range(len(x)-1)))
    if h=='w5': return B(all(x[i]<=x[i+1] for i in range(len(x)-1)))
    if h=='w6': return B(all(x[i]>=x[i+1] for i in range(len(x)-1)))
    if h=='w7':
        r=0
        for v in x: r=r+v
        return r
    if h=='w8':
        r=1
        for v in x: r=r*v
        return r
    if h=='w9':
        r=0
        for v in x: r=r*2048+v
        return r
    if h=='w10': return x[0]-x[1]
    if h=='w11': return -x[0]
    if h=='w12': return F(x[0])/F(x[1])
    if h=='w13': return B(x[0]==Fa)
    if h=='w14': return B(all(v==T for v in x))
    if h=='w15': return B(any(v==T for v in x))
    if h=='w22': return B(x[0]==Fa or x[1]==T)
    if h=='w16': return list(x)
    if h=='w17': return F(len(x[0]))
    if h=='w18': return x[0][int(x[1])-1]
    if h=='w19': return F(sum(1 for v in x[1] if v==x[0]))
    if h=='w25': return sum(x[0],F(0))/len(x[0])
    if h=='w26': return F(sum(1 for v in x[1] if v==x[0]),len(x[1]))
    if h=='w27': return [[p,q] for p in x[0] for q in x[1]]
    if h=='w28': return x[0][1:]
    if h=='w30': return F(PAY[(x[0],x[1])])
    if h=='w31': return strat(x[0],[tuple(p) for p in x[1]])
    if h=='w32': return tolist(play(x[0],x[1],int(x[2])))
    if h=='w33': return F(sum(PAY[p] for p in play(x[0],x[1],int(x[2]))))
    if h=='w34':
        b,ex=x
        if isinstance(b,complex): return b**int(ex)
        return F(b)**int(ex)
    if h=='w35': return abs(x[0])
    if h=='w37': return sum(p*q for p,q in zip(x[0],x[1]))
    if h=='w40':
        a,b=x; return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
    raise Unk(h)
res={'true':[],'false':[],'unk':[]}
for k,e in enumerate(top):
    if not isinstance(e,list): continue
    try:
        r=ev(e,{})
        res['true' if r==T else 'false' if r==Fa else 'unk'].append(k)
    except (Unk,KeyError,TypeError,IndexError,ZeroDivisionError) as ex:
        res['unk'].append(k)
print(len(res['true']),len(res['false']),len(res['unk']))
for k in res['false']: print('FALSE',k,s(top[k])[:200])
pickle.dump(res,open('/work/res.pkl','wb'))

# ---- run 39 ----
import pickle,sys,itertools
exec(open('/dev/stdin').read()) if False else None

# ---- run 40 ----
code=r'''
import pickle,sys,cmath,math
from fractions import Fraction as F
sys.setrecursionlimit(10000)
top=pickle.load(open('/work/top.pkl','rb'))
def s(e): return '('+' '.join(s(x) for x in e)+')' if isinstance(e,list) else e
class Unk(Exception): pass
T,Fa='c1','c2'
def B(x): return T if x else Fa
PAY={('c5','c5'):3,('c6','c6'):5,('c5','c6'):7,('c6','c5'):2}
SAMPLES={}
def strat(name,h):
    if name=='c9': return ['c5']
    if name=='c10': return ['c6']
    if name=='c11': return ['c5'] if not h else [h[-1][1]]
    if name=='c12': return ['c6'] if not h else [h[-1][1]]
    if name=='c13': return ['c5'] if all(p[1]!='c6' for p in h) else ['c6']
    if name=='c14':
        if not h: return ['c5']
        return ['c5'] if h[-1][0]==h[-1][1] else ['c6']
    if name=='c15':
        if not h: return ['c5']
        return ['c5'] if h[-1][1]=='c5' else ['c5','c6','c6']
    if name=='c16': return ['c5','c6']
    raise Unk(name)
def play(a,b,n):
    ha=[];hb=[]
    for _ in range(n):
        ma=strat(a,ha);mb=strat(b,hb)
        if len(ma)>1 or len(mb)>1: raise Unk('random')
        ha.append((ma[0],mb[0]));hb.append((mb[0],ma[0]))
    return ha
def ev(e,env):
    if not isinstance(e,list):
        if e[0]=='#': return F(int(e[1:]))
        if e in env: return env[e]
        if e in ('c1','c2','c5','c6') or e in ['c%d'%i for i in range(9,17)]: return e
        if e=='c17': return ['c9','c10','c11','c12','c13','c14']
        if e=='c19': return complex(0,1)
        if e=='c22': return math.pi
        if e=='c21': return math.e
        if e in SAMPLES: return SAMPLES[e]
        raise Unk(e)
    h=e[0]; a=e[1:]
    if h in('w20','w21'):
        v=a[0]; S=ev(a[1],env)
        if not isinstance(S,list): raise Unk('set')
        rs=[ev(a[2],{**env,v:x})==T for x in S]
        return B(all(rs) if h=='w20' else any(rs))
    if h=='w24':
        v=a[0]; S=ev(a[1],env)
        if not isinstance(S,list): raise Unk('set')
        return [ev(a[2],{**env,v:x}) for x in S]
    if h=='w44': return ev(a[2],{**env,a[0]:ev(a[1],env)})
    if h=='w29':
        c=ev(a[0],env); return ev(a[1] if c==T else a[2],env)
    if h=='w23': return apply(a[0],ev(a[1],env))
    return apply(h,[ev(x,env) for x in a])
def close(a,b):
    if isinstance(a,(complex,float)) or isinstance(b,(complex,float)): return abs(complex(a)-complex(b))<1e-9
    return a==b
def apply(h,x):
    if h=='w1': return B(all(close(v,x[0]) for v in x))
    if h=='w2': return B(not close(x[0],x[1]))
    if h=='w3': return B(all(x[i]<x[i+1] for i in range(len(x)-1)))
    if h=='w4': return B(all(x[i]>x[i+1] for i in range(len(x)-1)))
    if h=='w5': return B(all(x[i]<=x[i+1] for i in range(len(x)-1)))
    if h=='w6': return B(all(x[i]>=x[i+1] for i in range(len(x)-1)))
    if h=='w7':
        r=0
        for v in x: r=r+v
        return r
    if h=='w8':
        r=1
        for v in x: r=r*v
        return r
    if h=='w9':
        r=0
        for v in x: r=r*2048+v
        return r
    if h=='w10': return x[0]-x[1]
    if h=='w11': return -x[0]
    if h=='w12': return x[0]/x[1] if isinstance(x[0],(complex,float)) or isinstance(x[1],(complex,float)) else F(x[0])/F(x[1])
    if h=='w13': return B(x[0]==Fa)
    if h=='w14': return B(all(v==T for v in x))
    if h=='w15': return B(any(v==T for v in x))
    if h=='w22': return B(x[0]==Fa or x[1]==T)
    if h=='w16': return list(x)
    if h=='w17': return F(len(x[0]))
    if h=='w18': return x[0][int(x[1])-1]
    if h=='w19': return F(sum(1 for v in x[1] if v==x[0]))
    if h=='w25': return sum(x[0],F(0))/len(x[0])
    if h=='w26': return F(sum(1 for v in x[1] if v==x[0]),len(x[1]))
    if h=='w27': return [[p,q] for p in x[0] for q in x[1]]
    if h=='w28': return x[0][1:]
    if h=='w30': return F(PAY[(x[0],x[1])])
    if h=='w31': return strat(x[0],[tuple(p) for p in x[1]])
    if h=='w32': return [list(p) for p in play(x[0],x[1],int(x[2]))]
    if h=='w33': return F(sum(PAY[p] for p in play(x[0],x[1],int(x[2]))))
    if h=='w34':
        b,ex=x
        if isinstance(b,(complex,float)) : return b**ex
        return F(b)**int(ex)
    if h=='w35': return abs(x[0])
    if h=='w36': return cmath.exp(complex(x[0]))
    if h=='w38': return cmath.cos(complex(x[0]))
    if h=='w37': return sum(p*q for p,q in zip(x[0],x[1]))
    if h=='w40':
        a,b=x; return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
    raise Unk(h)
'''
open('/work/ev.py','w').write(code)

# ---- run 41 ----
import sys; sys.path.insert(0,'/work')
import ev as E
from fractions import Fraction as F
E.SAMPLES.update({'c3':[F(i) for i in range(0,5)],
 'c4':[F(i) for i in range(-3,4)]+[F(1,2),F(-2,3)],
 'c18':[F(i) for i in range(-2,3)]+[F(1,2),F(-3,4)],
 'c20':[complex(1,2),complex(-1,0.5),complex(0,1),complex(2,0)]})
res={'true':[],'false':[],'unk':[]}
for k,e in enumerate(E.top):
    if not isinstance(e,list): continue
    try:
        r=E.ev(e,{})
        res['true' if r==E.T else 'false' if r==E.Fa else 'unk'].append(k)
    except Exception as ex:
        res['unk'].append(k)
print(len(res['true']),len(res['false']),len(res['unk']))
for k in res['false']: print('FALSE',k,E.s(E.top[k])[:220])

# ---- run 42 ----
import sys; sys.path.insert(0,'/work')
import ev as E
from fractions import Fraction as F
ok=[]
for k in list(range(343,415))+[1020,1021,1022]:
    try: r=E.ev(E.top[k],{})
    except Exception as ex: r='unk:'+str(ex)
    ok.append((k,r))
print([x for x in ok if x[1]!='c1'])
S=['c9','c10','c11','c12','c13','c14']
for a in S:
    row=[sum(E.PAY[p] for p in E.play(a,b,255)) for b in S]
    print(a,row,sum(row))

# ---- run 43 ----
import math
c=2.99792458e8; hbar=1.054571817e-34; G=6.67430e-11; kB=1.380649e-23; e=1.602176634e-19; eps0=8.8541878128e-12
me=9.1093837e-31; mp=1.67262192e-27; mn=1.67492750e-27
lP=math.sqrt(hbar*G/c**3); tP=math.sqrt(hbar*G/c**5); mP=math.sqrt(hbar*c/G); TP=mP*c**2/kB
k=1/(4*math.pi*eps0)
Ry=13.605693*e  # J (infinite mass) ; use reduced-mass hydrogen
Ry_H=Ry/(1+me/mp)
E21=0.75*Ry_H
def chk(name,lo,val,hi): print(f'{name:40s} {lo:.6g} < {val:.6g} < {hi:.6g}  {"OK" if lo<val<hi else "FAIL"}')
chk('mp/me',1836,mp/me,1837)
chk('mn/me',1838,mn/me,1839)
chk('mn/mp',1+2**-11,mn/mp,1+2**-9)
chk('m(D)/m(H)',2-2**-9,2.014101778/1.007825032,2)
chk('alpha',1/138,k*e**2/(hbar*c),1/137)
chk('Fe/Fg (p,e) log2',130,math.log2(k*e*e/(G*mp*me)),131)
chk('mp/mP log2',-64,math.log2(mp/mP),-63)
chk('me/mP log2',-75,math.log2(me/mP),-74)
f21=1420405751.77; E_hf=2*math.pi*hbar*f21
chk('E(21cm)/E21 log2',-21,math.log2(E_hf/E21),-20)
chk('1/(f tP) log2',113,math.log2(1/(f21*tP)),114)
chk('lambda/lP log2',113,math.log2(c/f21/lP),114)
chk('E21/(me c2) log2',-16,math.log2(E21/(me*c*c)),-15)
chk('tau_n/tP log2',153,math.log2(879.4/tP),154)
chk('t1/2 C14 / H3 log2',8,math.log2(5730/12.32),9)
chk('K0/me',973,497.611e6*e/c**2/me,975)
chk('KL asym (1+d)/(1-d)',1+2**-8,(1+3.32e-3)/(1-3.32e-3),1+2**-7)
chk('Ttp H2/H2O *2^11',103,13.8033/273.16*2048,104)
chk('Ttp Ne/H2O *2^13',736,24.5561/273.16*8192,737)
chk('Ttp Ar/H2O *2^12',1256,83.8058/273.16*4096,1257)
chk('k Ttp(H2O)/E21 *2^17',302,kB*273.16/E21*2**17,303)
chk('Ttp/TP *2^106',156,273.16/TP*2**106,157)
pP=mP/(lP*tP**2)
chk('ptp(H2O)/pP *2^376',203,611.657/pP*2**376,204)
chk('ptp H2/H2O',11,7.041e3/611.657,12)
chk('ptp Ne/H2O *2',141,43.368e3/611.657*2,143)
chk('ptp Ar/H2O',112,68.89e3/611.657,113)
chk('m He4/(4 m H1)',1-2**-7,4.002602/(4*1.007825032),1-2**-8)
chk('T_CMB/Ttp *2^14',163,2.7255/273.16*2**14,164)
Ms=1.98847e30; Rs=6.957e8; Ts=5772; Ls=3.828e26
chk('Msun/mp log2',189,math.log2(Ms/mp),190)
chk('Rsun/lP log2',144,math.log2(Rs/lP),145)
chk('Tsun/Ttp',21,Ts/273.16,22)
chk('Lsun/(c5/G) log2',-87,math.log2(Ls/(c**5/G)),-86)
chk('AU/lP log2',152,math.log2(1.495978707e11/lP),153)
chk('yr/tP log2',168,math.log2(3.15581e7/tP),169)
chk('Mearth/mp log2',171,math.log2(5.9722e24/mp),172)
Msg=4.297e6*Ms; R0=8.178e3*3.0857e16
chk('MSgrA/mp log2',211,math.log2(Msg/mp),212)
chk('R0/lP log2',183,math.log2(R0/lP),184)
chk('Pgal(230Myr)/tP log2',196,math.log2(230e6*3.15581e7/tP),197)
chk('Mencl/MSgr log2 (230Myr)',12,math.log2(4*math.pi**2*R0**3/(G*Msg*(230e6*3.15581e7)**2)),16)
chk('v_rot/c log2 (240km/s)',-11,math.log2(240e3/c),-10)
chk('U/c log2 (11 km/s)',-99,math.log2(11.1e3/c),-13)
chk('W/c log2 (7.25 km/s)',-99,math.log2(7.25e3/c),-14)
chk('sigmaT4 check sigma',5.67e-8,math.pi**2/60*kB**4/(hbar**3*c**2),5.68e-8)

# ---- run 44 ----
import math
tP=5.391247e-44
P={'c51 Crab B0531+21':(0.0333924,4.2e-13,184.56,-5.78,(138,139),(106/2**48,131/2**48),[(-1,-15/16),(-5/32,0),(-5/32,-1/32)]),
'c52 Vela B0833-45':(0.0893,1.25e-13,263.55,-2.79,(140,141),(126/2**50,155/2**50),[(-3/16,-1/32),(-1,-15/16),(-1/8,1/32)]),
'c53 J0437-4715':(0.0057575,5.73e-20,253.39,-41.96,(136,137),(121/2**71,149/2**71),[(-9/32,-5/32),(-25/32,-21/32),(-23/32,-19/32)]),
'c54 B1937+21':(0.0015578,1.05e-19,57.51,-0.29,(134,135),(111/2**70,137/2**70),[(15/32,19/32),(25/32,29/32),(-1/16,1/16)]),
'c55 B0329+54':(0.71452,2.05e-15,144.99,-1.22,(143,144),(2**-49,2**-48),[(-7/8,-3/4),(1/2,5/8),(-3/32,1/32)]),
'c56 B1919+21':(1.33730,1.348e-15,55.78,3.50,(144,145),(2**-50,2**-49),[(1/2,5/8),(3/4,29/32),(0,1/8)])}
for n,(p,pd,l,b,pr,pdr,dr) in P.items():
    lp=math.log2(p/tP); L,Bb=math.radians(l),math.radians(b)
    v=(math.cos(Bb)*math.cos(L),math.cos(Bb)*math.sin(L),math.sin(Bb))
    ok=[pr[0]<lp<pr[1], pdr[0]<pd<pdr[1]]+[lo<x<hi for x,(lo,hi) in zip(v,dr)]
    print(n, round(lp,2), pd, [round(x,3) for x in v], ok)

# ---- run 45 ----
bits=open('/work/bits.txt').read()
N=len(bits);P=415930
print(N, bits[1240500:1240540]); print(bits[1240500+P:N])
# which copy-start (prime block) offsets
for n in range(4): print('prime block at',286206+n*P - P, 286206+n*P)
print('file starts at offset into message (from prime block):', (0-(286206-P)))

# ---- run 46 ----
import pickle,collections
top=pickle.load(open('/work/top.pkl','rb'))
first={};cnt=collections.Counter()
def walk(e,k):
    if isinstance(e,list):
        for x in e: walk(x,k)
    else:
        if e[0]!='#':
            cnt[e]+=1
            first.setdefault(e,k)
for k,e in enumerate(top): walk(e,k)
bytag=collections.defaultdict(list)
for a in first: bytag[a[0]].append(a)
for t in sorted(bytag):
    L=sorted(bytag[t],key=lambda a:int(a[1:]))
    print(t,len(L),' '.join(f'{a}@{first[a]}' for a in L))
