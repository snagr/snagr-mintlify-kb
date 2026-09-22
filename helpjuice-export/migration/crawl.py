import csv, sys, re, json, os, time, collections
import urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
csv.field_size_limit(sys.maxsize)
S = os.path.dirname(os.path.abspath(__file__))
EXP = '/Users/Shared/Github/snagr-mintlify-kb/helpjuice-export'
def load(f):
    with open(os.path.join(EXP,f), newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))
cats = load('snagr-categories-2026-09-22.csv')
qs = load('snagr-questions-2026-09-22.csv')
BASE='https://snagr.helpjuice.com'
def fetch(url, cache):
    if os.path.exists(cache):
        return open(cache, encoding='utf-8').read()
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=40) as r:
                html = r.read().decode('utf-8','replace')
                html = f'<!--EFFECTIVE:{r.geturl()}-->\n' + html
            open(cache,'w',encoding='utf-8').write(html); return html
        except Exception as e:
            err = e; time.sleep(2*(attempt+1))
    print("FAIL", url, err); return ''
def crawl_cat(c):
    return c['id'], fetch(f"{BASE}/{c['id']}", f"{S}/crawl/cats/{c['id']}.html")
with ThreadPoolExecutor(6) as ex:
    pages = dict(ex.map(crawl_cat, cats))
link_re = re.compile(r'href="/(\d+)-([^/"?#]+)/([^/"?#]+)"')
# category -> ordered list of codenames (from the category's own page, own-id links only)
cat_q = collections.OrderedDict()
cat_lang = {}
cat_slug = {}
for c in cats:
    html = pages[c['id']]
    m = re.match(r'<!--EFFECTIVE:(.*?)-->', html)
    eff = m.group(1) if m else ''
    lm = re.search(r'helpjuice\.com/([a-z]{1,2}_[A-Z]{2})/', eff)
    cat_lang[c['id']] = lm.group(1) if lm else 'en_US'
    seen=[]
    for cid, cslug, code in link_re.findall(html):
        if cid == c['id']:
            cat_slug[cid]=cslug
            if code not in seen: seen.append(code)
    cat_q[c['id']] = seen
    if 'pagination' in html.lower() or 'page=2' in html:
        print("PAGINATION?", c['id'], c['name'])
print("categories with questions:", sum(1 for v in cat_q.values() if v), "total links:", sum(len(v) for v in cat_q.values()))
# resolve codename -> question id
bycode = collections.defaultdict(list)
for q in qs: bycode[q['codename']].append(q)
mapping = {}  # qid -> (catid, order)
ambiguous = []
missing = []
for cid, codes in cat_q.items():
    for i, code in enumerate(codes):
        cands = bycode.get(code, [])
        if len(cands)==1:
            mapping[cands[0]['id']] = (cid, i)
        elif len(cands)==0:
            missing.append((cid, code))
        else:
            ambiguous.append((cid, i, code))
print("mapped:", len(mapping), "ambiguous:", len(ambiguous), "missing:", len(missing))
def resolve(item):
    cid, i, code = item
    html = fetch(f"{BASE}/{cid}-{cat_slug[cid]}/{code}", f"{S}/crawl/qs/{cid}_{code}.html")
    m = re.search(r'question-id" content="(\d+)"', html)
    return (cid, i, code, m.group(1) if m else None)
with ThreadPoolExecutor(6) as ex:
    for cid,i,code,qid in ex.map(resolve, ambiguous):
        if qid: mapping[qid]=(cid,i)
        else: print("UNRESOLVED", cid, code)
print("mapped after resolve:", len(mapping))
pub = [q for q in qs if q['is_published']=='true']
unmapped = [ (q['id'], q['codename'], q['name'], q['language_id']) for q in pub if q['id'] not in mapping]
print("published unmapped:", len(unmapped)); 
for u in unmapped[:40]: print("  ", u)
print("missing codes:", missing[:20])
json.dump({'mapping':mapping,'cat_lang':cat_lang,'cat_slug':cat_slug,'cat_q':cat_q}, open(f"{S}/mapping.json",'w'), indent=1, ensure_ascii=False)
