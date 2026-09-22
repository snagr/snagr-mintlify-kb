import csv, sys, re, json, os, html, collections, unicodedata, urllib.parse, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from convert import Converter
csv.field_size_limit(sys.maxsize)
S = os.path.dirname(os.path.abspath(__file__))
ROOT = '/Users/Shared/Github/snagr-mintlify-kb'
EXP = f'{ROOT}/helpjuice-export'
def load(f):
    with open(os.path.join(EXP,f), newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))
cats = load('snagr-categories-2026-09-22.csv')
qs_all = load('snagr-questions-2026-09-22.csv')
ans = {a['question_id']: a['body'] for a in load('snagr-answers-2026-09-22.csv')}
qmap = json.load(open(f'{S}/qmap.json'))
mapping = json.load(open(f'{S}/mapping.json'))
media_items = json.load(open(f'{S}/media_map.json'))
media = {}
for i in media_items:
    if i.get('status')=='ok': media[i['url']] = '/'+i['local']
    elif i['kind'] in ('dead-confluence','helpjuice-other','helpjuice','helpjuice-direct','guidde','unknown'): media[i['url']] = None

LANG = {'en_US':'en','nl_NL':'nl','de_DE':'de','it_IT':'it','t_CN':'zh-Hant','cn_CN':'cn'}
LANGID = {'1':'en_US','7':'nl_NL','15':'t_CN','4':'de_DE','6':'it_IT','13':'cn_CN'}
LANGDIR = {'en':'en','nl':'nl','de':'de','it':'it','zh-Hant':'zh-hant','cn':'cn'}

# ---------- manual placements for articles not visible on the public site ----------
MANUAL_CAT = {
 '378714':'56448','377203':'56987','389566':'56987','389567':'56987','389568':'56987','389569':'56987','389571':'56987',
 '389572':'56987','389573':'56987','389574':'56987','389575':'56987','389576':'56987','391374':'56448',
 '394794':'56990','484402':'56990','394803':'56989','484404':'56989','484403':'56987',
 '400392':'59639','400393':'59639','400394':'59639','400395':'59639','400396':'59639',
 '448362':'71627','448363':'71627','448364':'71628','530656':'90581','530664':'90581','530667':'90581',
 '266210':'37464','305040':'44032',
}
PRIVATE_ROOTS = {'56448','59206','71626'}   # AAHK-TRD, AAHK-CWD, Power BI Integration (login-only on Helpjuice)

CJK_SLUG = {
 '入門指南':'getting-started','你的角色是什麼？':'what-is-your-role','簡介':'introduction','初階指引：如何提交表格？':'starter-guide-how-to-submit-forms',
 '如何傳出表格到PDF格式？':'export-forms-to-pdf','如何在手提裝置上填寫表格？':'complete-forms-on-device','如何在網站上填寫表格？':'complete-forms-on-website',
 '我如何從手機應用程式下載項目？':'download-project-on-app','我如何從目前的圖紙前往另一張圖紙？':'go-from-one-drawing-to-another','我如何把文件鏈接到表格？':'link-documents-to-forms',
 '我如何把缺陷鏈接到表格？':'link-issues-to-forms','我如何搜尋表格？':'search-forms','我如何追蹤表格的變化？':'track-form-changes','初階指引：如何記錄缺陷？':'starter-guide-how-to-take-issues',
 '報告':'reporting','PDF報告':'pdf-report','分析表':'analytics','訂製PDF報告':'custom-pdf-report',
 '常見問題':'faq','一般問題':'general','位置':'locations','使用移動應用程式前的準備':'get-ready-on-mobile','疑難排解 - 移動應用程式 (APP)':'troubleshooting-on-mobile','疑難排解 - 管理員 (Admin)':'troubleshooting-for-admins',
 '成功經驗':'success-stories','地盤工序':'site-operations','安全管理':'safety','質量':'quality',
 '新功能 🆙':'new-features','其他':'others','文件存儲庫（升級）':'document-repository-upgrade','雙重身份驗證 (2FA)':'2fa',
 '缺陷模式':'issues','報告和分析':'report-and-analytics','更新缺陷':'update-issues','查找缺陷':'find-issues','添加缺陷':'add-issues','編輯缺陷':'edit-issues',
 '表格/檢查模式':'forms','導出表格':'export-forms','提交表格':'submit-forms','搜索、編輯表格':'find-and-edit-forms','鏈接缺陷和文件到表格':'link-issues-and-documents-to-forms',
 '項目文件存儲庫':'documents','上載文件':'upload-documents','下載文檔':'download-documents','管理文件':'manage-documents',
 '項目設置':'set-up-project','一般設定':'general-settings','位置 - 項目管理區域':'locations-project-level','圖紙 - 項目管理區域':'drawings-project-level',
 '工程項目檢查清單及進度':'checklists-and-scheduling-company-level','帳戶及權限 - 公司管理區域':'accounts-and-permissions-company-level','帳戶及權限設定 - 項目管理區域':'accounts-and-permissions-project-level',
 '缺陷列表 - 公司管理區域':'standard-issue-list-company-level','缺陷列表 - 項目管理區域':'standard-issue-list-project-level','表格 - 公司管理區域':'forms-company-level','許可證 - 公司管理區域':'permits-company-level','通知 - 項目管理區域':'notifications-project-level',
 '入门指南':'getting-started','必备技能':'essential-skills','手机设置常见问题':'mobile-setup-faq','简介':'introduction','设置手机':'set-up-mobile',
 '成功经验':'success-stories','项目验收':'project-handover','文件管理':'documents','上传文档':'upload-documents','下载文档':'download-documents','管理文档':'manage-documents',
 '管理员模式':'admin','图纸':'drawings','帐户及权限设定':'accounts-and-permissions','设定缺陷列表':'standard-issue-list','设定表格模板':'form-templates','通知':'notifications',
 '报告和分析':'report-and-analytics','更新缺陷':'update-issues','查找缺陷':'find-issues','添加缺陷':'add-issues','编辑缺陷':'edit-issues',
 '表格模式':'forms','完成或编辑表格':'complete-or-edit-forms','导出表格':'export-forms','搜索表格':'search-forms','链接缺陷和文件到表格':'link-issues-and-documents-to-forms',
}

def norm_name(n):
    n = re.sub(r'\s+',' ', re.sub(r'[\x00-\x1f\x7f]',' ', n)).strip()
    return re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', n)
def slugify(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace('ß','ss').replace('&',' and ')
    s = re.sub(r'[^A-Za-z0-9]+','-', s).strip('-').lower()
    s = re.sub(r'-+','-', s)
    return s
def has_cjk(s): return any('一'<=ch<='鿿' for ch in s)

# ---------- categories ----------
byid = {c['id']:c for c in cats}
children = collections.defaultdict(list)
for c in cats: children[c['parent_id']].append(c)
def root_of(cid):
    while byid[cid]['parent_id']: cid = byid[cid]['parent_id']
    return cid
def path_of(cid):
    p=[]
    while cid: p.append(cid); cid = byid[cid]['parent_id']
    return list(reversed(p))

# ---------- questions ----------
pub = [q for q in qs_all if q['is_published']=='true']
pages = {}   # qid -> dict
report = {'private_placed':[], 'unresolved_links':collections.Counter(), 'missing_images':{}, 'unpublished':[], 'nocat':[], 'dup_slugs':[], 'empty':[]}
for q in qs_all:
    if q['is_published']!='true': report['unpublished'].append((q['id'], norm_name(q['name'])))
for q in pub:
    info = qmap.get(q['id'], {})
    cid = info.get('cat') or MANUAL_CAT.get(q['id'])
    if not cid:
        report['nocat'].append((q['id'], norm_name(q['name']))); continue
    lang = info.get('lang') or LANGID[q['language_id']]
    if info.get('private') or q['id'] in MANUAL_CAT:
        report['private_placed'].append((q['id'], norm_name(q['name']), ' > '.join(norm_name(byid[x]['name']) for x in path_of(cid))))
    pages[q['id']] = {'q':q, 'cat':cid, 'lang':LANG[lang], 'title':norm_name(q['name']), 'order':None}
    if q['id'] in mapping['mapping'] and mapping['mapping'][q['id']][0]==cid:
        pages[q['id']]['order'] = mapping['mapping'][q['id']][1]

# language of each category = language of its pages (fallback: root name heuristics)
cat_lang = {}
for p in pages.values():
    for c in path_of(p['cat']): cat_lang.setdefault(c, p['lang'])

# ---------- category slugs and page paths ----------
cat_slug = {}
for c in cats:
    name = norm_name(c['name'])
    if has_cjk(name):
        key = name.replace(' ',''); s = CJK_SLUG.get(name) or CJK_SLUG.get(key) or CJK_SLUG.get(key.rstrip('？?')) or f'c{c["id"]}'
        if s.startswith('c') and s[1:].isdigit(): print("NO CJK SLUG:", name)
    else:
        s = slugify(name) or f'c{c["id"]}'
    cat_slug[c['id']] = s
# dedupe sibling slugs
for pid, sibs in children.items():
    seen=collections.Counter()
    for c in sibs:
        key=(cat_lang.get(c['id']), cat_slug[c['id']])
        seen[key]+=1
        if seen[key]>1: cat_slug[c['id']] += f"-{seen[key]}"
def cat_dir(cid, lang):
    return '/'.join([LANGDIR[lang]] + [cat_slug[x] for x in path_of(cid)])

def page_slug(p):
    q=p['q']; code = urllib.parse.unquote(q['codename']).strip().lower()
    code = re.sub(r'[^a-z0-9]+','-', code).strip('-')
    m = re.match(r'^(\d+)-(.*)$', code)
    if m:
        rest = m.group(2)
        code = rest if rest and not rest.startswith('untitled') else ''
    if code.isdigit(): code=''
    if p['lang']=='nl' and code.startswith('nl-'): code = code[3:]
    if not code:
        t = slugify(p['title'])
        code = t if (t and not has_cjk(p['title'])) else q['id']
    code = re.sub(r'-+','-', code).strip('-')
    return code[:110].rstrip('-')

used_paths = collections.Counter()
for qid, p in sorted(pages.items(), key=lambda kv: (kv[1]['order'] is None, kv[1]['order'] or 0, kv[1]['q']['created_at'])):
    d = cat_dir(p['cat'], p['lang'])
    s = page_slug(p)
    path = f'{d}/{s}'
    used_paths[path]+=1
    if used_paths[path]>1:
        report['dup_slugs'].append((qid, p['title'], path))
        path = f'{path}-{used_paths[path]}'
    p['path'] = path

# ---------- link resolution ----------
by_code = collections.defaultdict(list)
for qid,p in pages.items(): by_code[p['q']['codename'].lower()].append(qid)
by_code_dec = collections.defaultdict(list)
for qid,p in pages.items(): by_code_dec[urllib.parse.unquote(p['q']['codename']).lower().rstrip('?')].append(qid)
by_slug = collections.defaultdict(list)
for qid,p in pages.items(): by_slug[p['path'].rsplit('/',1)[1]].append(qid)
LINKCACHE = json.load(open(f'{S}/linkcache.json')) if os.path.exists(f'{S}/linkcache.json') else {}
LANGPREFIX = re.compile(r'^/(en_US|nl_NL|de_DE|it_IT|t_CN|cn_CN)(/|$)')
def first_page_of_cat(cid):
    ordered = sorted([p for p in pages.values() if p['cat']==cid], key=lambda p:(p['order'] is None, p['order'] or 0, p['q']['created_at']))
    if ordered: return ordered[0]['path']
    for ch in children.get(cid, []):
        r = first_page_of_cat(ch['id'])
        if r: return r
    return None
def make_resolver(cur):
    def pick(cands, langhint):
        if not cands: return None
        same = [c for c in cands if pages[c]['lang']==langhint] if langhint else []
        return same[0] if same else (cands[0] if len(cands)==1 or not langhint else cands[0])
    def resolve(href):
        h = html.unescape(href).strip()
        if not h or h.startswith(('mailto:','#','tel:')): return h
        if h.startswith('snagr.helpjuice.com'): h = 'https://' + h
        u = urllib.parse.urlparse(h)
        langhint = cur['lang']
        qsd = urllib.parse.parse_qs(u.query)
        if 'kb_language' in qsd: langhint = LANG.get(qsd['kb_language'][0], langhint)
        if u.netloc and 'snagr.helpjuice.com' not in u.netloc: return h
        if not u.netloc and not h.startswith('/'):
            # relative junk like 'locaties-projectniveau/hoe-...' or plain text
            if re.match(r'^[a-z0-9-]+/[a-z0-9-]+$', h): path='/'+h
            else: report['unresolved_links'][h]+=1; return None
        else: path = u.path
        path = LANGPREFIX.sub('/', path).rstrip('/')
        path = urllib.parse.unquote(path).strip()
        path = re.sub(r'\s+','',path)
        qid=None; cid=None
        m = re.match(r'^/_questions/(\d+)$', path)
        if m: qid=m.group(1)
        m = re.match(r'^/_categories/(\d+)$', path)
        if m: cid=m.group(1)
        m = re.match(r'^/(\d+)$', path)
        if m: qid = m.group(1) if m.group(1) in pages else None; cid = m.group(1) if m.group(1) in byid and not qid else None
        m = re.match(r'^/(\d+)/(\d+)$', path)
        if m: qid = m.group(2)
        if not qid and not cid:
            m = re.match(r'^/(?:[^/]+/)?(\d+)-([^/]*)$', path)
            if m and m.group(1) in pages: qid=m.group(1)
        if not qid and not cid:
            m = re.match(r'^/(?:[^/]+/)?([^/]+)$', path)
            if m:
                code = m.group(1).lower()
                cands = by_code.get(code) or by_code_dec.get(code.rstrip('?')) or by_code.get('nl-'+code)
                if not cands:
                    m2 = re.match(r'^(\d+)-', code)
                    if m2 and m2.group(1) in pages: cands=[m2.group(1)]
                if not cands and code in by_slug:
                    cands = by_slug[code]
                if not cands:
                    m3 = re.match(r'^(\d+)$', code)
                    if m3 and m3.group(1) in byid: cid=m3.group(1)
                qid = pick(cands, langhint) if cands else None
        if (not qid or qid not in pages) and h in LINKCACHE:
            lc = LINKCACHE[h]
            if lc.get('qid') in pages: qid = lc['qid']
            elif lc.get('cid') in byid: cid = lc['cid']
        if qid and qid in pages: return '/'+pages[qid]['path']
        if cid and cid in byid:
            fp = first_page_of_cat(cid)
            if fp: return '/'+fp
        report['unresolved_links'][h]+=1
        return None   # dead internal link: converter keeps the text only
    return resolve

# ---------- write pages ----------
# wipe previously generated language dirs
for d in set(LANGDIR.values()):
    if os.path.isdir(f'{ROOT}/{d}'): shutil.rmtree(f'{ROOT}/{d}')
def yaml_str(s): return json.dumps(s, ensure_ascii=False)
for qid, p in pages.items():
    conv = Converter(media, make_resolver(p), qid)
    body = ans.get(qid,'') or ''
    md = conv.convert(body) if body.strip() else ''
    if not md.strip(): report['empty'].append((qid, p['title'], p['path']))
    fm = ['---', f'title: {yaml_str(p["title"])}']
    desc = norm_name(p['q']['description'])
    if desc: fm.append(f'description: {yaml_str(desc)}')
    fm.append('---')
    out = '\n'.join(fm) + '\n\n'
    if conv.missing_images:
        n = len(conv.missing_images)
        report['missing_images'][p['path']] = conv.missing_images
        out += f'{{/* TODO: {n} image(s) from the retired support.snagr.co.uk site could not be retrieved and were removed. */}}\n\n'
    out += md if md.strip() else '{/* TODO: this article had no content in the Helpjuice export. */}\n'
    fp = f'{ROOT}/{p["path"]}.mdx'
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp,'w',encoding='utf-8').write(out)

# ---------- navigation ----------
def anchors_in_order(htmlfile):
    if not os.path.exists(htmlfile): return []
    t = open(htmlfile, encoding='utf-8').read()
    out=[]
    for m in re.finditer(r'<a\b[^>]*href="(/[^"]*)"[^>]*>(.*?)</a>', t, re.S):
        txt = norm_name(html.unescape(re.sub(r'<[^>]+>','',m.group(2))))
        out.append((m.group(1), txt))
    return out
def order_children(pid, lang, htmlfile):
    sibs = [c for c in children.get(pid, []) if cat_lang.get(c['id'], lang if pid else None)==lang]
    anchors = anchors_in_order(htmlfile)
    pos = {}
    for i,(href,txt) in enumerate(anchors):
        for c in sibs:
            if c['id'] in pos: continue
            if href.startswith(f'/{c["id"]}-') or href==f'/{c["id"]}' or (txt and txt==norm_name(c['name'])):
                pos[c['id']]=i
    return sorted(sibs, key=lambda c:(c['id'] not in pos, pos.get(c['id'],0), norm_name(c['name'])))
ROOT_PRIORITY = ['getting-started','issues','forms','documents','set-up-project','reporting','faq','new-features','success-stories','snagr-home']
def root_key(c):
    s = cat_slug[c['id']]; kws = {'getting-started':['getting','start','cominciare','fangen','入門','入门'],'issues':['issue','actiepunt','aktionspunkt','difett','缺陷'],
        'forms':['form','ispezion','表格'],'documents':['document','dokument','文件'],'set-up-project':['set up','opzetten','einricht','impostazion','項目設置','管理员'],
        'reporting':['report','verslag','bericht','報告'],'faq':['faq','vragen','fragen','常見'],'new-features':['new feature','nieuwe','新功能'],'success-stories':['success','succes','erfolg','casi','成功'],'snagr-home':['home']}
    n = norm_name(c['name']).lower()
    for i,k in enumerate(ROOT_PRIORITY):
        if any(w in n for w in kws[k]): return i
    return 99
curated_pages = []
def has_pages(cid):
    if any(p['cat']==cid for p in pages.values()): return True
    return any(has_pages(ch['id']) for ch in children.get(cid, []))
def curated_index(c, lang):
    cid=c['id']
    f=f'{S}/crawl/cats/{cid}.html'
    if not os.path.exists(f): return None
    t=open(f,encoding='utf-8').read()
    links=[]
    def descendants(x):
        out={x}
        for ch in children.get(x, []): out |= descendants(ch['id'])
        return out
    desc = descendants(cid)
    for m in re.finditer(r'<a\b[^>]*href="/(\d+)-[^"/]*/([^"/?#]+)"[^>]*>', t):
        if m.group(1) in desc: continue
        cands = by_code.get(m.group(2).lower()) or by_code_dec.get(urllib.parse.unquote(m.group(2)).lower())
        cands = [x for x in (cands or []) if pages[x]['lang']==lang and pages[x]['cat']==m.group(1)] or [x for x in (cands or []) if pages[x]['lang']==lang]
        if cands and cands[0] not in links: links.append(cands[0])
    if not links: return None
    d = cat_dir(cid, lang); path=f'{d}/index'
    body = f'---\ntitle: {yaml_str(norm_name(c["name"]))}\n---\n\n' + '\n'.join(f'- [{pages[x]["title"]}](/{pages[x]["path"]})' for x in links) + '\n'
    os.makedirs(f'{ROOT}/{d}', exist_ok=True); open(f'{ROOT}/{path}.mdx','w',encoding='utf-8').write(body)
    curated_pages.append((path, norm_name(c['name']), len(links)))
    return path
def nav_group(c, lang):
    cid=c['id']
    own = sorted([p for p in pages.values() if p['cat']==cid], key=lambda p:(p['order'] is None, p['order'] or 0, p['q']['created_at']))
    items = [p['path'] for p in own]
    if not own and not has_pages(cid):
        ci = curated_index(c, lang)
        if ci: items.append(ci)
    for ch in order_children(cid, lang, f'{S}/crawl/cats/{cid}.html'):
        g = nav_group(ch, lang)
        if g: items.append(g)
    if not items: return None
    return {'group': norm_name(c['name']), 'pages': items}

LANDING = {
 'en': ('SnagR Support','Guides and answers for the SnagR app and website.','Browse by topic'),
 'nl': ('SnagR Ondersteuning','Handleidingen en antwoorden voor de SnagR-app en -website.','Blader per onderwerp'),
 'de': ('SnagR Support','Anleitungen und Antworten für die SnagR-App und -Website.','Nach Thema durchsuchen'),
 'it': ('Supporto SnagR',"Guide e risposte per l'app e il sito web SnagR.",'Sfoglia per argomento'),
 'zh-Hant': ('SnagR 支援中心','SnagR 應用程式與網站的使用指南與常見問題解答。','依主題瀏覽'),
 'cn': ('SnagR 支持中心','SnagR 应用程序与网站的使用指南与常见问题解答。','按主题浏览'),
}
ICONS = {0:'rocket',1:'map-pin',2:'clipboard-check',3:'folder-open',4:'gear',5:'chart-column',6:'circle-question',7:'sparkles',8:'trophy',9:'house'}
languages=[]; private_nav=[]
lang_home = {'en':'home_en_US.html','nl':'home_nl_NL.html','de':'home_de_DE.html','it':'home_it_IT.html','zh-Hant':'home_t_CN.html','cn':'home_cn_CN.html'}
for lang in ['en','nl','de','it','zh-Hant','cn']:
    roots = [c for c in children[''] if cat_lang.get(c['id'])==lang]
    roots.sort(key=lambda c:(root_key(c), norm_name(c['name'])))
    groups=[]; cards=[]
    for c in roots:
        g = nav_group(c, lang)
        if not g: continue
        if c['id'] in PRIVATE_ROOTS:
            private_nav.append(g); continue
        groups.append(g)
        first = g['pages'][0]
        while isinstance(first, dict): first = first['pages'][0]
        cards.append((norm_name(c['name']), '/'+first, ICONS.get(root_key(c),'book')))
    title, desc, browse = LANDING[lang]
    d = LANGDIR[lang]
    landing = f'---\ntitle: {yaml_str(title)}\ndescription: {yaml_str(desc)}\n---\n\n## {browse}\n\n<Columns cols={{2}}>\n'
    for name, href, icon in cards:
        landing += f'  <Card title={yaml_str(name)} icon="{icon}" href="{href}" />\n'
    landing += '</Columns>\n'
    open(f'{ROOT}/{d}/index.mdx','w',encoding='utf-8').write(landing)
    languages.append({'language': lang, 'groups': [{'group': title, 'pages':[f'{d}/index']}] + groups})

docs = json.load(open(f'{ROOT}/docs.json'))
docs['name'] = 'SnagR Support'
docs['navigation'] = {'languages': languages}
json.dump(docs, open(f'{ROOT}/docs.json','w'), indent=2, ensure_ascii=False); open(f'{ROOT}/docs.json','a').write('\n')
json.dump(private_nav, open(f'{S}/private_nav.json','w'), indent=2, ensure_ascii=False)
report['curated_pages']=curated_pages
report['pages']={qid:{'path':p['path'],'title':p['title'],'lang':p['lang']} for qid,p in pages.items()}
json.dump({k:(v if not isinstance(v,collections.Counter) else dict(v)) for k,v in report.items()}, open(f'{S}/report.json','w'), indent=1, ensure_ascii=False)
print("pages written:", len(pages), "per lang:", collections.Counter(p['lang'] for p in pages.values()))
print("private placed:", len(report['private_placed']), "nocat:", report['nocat'], "dup slugs:", len(report['dup_slugs']), "empty:", len(report['empty']))
print("pages with missing images:", len(report['missing_images']), "total missing refs:", sum(len(v) for v in report['missing_images'].values()))
print("unresolved links:", sum(report['unresolved_links'].values()), list(report['unresolved_links'].items())[:15])
print("private nav groups:", [g['group'] for g in private_nav])
