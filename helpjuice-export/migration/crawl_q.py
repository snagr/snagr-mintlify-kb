import csv, sys, re, json, os, time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
csv.field_size_limit(sys.maxsize)
S = os.path.dirname(os.path.abspath(__file__))
EXP = '/Users/Shared/Github/snagr-mintlify-kb/helpjuice-export'
def load(f):
    with open(os.path.join(EXP,f), newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))
qs = [q for q in load('snagr-questions-2026-09-22.csv') if q['is_published']=='true']
def fetch(url, cache):
    if os.path.exists(cache): return open(cache, encoding='utf-8').read()
    err=None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=40) as r:
                html = f'<!--EFFECTIVE:{r.geturl()}-->\n' + r.read().decode('utf-8','replace')
            open(cache,'w',encoding='utf-8').write(html); return html
        except Exception as e:
            err=e; time.sleep(2*(attempt+1))
    print("FAIL", url, err); return ''
def one(q):
    html = fetch(f"https://snagr.helpjuice.com/_questions/{q['id']}", f"{S}/crawl/q/{q['id']}.html")
    eff = re.match(r'<!--EFFECTIVE:(.*?)-->', html); eff = eff.group(1) if eff else ''
    cid = re.search(r'name="category-id" content="(\d*)"', html)
    qid = re.search(r'name="question-id" content="(\d*)"', html)
    lang = re.search(r'name="current-language" content="([^"]*)"', html)
    return q['id'], {'cat': cid.group(1) if cid else None, 'qid': qid.group(1) if qid else None,
                     'lang': lang.group(1) if lang else None, 'url': eff, 'private': 'users/sign_in' in eff}
with ThreadPoolExecutor(6) as ex:
    res = dict(ex.map(one, qs))
json.dump(res, open(f"{S}/qmap.json",'w'), indent=1)
import collections
print("total", len(res), "with cat", sum(1 for v in res.values() if v['cat']), "private", sum(1 for v in res.values() if v['private']), "nocat-nonprivate", [k for k,v in res.items() if not v['cat'] and not v['private']][:20])
print("lang counts", collections.Counter(v['lang'] for v in res.values()))
