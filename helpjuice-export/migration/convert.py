"""HTML (Froala/Helpjuice) -> MDX converter using only the stdlib."""
import re, html, urllib.parse
from html.parser import HTMLParser

VOID = {'img','br','hr','input','meta','link','source','wbr'}
BLOCK = {'p','div','ul','ol','table','pre','h1','h2','h3','h4','h5','h6','hr','blockquote','article','section','figure','header','footer','nav','tbody','thead','tr','td','th','li','iframe','center'}

class Node:
    __slots__=('tag','attrs','children','parent')
    def __init__(self, tag, attrs=None, parent=None):
        self.tag=tag; self.attrs=dict(attrs or {}); self.children=[]; self.parent=parent
    def cls(self): return self.attrs.get('class','') or ''
    def text(self):
        return ''.join(c if isinstance(c,str) else c.text() for c in self.children)

class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root=Node('root'); self.cur=self.root
    def handle_starttag(self, tag, attrs):
        n=Node(tag, attrs, self.cur); self.cur.children.append(n)
        if tag not in VOID: self.cur=n
    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))
    def handle_endtag(self, tag):
        n=self.cur
        while n is not self.root and n.tag!=tag: n=n.parent
        if n is not self.root: self.cur=n.parent
    def handle_data(self, data):
        self.cur.children.append(data)

def parse(h):
    tb=TreeBuilder(); tb.feed(h); tb.close(); return tb.root

def esc(t):
    """Escape text for MDX."""
    t = t.replace('\\', '\\\\')
    t = t.replace('{','\\{').replace('}','\\}')
    t = t.replace('<','&lt;').replace('>','&gt;')
    t = t.replace('*','\\*').replace('`','\\`').replace('[','\\[').replace(']','\\]')
    t = re.sub(r'(?<![\w])_|_(?![\w])', r'\\_', t)
    t = t.replace('~~','\\~\\~')
    return t

def px(style, key='width'):
    m = re.search(key+r'\s*:\s*(\d+(?:\.\d+)?)\s*px', style or '')
    return float(m.group(1)) if m else None

class Converter:
    def __init__(self, media, resolve_link, page_id=None):
        self.media=media            # url -> local path ('/images/..') or None if dead
        self.resolve_link=resolve_link  # href -> new href
        self.missing_images=[]
        self.notes=[]
        self.page_id=page_id

    # ---------- inline ----------
    def inline(self, nodes, in_table=False):
        out=[]
        for n in nodes:
            if isinstance(n,str):
                t = n.replace('\xa0',' ').replace('\r\n','\n').replace('\r','\n')
                t = re.sub(r'[ \t]*\n[ \t]*', ' ', t)
                t = re.sub(r'[ \t]{2,}', ' ', t)
                out.append(esc(t)); continue
            tag=n.tag
            if tag=='br':
                out.append('<br />' if in_table else '\n'); continue
            if tag=='img':
                out.append(self.image(n, in_table)); continue
            if tag=='iframe':
                out.append(self.iframe(n)); continue
            if tag in ('script','style','button','svg','input','select','textarea','noscript'): continue
            if tag in ('strong','b'):
                out.append(self.wrap(n, '**', in_table)); continue
            if tag in ('em','i'):
                out.append(self.wrap(n, '_', in_table)); continue
            if tag in ('s','strike','del'):
                out.append(self.wrap(n, '~~', in_table)); continue
            if tag=='u':
                inner=self.inline(n.children, in_table)
                out.append(f'<u>{inner}</u>' if inner.strip() and '\n\n' not in inner else inner); continue
            if tag=='code':
                t = n.text().replace('\xa0',' ')
                out.append('`'+t.replace('`','')+'`' if t.strip() else ''); continue
            if tag=='a':
                out.append(self.link(n, in_table)); continue
            if tag in BLOCK:
                # block inside inline context (e.g. p inside li/td): render as block and mark paragraph break
                if in_table:
                    out.append(self.inline(n.children, in_table)+'<br />'); continue
                out.append('\n\n'+self.block(n)+'\n\n'); continue
            out.append(self.inline(n.children, in_table))
        return ''.join(out)

    def wrap(self, n, mark, in_table):
        inner=self.inline(n.children, in_table)
        if not inner.strip() or '\n\n' in inner: return inner
        lead = inner[:len(inner)-len(inner.lstrip())]
        trail = inner[len(inner.rstrip()):]
        core = inner.strip()
        # avoid doubling the same marker
        if core.startswith(mark) and core.endswith(mark) and len(core)>2*len(mark): return inner
        return f'{lead}{mark}{core}{mark}{trail}'

    def link(self, n, in_table):
        href = (n.attrs.get('href') or '').strip()
        inner = self.inline(n.children, in_table)
        if not href or href in ('#',) : return inner
        new = self.resolve_link(href)
        if new is None or '\n\n' in inner:
            return inner
        text = inner.strip() or new
        lead = inner[:len(inner)-len(inner.lstrip())]; trail = inner[len(inner.rstrip()):]
        return f'{lead}[{text}]({new}){trail}'

    def image(self, n, in_table=False):
        src = html.unescape(n.attrs.get('src') or '').strip()
        if not src: return ''
        local = self.media.get(src)
        if local is None:
            self.missing_images.append(src); return ''
        name = n.attrs.get('data-name') or src.split('/')[-1].split('?')[0]
        name = urllib.parse.unquote(html.unescape(name)).replace('+',' ')
        name = re.sub(r'^\d{13}-','', name)
        alt = (n.attrs.get('alt') or '').strip() or re.sub(r'\.[a-zA-Z0-9]+$','', name).replace('_',' ').replace('-',' ').strip()
        alt = re.sub(r'\s+',' ',alt)
        alt = alt.replace('"','').replace('{','').replace('}','').replace('[','').replace(']','')
        style = n.attrs.get('style','')
        w = px(style)
        if (w is not None and w<=64) or in_table:
            wa = f' width="{int(w)}"' if w else ''
            return f'<img src="{local}" alt="{alt}"{wa} />'
        return f'\n\n<img src="{local}" alt="{alt}" />\n\n'

    def iframe(self, n):
        src = html.unescape(n.attrs.get('src') or '').strip()
        if not src: return ''
        if src.startswith('//'): src='https:'+src
        m = re.search(r'youtube\.com/embed/([\w-]+)', src)
        if m: src = f'https://www.youtube.com/embed/{m.group(1)}'
        m = re.search(r'player\.vimeo\.com/video/(\d+)', src)
        if m: src = f'https://player.vimeo.com/video/{m.group(1)}'
        return (f'\n\n<iframe src="{src}" width="100%" height="400" frameBorder="0" '
                f'allow="autoplay; fullscreen; picture-in-picture" allowFullScreen></iframe>\n\n')

    # ---------- block ----------
    def block(self, node):
        """Render children of a container node as blocks; returns markdown."""
        parts=[]; run=[]
        def flush():
            if run:
                s=self.inline(run)
                s=self.clean_para(s)
                if s: parts.append(s)
                run.clear()
        for c in node.children:
            if isinstance(c,str) or c.tag not in BLOCK:
                run.append(c); continue
            flush()
            r=self.render_block(c)
            if r: parts.append(r)
        flush()
        return '\n\n'.join(p for p in parts if p)

    def clean_para(self, s):
        s = re.sub(r'[ \t]+\n', '\n', s)
        s = re.sub(r'\n{3,}', '\n\n', s)
        s = s.strip()
        # single newlines inside a paragraph (from <br>) become hard breaks
        s = '\n\n'.join(re.sub(r'\n', '  \n', p) for p in s.split('\n\n'))
        # leading '#' or '>' or '-' would become markdown syntax
        s = re.sub(r'(^|\n)([#>+\-]|\d+\.)(\s)', r'\1\\\2\3', s)
        return s

    def render_block(self, n):
        tag=n.tag
        if tag in ('h1','h2','h3','h4','h5','h6'):
            t=self.inline(n.children).strip().replace('\n',' ')
            t=re.sub(r'\s+',' ',t)
            if not t: return ''
            level={'h1':2,'h2':2,'h3':3,'h4':4,'h5':4,'h6':4}[tag]
            return '#'*level+' '+t
        if tag=='p' or tag=='center':
            return self.clean_para(self.inline(n.children))
        if tag=='hr': return '---'
        if tag=='pre':
            t=n.text().replace('\xa0',' ').replace('\r\n','\n').replace('\r','\n').strip('\n')
            lang='json' if t.lstrip().startswith(('{','[')) else 'text'
            return f'```{lang}\n{t}\n```'
        if tag in ('ul','ol'): return self.list(n, '')
        if tag=='table': return self.table(n)
        if tag=='iframe': return self.iframe(n).strip()
        if tag=='li': return self.list_item(n, '', '-')
        if tag in ('tbody','thead','tr','td','th'):
            return self.block(n)
        if tag=='blockquote':
            inner=self.block(n)
            return '\n'.join('> '+l for l in inner.split('\n'))
        if tag=='div':
            c=n.cls()
            if 'helpjuice-callout-delete' in c: return ''
            inner=self.block(n)
            if not inner.strip(): return ''
            if any(k in c for k in ('callout','alert','note','hj-info','warning')) and 'callout-body' not in c and not inner.startswith(('<Note>','<Warning>')):
                comp='Warning' if ('warning' in c or 'danger' in c) else 'Note'
                return f'<{comp}>\n{inner}\n</{comp}>'
            return inner
        # generic container
        return self.block(n)

    def list(self, n, indent=''):
        items=[]
        ordered = n.tag=='ol'
        i=0
        for c in n.children:
            if isinstance(c,str):
                if c.strip(): items.append(indent + '- ' + esc(c.strip()))
                continue
            if c.tag=='li':
                i+=1
                items.append(self.list_item(c, indent, f'{i}.' if ordered else '-'))
            elif c.tag in ('ul','ol'):
                items.append(self.list(c, indent+'  '))
            else:
                s=self.inline([c]).strip()
                if s: items.append(indent + '- ' + s)
        return '\n'.join(x for x in items if x)

    def list_item(self, li, indent, marker):
        cont=indent+' '*(len(marker)+1)
        run=[]; sub=[]
        for c in li.children:
            if not isinstance(c,str) and c.tag in ('ul','ol'):
                sub.append(self.list(c, cont))
            else:
                run.append(c)
        s=self.inline(run)
        s=re.sub(r'\n{2,}','\n',s).strip()
        s=re.sub(r'[ \t]+\n','\n',s)
        lines=s.split('\n')
        first=lines[0] if lines else ''
        rest=[cont+l for l in lines[1:] if l.strip()]
        out=[f'{indent}{marker} {first}'.rstrip()] + rest
        # images inside list items were emitted as block img lines; keep them indented
        out += sub
        return '\n'.join(out)

    def table(self, n):
        rows=[]
        def walk(x):
            for c in x.children:
                if isinstance(c,str): continue
                if c.tag=='tr': rows.append(c)
                elif c.tag in ('tbody','thead','tfoot'): walk(c)
        walk(n)
        if not rows: return ''
        grid=[]
        for r in rows:
            cells=[]
            for c in r.children:
                if isinstance(c,str) or c.tag not in ('td','th'): continue
                s=self.inline(c.children, in_table=True)
                s=re.sub(r'\s*<br />\s*(<br />\s*)+','<br />',s).strip()
                s=re.sub(r'^(<br />)+|(<br />)+$','',s).strip()
                s=s.replace('|','\\|').replace('\n',' ')
                cells.append(s)
            if cells: grid.append(cells)
        if not grid: return ''
        w=max(len(r) for r in grid)
        for r in grid: r += ['']*(w-len(r))
        head=grid[0]
        if all(not h.strip() for h in head): head=['']*w
        lines=['| '+' | '.join(h or ' ' for h in head)+' |', '|'+'---|'*w]
        for r in grid[1:]:
            lines.append('| '+' | '.join(c or ' ' for c in r)+' |')
        return '\n'.join(lines)

    def convert(self, h):
        h = h.replace('\r\n','\n')
        root=parse(h)
        md=self.block(root)
        md=re.sub(r'\n{3,}','\n\n',md).strip()+'\n'
        return md
