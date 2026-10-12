import json, re, subprocess, sys, xml.etree.ElementTree as ET
d = json.load(open(sys.argv[1]))
from collections import Counter
print(Counter(i['subtype'] for i in d), len(d))
ids=set()
for it in d:
    assert it['id'] not in ids; ids.add(it['id'])
    assert set(it)=={"id","area","subtype","difficulty","prompt","figure","options","answer","explanation"}
    assert it['area']=='espacial' and it['difficulty'] in ('facil','media','dificil')
    assert 0<=it['answer']<len(it['options'])
    assert len(set(it['options']))==len(it['options']), it['id']
    for s in [it['figure']]+it['options']:
        if s.startswith('<svg'):
            ET.fromstring(s)
            assert 'viewBox' in s and ' width="' not in s.split('>')[0] and '<script' not in s
            for f in re.findall(r'fill="([^"]*)"', s):
                assert f in ('none','currentColor','var(--fig-a)','var(--fig-b)'), f
            for f in re.findall(r'stroke="([^"]*)"', s):
                assert f in ('none','currentColor'), f
            for w in re.findall(r'stroke-width="([^"]*)"', s):
                assert w in ('2','1'), w
    # composite sheet
    parts=[]; y=0
    def emb(s,x,y,w,h):
        return s.replace('<svg ', f'<svg x="{x}" y="{y}" width="{w}" height="{h}" ',1)
    if it['figure']:
        parts.append(emb(it['figure'],0,0,500,200)); y=210
    for k,o in enumerate(it['options']):
        x=k*125
        if o.startswith('<svg'): parts.append(emb(o,x,y,115,115))
        else: parts.append(f'<text x="{x+50}" y="{y+60}" font-size="24">{o}</text>')
        mark = '*' if k==it['answer'] else ''
        parts.append(f'<text x="{x+5}" y="{y+135}" font-size="16">{"ABCD"[k]}{mark}</text>')
    full=f'<svg xmlns="http://www.w3.org/2000/svg" width="510" height="{y+145}" style="color:#222;background:#fff"><rect width="100%" height="100%" fill="#fff"/>'+''.join(parts)+'</svg>'
    full=full.replace('var(--fig-a)','#e6ecf5').replace('var(--fig-b)','#9fb3cf').replace('currentColor','#222')
    open(f'render/{it["id"]}.svg','w').write(full)
    subprocess.run(['rsvg-convert','-o',f'render/{it["id"]}.png',f'render/{it["id"]}.svg'],check=True)
print("OK")
