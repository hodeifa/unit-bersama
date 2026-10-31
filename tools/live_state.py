import re, json, sys
p = sys.argv[1]
h = open(p, encoding='utf8').read()
m = re.search(r'<script type="application/json" id="state">(.*?)</script>', h, re.S)
s = json.loads(m.group(1))
def short(o):
    if isinstance(o, dict): return {k: short(v) for k, v in o.items()}
    if isinstance(o, list): return [short(v) for v in o]
    if isinstance(o, str) and len(o) > 80: return o[:40] + '...[%d chars]' % len(o)
    return o
print(json.dumps(short(s), ensure_ascii=False, indent=1)[:6000])
print('models', len(s['models']), 'members', len(s['members']), 'tiers', len(s['tiers']), 'brands', len(s['brands']))
