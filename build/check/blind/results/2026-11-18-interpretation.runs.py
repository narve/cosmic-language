# The code the blind reader ran, in order (2026-11-18, interpretation, full message, Opus).

# ---- run 1 ----
s=open('/work/bits.txt').read();print(len(s),repr(s[:300]),set(s))
t=s.strip();n=len(t);print(n)
import sympy;print(sympy.factorint(n))
from collections import Counter;print(Counter(t))

# ---- run 2 ----
t=open('/work/bits.txt').read().strip();n=len(t)
def fac(n):
  f=[];d=2
  while d*d<=n:
    while n%d==0:f.append(d);n//=d
    d+=1
  if n>1:f.append(n)
  return f
print(fac(n))
i=t.index('0000000000');print(i)
print([len(x) for x in t[:i].split('0')])
for k in range(i,i+16*40,16):print(t[k:k+16],int(t[k:k+16],2))

# ---- run 3 ----
r=t[172:];print(len(r),len(r)/16)
w=[int(r[k:k+16],2) for k in range(0,len(r)-len(r)%16,16)]
print(len(w))
print(w[:400])

# ---- run 4 ----
t=open('/work/bits.txt').read().strip()
r=t[172:];print(len(r),len(r)/16)
w=[int(r[k:k+16],2) for k in range(0,len(r)-len(r)%16,16)]
print(len(w))
print(w[:600])

# ---- run 5 ----
t=open('/work/bits.txt').read().strip()
r=t[172:]
w=[int(r[k:k+16],2) for k in range(0,len(r)-len(r)%16,16)]
print('tail bits',r[-(len(r)%16):], w[-30:])
from collections import Counter
c=Counter(x for x in w[269:])
print(sorted(c.items()))
import json;json.dump(w,open('/work/w.json','w'))

# ---- run 6 ----
import json
w=json.load(open('/work/w.json'))
t=open('/work/bits.txt').read().strip()
# find end of structure
d=0;tops=[];start=None
for i,x in enumerate(w):
  if i<269: continue
  if x==256:
    if d==0:start=i
    d+=1
  elif x==257:
    d-=1
    if d==0:tops.append((start,i))
  elif d==0: print('outside',i,x)
print(len(tops),tops[-1])
end=tops[-1][1]+1
print(t[172+16*end:])
print(len(t[172+16*end:]))

# ---- run 7 ----
import json
w=json.load(open('/work/w.json'))
names={513:'=',514:'≠',515:'<',516:'>',517:'≤',518:'≥'}
def nm(x):
  if x<256: return str(x)
  return names.get(x,'%X'%x)
def parse(i):
  assert w[i]==256
  out=[];i+=1
  while w[i]!=257:
    if w[i]==256:
      e,i=parse(i);out.append(e)
    else: out.append(w[i]);i+=1
  return out,i+1
stmts=[];i=268
while i<len(w) and w[i]==256:
  e,i=parse(i);stmts.append(e)
print(len(stmts),i,len(w))
def show(e):
  if isinstance(e,list): return '('+' '.join(show(x) for x in e)+')'
  return nm(e)
lines=[show(e) for e in stmts]
open('/work/lines.txt','w').write('\n'.join(lines))
json.dump(stmts,open('/work/stmts.json','w'))
print('\n'.join(lines[:150]))

# ---- run 8 ----
L=open('/work/lines.txt').read().split('\n')
for k in range(150,330):print(k,L[k][:300])

# ---- run 9 ----
L=open('/work/lines.txt').read().split('\n')
for k in range(330,480):print(k,L[k][:400])

# ---- run 10 ----
L=open('/work/lines.txt').read().split('\n')
for k in range(480,600):print(k,L[k][:500])

# ---- run 11 ----
L=open('/work/lines.txt').read().split('\n')
for k in range(600,720):print(k,L[k][:600])

# ---- run 12 ----
L=open('/work/lines.txt').read().split('\n')
for k in range(720,830):print(k,L[k][:700])

# ---- run 13 ----
L=open('/work/lines.txt').read().split('\n')
for k in range(830,967):print(k,L[k][:900])

# ---- run 14 ----
import json
t=open('/work/bits.txt').read().strip()
tail=t[172+16*18707:]
print(len(tail), tail==t[:172], tail==t[:172][::-1])
print(tail)
# tournament
C,D='C','D'
cost={(C,C):3,(D,D):5,(C,D):7,(D,C):2}
def allc(h):return C
def alld(h):return D
def tft(h):return C if not h else h[-1][1]
def stft(h):return D if not h else h[-1][1]
def grim(h):return D if any(x[1]==D for x in h) else C
def pav(h):
  if not h:return C
  return C if h[-1][0]==h[-1][1] else D
S={'330allC':allc,'331allD':alld,'332TFT':tft,'333STFT':stft,'334GRIM':grim,'335PAV':pav}
def play(a,b,n):
  ha=[];hb=[];tot=0
  for _ in range(n):
    x=a(ha);y=b(hb);ha.append((x,y));hb.append((y,x));tot+=cost[(x,y)]
  return tot,ha
for a in S:
  print(a,[play(S[a],S[b],255)[0] for b in S], sum(play(S[a],S[b],255)[0] for b in S))
print(play(tft,alld,4)[1], play(tft,alld,4)[0])
claimed={'332TFT':(2,253),'331allD':(4,251)}
print('claims: 941..958 pairs', [(a,b,256*a+b) for a,b in [(2,253),(4,251),(4,253),(4,248),(6,249),(1,254),(5,251),(3,123),(4,126),(4,121),(4,250),(4,250),(21,111),(21,235),(21,238),(22,149),(25,95),(27,11)]])

# ---- run 15 ----
import json
st=json.load(open('/work/stmts.json'))
first={};cnt={}
def walk(e,k):
  for x in e:
    if isinstance(x,list): walk(x,k)
    elif x>=256:
      first.setdefault(x,k);cnt[x]=cnt.get(x,0)+1
for k,e in enumerate(st): walk(e,k)
for x in sorted(first): print('%X'%x,first[x],cnt[x],end=' | ')
print()
# usage of 31C.. after 826, 336/337, 323 and 30F links
L=open('/work/lines.txt').read().split('\n')
for sym in ['31C','31E','320','31F','30F','310','336','337','262','263','24F','507']:
  print(sym,[k for k,l in enumerate(L) if sym in l.replace('(',' ').replace(')',' ').split()])

# ---- run 16 ----
import json
st=json.load(open('/work/stmts.json'))
items=[1,2,3,5,7,11,13,17,19,23,29,31]
for k,q in [(509,[513,1,1]),(510,[513,3,3]),(511,[514,0,1]),(512,[513,5,5]),(513,[513,2,3]),(515,[513,[519,2,2],5]),(516,[513,6,6]),(517,[515,5,6]),(518,[513,[519,3,3],6])]:
  print(k,q,sum(1 for s in st if s==q))
# what's the 16-bit numeral list right before statements; count items
w=json.load(open('/work/w.json'));print(w[:13],w[12:15], w[266:270])
# check if numeric 0..256 counting exists
print(st[164])

# ---- run 17 ----
from math import *
hbar=1.054571817e-34;c=2.99792458e8;G=6.6743e-11;kB=1.380649e-23;me=9.1093837e-31;mp=1.67262192e-27;mn=1.67492750e-27;e=1.602176634e-19;eps=8.8541878128e-12
lP=sqrt(hbar*G/c**3);tP=lP/c;mP=sqrt(hbar*c/G);TP=mP*c**2/kB
ke=1/(4*pi*eps);Ry=13.605693*e;dE12=0.75*Ry
def chk(name,lo,val,hi):print(name, lo<val<hi, lo,val,hi)
chk('mp/me',1836,mp/me,1837);chk('mn/mp',1+2**-11,mn/mp,1+2**-9)
chk('alpha',1/138,ke*e**2/(hbar*c),1/137)
chk('Coul/Grav',2**130,ke*e**2/(G*mp*me),2**131)
chk('mp/mP',2**-64,mp/mP,2**-63);chk('me/mP',2**-75,me/mP,2**-74)
E21=hbar*2*pi*1.420405751e9
chk('21cm/Lya',2**-21,E21/dE12,2**-20);chk('1/(f tP)',2**113,1/(1.420405751e9*tP),2**114)
chk('Lya/mec2',2**-16,dE12/(me*c*c),2**-15)
chk('tau_n/tP',2**153,879.4/tP,2**154);chk('C14/H3',2**8,5730/12.32,2**9)
chk('K0/me',973,497.611e6*e/c**2/me,975)
d=3.32e-3;chk('KL asym',1+2**-8,(1+d)/(1-d),1+2**-7)
Ttp=273.16
chk('H2tp',103/2048,13.8033/Ttp,104/2048);chk('Ne',736/8192,24.5561/Ttp,737/8192);chk('Ar',1256/4096,83.8058/Ttp,1257/4096)
chk('kTtp/Lya',302/2**17,kB*Ttp/dE12,303/2**17);chk('Ttp/TP',156/2**106,Ttp/TP,157/2**106)
pP=c**7/(hbar*G**2);chk('ptp/pP',203/2**376,611.657/pP,204/2**376)
chk('pH2/pw',11,7041/611.657,12);chk('pNe',70.5,43368/611.657,71.5);chk('pAr',112,68891/611.657,113)
chk('He4/4H',1-2**-7,4.002602/(4*1.007825),1-2**-8)
chk('Tcmb',163/2**14,2.7255/Ttp,164/2**14)
Ms=1.989e30;chk('Msun/mp',2**189,Ms/mp,2**190);chk('Rsun',2**144,6.957e8/lP,2**145);chk('Tsun',21,5772/Ttp,22)
chk('Lsun',2**-87,3.828e26/(c**5/G),2**-86);chk('AU',2**152,1.495978707e11/lP,2**153);chk('yr',2**168,3.15576e7/tP,2**169)
chk('Mearth',2**171,5.972e24/mp,2**172);chk('SgrA',2**211,4.3e6*Ms/mp,2**212);chk('R0',2**183,8.2e3*3.0857e16/lP,2**184)
chk('v',2**-11,230e3/c,2**-10);chk('galyr',2**196,230e6*3.156e7/tP,2**197)
for nm,P,Pd,l,b in [('Crab',0.0334,4.2e-13,184.56,-5.78),('Vela',0.0893,1.25e-13,263.55,-2.79),('J0437',0.005757,5.73e-20,253.39,-41.96),('B1937',0.0015578,1.05e-19,57.51,-0.29),('B0329',0.7145,2.05e-15,145.0,-1.22),('B1919',1.3373,1.35e-15,55.78,3.50)]:
  print(nm,log2(P/tP),Pd*2**48, [round(v*32,2) for v in (cos(radians(b))*cos(radians(l)),cos(radians(b))*sin(radians(l)),sin(radians(b)))])

# ---- run 18 ----
import json
w=json.load(open('/work/w.json'))
starts=[];i=268;d=0
for j in range(268,18707):
  if w[j]==256 and d==0: starts.append(j)
  if w[j]==256:d+=1
  elif w[j]==257:d-=1
for k in [0,158,206,335,365,444,506,526,550,592,603,660,723,742,782,799,811,815,827,843,853,892,926,959,966]:
  print(k,'bit',172+16*starts[k])
print('end bit',172+16*18707)
