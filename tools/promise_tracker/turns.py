import re,sys
txt=open(sys.argv[1]).read().split('\n')
start=int(sys.argv[2]) if len(sys.argv)>2 else 0
mgmt=('Tanushree','Rohit','Parmjit','Management','Paramjit','Vivek','Gurdeep','Herbert','Soni','Mukesh','Rahul','Ankit','Jatin')
cur=None;buf=[]
out=[]
def flush():
    if cur is None: return
    t=' '.join(buf)
    t=re.sub(r'Uniparts India Limited [A-Z][a-z]+ \d\d, 20\d\d','',t)
    if any(cur.startswith(m) for m in mgmt): out.append(f"**{cur}: {t}")
    elif cur=='Moderator': out.append(f"[Mod] {t[:80]}")
    else: out.append(f"Q {cur}: {t[:260]}")
for i,l in enumerate(txt):
    if i<start: continue
    m=re.match(r'^([A-Z][A-Za-z\.]+(?: [A-Z][A-Za-z\.]+){0,3}):\s?(.*)',l)
    if m and len(m.group(1))<35 and m.group(1) not in ('Tel','Subject','Scrip Code','Regd. Office','Corporate Office','Date','DN','Encl'):
        flush(); cur=m.group(1); buf=[m.group(2)]
    else: buf.append(l.strip())
flush()
print('\n'.join(out))
