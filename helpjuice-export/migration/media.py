import csv, sys, re, json, os, time, html, hashlib, collections
import urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
csv.field_size_limit(sys.maxsize)
S = os.path.dirname(os.path.abspath(__file__))
EXP = '/Users/Shared/Github/snagr-mintlify-kb/helpjuice-export'
ROOT = '/Users/Shared/Github/snagr-mintlify-kb'
def load(f):
    with open(os.path.join(EXP,f), newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))
qs = {q['id']:q for q in load('snagr-questions-2026-09-22.csv')}
ans = [a for a in load('snagr-answers-2026-09-22.csv') if qs[a['question_id']]['is_published']=='true']
urls = collections.OrderedDict()
for a in ans:
    b = a['body']
    for m in re.finditer(r'<(img|iframe|a|source|video)\b[^>]*?(?:src|href)="([^"]+)"', b):
        u = html.unescape(m.group(2)).strip()
        urls.setdefault(u, set()).add(a['question_id'])
def safe(name):
    name = urllib.parse.unquote(name).replace('+',' ')
    name = re.sub(r'[^\w.\-]+', '-', name).strip('-')
    name = re.sub(r'-+', '-', name)
    return name[:120]
def classify(u):
    if u.startswith('data:'): return 'data', None
    m = re.match(r'https?://static\.helpjuice\.com/helpjuice_production/uploads/upload/image/3577/(\d+)/(.+)$', u)
    if m: return 'helpjuice', f"images/{m.group(1)}/{safe(m.group(2))}"
    m = re.match(r'https?://s3\.amazonaws\.com/helpjuice-static/helpjuice_production(?:%2F|/)uploads(?:%2F|/)upload(?:%2F|/)image(?:%2F|/)3577(?:%2F|/)direct(?:%2F|/)(.+)$', u)
    if m: return 'helpjuice-direct', f"images/direct/{safe(m.group(1))}"
    if 'static.helpjuice.com' in u or 'helpjuice-static' in u:
        return 'helpjuice-other', f"images/other/{safe(u.split('/')[-1] or hashlib.md5(u.encode()).hexdigest())}"
    if 'firebasestorage.googleapis.com' in u:
        p = urllib.parse.unquote(urllib.parse.urlparse(u).path).split('/')[-1]
        return 'guidde', f"images/guidde/{safe(p)}"
    if 'player.vimeo.com' in u or 'youtube.com' in u or 'youtu.be' in u: return 'video', None
    if 'support.snagr.co.uk' in u or u.startswith('/download/'): return 'dead-confluence', None
    if re.match(r'https?://', u) or u.startswith('mailto:') or u.startswith('/') or u.startswith('#'): return 'link', None
    return 'unknown', None
items = []
for u, qids in urls.items():
    kind, local = classify(u)
    items.append({'url':u, 'kind':kind, 'local':local, 'questions':sorted(qids)})
print(collections.Counter(i['kind'] for i in items))
print("unknown:", [i['url'][:120] for i in items if i['kind']=='unknown'][:10])
print("helpjuice-other:", [i['url'][:160] for i in items if i['kind']=='helpjuice-other'][:10])
# collision check on local paths
loc = collections.Counter(i['local'] for i in items if i['local'])
dups = [l for l,c in loc.items() if c>1]
print("local collisions:", len(dups), dups[:5])
for d in dups:
    n=0
    for i in items:
        if i['local']==d:
            n+=1
            if n>1:
                b,e = os.path.splitext(d); i['local']=f"{b}-{n}{e}"
def dl(i):
    if not i['local']: return i
    dest = os.path.join(ROOT, i['local'])
    if os.path.exists(dest) and os.path.getsize(dest)>0:
        i['status']='ok'; return i
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    u = i['url']
    if u.startswith('http://'): u = 'https://' + u[7:]
    err=None
    for attempt in range(4):
        try:
            req = urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read(); ct = r.headers.get('Content-Type','')
            if not data: raise Exception("empty")
            open(dest,'wb').write(data); i['status']='ok'; i['ct']=ct; i['bytes']=len(data); return i
        except urllib.error.HTTPError as e:
            err=e
            if e.code in (403,404,410): break
            time.sleep(2*(attempt+1))
        except Exception as e:
            err=e; time.sleep(2*(attempt+1))
    i['status']=f'fail: {err}'; return i
with ThreadPoolExecutor(8) as ex:
    items = list(ex.map(dl, items))
json.dump(items, open(f"{S}/media_map.json",'w'), indent=1)
print("download status:", collections.Counter((i['kind'], i.get('status','-')) for i in items))
print("failures:", [(i['url'][:120], i['status']) for i in items if i.get('status','ok')!='ok' and i['local']][:30])
