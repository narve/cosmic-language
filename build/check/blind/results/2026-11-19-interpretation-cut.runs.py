# The code the blind reader ran, in order (2026-11-19, interpretation, full message repeated 5 times, cut inside the first and last repetition, every bit inverted, as received.bin; Opus).
# stream: message 306984 bits × 5, received bits 114386 to 1501450 (1387064 bits, then 0 random bits to fill 173383 bytes; starts 114386 bits into a repetition, ends 273514 bits into the last), inverted

# ---- run 1 ----
import os
d=open('/work/received.bin','rb').read()
print(len(d), len(d)*8)
print(d[:64].hex())
from collections import Counter
bits=''.join(f'{b:08b}' for b in d)
print(Counter(bits))
print(bits[:2000])

# ---- run 2 ----
import re
runs=[len(r) for r in bits.split('0')]
c=Counter(runs);print(sorted(c.items()))
print(runs[:200])

# ---- run 3 ----
from collections import Counter
d=open('/work/received.bin','rb').read()
bits=''.join(f'{b:08b}' for b in d)
open('/work/bits.txt','w').write(bits)
runs=[len(r) for r in bits.split('0')]
c=Counter(runs);print(sorted(c.items()))
print(runs[:300])

# ---- run 4 ----
bits=open('/work/bits.txt').read()
import re
toks=re.split('0(?=1{14}0)1{14}',bits)  # tentative
toks2=bits.split('0'+'1'*14+'0')
print(len(toks2))
c=Counter(toks2)
print(len(c))
for t,n in c.most_common(60): print(n,repr(t))

# ---- run 5 ----
from collections import Counter
bits=open('/work/bits.txt').read()
toks2=bits.split('0'+'1'*14+'0')
c=Counter(toks2)
print(len(toks2),len(c))
for t,n in c.most_common(80): print(n,len(t),repr(t))

# ---- run 6 ----
from collections import Counter
import re
bits=open('/work/bits.txt').read()
pos=[m.start() for m in re.finditer('(?=0'+'1'*14+'0)',bits)]
print(len(pos),Counter(p%8 for p in pos),Counter(p%16 for p in pos))

# ---- run 7 ----
from collections import Counter
bits=open('/work/bits.txt').read()
b=bits[1:]
by=[b[i:i+8] for i in range(0,len(b)-7,8)]
print(len(b)%8)
c=Counter(by);print(len(c))
for t,n in c.most_common(70):print(n,t,hex(int(t,2)), hex(255-int(t,2)))

# ---- run 8 ----
bits=open('/work/bits.txt').read()
toks=bits.split('0'+'1'*14+'0')
def hx(t):
    if len(t)%8==0: return ' '.join('%02x'%int(t[i:i+8],2) for i in range(0,len(t),8))
    return 'RAW:'+t
for i,t in enumerate(toks[:150]): print(i,hx(t))

# ---- run 9 ----
import numpy as np
bits=open('/work/bits.txt').read()
a=np.frombuffer(bits.encode(),dtype=np.uint8)-48
x=a-a.mean()
N=len(x)
f=np.fft.rfft(x,2**22)
ac=np.fft.irfft(f*np.conj(f))[:20000]
ac/=ac[0]
top=np.argsort(ac[1:])[::-1][:40]+1
print(sorted(zip(top,ac[top].round(3)),key=lambda t:-t[1]))
# zero density in chunks
ch=N//60
print([round(1-a[i*ch:(i+1)*ch].mean(),3) for i in range(60)])

# ---- run 10 ----
bits=open('/work/bits.txt').read()
N=len(bits);ch=N//80
print([round(bits[i*ch:(i+1)*ch].count('0')/ch,3) for i in range(80)])

# ---- run 11 ----
bits=open('/work/bits.txt').read()
for L in (64,128,256):
  for s in (0,1000,5000):
    pat=bits[s:s+L]
    idx=[];i=bits.find(pat,1)
    while i!=-1: idx.append(i); i=bits.find(pat,i+1)
    print(L,s,idx[:20])

# ---- run 12 ----
bits=open('/work/bits.txt').read()
P=306984
N=len(bits)
copies=[bits[k*P:(k+1)*P] for k in range(5)]
print([len(c) for c in copies])
for k in range(1,5):
    c=copies[k]; diff=sum(1 for i in range(len(c)) if c[i]!=copies[0][i])
    print(k,diff)
print(P, P/8, P%8, N-4*P)

# ---- run 13 ----
import re
bits=open('/work/bits.txt').read()
P=306984
for m in re.finditer('1{30,}',bits):
    if m.start()<P: print(m.start(), m.end()-m.start())

# ---- run 14 ----
bits=open('/work/bits.txt').read()
s=198900
seg=bits[s:s+900]
for i in range(0,len(seg),100): print(s+i, seg[i:i+100])

# ---- run 15 ----
def fac(n):
    f=[];d=2
    while d*d<=n:
        while n%d==0: f.append(d); n//=d
        d+=1
    if n>1: f.append(n)
    return f
print(fac(306984), fac(38373), fac(1387064))

# ---- run 16 ----
bits=open('/work/bits.txt').read()
P=306984
def uart(bits,n,stop=1):
    i=0;out=[];err=0
    L=len(bits)
    while i<L-n-1-stop:
        if bits[i]=='0':
            d=bits[i+1:i+1+n]
            s=bits[i+1+n:i+1+n+stop]
            if s!='1'*stop: err+=1
            out.append(d); i=i+1+n+stop
        else: i+=1
    return out,err
for n in range(5,10):
    out,err=uart(bits[:P],n)
    print(n,len(out),err)

# ---- run 17 ----
import re
bits=open('/work/bits.txt').read()
P=306984
pos=[m.start() for m in re.finditer('(?=0'+'1'*14+'0)',bits[:P])]
prev=None;segs=[]
for p in pos:
    o=p%8
    if o!=prev: segs.append((p,o)); prev=o
print(len(segs)); print(segs[:100])

# ---- run 18 ----
bits=open('/work/bits.txt').read()
P=306984
cyc=bits[1:]+bits[:1]  # framing offset 1
cyc=bits[1:P+1]
inv=bytes(255-int(cyc[i:i+8],2) for i in range(0,P,8))
open('/work/inv.bin','wb').write(inv)
for r in range(0,640,32): print(r, inv[r:r+32].hex(' '))

# ---- run 19 ----
bits=open('/work/bits.txt').read()
s=192800
seg=bits[s:s+6600]
for i in range(0,len(seg),120): print(s+i, seg[i:i+120])

# ---- run 20 ----
bits=open('/work/bits.txt').read()
s=192900;e=197080
seg=bits[s:e]
# try: items = '11111111' + 8-bit value? Look for ordering from end
import re
# locate '0'*8 near end
print(seg[-200:])

# ---- run 21 ----
bits=open('/work/bits.txt').read()
end=bits.find('1111111100000000',196900)+16
print(end)
# parse backward variable: assume item = '1'*8 + binary, find previous by matching
i=end; vals=[]
cur=0
while True:
    # value cur expected at bits ending at i; try widths
    found=False
    for w in range(8,20):
        st=i-w
        if bits[st:i]==format(cur,'0%db'%w) and bits[st-8:st]=='1'*8:
            # ambiguity check
            vals.append((cur,w,st-8)); i=st-8; cur+=1; found=True; break
    if not found: break
print(len(vals), vals[-5:], vals[:3])
print(bits[i-300:i])

# ---- run 22 ----
bits=open('/work/bits.txt').read()
s=190500;e=192970
seg=bits[s:e]
for i in range(0,len(seg),120): print(s+i, seg[i:i+120])

# ---- run 23 ----
bits=open('/work/bits.txt').read()
seg=bits[192418:192780]
print(seg)
import re
print([len(x) for x in seg.split('1')])

# ---- run 24 ----
bits=open('/work/bits.txt').read()
seg=bits[192770:192962]
print(seg)
# try ones-prefix + k-bit
for k in range(3,9):
    for pre in range(6,14):
        L=pre+k
        for off in range(L):
            items=[seg[j:j+L] for j in range(off,len(seg)-L+1,L)]
            if len(items)>5 and all(it.startswith('1'*pre) for it in items):
                vals=[int(it[pre:],2) for it in items]
                if all(vals[i]==vals[i+1]+1 for i in range(len(vals)-1)):
                    print(k,pre,off,vals)

# ---- run 25 ----
bits=open('/work/bits.txt').read()
seg=bits[192770:192962]
for o in range(0,16):
    print(o,[seg[j:j+16] for j in range(o,len(seg)-15,16)][:12])

# ---- run 26 ----
bits=open('/work/bits.txt').read()
inv=bits.translate(str.maketrans('01','10'))
open('/work/inv.txt','w').write(inv)
s=197058
seg=inv[s:s+2400]
for i in range(0,len(seg),96): print(s+i, seg[i:i+96].replace('0','.'))

# ---- run 27 ----
inv=open('/work/inv.txt').read()
P=306984
start=192418
cyc=(inv[start:]+inv)[:P]  # but inv has many copies; use inv[start:start+P]
cyc=inv[start:start+P]
open('/work/cyc.txt','w').write(cyc)
W=4096
for w in range(0,P,W):
    s=cyc[w:w+W]
    ones=[i for i,c in enumerate(s) if c=='1']
    S=set(ones)
    best=[]
    for lag in range(2,700):
        cnt=sum(1 for i in ones if i+lag in S)
        best.append((cnt,lag))
    best.sort(reverse=True)
    print(w+start, len(ones), best[:4])

# ---- run 28 ----
import math
from collections import Counter
inv=open('/work/inv.txt').read()
P=306984
cyc=inv[:P]
def ent(o,s):
    c=Counter(s[i:i+8] for i in range(o,len(s)-8,8));n=sum(c.values())
    return -sum(v/n*math.log2(v/n) for v in c.values())
print([round(ent(o,cyc),3) for o in range(8)])
for a in range(0,P,P//10):
    print(a,[round(ent(o,cyc[a:a+P//10]),2) for o in range(8)])

# ---- run 29 ----
inv=open('/work/inv.txt').read()
s=189780
for r in range(12):
    print(s+r*240, inv[s+r*240:s+(r+1)*240].replace('0','.'))

# ---- run 30 ----
import math
from collections import Counter
inv=open('/work/inv.txt').read()
def ent(o,s):
    c=Counter(s[i:i+8] for i in range(o,len(s)-8,8));n=sum(c.values())
    return -sum(v/n*math.log2(v/n) for v in c.values())
for a in range(184000,192400,1200):
    e=[round(ent(o,inv[a:a+1200]),2) for o in range(8)]
    print(a,e, e.index(min(e)))

# ---- run 31 ----
inv=open('/work/inv.txt').read()
import itertools
seg=inv[192300:192800]
runs=[(k,len(list(g))) for k,g in itertools.groupby(seg)]
print(runs)

# ---- run 32 ----
import itertools
from collections import Counter
inv=open('/work/inv.txt').read()
P=306984
cyc=inv[192418:192418+P]
r=[(k,len(list(g))) for k,g in itertools.groupby(cyc)]
print(sorted(Counter(l for k,l in r if k=='1').items()))
print(sorted(Counter(l for k,l in r if k=='0').items()))

# ---- run 33 ----
import re
inv=open('/work/inv.txt').read()
s=197000
seg=inv[s:s+3000]
parts=re.split('(0{7,})',seg)
out=[]
for p in parts:
    if not p: continue
    if p[0]=='0': out.append(str(len(p)))
    else: out.append('['+p+']')
print(' '.join(out))

# ---- run 34 ----
inv=open('/work/inv.txt').read()
s=197058
w=[int(inv[i:i+16],2) for i in range(s,s+16*400,16)]
print(' '.join('%04x'%x for x in w))

# ---- run 35 ----
from collections import Counter
inv=open('/work/inv.txt').read()
P=306984
# word alignment: positions ≡2 mod 16 in absolute stream
base=2
words=[int(inv[i:i+16],2) for i in range(base,len(inv)-15,16)]
print(len(words), P/16)
hi=Counter(w>>8 for w in words[:P//16+1]); print(sorted(hi.items()))
c=Counter(words[:P//16+1])
print(len(c))
print(sorted((hex(k),v) for k,v in c.items() if k>=0x100))

# ---- run 36 ----
inv=open('/work/inv.txt').read()
s=197058
by=[int(inv[i:i+8],2) for i in range(s,s+8*6000,8)]
# print in hex, break lines at 01 00 (open)
out=[];line=[]
i=0
txt=' '.join('%02x'%b for b in by)
# find first place where 16-bit parse looks wrong: show from word 400 onwards
w=[int(inv[i:i+16],2) for i in range(s,s+16*3000,16)]
for k,x in enumerate(w):
    if (x>>8)>2: print('first odd word at',k, s+16*k); break
print(' '.join('%04x'%x for x in w[k-40:k+40]))

# ---- run 37 ----
inv=open('/work/inv.txt').read()
P=306984
S=192418
W=2048
res=[]
for a in range(S,S+P,W):
    sc=[]
    for o in range(16):
        st=a+((o-a)%16)
        ws=[int(inv[i:i+16],2) for i in range(st,a+W-15,16)]
        sc.append(sum(1 for x in ws if (x>>8)<=0x0b)/max(1,len(ws)))
    best=max(range(16),key=lambda o:sc[o])
    res.append((a,best,round(sc[best],2)))
prev=None
for a,b,s in res:
    if b!=prev or s<0.9: print(a,b,s)
    prev=b

# ---- run 38 ----
inv=open('/work/inv.txt').read()
P=306984
st=192962+4096  # after count = 197058
ws=[int(inv[i:i+16],2) for i in range(st,192418+P,16)]
# parse sequence of top-level expressions
def parse(i):
    w=ws[i]
    if w==0x100:
        lst=[];i+=1
        while True:
            if i>=len(ws): raise ValueError('eof')
            if ws[i]==0x101: return lst,i+1
            e,i=parse(i); lst.append(e)
    elif w==0x101: raise ValueError('unexpected close at %d'%i)
    else: return w,i+1
i=0;exprs=[]
try:
    while i<len(ws):
        e,j=parse(i); exprs.append((i,e)); i=j
except Exception as ex:
    print('stop',i, st+16*i, ex)
print(len(exprs))
def show(e):
    if isinstance(e,list): return '('+' '.join(show(x) for x in e)+')'
    return '%x'%e
for k,e in exprs[-5:]: print(k,show(e)[:300])
print(' '.join('%04x'%x for x in ws[i:i+60]))

# ---- run 39 ----
inv=open('/work/inv.txt').read()
P=306984
st=197058
ws=[int(inv[i:i+16],2) for i in range(st,192418+P,16)]
def parse(i):
    w=ws[i]
    if w==0x100:
        lst=[];i+=1
        while ws[i]!=0x101:
            e,i=parse(i); lst.append(e)
        return lst,i+1
    return w,i+1
i=0;exprs=[]
while i<len(ws):
    try: e,j=parse(i)
    except IndexError: print('incomplete at',i,st+16*i);break
    exprs.append((i,e)); i=j
print(len(ws),i, len(exprs))
endpos=st+16*exprs[-1][0]
# find end of last expression
e,j=parse(exprs[-1][0]); print('last ends at word',j,'bit',st+16*j)
print(' '.join('%04x'%x for x in ws[j-5:]))
import pickle
pickle.dump((ws,exprs),open('/work/exprs.pkl','wb'))
tail=inv[st+16*j:192418+P]
print(len(tail))
for k in range(0,len(tail),120): print(tail[k:k+120].replace('0','.'))

# ---- run 40 ----
inv=open('/work/inv.txt').read()
print(inv[192394:192426], inv[192426:192470])
print(inv[192394+306984:192470+306984])
# unary region length
a=192426; b=192770
print(b-a, inv[a:b].count('0'))

# ---- run 41 ----
inv=open('/work/inv.txt').read()
seg=inv[192426:192770]
print(seg.split('0'))
print([len(x) for x in seg.split('0')])
print(inv[192770-20:192770+20])

# ---- run 42 ----
import pickle
ws,exprs=pickle.load(open('/work/exprs.pkl','rb'))
def show(e):
    if isinstance(e,list): return '('+' '.join(show(x) for x in e)+')'
    return '%x'%e
lines=[f'{k}: {show(e)}' for k,e in exprs]
open('/work/exprs.txt','w').write('\n'.join(lines))
for l in lines[:140]: print(l[:200])

# ---- run 43 ----
import pickle
ws,exprs=pickle.load(open('/work/exprs.pkl','rb'))
names={0x201:'=',0x202:'≠',0x203:'<',0x204:'>',0x205:'≤',0x206:'≥',0x207:'+',0x208:'*',0x209:'NUM',0x20a:'-',0x20b:'neg',0x20c:'/'}
def show(e):
    if isinstance(e,list): return '('+' '.join(show(x) for x in e)+')'
    if e in names: return names[e]
    if e<0x100: return str(e)
    return '%x'%e
pickle.dump(names,open('/work/names.pkl','wb'))
for k,e in exprs[125:260]: print(k,show(e)[:220])

# ---- run 44 ----
import pickle
ws,exprs=pickle.load(open('/work/exprs.pkl','rb'))
names=pickle.load(open('/work/names.pkl','rb'))
names.update({0x301:'T',0x302:'F',0x20d:'not',0x20e:'and',0x20f:'or',0x210:'list',0x211:'len',0x212:'nth',0x213:'count',0x214:'all',0x215:'some',0x401:'x',0x402:'y',0x403:'z',0x404:'w',0x303:'N?'})
pickle.dump(names,open('/work/names.pkl','wb'))
def show(e):
    if isinstance(e,list): return '('+' '.join(show(x) for x in e)+')'
    if e in names: return names[e]
    if e<0x100: return str(e)
    return '%x'%e
for k,e in exprs[260:400]: print(k,show(e)[:260])

# ---- run 45 ----
import pickle
ws,exprs=pickle.load(open('/work/exprs.pkl','rb'))
names=pickle.load(open('/work/names.pkl','rb'))
names.update({0x303:'Nat',0x304:'Rat',0x305:'Real',0x306:'i',0x307:'Cplx',0x216:'imp',0x217:'fold',0x218:'map',0x219:'mean',0x21a:'freq',0x21b:'prod',0x21c:'tail',0x21d:'if',0x21e:'pow',0x21f:'abs',0x220:'exp'})
pickle.dump(names,open('/work/names.pkl','wb'))
def show(e):
    if isinstance(e,list): return '('+' '.join(show(x) for x in e)+')'
    if e in names: return names[e]
    if e<0x100: return str(e)
    return '%x'%e
for k,e in exprs[400:520]: print(k,show(e)[:300])

# ---- run 46 ----
import pickle
ws,exprs=pickle.load(open('/work/exprs.pkl','rb'))
names=pickle.load(open('/work/names.pkl','rb'))
names.update({0x308:'e',0x309:'pi',0x30a:'R3',0x30b:'S2',0x221:'dot',0x222:'cos',0x223:'angle',0x224:'cross',0x225:'avg',0x226:'quote',0x227:'kind',0x228:'let',0x229:'eval',0x30c:'Expr',0x30d:'MSG'})
pickle.dump(names,open('/work/names.pkl','wb'))
def show(e):
    if isinstance(e,list): return '('+' '.join(show(x) for x in e)+')'
    if e in names: return names[e]
    if e<0x100: return str(e)
    return '%x'%e
for k,e in exprs[520:640]: print(k,show(e)[:300])

# ---- run 47 ----
import pickle
ws,exprs=pickle.load(open('/work/exprs.pkl','rb'))
names=pickle.load(open('/work/names.pkl','rb'))
names.update({0x22a:'subst',0x30e:'HOLE',0x230:'FACT',0x231:'mass',0x232:'charge',0x501:'P1',0x502:'P2',0x503:'P3',0x504:'P4',0x601:'A1',0x602:'A2',0x606:'A6',0x608:'A8',0x313:'Atoms',0x233:'isotope',0x234:'stable',0x235:'level',0x236:'dim',0x701:'M',0x702:'L',0x703:'T',0x704:'Q',0x314:'Photons',0x237:'speed',0x238:'wavelen',0x239:'freq',0x23a:'energy',0x23b:'transition',0x801:'c',0x802:'hbar',0x803:'G',0x315:'Bodies',0x23c:'dist',0x23d:'force'})
pickle.dump(names,open('/work/names.pkl','wb'))
def show(e):
    if isinstance(e,list): return '('+' '.join(show(x) for x in e)+')'
    if e in names: return names[e]
    if e<0x100: return str(e)
    return '%x'%e
for k,e in exprs[640:760]: print(k,show(e)[:400])

# ---- run 48 ----
import pickle
ws,exprs=pickle.load(open('/work/exprs.pkl','rb'))
names=pickle.load(open('/work/names.pkl','rb'))
names.update({0x23e:'Fcoul',0x804:'k_e',0x316:'Wires',0x23f:'current',0x240:'Fmag',0x805:'mu',0x806:'lP',0x807:'tP',0x808:'mP',0x809:'Ph21',0x317:'Gases',0x241:'KE',0x80a:'kB',0x242:'temp',0x705:'Θ',0x318:'BlackBodies',0x243:'radiance',0x80b:'TP',0x244:'lifetime',0x319:'Times',0x245:'survive',0x246:'halflife',0x247:'spin',0x248:'spins?',0x249:'spinaxis',0x24a:'corrA',0x24b:'corrB',0x505:'P5',0x31a:'Loops',0x24c:'radius',0x24d:'Bfield',0x24e:'circ',0x24f:'moment',0x506:'P6',0x507:'P7',0x250:'yield',0x251:'shellcap',0x252:'inert',0x60a:'A10',0x612:'A18',0x624:'A36',0x636:'A54',0x656:'A86',0x901:'Mol1',0x902:'Mol2'})
pickle.dump(names,open('/work/names.pkl','wb'))
def show(e):
    if isinstance(e,list): return '('+' '.join(show(x) for x in e)+')'
    if e in names: return names[e]
    if e<0x100: return str(e)
    return '%x'%e
for k,e in exprs[760:880]: print(k,show(e)[:400])

# ---- run 49 ----
import pickle
ws,exprs=pickle.load(open('/work/exprs.pkl','rb'))
names=pickle.load(open('/work/names.pkl','rb'))
names.update({0x903:'CH4',0x904:'NH3',0x905:'CO2',0x906:'Adenine',0x907:'Thymine',0x908:'Guanine',0x909:'Cytosine',0x607:'A7',0x253:'atomsOf',0x254:'bonds',0x255:'Ttriple',0x256:'Ptriple',0x31b:'Stars',0x257:'lum',0x258:'orbits',0x259:'period',0x25a:'semimaj',0x25b:'CMB_T',0x31c:'axC',0x31d:'axD',0x31e:'axE',0x31f:'Sun',0x320:'Home',0x321:'GC',0x25c:'at',0x25d:'dirto',0x25e:'vel',0x322:'uGC',0x323:'uRot',0x324:'uN',0x30f:'SENDER',0x310:'RECEIVER',0x311:'Agents',0x312:'Chains',0x22b:'author',0x22c:'addressee',0x22d:'SAYS',0x22e:'accept',0x22f:'reject'})
pickle.dump(names,open('/work/names.pkl','wb'))
def show(e):
    if isinstance(e,list): return '('+' '.join(show(x) for x in e)+')'
    if e in names: return names[e]
    if e<0x100: return str(e)
    return '%x'%e
for k,e in exprs[880:990]: print(k,show(e)[:500])

# ---- run 50 ----
import pickle
ws,exprs=pickle.load(open('/work/exprs.pkl','rb'))
inv=open('/work/inv.txt').read()
pw=[int(inv[i:i+16],2) for i in range(192770,197058,16)]
MSG=pw+[e for k,e in exprs]
print(len(pw), MSG[:13])
def nested_count(t,e):
    c=1 if e==t else 0
    if isinstance(e,list): c+=sum(nested_count(t,x) for x in e)
    return c
tests=[([0x201,1,1],1),([0x202,0,1],1),([0x201,3,3],1),([0x201,5,5],2),([0x201,2,3],0),([0x203,3,2],0),([0x201,[0x207,2,2],5],0),([0x201,6,6],0),([0x203,5,6],0),([0x201,[0x207,3,3],6],0)]
for t,claim in tests:
    top=sum(1 for e in MSG if e==t); nest=sum(nested_count(t,e) for e in MSG)
    print(t,claim,top,nest)

# ---- run 51 ----
import pickle, math
from fractions import Fraction as Fr
ws,exprs=pickle.load(open('/work/exprs.pkl','rb'))
inv=open('/work/inv.txt').read()
pw=[int(inv[i:i+16],2) for i in range(192770,197058,16)]
MSG=('MSGLIST',pw+[e for k,e in exprs])
class Skip(Exception): pass
T,F=0x301,0x302
C,D=0x32c,0x32d
def B(x): return T if x else F
def ev(e,env):
    if isinstance(e,int):
        if e<0x100: return Fr(e)
        if e in (T,F,C,D): return e
        if e in env: return env[e]
        if e==0x30d: return MSG[1]
        if e==0x306: return complex(0,1)
        if 0x330<=e<=0x337: return e
        raise Skip(hex(e))
    if isinstance(e,tuple): return e
    if not e: raise Skip('empty')
    op=e[0];a=e[1:]
    if op==0x226: return ('Q',a[0])
    if op==0x214 or op==0x215 or op==0x218 or op==0x228:
        v=a[0]
        if op==0x228:
            env2=dict(env);env2[v]=ev(a[1],env);return ev(a[2],env2)
        dom=ev(a[1],env)
        if not isinstance(dom,list): raise Skip('dom')
        res=[]
        for x in dom:
            env2=dict(env);env2[v]=x;res.append(ev(a[2],env2))
        if op==0x218: return res
        if op==0x214: return B(all(r==T for r in res))
        return B(any(r==T for r in res))
    if op==0x217:
        f=a[0]; lst=ev(a[1],env)
        if not isinstance(lst,list): raise Skip('fold')
        return ev([f]+[('V',x) for x in lst],env) if False else apply(f,lst)
    if op==0x21d:
        c=ev(a[0],env); return ev(a[1],env) if c==T else ev(a[2],env)
    args=[ev(x,env) for x in a]
    return apply(op,args)
def num(x):
    if isinstance(x,(Fr,complex)): return x
    raise Skip('num')
def apply(op,args):
    if op==0x201: return B(all(x==args[0] for x in args))
    if op==0x202: return B(args[0]!=args[1])
    if op in (0x203,0x204,0x205,0x206):
        f={0x203:lambda a,b:a<b,0x204:lambda a,b:a>b,0x205:lambda a,b:a<=b,0x206:lambda a,b:a>=b}[op]
        return B(all(f(num(args[i]),num(args[i+1])) for i in range(len(args)-1)))
    if op==0x207: 
        s=0
        for x in args: s+=num(x)
        return s
    if op==0x208:
        s=Fr(1)
        for x in args: s*=num(x)
        return s
    if op==0x209:
        s=Fr(0)
        for x in args: s=s*256+num(x)
        return s
    if op==0x20a: return num(args[0])-num(args[1])
    if op==0x20b: return -num(args[0])
    if op==0x20c: return num(args[0])/num(args[1])
    if op==0x20d: return B(args[0]==F)
    if op==0x20e: return B(all(x==T for x in args))
    if op==0x20f: return B(any(x==T for x in args))
    if op==0x210: return list(args)
    if op==0x211: return Fr(len(lst(args[0])))
    if op==0x212: return lst(args[0])[int(args[1])-1]
    if op==0x213: return Fr(sum(1 for x in lst(args[1]) if x==args[0]))
    if op==0x216: return B(args[0]==F or args[1]==T)
    if op==0x219: l=lst(args[0]); return sum(l,Fr(0))/len(l)
    if op==0x21a: l=lst(args[1]); return Fr(sum(1 for x in l if x==args[0]),len(l))
    if op==0x21b: return [[x,y] for x in lst(args[0]) for y in lst(args[1])]
    if op==0x21c: return lst(args[0])[1:]
    if op==0x21e:
        b,e=num(args[0]),num(args[1])
        if isinstance(b,complex) or isinstance(e,Fr) and e.denominator==1: return b**int(e) if not isinstance(b,complex) else b**int(e)
        raise Skip('pow')
    if op==0x21f: return Fr(abs(num(args[0]))) if isinstance(args[0],Fr) else abs(args[0])
    if op==0x227:
        q=args[0]
        if isinstance(q,tuple): q=q[1]
        raise Skip('kind')
    if op==0x229:
        q=args[0]
        if isinstance(q,tuple) and q[0]=='Q': return ev(q[1],{})
        return q
    if isinstance(op,int) and op in (0x201,): pass
    if isinstance(op,(Fr,)) : raise Skip('x')
    if op==0x261 or op==0x261: pass
    if op==0x261: pass
    if op==0x261: pass
    raise Skip('op %x'%op if isinstance(op,int) else 'op')
def lst(x):
    if isinstance(x,list): return x
    if isinstance(x,tuple) and x[0]=='Q' and isinstance(x[1],list): return x[1]
    raise Skip('lst')
# normalize complex comparisons for equality
res={'T':0,'F':[],'skip':0}
for k,e in exprs:
    try:
        r=ev(e,{})
        if r==T: res['T']+=1
        else: res['F'].append(k)
    except (Skip,ZeroDivisionError,TypeError,IndexError,ValueError) as ex:
        res['skip']+=1
print(res['T'],res['skip'],res['F'])

# ---- run 52 ----
import pickle, math
from fractions import Fraction as Fr
ws,exprs=pickle.load(open('/work/exprs.pkl','rb'))
inv=open('/work/inv.txt').read()
pw=[int(inv[i:i+16],2) for i in range(192770,197058,16)]
class Sym:
    __slots__=('v',)
    def __init__(s,v): s.v=v
    def __eq__(s,o): return isinstance(o,Sym) and o.v==s.v
    def __hash__(s): return hash(('S',s.v))
    def __repr__(s): return 'S%x'%s.v
def q(e):
    if isinstance(e,list): return [q(x) for x in e]
    if e<0x100: return Fr(e)
    return Sym(e)
def unq(e):
    if isinstance(e,list): return [unq(x) for x in e]
    if isinstance(e,Fr): return int(e)
    if isinstance(e,Sym): return e.v
    raise Skip('unq')
MSGL=[q(x) for x in pw+[e for k,e in exprs]]
class Skip(Exception): pass
T,F=Sym(0x301),Sym(0x302)
C,D=Sym(0x32c),Sym(0x32d)
def B(x): return T if x else F
ATOMS={0x301,0x302,0x32c,0x32d}|set(range(0x330,0x338))
payoff={(C,C):3,(D,D):5,(C,D):7,(D,C):2}
def strat(s,h):
    s=s.v
    if s==0x330: return [C]
    if s==0x331: return [D]
    if s in (0x332,0x333):
        if not h: return [C] if s==0x332 else [D]
        return [h[-1][1]]
    if s==0x334: return [D] if any(p[1]==D for p in h) else [C]
    if s==0x335:
        if not h: return [C]
        return [C] if h[-1][0]==h[-1][1] else [D]
    if s==0x336:
        if not h: return [C]
        return [C] if h[-1][1]==C else [C,D,D]
    if s==0x337: return [C,D]
def play(x,y,n):
    hx=[];hy=[]
    for _ in range(n):
        a=strat(x,hx);b=strat(y,hy)
        if len(a)>1 or len(b)>1: raise Skip('random')
        hx.append([a[0],b[0]]);hy.append([b[0],a[0]])
    return hx
def ev(e,env):
    if isinstance(e,int):
        if e<0x100: return Fr(e)
        if e in env: return env[e]
        if e in ATOMS: return Sym(e)
        if e==0x30d: return MSGL
        if e==0x338: return [Sym(x) for x in range(0x330,0x336)]
        if e==0x306: return complex(0,1)
        raise Skip(hex(e))
    if not e: raise Skip('empty')
    op=e[0];a=e[1:]
    if op==0x226: return q(a[0])
    if op in (0x214,0x215,0x218,0x228):
        v=a[0]
        if op==0x228:
            env2=dict(env);env2[v]=ev(a[1],env);return ev(a[2],env2)
        dom=ev(a[1],env)
        if not isinstance(dom,list): raise Skip('dom')
        res=[]
        for x in dom:
            env2=dict(env);env2[v]=x;res.append(ev(a[2],env2))
        if op==0x218: return res
        if op==0x214: return B(all(r==T for r in res))
        return B(any(r==T for r in res))
    if op==0x217:
        lst_=ev(a[1],env)
        if not isinstance(lst_,list): raise Skip('fold')
        return apply(a[0],lst_)
    if op==0x21d:
        c=ev(a[0],env); return ev(a[1],env) if c==T else ev(a[2],env)
    args=[ev(x,env) for x in a]
    return apply(op,args)
def num(x):
    if isinstance(x,(Fr,complex)): return x
    raise Skip('num')
def apply(op,args):
    if op==0x201: return B(all(x==args[0] for x in args))
    if op==0x202: return B(args[0]!=args[1])
    if op in (0x203,0x204,0x205,0x206):
        f={0x203:lambda a,b:a<b,0x204:lambda a,b:a>b,0x205:lambda a,b:a<=b,0x206:lambda a,b:a>=b}[op]
        return B(all(f(num(args[i]),num(args[i+1])) for i in range(len(args)-1)))
    if op==0x207:
        s=Fr(0)
        for x in args: s+=num(x)
        return s
    if op==0x208:
        s=Fr(1)
        for x in args: s*=num(x)
        return s
    if op==0x209:
        s=Fr(0)
        for x in args: s=s*256+num(x)
        return s
    if op==0x20a: return num(args[0])-num(args[1])
    if op==0x20b: return -num(args[0])
    if op==0x20c: return num(args[0])/num(args[1])
    if op==0x20d: return B(args[0]==F)
    if op==0x20e: return B(all(x==T for x in args))
    if op==0x20f: return B(any(x==T for x in args))
    if op==0x210: return list(args)
    if op==0x211: return Fr(len(L(args[0])))
    if op==0x212: return L(args[0])[int(args[1])-1]
    if op==0x213: return Fr(sum(1 for x in L(args[1]) if x==args[0]))
    if op==0x216: return B(args[0]==F or args[1]==T)
    if op==0x219: l=L(args[0]); return sum(l,Fr(0))/len(l)
    if op==0x21a: l=L(args[1]); return Fr(sum(1 for x in l if x==args[0]),len(l))
    if op==0x21b: return [[x,y] for x in L(args[0]) for y in L(args[1])]
    if op==0x21c: return L(args[0])[1:]
    if op==0x21e:
        b,e=num(args[0]),num(args[1])
        if isinstance(e,Fr) and e.denominator==1: return b**int(e)
        raise Skip('pow')
    if op==0x21f:
        if isinstance(args[0],Fr): return abs(args[0])
        raise Skip('abs')
    if op==0x227:
        x=args[0]
        if isinstance(x,Fr): return Fr(0)
        if isinstance(x,list): return Fr(1)
        if isinstance(x,Sym):
            v=x.v
            if v in (0x301,0x302): return Fr(3)
            if 0x200<=v<0x300: return Fr(2)
            if 0x400<=v<0x500: return Fr(4)
            return Fr(v>>8)
        raise Skip('kind')
    if op==0x229: return ev(unq(args[0]),{})
    if op==0x22a:
        def sub(x,y):
            if x==Sym(0x30e): return y
            if isinstance(x,list): return [sub(z,y) for z in x]
            return x
        return sub(args[0],args[1])
    if op==0x261: return Fr(payoff[(args[0],args[1])])
    if op==0x262:
        h=args[1]; return strat(args[0],h)
    if op==0x263: return play(args[0],args[1],int(args[2]))
    if op==0x264:
        h=play(args[0],args[1],int(args[2])); return Fr(sum(payoff[(p[0],p[1])] for p in h))
    raise Skip('op %x'%op if isinstance(op,int) else 'op')
def L(x):
    if isinstance(x,list): return x
    raise Skip('lst')
nT=0;skips={};fails=[]
for k,e in exprs:
    try:
        r=ev(e,{})
        if r==T: nT+=1
        else: fails.append(k)
    except (Skip,ZeroDivisionError,TypeError,IndexError,ValueError,KeyError) as ex:
        skips[str(ex)[:12]]=skips.get(str(ex)[:12],0)+1
print(nT,sum(skips.values()),fails)
print(sorted(skips.items(),key=lambda t:-t[1])[:30])

# ---- run 53 ----
import random, math
# uGC=(c1,d1,e1), uRot=(c2,d2,e2) in orthonormal frame (axC,axD,axE); signs of d1 free
found=0
for _ in range(400000):
    c1=random.uniform(.25,.5); e1=random.uniform(-1,-.75)
    r=1-c1*c1-e1*e1
    if r<0: continue
    d1=random.choice([1,-1])*math.sqrt(r)
    c2=random.uniform(.5,1); d2=random.uniform(.125,.875); 
    r2=1-c2*c2-d2*d2
    if r2<0: continue
    e2=math.sqrt(r2)
    if not (.25<e2<.75): continue
    if abs(c1*c2+d1*d2+e1*e2)<0.01: found+=1
print('feasible samples',found)
# pulsar checks with remembered catalogue (l,b) deg
ps={'Crab':(184.56,-5.78),'Vela':(263.55,-2.79),'J0437':(253.39,-41.96),'B1937+21':(57.51,-0.29),'B0329+54':(145.0,-1.22),'B1919+21':(55.78,3.50)}
for n,(l,b) in ps.items():
    l,b=math.radians(l),math.radians(b)
    print(n,round(math.cos(b)*math.cos(l),3),round(math.cos(b)*math.sin(l),3),round(math.sin(b),3))

# ---- run 54 ----
import math
tP=5.391247e-44
for name,P,Pd,(lo,hi),(dlo,dhi) in [('Crab',0.0337,4.21e-13,(138,139),(106/2**48,131/2**48)),('Vela',0.0893,1.25e-13,(140,141),(126/2**50,155/2**50)),('J0437',0.005757,5.73e-20,(136,137),(121/2**71,149/2**71)),('B1937',0.001558,1.05e-19,(134,135),(111/2**70,137/2**70)),('B0329',0.7145,2.05e-15,(143,144),(2**-49,2**-48)),('B1919',1.3373,1.35e-15,(144,145),(2**-50,2**-49))]:
    print(name, round(math.log2(P/tP),3),(lo,hi), dlo<Pd<dhi, '%.3g %.3g'%(dlo,dhi))

# ---- run 55 ----
import pickle
ws,exprs=pickle.load(open('/work/exprs.pkl','rb'))
names=pickle.load(open('/work/names.pkl','rb'))
first={};cnt={}
def walk(e,k):
    if isinstance(e,list):
        for x in e: walk(x,k)
    else:
        if e>=0x100:
            first.setdefault(e,k); cnt[e]=cnt.get(e,0)+1
for k,e in exprs: walk(e,k)
missing=[hex(s) for s in sorted(first) if s not in names]
print(len(first), 'unnamed:',missing)
for s in sorted(first): print('%04x'%s, names.get(s,'?'), first[s], cnt[s], 'bit', 197058+16*first[s])

# ---- run 56 ----
import pickle
ws,exprs=pickle.load(open('/work/exprs.pkl','rb'))
first={};cnt={}
def walk(e,k):
    if isinstance(e,list):
        for x in e: walk(x,k)
    elif e>=0x100: first.setdefault(e,k); cnt[e]=cnt.get(e,0)+1
for k,e in exprs: walk(e,k)
M={
0x201:('equals (n-ary)','(=1 1),(=255 255),(=3 3 3)','H'),0x202:('not equal','(≠ 0 1),(≠ 254 255)','H'),
0x203:('less than (chainable)','(<0 1)…(<0 5 9 255)','H'),0x204:('greater than','(>1 0),(>9 4 1 0)','H'),
0x205:('≤','(≤2 2),(≤1 1 2 5)','H'),0x206:('≥','(≥2 2),(≥9 0)','H'),0x207:('addition','(=(+ 2 3) 5),(+ 1 2 3)=6','H'),
0x208:('multiplication','(*3 4)=12,(*15 15)=225','H'),0x209:('base-256 numeral','(NUM 1 0)=(* 16 16); (NUM 1 0)=(+255 1)','H'),
0x20a:('subtraction','(- 5 3)=2,(- 3 5)=(neg 2)','H'),0x20b:('negation','(+(neg 2)2)=0','H'),0x20c:('division','(/6 3)=2,(+(/1 2)(/1 3))=(/5 6)','H'),
0x20d:('not','(not T)=F','H'),0x20e:('and','truth table','H'),0x20f:('or','truth table','H'),
0x210:('list constructor','(len (list 4 7 9))=3','H'),0x211:('length','(len (list))=0','H'),0x212:('n-th element, 1-based','(nth (list 4 7 9) 1)=4','H'),
0x213:('count occurrences','(count 3 (list 3 1 3))=2','H'),0x214:('for all x in S','(all x (list 1 2 3) (<x 4))=(and …)','H'),
0x215:('there exists x in S','(some x (list 1 2 3)(= x 2))','H'),0x216:('implies','truth table T→F=F only','H'),
0x217:('fold/reduce op over list','(fold + (list 1 2 3))=6; (fold < (list 1 5 9))=T','H'),0x218:('map','(map x (list 1 2 3)(* x x))=(list 1 4 9)','H'),
0x219:('arithmetic mean','mean(2 4 9)=5','H'),0x21a:('relative frequency / probability','freq 3 in (3 1 3)=2/3','H'),
0x21b:('Cartesian product','(prod (1 2)(3 4)) given','H'),0x21c:('tail (drop first)','(tail (4 7 9))=(7 9)','H'),
0x21d:('if-then-else','(if T 1 2)=1','H'),0x21e:('power','(pow 2 3)=8,(pow 5 0)=1','H'),0x21f:('absolute value / modulus','(abs (+3 (*4 i)))=5','H'),
0x220:('exponential function','exp(0)=1, exp(x+y)=exp x·exp y, exp(iπ)=−1','H'),0x221:('dot product in R3','(dot (1 2 3)(4 5 6))=32','H'),
0x222:('cosine','cos x=(e^{ix}+e^{-ix})/2','H'),0x223:('angle between unit vectors','angle((1 0 0),(0 1 0))=π/2','H'),
0x224:('cross product','x̂×ŷ=ẑ, component formula','H'),0x225:('average over a set (uniform)','avg over S2 of x1²=1/3','H'),
0x226:('quote','(quote (+ 2 3))=(list (quote +) 2 3)','H'),0x227:('kind of item: 0 number,1 list,2 operator,3 constant,4 variable,5 particle,6 atom,7 dimension,8 physical constant,9 molecule','(kind 5)=0 … (kind (quote Mol2))=9','H'),
0x228:('let-binding','(let x 4 (= (+ x x) 8))','H'),0x229:('evaluate quoted expression','(eval (quote (+ 2 3)))=5','H'),
0x22a:('substitute value into the blank 30e','subst (= (+ 2 3) □) 5 → (= (+ 2 3) 5)','H'),0x22b:('author of a message','(author MSG)=30f','M'),
0x22c:('addressee of a message','(addressee MSG)=310','M'),0x22d:('the sender asserts/declares','prefixes self-statements only','M'),
0x22e:('sender would accept dialogue [question, answer] as correct','accepts 2+3=□ → 5, rejects 4','M'),0x22f:('sender would reject it','all false x → reject','M'),
0x230:('empirical fact about the physical world','prefixes all measured statements','M'),0x231:('rest mass','m(501)<m(502)<m(503); ratios 1836–1839','H'),
0x232:('electric charge','q(502)=−q(501), q(503)=0','H'),0x233:('isotope (element, neutron count)','count 503 (isotope x y)=y','H'),
0x234:('stable / exists','H-1,H-2,He-3,He-4,C-12,C-13,O-16 listed','M'),0x235:('bound-state energy level n of an atom','(E2−E1)/(E3−E2)=27/5 (Rydberg)','H'),
0x236:('physical dimension of','dim(energy)=M L²/T²','H'),0x237:('speed','speed of every photon = 801','H'),0x238:('wavelength','λ·ν=c','H'),
0x239:('frequency (cycles per time)','dim=1/T, E=ħ·2πν','H'),0x23a:('photon energy','=802·2π·ν','H'),0x23b:('photon emitted in transition atom,n→m','ħω(2→1)=E2−E1','H'),
0x23c:('distance between bodies','symmetric, dim L','H'),0x23d:('gravitational force','=G m m/r²','H'),0x23e:('Coulomb force','=k q q/r², p–e attractive','H'),
0x23f:('electric current','dim Q/T','H'),0x240:('force per length between parallel wires','=−2μ I I/d, dim M/T²','H'),0x241:('mean kinetic energy of gas particle','=3/2 k T','H'),
0x242:('temperature','dim Θ','H'),0x243:('radiated power per area','σT⁴ formula with π²/60','H'),0x244:('mean lifetime','neutron lifetime 2^153–2^154 tP','H'),
0x245:('survival probability after time t','exp(−t/τ); 1/2 at half-life','H'),0x246:('half-life','C-14 / H-3 ratio 256–512','H'),0x247:('spin angular momentum','e,p,n=ħ/2, photon=ħ','H'),
0x248:('particle spins in sense from y toward z (rotation sense)','defines spin axis via cross','M'),0x249:('spin axis direction','=y×z','M'),
0x24a:('decay asymmetry w.r.t. parent spin (A, B coefficients)','A(e,n)∈(−1,0), A(505,n)>0','L'),0x24b:('helicity (or similar polarisation)','e∈(−1,0), 505 ≈ +1','L'),
0x24c:('loop radius','dim L','H'),0x24d:('magnetic field at loop centre','=2π μ I / r','H'),0x24e:('current circulates from y toward z','analog of 248','M'),
0x24f:('magnetic-moment direction','p moment ∥ spin, e,n antiparallel','H'),0x250:('branching fraction: decay of y yields x','(yield e n)=1; kaon e+/e− 1.004–1.008','M'),
0x251:('number of states in shell n','2,8,18,32 = 2n²','H'),0x252:('chemically inert (noble)','He,Ne,Ar,Kr,Xe,Rn','M'),0x253:('atoms of molecule (list)','H2O → (O H H)','H'),
0x254:('bonds (atom i, atom j, order)','CO2 double bonds','H'),0x255:('triple-point temperature','H2/H2O ≈ 0.0505, Ne, Ar match','H'),0x256:('triple-point pressure','water 611.66 Pa in Planck units','H'),
0x257:('luminosity','=4πR²σT⁴','H'),0x258:('x orbits y','Kepler III','H'),0x259:('orbital period','dim T','H'),0x25a:('orbital semi-major axis','dim L','H'),
0x25b:('CMB temperature in direction x','isotropic to 1/256; 2.725 K','H'),0x25c:('is located at/on','sender at 320','M'),0x25d:('unit direction from x to y','unit, antisymmetric','H'),
0x25e:('velocity of x relative to y','Sun around 321 ≈ 146–293 km/s','H'),0x25f:('pulse period','dim T; Crab 2^138–2^139 tP','H'),0x260:('period derivative','Crab 3.8–4.7e−13','H'),
0x261:('cost (lower=better) to first player of a move pair','(C,C)=3,(D,D)=5,(C,D)=7,(D,C)=2','H'),0x262:('strategy’s possible next moves given history','TFT copies last','H'),
0x263:('history of z rounds of x vs y','length z, mirrored','H'),0x264:('total cost over z rounds','TFT vs TFT 255 rounds=765','H'),0x265:('strategy agent x uses toward y','sender → 332','M'),
0x301:('true','(= (= 2 2) T)','H'),0x302:('false','(not T)=F','H'),0x303:('natural numbers incl. 0','no x<0; 0 in it; x+1 in it','H'),0x304:('rationals','±x/(y+1); no √2','H'),
0x305:('reals','√2, ∛2 exist; x²≥0','H'),0x306:('imaginary unit i','i²=−1','H'),0x307:('complex numbers','x=a+bi, x²=−1 solvable','H'),0x308:('e','=exp 1, 8/3<e<11/4','H'),
0x309:('π','e^{iπ}=−1, 223/71<π<22/7, Leibniz, Basel','H'),0x30a:('R³ vectors','len 3 real lists','H'),0x30b:('unit vectors (sphere S²)','dot=1','H'),
0x30c:('all expressions / data','contains 5, +, (+ 2 3)','H'),0x30d:('this message (list of its top-level items)','nth 1=1, nth 13=0; counts verified','H'),
0x30e:('blank / placeholder','subst fills it','H'),0x30f:('the sender','author of MSG','H'),0x310:('the receiver','addressee of MSG','H'),0x311:('agents/communicators','sender, receiver ∈','M'),
0x312:('reply chains (dialogues)','alternating author/addressee definition','M'),0x313:('atoms','≥1 proton each','H'),0x314:('photons','speed c','H'),0x315:('bodies (massive objects)','gravity/Coulomb law','H'),
0x316:('straight current-carrying wires','force per length','M'),0x317:('ideal gases (particles)','3/2 kT','M'),0x318:('black bodies','σT⁴','H'),0x319:('time intervals','dim T','M'),
0x31a:('current loops','radius, field, moment','H'),0x31b:('stars','bodies; L=4πR²σT⁴; H>He>C,O','H'),0x31c:('CMB principal (quadrupole) axis 1','max of quadrupole form','M'),
0x31d:('CMB axis 2 (max among ⊥ axC)','','M'),0x31e:('axis 3 = axC×axD','','H'),0x31f:('the sender’s star (Sun-like)','mass, radius, T, L match Sun','H'),
0x320:('sender’s home planet (Earth-like)','orbits 31f; Earth mass/orbit','H'),0x321:('Galactic-centre massive object','~4×10⁶ M☉, ~8 kpc','H'),0x322:('unit vector Sun→Galactic centre','','H'),
0x323:('direction of Galactic rotation','Sun velocity ∥ it','H'),0x324:('third axis 322×323 (≈ north Galactic pole)','pulsar latitudes fit','H'),0x325:('pulsars','period, Pdot, direction','H'),
0x326:('Crab pulsar','P, Pdot, direction','H'),0x327:('Vela pulsar','','H'),0x328:('PSR J0437−4715','','H'),0x329:('PSR B1937+21','','H'),0x32a:('PSR B0329+54','','M'),0x32b:('PSR B1919+21','','M'),
0x32c:('move: cooperate','mutual 32c cheaper than mutual 32d','H'),0x32d:('move: defect','dominant move','H'),0x32e:('set of moves (C D)','len 2','H'),0x32f:('game histories (lists of [mine, theirs])','','H'),
0x330:('strategy: always cooperate','','H'),0x331:('always defect','','H'),0x332:('tit-for-tat','C first, then copy','H'),0x333:('suspicious tit-for-tat','D first, then copy','H'),
0x334:('grim trigger','D forever after any D','H'),0x335:('Pavlov-like: C if last two moves equal','','H'),0x336:('generous TFT: after D, C with prob 1/3','returns (C D D)','M'),0x337:('random 50/50','','H'),
0x338:('tournament set of 6 deterministic strategies 330–335','','H'),
0x401:('variable x','bound by all/some/map/let','H'),0x402:('variable y','','H'),0x403:('variable z','','H'),0x404:('variable w','','H'),
0x501:('electron','lightest, q=−q(502), in all atoms','H'),0x502:('proton','count in He=2, m/me 1836–1837','H'),0x503:('neutron','neutral, m/me 1838–1839, decays','H'),
0x504:('photon','mass 0, charge 0, spin ħ','H'),0x505:('(anti)neutrino','neutral, lighter than e, helicity ≈+1','M'),0x506:('positron','e-mass, opposite charge, absent from atoms','H'),
0x507:('neutral kaon (K_L)','neutral, 973–975 mₑ; e+ vs e− yield asymmetry','M'),0x601:('hydrogen','1 proton','H'),0x602:('helium','2','H'),0x606:('carbon','6','H'),0x607:('nitrogen','in NH3; Z by code','H'),
0x608:('oxygen','8','H'),0x60a:('neon','10 protons','H'),0x612:('argon','18','H'),0x624:('krypton','36','H'),0x636:('xenon','54','H'),0x656:('radon','86','H'),
0x701:('dimension mass','','H'),0x702:('dimension length','','H'),0x703:('dimension time','','H'),0x704:('dimension charge','','H'),0x705:('dimension temperature','','H'),
0x801:('speed of light c','photon speed','H'),0x802:('reduced Planck const ħ','dim M L²/T; spin ħ/2','H'),0x803:('G','Newton law','H'),0x804:('Coulomb constant k=1/4πε₀','dim M L³/(T²Q²)','H'),
0x805:('μ₀/4π','k/μ = c²','H'),0x806:('Planck length','√(ħG/c³)','H'),0x807:('Planck time','√(ħG/c⁵)','H'),0x808:('Planck mass','√(ħc/G)','H'),
0x809:('hydrogen 21-cm photon','E/(E2−E1) 2^-21–2^-20','H'),0x80a:('Boltzmann constant','3/2 kT','H'),0x80b:('Planck temperature','kB·TP = mP c²','H'),
0x901:('H₂','2 H, bond (1 2 1)','H'),0x902:('H₂O','O,H,H; 10 protons','H'),0x903:('CH₄','','H'),0x904:('NH₃','','H'),0x905:('CO₂','double bonds','H'),
0x906:('adenine C5H5N5','formula only','M'),0x907:('thymine C5H6N2O2','','M'),0x908:('guanine C5H5N5O','','M'),0x909:('cytosine C4H5N3O','','M'),
}
miss=[hex(s) for s in first if s not in M]
print('missing',miss)
rows=[]
for s in sorted(first):
    m,ev_,c=M[s]
    rows.append(f'| `{s:04x}` | {m} | {4632+16*first[s]} | {ev_} | {c} |')
open('/work/vocab.md','w').write('\n'.join(rows))
print(len(rows))

# ---- run 57 ----
print(open('/work/vocab.md').read())
