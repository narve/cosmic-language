# The code the blind reader ran, in order (2026-11-20, interpretation, decoy message (Kepler-1647), Opus).
# Received: the decoy repeated 5 times, cut inside the first and last copy, every bit inverted, as /work/received.bin.

# ---- run 1 ----

import os
d=open('/work/received.bin','rb').read()
print(len(d), len(d)*8)
print(d[:64].hex())
from collections import Counter
bits=''.join(f'{b:08b}' for b in d)
print(Counter(bits))
import sympy
n=len(bits); print(sympy.factorint(n))
print(bits[:400])

# ---- run 2 ----

d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
n=len(bits)
def fac(n):
    f=[];p=2
    while p*p<=n:
        while n%p==0: f.append(p); n//=p
        p+=1
    if n>1:f.append(n)
    return f
print(fac(n))
import re
from collections import Counter
print(Counter(len(m) for m in re.findall('0+',bits)).most_common(20))
print(Counter(len(m) for m in re.findall('1+',bits)).most_common(30))
for i in range(0,1200,100): print(bits[i:i+100])

# ---- run 3 ----

for m in re.finditer('0{6,}',bits):
    if len(m.group())>8: print(m.start(),len(m.group()), bits[m.start()-40:m.start()], bits[m.end():m.end()+40])

# ---- run 4 ----

import re
d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
open('/work/bits.txt','w').write(bits)
for m in re.finditer('0{9,}',bits):
    print(m.start(),len(m.group()), bits[m.start()-40:m.start()], bits[m.end():m.end()+40])

# ---- run 5 ----

bits=open('/work/bits.txt').read();n=len(bits)
P=357758
diff=[i for i in range(n-P) if bits[i]!=bits[i+P]]
print(len(diff), n-P, diff[:50])
print(n/P)

# ---- run 6 ----

def fac(n):
    f=[];p=2
    while p*p<=n:
        while n%p==0: f.append(p); n//=p
        p+=1
    if n>1:f.append(n)
    return f
print(fac(357758), bits[-20:], bits[-20-P:-P])
print(n - 3*P, 273209-P)

# ---- run 7 ----

bits=open('/work/bits.txt').read();n=len(bits);P=357758
def fac(n):
    f=[];p=2
    while p*p<=n:
        while n%p==0: f.append(p); n//=p
        p+=1
    if n>1:f.append(n)
    return f
print(fac(P), bits[-20:], bits[-20-P:-P])
# look at tokenization: split on '0'
toks=bits[:P].split('0')
from collections import Counter
c=Counter(toks);print(len(c));print(c.most_common(40))

# ---- run 8 ----

bits=open('/work/bits.txt').read();P=357758
L=[len(t) for t in bits[:P].split('0')]
print(len(L))
print(L[:600])

# ---- run 9 ----

import numpy as np
bits=open('/work/bits.txt').read();P=357758
a=np.frombuffer(bits[:P].encode(),dtype=np.uint8)-48
z=1-a
for k in range(2,40):
    pos=np.nonzero(z)[0]%k
    c=np.bincount(pos,minlength=k)
    print(k, (c.max()/c.sum()).round(3), end='; ')
print()
x=z-z.mean()
f=np.fft.rfft(x,2**20);ac=np.fft.irfft(f*np.conj(f))[:200]
print(np.argsort(-ac[1:200])[:20]+1)

# ---- run 10 ----

bits=open('/work/bits.txt').read();P=357758
s=bits[:P]
pos=[i for i,c in enumerate(s) if c=='0']
for k in range(2,40):
    c=[0]*k
    for p in pos:c[p%k]+=1
    print(k, round(max(c)/len(pos),3), end='; ')
print()
zs=set(pos)
ac=[(sum(1 for p in pos if p+l in zs),l) for l in range(1,120)]
print(sorted(ac,reverse=True)[:25])

# ---- run 11 ----

bits=open('/work/bits.txt').read();P=357758
s=bits[:P]
pos=[i for i,c in enumerate(s) if c=='0']
c=[0]*8
for p in pos:c[p%8]+=1
print(c)
# local phase across the file in windows
for w in range(0,len(bits),20000):
    seg=bits[w:w+20000];c=[0]*8
    for i,ch in enumerate(seg):
        if ch=='0':c[(w+i)%8]+=1
    print(w, c.index(max(c)), c)

# ---- run 12 ----

bits=open('/work/bits.txt').read();P=357758
from collections import Counter
B=[int(bits[i:i+8],2) for i in range(0,272000,8)]
c=Counter(B);print(len(c))
for b,k in c.most_common(): print(f'{b:02x} {b:08b} {k}', end=' | ')

# ---- run 13 ----

bits=open('/work/bits.txt').read()
s=bits[:6000]
for i in range(0,3000,64): print(s[i:i+64].replace('1','.').replace('0','#'))

# ---- run 14 ----

bits=open('/work/bits.txt').read()
s=bits[:272000]
for k in (16,32,64):
    c=[0]*k
    for i,ch in enumerate(s):
        if ch=='0':c[i%k]+=1
    print(k,c)

# ---- run 15 ----

bits=open('/work/bits.txt').read()
from collections import Counter
W=[bits[i:i+16] for i in range(0,272000,16)]
c=Counter(W);print(len(c))
for w,k in c.most_common(60): print(w,k)

# ---- run 16 ----

bits=open('/work/bits.txt').read()
W=[int(bits[i:i+16],2)^0xffff for i in range(0,272000,16)]
for r in range(0,800,16): print(r, ' '.join(f'{w:04x}' for w in W[r:r+16]))

# ---- run 17 ----

bits=open('/work/bits.txt').read()
print(bits[272800:273400])

# ---- run 18 ----

bits=open('/work/bits.txt').read()
st=273150
for i in range(st,273400,16): print(i, i%16, bits[i:i+16], f'{int(bits[i:i+16],2)^0xffff:04x}')

# ---- run 19 ----

bits=open('/work/bits.txt').read()
for i in range(273136,273216,16): print(i, bits[i:i+16], f'{int(bits[i:i+16],2)^0xffff:04x}')
s=bits[273180:273400]
print(s)
# parse zero runs between ones starting at 273184
i=273184; runs=[]
seg=bits[273184:273360]
print([len(x) for x in seg.split('1')])

# ---- run 20 ----

bits=open('/work/bits.txt').read()
c=[0]*16
for i in range(273400,630000):
    if bits[i]=='0': c[i%16]+=1
print(c)
print(sum([1,1,2,3,5,7,11,13,17,19,23,29,31])+13)

# ---- run 21 ----

bits=open('/work/bits.txt').read()
P=357758; S=273184
msg=bits[S:S+P]
assert msg==bits[S+P:S+2*P]
open('/work/msg.txt','w').write(msg)
words=[int(msg[190+16*k:190+16*k+16],2)^0xffff for k in range(22348)]
import json; json.dump(words,open('/work/words.json','w'))
from collections import Counter
print(Counter(w&0x7800 for w in words))
f=Counter((w>>15, (w>>7)&1) for w in words);print(f)
c=Counter(((w>>8)&7, w&0x7f) for w in words)
print(len(c))
byt=Counter((w>>8)&7 for w in words);print(byt)
for t in range(8):
    print(t, sorted(Counter(w&0x7f for w in words if (w>>8)&7==t).items()))

# ---- run 22 ----

import json
words=json.load(open('/work/words.json'))
def tok(w):
    t=(w>>8)&7; x=w&0x7f; f=('A' if w>>15 else '')+('b' if (w>>7)&1 else '')
    return f"{'NWVXY'[t]}{x}{('.'+f) if f else ''}"
out=[tok(w) for w in words]
for r in range(0,600,20): print(r,' '.join(out[r:r+20]))

# ---- run 23 ----

import json
from collections import Counter
words=json.load(open('/work/words.json'))
c=Counter()
for w in words:
    hi=(w>>8)&0xff; lo=w&0xff
    c[('hi',bin(hi).count('1')%2)]+=1
    c[('lo',bin(lo).count('1')%2)]+=1
    c[('w',bin(w).count('1')%2)]+=1
print(c)

# ---- run 24 ----

import json
from collections import Counter,defaultdict
words=json.load(open('/work/words.json'))
d=defaultdict(Counter)
for w in words:
    d[((w>>8)&7, w&0x7f)][(w>>15,(w>>7)&1)]+=1
for k in sorted(d):
    if sum(d[k].values())>40: print(k, dict(d[k]))

# ---- run 25 ----

import json
from collections import Counter
words=json.load(open('/work/words.json'))
A=''.join(str(w>>15) for w in words)
b=''.join(str((w>>7)&1) for w in words)
print(A[:400]);print(b[:400])
# A on non-separator tokens only
A2=''.join(str(w>>15) for w in words if (w&0x7fff)!=0x0080)
print(A2[:400])

# ---- run 26 ----

import json
from collections import Counter
words=json.load(open('/work/words.json'))
for r in range(0,22348,500):
    seg=words[r:r+500]
    tc=Counter((w>>8)&7 for w in seg)
    sep=sum(1 for w in seg if w==0x8080)
    vals=Counter(w&0x7f for w in seg if (w>>8)&7==1)
    print(r, dict(sorted(tc.items())), sep, sorted(vals)[:30])

# ---- run 27 ----

import json
words=json.load(open('/work/words.json'))
def tok(w):
    t=(w>>8)&7; x=w&0x7f; f=('A' if w>>15 else '')+('b' if (w>>7)&1 else '')
    return f"{'NWVXY'[t]}{x}{('.'+f) if f else ''}"
segs=[];cur=[]
for w in words:
    if w==0x8080:
        segs.append(cur);cur=[]
    else: cur.append(w)
segs.append(cur)
print(len(segs))
from collections import Counter
print(Counter(len(s) for s in segs).most_common(20))
for s in segs[:80]: print(' '.join(tok(w) for w in s))

# ---- run 28 ----

import json
from collections import Counter
words=json.load(open('/work/words.json'))
# statements: split on 0x0080 or 0x8080 (low byte 0x80 with type 0, value 0)
stm=[];cur=[]
for w in words:
    cur.append(w)
    if (w&0x7fff)==0x0080:
        stm.append(cur);cur=[]
print(len(stm))
c=Counter(); c2=Counter()
for s in stm:
    a=sum(w>>15 for w in s)%2
    c[(len(s)>1,a)]+=1
    ones=sum(bin(w).count('1') for w in s)%2
    c2[ones]+=1
print(c,c2)

# ---- run 29 ----

import json
words=json.load(open('/work/words.json'))
def tok(w):
    t=(w>>8)&7; x=w&0x7f; f=('A' if w>>15 else '')+('b' if (w>>7)&1 else '')
    return f"{'NWVXY'[t]}{x}{('.'+f) if f else ''}"
stm=[];cur=[]
for w in words:
    cur.append(w)
    if (w&0x7fff)==0x0080:
        stm.append(cur);cur=[]
for i,s in enumerate(stm[:400]):
    if len(s)>1: print(i,' '.join(tok(w) for w in s))

# ---- run 30 ----

import json
words=json.load(open('/work/words.json'))
def tok(w):
    if w==0x8080: return '{'
    if w==0x0080: return '}'
    t=(w>>8)&7; x=w&0x7f; f=('A' if w>>15 else '')+('b' if (w>>7)&1 else '')
    return f"{'NWVXY'[t]}{x}{('.'+f) if f else ''}"
s=' '.join(tok(w) for w in words[:1500])
import textwrap
print(textwrap.fill(s,200))

# ---- run 31 ----

import json, math
from collections import Counter
words=json.load(open('/work/words.json'))
A=[w>>15 for w in words]
n=len(A)
for k in range(1,13):
    c=Counter(tuple(A[i:i+k]) for i in range(n-k))
    H=-sum(v/(n-k)*math.log2(v/(n-k)) for v in c.values())
    print(k, round(H,3), round(H/k,3))
# A conditional on token class
cls=Counter(); 
for w in words:
    t=(w>>8)&7; cls[(t, (w&0x80)>0, w>>15)]+=1
print(cls)

# ---- run 32 ----

import json, math
from collections import Counter,defaultdict
words=json.load(open('/work/words.json'))
def cls(w): 
    w&=0x7fff
    if w==0x80: return 'B'
    t=(w>>8)&7
    return 'NWVXY'[t]+('b' if w&0x80 else '')
def MI(pairs):
    c=Counter(pairs);n=len(pairs)
    ca=Counter(a for a,b in pairs);cb=Counter(b for a,b in pairs)
    return sum(v/n*math.log2(v*n/(ca[a]*cb[b])) for (a,b),v in c.items())
A=[w>>15 for w in words]
for off in (-3,-2,-1,0,1,2,3):
    pairs=[(A[i],cls(words[i+off])) for i in range(3,len(words)-3)]
    print(off, round(MI(pairs),4))
pairs=[(A[i],(cls(words[i-1]),cls(words[i]),cls(words[i+1]))) for i in range(3,len(words)-3)]
print('ctx', round(MI(pairs),4))
d=defaultdict(Counter)
for i in range(1,len(words)-1): d[(cls(words[i-1]),cls(words[i]),cls(words[i+1]))][A[i]]+=1
for k,v in sorted(d.items(),key=lambda x:-sum(x[1].values()))[:30]: print(k,dict(v))

# ---- run 33 ----

import json
words=json.load(open('/work/words.json'))
N=len(words)
def solve(rows):
    # rows: list of (int mask of features, target bit) ; gaussian elimination GF2
    piv={}
    for m,t in rows:
        x=(m<<1)|t
        while x>>1:
            h=(x>>1).bit_length()-1
            if h in piv: x^=piv[h]
            else: piv[h]=x;break
        else:
            if x&1: return False
    return True
def feats(i,offs):
    m=0
    for o in offs:
        w=words[i+o] if 0<=i+o<N else 0
        if o==0: w&=0x7fff
        m=(m<<16)|w
    return (m<<1)|1
for offs in ([0],[-1,0],[0,1],[-1,0,1],[-2,-1,0],[-2,-1,0,1,2]):
    rows=[(feats(i,offs),words[i]>>15) for i in range(2,N-2)]
    print(offs, solve(rows))

# ---- run 34 ----

import json
words=json.load(open('/work/words.json'))
N=len(words)
def isB(w): return (w&0x7fff)==0x80
depth=0; mind=0; trace=[]
for i,w in enumerate(words):
    if isB(w):
        nxt=words[i+1] if i+1<N else 0
        if not isB(nxt) and ((nxt>>8)&7)!=0: depth+=1
        else: depth-=1
    trace.append(depth); mind=min(mind,depth)
print(depth,mind, max(trace))
print(trace[:200])

# ---- run 35 ----

import json
words=json.load(open('/work/words.json'))
N=len(words)
def tok(w):
    if (w&0x7fff)==0x80: return 'B'+('1' if w>>15 else '0')
    t=(w>>8)&7; x=w&0x7f; f=('A' if w>>15 else '')+('b' if (w>>7)&1 else '')
    return f"{'NWVXY'[t]}{x}{('.'+f) if f else ''}"
def isB(w): return (w&0x7fff)==0x80
depth=0; last0=0
for i,w in enumerate(words):
    if isB(w):
        nxt=words[i+1] if i+1<N else 0
        if not isB(nxt) and ((nxt>>8)&7)!=0: depth+=1
        else: depth-=1
    if depth==0: last0=i
    if i-last0>60: print(i,last0); break
print(' '.join(tok(w) for w in words[last0-20:i+5]))

# ---- run 36 ----

import json
words=json.load(open('/work/words.json'))
N=len(words)
def isB(w): return (w&0x7fff)==0x80
def cl(w):
    w&=0x7fff
    if w==0x80: return 'B'
    return 'NWVXY'[(w>>8)&7]+('b' if w&0x80 else '')
for rule in (['W'],['W','V'],['W','V','X'],['W','V','X','Y'],['W','X','Y']):
    depth=0; mind=0; neg=None
    for i,w in enumerate(words):
        if isB(w):
            nxt=cl(words[i+1]) if i+1<N else 'B'
            if nxt in rule: depth+=1
            else: depth-=1
            if depth<0 and neg is None: neg=i
        mind=min(mind,depth)
    print(rule, depth, mind, neg)

# ---- run 37 ----

import json
from collections import Counter
words=json.load(open('/work/words.json'))
N=len(words)
def cl(w):
    w&=0x7fff
    if w==0x80: return 'B'
    return 'NWVXY'[(w>>8)&7]+('b' if w&0x80 else '')
def atom(w):
    return (cl(w), w&0x7f, w>>15)
pos=20  # header
def parse(i):
    # words[i] is open B
    assert cl(words[i])=='B'
    node={'openA':words[i]>>15,'head':atom(words[i+1]),'args':[]}
    i+=2
    while True:
        w=words[i]
        if cl(w)=='B':
            if i+1<N and cl(words[i+1])=='W':
                ch,i=parse(i); node['args'].append(ch)
            else:
                node['closeA']=w>>15; return node,i+1
        else:
            node['args'].append(atom(w)); i+=1
trees=[]
i=20
while i<N:
    t,i=parse(i); trees.append(t)
print(len(trees))
c=Counter(); 
def walk(t,d=0):
    c[('open',d==0,t['openA'])]+=1; c[('close',d==0,t['closeA'])]+=1
    for a in t['args']:
        if isinstance(a,dict): walk(a,d+1)
for t in trees: walk(t)
print(c)
import pickle; pickle.dump(trees,open('/work/trees.pkl','wb'))

# ---- run 38 ----

import pickle
trees=pickle.load(open('/work/trees.pkl','rb'))
def s(a,showA=True):
    if isinstance(a,dict):
        h=s(a['head'],showA)
        body=' '.join([h]+[s(x,showA) for x in a['args']])
        return ('*' if showA and a['openA'] else '')+'('+body+')'+('*' if showA and a['closeA'] else '')
    c,v,A=a
    name={'N':'','W':'w','V':'v','X':'x','Y':'y','Wb':'W','Vb':'V','Xb':'X','Yb':'Y'}[c]+str(v)
    return name+('*' if showA and A else '')
out=[s(t) for t in trees]
open('/work/stmts.txt','w').write('\n'.join(out))
for i,o in enumerate(out[:150]): print(i,o)

# ---- run 39 ----

import pickle
trees=pickle.load(open('/work/trees.pkl','rb'))
rows=[]
for t in trees:
    if t['head'][:2]==('W',0) and len(t['args'])==2:
        a,c=t['args']
        if isinstance(a,dict) and a['head'][:2]==('W',3) and all(not isinstance(x,dict) and x[0]=='N' for x in a['args']) and not isinstance(c,dict) and c[0]=='N':
            rows.append(([(x[1],x[2]) for x in a['args']],(c[1],c[2]), t['closeA'], a['closeA']))
for r in rows: print(r, '2v+A:', sum(2*v+A for v,A in r[0]), 2*r[1][0]+r[1][1])

# ---- run 40 ----

bits=open('/work/bits.txt').read()
P=357758; S=273185
msg=bits[S:S+P]
assert msg==bits[S+P:S+2*P]
print(msg[:200])
# words start where?
st=191-1  # previously words at S_old+190 -> now same offset+1 -> S+190
W=[int(msg[st+16*k:st+16*k+16],2)^0xffff for k in range(22348)]
print(len(msg)-st-16*22348)
print(msg[st+16*22348:])
from collections import Counter
print(Counter(w>>12 for w in W), Counter((w>>8)&0xf for w in W))
import json; json.dump(W,open('/work/W.json','w')); open('/work/msg.txt','w').write(msg)

# ---- run 41 ----

import json
from collections import Counter
W=json.load(open('/work/W.json'))
N=len(W)
def cl(w):
    t=(w>>9)&7; b=(w>>8)&1
    return 'NWVXY'[t]+('b' if b else '')
print(Counter(cl(w) for w in W))
print(Counter(w for w in W if cl(w)=='Nb'))
for c in ['W','Wb','V','Vb','X','Xb','Y','Yb','N']:
    print(c, sorted(Counter(w&0xff for w in W if cl(w)==c).items()))

# ---- run 42 ----

import json,pickle
W=json.load(open('/work/W.json'))
N=len(W)
def cl(w):
    t=(w>>9)&7; b=(w>>8)&1
    if w==256: return '('
    if w==257: return ')'
    return 'NWVXY'[t]+('b' if b else '')
def name(w):
    c=cl(w); v=w&0xff
    if c=='N': return str(v)
    return {'W':'w','Wb':'W','V':'v','Vb':'V','X':'x','Xb':'X','Y':'y','Yb':'Y'}[c]+str(v)
# top-level parse
toks=[]; depth=0; cur=[]; stm=[]; pre=[]
for i,w in enumerate(W):
    c=cl(w)
    if c=='(':
        depth+=1; cur.append('(')
    elif c==')':
        depth-=1; cur.append(')')
        if depth==0: stm.append(' '.join(cur).replace('( ','(').replace(' )',')')); cur=[]
    else:
        if depth==0: pre.append(name(w))
        else: cur.append(name(w))
print('outside parens:', len(pre), pre[:40])
print(len(stm))
open('/work/stm.txt','w').write('\n'.join(stm))
for i,s in enumerate(stm[:140]): print(i,s)

# ---- run 43 ----

import re
stm=open('/work/stm.txt').read().split('\n')
first={}
for i,s in enumerate(stm):
    for t in re.findall(r'[wWvVxXyY]\d+',s):
        first.setdefault(t,i)
order=sorted(first.items(),key=lambda x:x[1])
print(len(order))
print(order)

# ---- run 44 ----

stm=open('/work/stm.txt').read().split('\n')
for i in range(140,330): print(i,stm[i])

# ---- run 45 ----

stm=open('/work/stm.txt').read().split('\n')
for i in range(330,520): print(i,stm[i])

# ---- run 46 ----

stm=open('/work/stm.txt').read().split('\n')
for i in range(520,720): print(i,stm[i][:400])

# ---- run 47 ----

stm=open('/work/stm.txt').read().split('\n')
for i in range(719,900): print(i,stm[i][:330])

# ---- run 48 ----

stm=open('/work/stm.txt').read().split('\n')
for i in range(900,1060): print(i,stm[i][:330])

# ---- run 49 ----

msg=open('/work/msg.txt').read()
s=msg[:230]
import re
print([ (m.start(),len(m.group())) for m in re.finditer('0+|1+',s)][-8:])
print(s[150:230])

# ---- run 50 ----

import json
msg=open('/work/msg.txt').read()
W=[int(msg[174+16*k:174+16*k+16],2)^0xffff for k in range(22349)]
assert 174+16*22349==len(msg)
json.dump(W,open('/work/W.json','w'))
def cl(w):
    if w==256: return '('
    if w==257: return ')'
    return 'NWVXY'[(w>>9)&7]+('b' if (w>>8)&1 else '')
def name(w):
    c=cl(w); v=w&0xff
    if c=='N': return str(v)
    return {'W':'w','Wb':'W','V':'v','Vb':'V','X':'x','Xb':'X','Y':'y','Yb':'Y'}[c]+str(v)
from collections import Counter
print(Counter(w>>12 for w in W), Counter(cl(w) for w in W))
depth=0;cur=[];stm=[];pre=[]
for w in W:
    c=cl(w)
    if c=='(': depth+=1;cur.append('(')
    elif c==')':
        depth-=1;cur.append(')')
        if depth==0: stm.append(' '.join(cur).replace('( ','(').replace(' )',')'));cur=[]
    else:
        (cur if depth else pre).append(name(w))
print(pre, len(stm))
open('/work/stm.txt','w').write('\n'.join(stm))
for i in range(1060,1223): print(i,stm[i][:300])

# ---- run 51 ----

import math
# PD: moves 'C'=W5,'D'=W6 ; cost matrix w30(me,opp)
cost={('C','C'):3,('D','D'):5,('C','D'):7,('D','C'):2}
def W9(h):return 'C'
def W10(h):return 'D'
def W11(h):return 'C' if not h else h[-1][1]
def W12(h):return 'D' if not h else h[-1][1]
def W13(h):return 'D' if any(o=='D' for m,o in h) else 'C'
def W14(h):return 'C' if not h or h[-1][0]==h[-1][1] else 'D'
S={'W9':W9,'W10':W10,'W11':W11,'W12':W12,'W13':W13,'W14':W14}
def play(a,b,n):
    ha=[];hb=[];tot=0
    for _ in range(n):
        x=S[a](ha);y=S[b](hb)
        tot+=cost[(x,y)]; ha.append((x,y)); hb.append((y,x))
    return tot
claims={('W11','W11'):2*256+253,('W10','W10'):4*256+251,('W11','W10'):4*256+253,('W10','W11'):4*256+248,('W9','W10'):6*256+249,('W10','W9'):256+254,('W14','W10'):5*256+251,('W10','W14'):3*256+123,('W11','W12'):4*256+126,('W12','W11'):4*256+121,('W13','W12'):4*256+250,('W12','W13'):4*256+250}
for k,v in claims.items(): print(k, play(*k,255), v)
print(play('W11','W10',4))
for a in S: print(a, sum(play(a,b,255) for b in S))
print('claimed', {'W11':21*256+111,'W13':21*256+235,'W9':21*256+238,'W14':22*256+149,'W10':25*256+95,'W12':27*256+11})

# ---- run 52 ----

import math
c=299792458;hbar=1.054571817e-34;G=6.67430e-11;kB=1.380649e-23;me=9.1093837e-31;mp=1.67262192e-27;mn=1.67492750e-27
e=1.602176634e-19;ke=8.9875517923e9;mu=1e-7
lP=math.sqrt(hbar*G/c**3);tP=math.sqrt(hbar*G/c**5);mP=math.sqrt(hbar*c/G);TP=math.sqrt(hbar*c**5/G/kB**2)
Ry=13.605693122994*e*(1/(1+me/mp))  # H reduced
E21=Ry*(1-1/4)
def chk(name,val,lo,hi): print(f"{name:40s} {val:.6g} in [{lo:.6g},{hi:.6g}] {lo<val<hi}")
chk('mp/me',mp/me,7*256+44,7*256+45)
chk('mn/me',mn/me,7*256+46,7*256+47)
chk('mn/mp',mn/mp,1+2**-11,1+2**-9)
chk('m(1H)/mp',1.00782503207*1.66053906660e-27/mp,1+2**-11,1+2**-9)
chk('m(D)/m(H)',2.01410177812/1.00782503207,2-2**-9,2)
chk('alpha',ke*e**2/(hbar*c),1/138,1/137)
chk('Fe/Fg p-e log2',math.log2(ke*e*e/(G*mp*me)),130,131)
chk('mp/mP log2',math.log2(mp/mP),-64,-63)
chk('me/mP log2',math.log2(me/mP),-75,-74)
E21cm=6.62607015e-34*1420405751.77
chk('E21cm/E21(Lya) log2',math.log2(E21cm/E21),-21,-20)
chk('1/(f21 tP) log2',math.log2(1/(1420405751.77*tP)),113,114)
chk('E21/(me c2) log2',math.log2(E21/(me*c*c)),-16,-15)
chk('tau_n/tP log2',math.log2(878.4/tP),153,154)
chk('t1/2(14C)/t1/2(3H) log2',math.log2(5730/12.32),8,9)
chk('m4He/(4 m1H)',4.00260325413/(4*1.00782503207),1-2**-7,1-2**-8)
chk('mK0/me',497.611/0.51099895,3*256+205,3*256+207)
chk('Ttp H2/H2O *2048',13.8033/273.16*2048,103,104)
chk('Ttp Ne/H2O *8192',24.5561/273.16*8192,736,737)
chk('Ttp Ar/H2O *4096',83.8058/273.16*4096,1256,1257)
chk('k*273.16/E21 *2^17',kB*273.16/E21*2**17,302,303)
chk('273.16/TP *2^106',273.16/TP*2**106,156,157)
pP=c**7/(hbar*G**2)
chk('611.657/pP*2^376',611.657/pP*2**376,203,204)
chk('ptp H2/H2O',7.04e3/611.657,11,12)
chk('ptp Ne/H2O',43.332e3/611.657,70.5,71.5)
chk('ptp Ar/H2O',68.891e3/611.657,112,113)
chk('Tcmb/273.16*2^14',2.7255/273.16*2**14,163,164)
chk('DNA rise/lP log2',math.log2(0.34e-9/lP),83,85)
chk('DNA pitch/lP log2',math.log2(3.4e-9/lP),87,88)
Msun=1.98892e30;Rsun=6.957e8;Lsun=3.828e26
print('W44 mass range Msun',7*2**187*mp/Msun,2**190*mp/Msun)
print('W44 radius range Rsun',2**145*lP/Rsun,2**146*lP/Rsun)
print('W44 T range K',16*273.16,32*273.16)
print('W44 L range Lsun',2**-85*c**5/G/Lsun,2**-83*c**5/G/Lsun)
print('companion mass',2**189*mp/Msun,2**190*mp/Msun,'R',2**144*lP/Rsun,2**145*lP/Rsun)
AU=1.495978707e11;yr=3.15576e7
print('binary sep AU',2**149*lP/AU,2**150*lP/AU,'P days',2**163*tP/86400,2**164*tP/86400)
print('planet a AU',2**154*lP/AU,2**155*lP/AU,'P yr',2**170*tP/yr,2**171*tP/yr,'R km',2**141*lP/1e3,2**142*lP/1e3,'M<MJ',2**182*mp/1.898e27)
kpc=3.0857e19
print('BH mass Msun',2**211*mp/Msun,2**212*mp/Msun,'dist kpc',2**183*lP/kpc,2**184*lP/kpc,'Pgal Myr',2**196*tP/yr/1e6,2**197*tP/yr/1e6)
print('vrot km/s',2**-11*c/1e3,9*2**-13*c/1e3)
print('being mass kg',2**94*mp,2**96*mp,'size m',2**116*lP,2**117*lP,'max',2**118*lP,'T K',9/8*273.16,73/64*273.16)
for nm,(a,b) in {'W51':(139,140),'W52':(139,141),'W53':(136,137),'W54':(134,135),'W55':(143,144),'W56':(144,145)}.items():
    print(nm,'P s',2**a*tP,2**b*tP)
print('Pdot',{'W51':(2**-48,2**-47),'W52':(2**-47,2**-41),'W53':(121*2**-71,149*2**-71),'W54':(111*2**-70,137*2**-70),'W55':(2**-49,2**-48),'W56':(2**-50,2**-49)})
print('DNA bp', 2**31,2**32)

# ---- run 53 ----

bits=open('/work/bits.txt').read();P=357758;S=273185;n=len(bits)
off=(n-1-S)%P
print(n, off, 'expected',bits[n-1-P],'got',bits[n-1], 'word index',(off-174)//16, 'bit in word',(off-174)%16)
print('file starts at message offset', (0-S)%P, 'word', ((0-S)%P-174)/16)
print('copies: partial', S, 'bits, full copies:', (n-S)//P, 'tail bits', (n-S)%P)
W=__import__('json').load(open('/work/W.json'))
k=(off-174)//16; print(hex(W[k]))

# ---- run 54 ----

import json
from fractions import Fraction as F
W=json.load(open('/work/W.json'))
def cl(w):
    if w==256: return '('
    if w==257: return ')'
    return 'NWVXY'[(w>>9)&7]+('b' if (w>>8)&1 else '')
# build trees
i=21; trees=[]
def parse(i):
    assert W[i]==256
    node=[('w',W[i+1]&0xff)]; i+=2
    while True:
        w=W[i]
        if w==256: ch,i=parse(i); node.append(ch)
        elif w==257: return node,i+1
        else:
            c=cl(w); node.append(('n',w&0xff) if c=='N' else (c,w&0xff)); i+=1
while i<len(W):
    t,i=parse(i); trees.append(t)
class U(Exception):pass
TRUE,FALSE=('Wb',1),('Wb',2)
def ev(x):
    if isinstance(x,tuple):
        if x[0]=='n': return F(x[1])
        if x in (TRUE,FALSE): return x==TRUE
        if x==('Wb',19): return 1j
        raise U
    h=x[0][1]; a=[ev(y) for y in x[1:]]
    if h==1: return all(v==a[0] for v in a)
    if h==2: return a[0]!=a[1]
    if h in(3,4,5,6):
        op={3:lambda p,q:p<q,4:lambda p,q:p>q,5:lambda p,q:p<=q,6:lambda p,q:p>=q}[h]
        return all(op(a[k],a[k+1]) for k in range(len(a)-1))
    if h==7: return sum(a,F(0))
    if h==8:
        r=F(1)
        for v in a: r*=v
        return r
    if h==9: return a[0]*256+a[1]
    if h==10: return a[0]-a[1]
    if h==11: return -a[0]
    if h==12: return F(a[0])/a[1]
    if h==13: return not a[0]
    if h==14: return all(a)
    if h==15: return any(a)
    if h==16: return tuple(a)
    if h==17: return len(a[0])
    if h==18: return a[0][int(a[1])-1]
    if h==19: return sum(1 for v in a[1] if v==a[0])
    if h==22: return (not a[0]) or a[1]
    if h==34: return a[0]**int(a[1]) if a[1].denominator==1 else (_ for _ in ()).throw(U())
    raise U
ok=bad=skip=0;bads=[]
for k,t in enumerate(trees):
    try:
        r=ev(t)
        if r is True: ok+=1
        else: bad+=1; bads.append(k)
    except (U,TypeError,IndexError,ZeroDivisionError,AttributeError): skip+=1
print(ok,bad,skip,bads[:20])

# ---- run 55 ----

stm=open('/work/stm.txt').read().split('\n'); print(stm[110], stm[102], stm[103])
