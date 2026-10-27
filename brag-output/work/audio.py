import numpy as np, wave, struct

SR=48000; DUR=20.0; N=int(SR*DUR); T=np.arange(N)/SR
BPM=120.0; B=60.0/BPM          # 0.5 s per beat, 2 s per bar
def idx(t): return int(round(t*SR))
def seg(t0,t1):
    a,b=max(0,idx(t0)),min(N,idx(t1)); return a,b,max(0,b-a)
def add(buf,t0,sig,g=1.0):
    a=idx(t0)
    if a>=N or len(sig)==0: return
    n=min(len(sig),N-a); buf[a:a+n]+=sig[:n]*g

def adsr(n,a,d,s,r):
    e=np.ones(n); A=int(a*SR); D=int(d*SR); R=int(r*SR)
    A=min(A,n); e[:A]=np.linspace(0,1,A,endpoint=False) if A else e[:A]
    if D and A+D<=n: e[A:A+D]=np.linspace(1,s,D,endpoint=False)
    if A+D<n: e[A+D:]=s
    if R and R<n: e[n-R:]*=np.linspace(1,0,R)
    return e

def lp1(x,cut):
    """one-pole lowpass; cut may be scalar or per-sample array"""
    c=np.full(len(x),cut,dtype=float) if np.isscalar(cut) else np.asarray(cut,dtype=float)
    a=1-np.exp(-2*np.pi*c/SR); y=np.empty_like(x); z=0.0
    for i in range(len(x)):
        z+=a[i]*(x[i]-z); y[i]=z
    return y

rng=np.random.default_rng(7)

# ---------------- voices ----------------
def bansuri(f,dur,amp=1.0,vib=5.2,breath=0.055):
    """sine-led flute-ish tone: soft 2nd/3rd harmonics, vibrato, breath noise"""
    n=int(dur*SR); t=np.arange(n)/SR
    depth=np.minimum(t/0.28,1.0)*0.006                 # vibrato eases in
    ph=2*np.pi*f*t+depth*np.sin(2*np.pi*vib*t)*f/vib*2*np.pi/ (2*np.pi)
    ph=2*np.pi*f*t+ (depth*f/vib)*np.sin(2*np.pi*vib*t)*2*np.pi
    s=np.sin(ph)+0.17*np.sin(2*ph)+0.055*np.sin(3*ph)
    air=lp1(rng.normal(0,1,n),2600+f*1.4)*breath
    e=adsr(n,0.085,0.18,0.82,min(0.30,dur*0.45))
    return (s*0.5+air)*e*amp

def pad(f,dur,amp=1.0):
    n=int(dur*SR); t=np.arange(n)/SR
    s=sum(np.sin(2*np.pi*f*k*t+k)* (0.6/k) for k in (1,2,3,4))
    s+=0.25*np.sin(2*np.pi*f*1.004*t)                   # slight detune
    return s*adsr(n,0.6,0.8,0.8,min(1.4,dur*0.5))*amp

def chug(f,dur,amp=1.0,mute=True):
    """palm-muted distorted saw"""
    n=int(dur*SR); t=np.arange(n)/SR
    saw=2*((f*t)%1.0)-1.0
    saw+=2*((f*1.5*t)%1.0)-1.0                          # fifth on top
    e=adsr(n,0.004,0.06 if mute else 0.4,0.25 if mute else 0.6,min(0.09 if mute else 0.6,dur*0.6))
    x=np.tanh(saw*4.2)*e
    return lp1(x,2100 if mute else 3000)*amp

def kick(amp=1.0,dur=0.5):
    n=int(dur*SR); t=np.arange(n)/SR
    f=45+95*np.exp(-t*34)
    s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)
    s+=lp1(rng.normal(0,1,n),130)*np.exp(-t*60)*0.55
    return np.tanh(s*1.5)*amp

def snare(amp=1.0,dur=0.35):
    n=int(dur*SR); t=np.arange(n)/SR
    nz=rng.normal(0,1,n); body=nz-lp1(nz,700)           # crude highpass
    tone=np.sin(2*np.pi*185*t)*np.exp(-t*26)*0.4
    return (body*np.exp(-t*19)+tone)*amp

def hat(amp=1.0,dur=0.09):
    n=int(dur*SR); t=np.arange(n)/SR
    nz=rng.normal(0,1,n); return (nz-lp1(nz,6500))*np.exp(-t*72)*amp

def boom(amp=1.0,dur=2.6):
    n=int(dur*SR); t=np.arange(n)/SR
    f=28+62*np.exp(-t*5.5)
    s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.2)
    s+=lp1(rng.normal(0,1,n),200)*np.exp(-t*13)*0.3
    return np.tanh(s*1.25)*amp

def riser(dur,amp=1.0,f0=220.0):
    n=int(dur*SR); t=np.arange(n)/SR; x=t/dur
    cut=350+5200*x**2.4
    nz=lp1(rng.normal(0,1,n),cut)*(x**1.7)
    tone=np.sin(2*np.pi*np.cumsum(f0*(1+2.1*x**2))/SR)*(x**2.6)*0.4
    return (nz*0.9+tone)*amp

def whoosh(dur=0.42,amp=1.0):
    n=int(dur*SR); t=np.arange(n)/SR; x=t/dur
    cut=5200*np.exp(-x*3.2)+320
    return lp1(rng.normal(0,1,n),cut)*np.exp(-x*3.4)*np.minimum(x*9,1)*amp

def tick(f=1500,amp=1.0,dur=0.07):
    n=int(dur*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*f*t)+0.5*np.sin(2*np.pi*f*2.3*t))*np.exp(-t*95)*amp

# ---------------- note table: A minor, Bhairavi-flavoured ----------------
A1,A2,E3,A3,A4,Bb4,Cs5,D5,E5,F5,G5,A5 = 55.0,110.0,164.81,220.0,440.0,466.16,554.37,587.33,659.25,698.46,783.99,880.0
Cs4,D4,E4,F4 = 277.18,293.66,329.63,349.23

MUS=np.zeros(N); FX=np.zeros(N)

# ---- drone bed: present the whole way, swelling with the picture ----
env=np.interp(T,[0,1.0,2.0,6.0,10.4,10.6,14.0,17.0,18.6,19.9,20.0],
                [0,0.18,0.42,0.52,0.52,0.34,0.46,0.70,0.52,0.0,0.0])
drone=(np.sin(2*np.pi*A1*T)*0.9+np.sin(2*np.pi*A2*T+0.6)*0.42
       +(2*((A2*T)%1.0)-1.0)*0.10)
MUS+=lp1(drone,420)*env*0.30

# ---- bansuri line ----
LEAD=[(0.15,A4,0.95,0.80),(1.05,Cs5,0.48,0.72),(1.53,D5,0.44,0.76),
      (3.05,E5,0.90,0.70),(3.95,D5,0.48,0.62),(4.45,Cs5,0.78,0.66),(5.25,A4,0.72,0.60),
      (6.50,A4,0.46,0.62),(7.00,Cs5,0.46,0.64),(7.50,E5,0.46,0.66),
      (8.00,D5,0.46,0.62),(8.50,Cs5,0.46,0.60),
      (9.00,A5,1.42,0.86),
      (11.00,E4,0.36,0.46),(11.50,D4,0.36,0.46),(12.00,Cs4,0.36,0.46),(12.50,A3,0.40,0.46),
      (14.50,A4,0.46,0.56),(15.00,Cs5,0.46,0.60),(15.50,E5,1.42,0.72),
      (17.00,A5,2.60,0.78),(17.00,A4,2.60,0.40)]
for t0,f,d,a in LEAD: add(MUS,t0,bansuri(f,d,a),0.30)

# ---- pads on the reveals ----
for t0,f,d,a in [(3.0,A3,3.0,0.55),(3.0,E3,3.0,0.40),(6.0,A2,4.5,0.42),
                 (14.0,A3,3.0,0.40),(17.0,A3,3.0,0.62),(17.0,E3,3.0,0.46)]:
    add(MUS,t0,pad(f,d,a),0.16)

# ---- guitar ----
t=6.0
while t<10.40:                                   # eighths under THE CULT
    acc=1.0 if abs((t/B)%2)<1e-6 else 0.62
    add(MUS,t,chug(A2,0.24,acc),0.17); t+=B/2
t=10.50
while t<13.95:                                   # half-time chugs under THE SET
    add(MUS,t,chug(A2,0.46,1.0),0.19)
    add(MUS,t,chug(E3,0.46,0.5),0.10); t+=B
t=14.0
while t<16.95:                                   # build under ON TOUR
    acc=1.0 if abs((t/B)%2)<1e-6 else 0.58
    add(MUS,t,chug(A2,0.24,acc),0.19); t+=B/2
add(MUS,17.0,chug(A2,2.6,1.0,mute=False),0.21)   # final ring-out chord
add(MUS,17.0,chug(E3,2.6,0.6,mute=False),0.12)

# ---- drums ----
for t in np.arange(2.0,17.01,2*B):               # kick on 1 and 3
    add(MUS,t,kick(1.0 if t>=6.0 else 0.75),0.30)
for t in np.arange(6.5,16.99,2*B):               # snare on 2 and 4
    add(MUS,t,snare(0.85),0.14)
for t in np.arange(6.0,17.0,B/2):                # hats
    add(MUS,t,hat(0.5 if (t/B)%1 else 0.75),0.045)
for t in [14.75,15.25,15.75,16.25,16.5,16.75,16.875]:   # fill into the outro
    add(MUS,t,snare(0.55+0.5*(t-14.75)),0.11)
add(MUS,17.0,kick(1.25),0.34)
add(MUS,17.0,snare(1.0),0.15)

# ---- effects: same key, same room, sitting under the music ----
add(FX,1.20,riser(0.80,0.85,f0=A2),0.26)         # into the collision
add(FX,2.00,boom(1.0),0.40)
for t in [3.0,6.0,10.5,14.0]:                    # scene cuts
    add(FX,t-0.20,whoosh(0.40,0.8),0.10)
add(FX,10.5,boom(0.45,1.6),0.16)
add(FX,14.0,boom(0.45,1.6),0.16)
add(FX,17.0,boom(0.9,3.0),0.30)
for i in range(5):                               # one tick per card
    add(FX,6.50+i*B,tick(1250+i*110,0.8),0.035)
for i in range(4):                               # one per track title
    add(FX,11.00+i*B,tick(900+i*90,0.7),0.030)
add(FX,9.00,tick(1800,0.6),0.035)

# ---------------- mix ----------------
mix=MUS+FX*0.72
tail=np.interp(T,[0,0.06,19.55,19.95,20.0],[0,1,1,0.0,0.0]); mix*=tail
mix=np.tanh(mix*1.18)*0.92                       # gentle glue / limiting
mix/=max(1e-9,np.abs(mix).max()); mix*=0.90

st=np.stack([mix,mix],axis=1)                    # light stereo spread on the lead
st[:,0]=np.roll(st[:,0],  9); st[:,1]=np.roll(st[:,1], -9)
st[:9]=0; st[-9:]=0
pcm=(np.clip(st,-1,1)*32767).astype('<i2')
with wave.open('track.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote track.wav  peak=%.3f  rms=%.4f"%(np.abs(mix).max(), np.sqrt((mix**2).mean())))
