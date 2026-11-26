import json,glob,base64,sys,os
# usage: join.py PREFIX out  -> finds tool results whose text starts with PREFIX<n>:
import sys as _s; D=_s.argv[3] if len(_s.argv)>3 else "/root/.claude/projects/-home-claude-ayah-daily-media/"+"*/tool-results/"
pre,out=sys.argv[1],sys.argv[2]; parts={}
for f in glob.glob(D+'*javascript_tool*.txt'):
    try: t=json.load(open(f))[0]['text'].strip()
    except Exception: continue
    if t.startswith('"'): t,_=json.JSONDecoder(strict=False).raw_decode(t)
    if t.startswith(pre):
        n=int(t[len(pre):t.index(':')]); parts[n]=(os.path.getmtime(f),t[t.index(':')+1:])
ks=sorted(parts); print(ks)
assert ks==list(range(len(ks)))
open(out,'wb').write(base64.b64decode(''.join(parts[k][1] for k in ks)))
print(os.path.getsize(out))
