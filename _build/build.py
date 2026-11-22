#!/usr/bin/env python3
"""뉴런 반응 연구실 v2 빌드: src/*.html의 약식 태그를 펼치고, 공통 CSS·JS와 쓰인 캐릭터 그림만 넣어 단일 파일을 만든다."""
import json, re, sys, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
SPR = json.load(open(os.path.join(HERE, 'sprites.json')))
CSS = open(os.path.join(HERE, 'lab.css'), encoding='utf-8').read()
JS = open(os.path.join(HERE, 'lab.js'), encoding='utf-8').read()
WHO = {
 'doc': ('박사', 'j', '심판'), 'asst': ('조수(하루)', 'u', 'USER팀'), 'robo': ('주판봇', 'u', 'USER팀 주장'),
 'sia': ('인턴1 시아', 'u', 'USER팀'), 'moa': ('인턴2 모아', 'u', 'USER팀'),
 'fly': ('초파리 연구원', 'b', '초파리와 features팀 주장'), 'x1': ('X1', 'b', '초파리와 features팀'), 'x2': ('X2', 'b', '초파리와 features팀'), 'x3': ('X3', 'b', '초파리와 features팀'),
}
XOK = {'e01','e02','e03','e04','e09','e13','e15','e16','e24'}
SITE = 'https://adminmrobo.github.io/neuron_reaction/'

def face(who, e):
    e = e.lower()
    if who.startswith('x') and e not in XOK:
        e = {'e07':'e13','e08':'e13','e10':'e16','e12':'e01','e19':'e01','e20':'e15'}.get(e, 'e13')
    k = f'{who}_{e}'
    if k not in SPR: raise SystemExit('그림 없음: ' + k)
    return k

def say(who, e, body, cls=''):
    name, team, role = WHO[who]
    body = body.strip()
    if not body.startswith('<p'): body = '<p>' + body + '</p>'
    return (f'<div class="say {cls}" data-team="{team}"><img class="who" data-s="{face(who,e)}" alt="{name}" width="62" height="62">'
            f'<div><div class="name {who}">{name}<small class="{team}">{role}</small></div>{body}</div></div>')

def expand(s):
    s = re.sub(r'<jt t="([^"]*)">(.*?)</jt>', r'<span class="jt" data-t="\1">\2</span>', s, flags=re.S)
    s = re.sub(r'<say who="(\w+)" e="(\w+)"( r)?>(.*?)</say>', lambda m: say(m.group(1), m.group(2), m.group(4), 'r' if m.group(3) else ''), s, flags=re.S)
    def rnd(m):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1))); inner = m.group(2)
        cu = re.search(r'<cu who="(\w+)" e="(\w+)">(.*?)</cu>', inner, re.S)
        cb = re.search(r'<cb who="(\w+)" e="(\w+)">(.*?)</cb>', inner, re.S)
        vd = re.search(r'<verdict e="(\w+)">(.*?)</verdict>', inner, re.S)
        win = attrs['win']
        wtxt = {'u':'주판봇 USER팀 1점', 'b':'초파리와 features팀 1점', 'd':'무승부 · 두 팀 0.5점씩'}[win]
        def claim(c, team, tname):
            who, e, t = c.group(1), c.group(2), c.group(3).strip()
            return (f'<div class="{team}"><b>{tname} · {WHO[who][0]}</b>'
                    f'<div style="display:flex;gap:8px;align-items:flex-start"><img data-s="{face(who,e)}" alt="{WHO[who][0]}" width="46" height="46" style="flex:0 0 46px;border-radius:9px;background:#fff">'
                    f'<p>{t}</p></div></div>')
        return (f'<div class="round" data-win="{win}" id="{attrs.get("id","")}"><h4><span>라운드 {attrs["no"]}</span> · {attrs["title"]}</h4>'
                f'<div class="claims">{claim(cu,"u","주판봇 USER팀")}{claim(cb,"b","초파리와 features팀")}</div>'
                f'<div class="pick"><span class="glabel">어느 팀 말이 맞을까요? 먼저 골라 보세요.</span>'
                f'<button class="bt" data-v="u">USER팀</button><button class="bt" data-v="b">초파리와 features팀</button><button class="bt" data-v="d">둘 다 반씩</button><button class="bt" data-v="skip">그냥 판정 보기</button></div>'
                f'<div class="result"><p class="calm mine" style="margin:0"></p>{say("doc", vd.group(1), "<p><b class=\"wtxt\">판정: " + wtxt + "</b></p>" + vd.group(2).strip())}</div></div>')
    s = re.sub(r'<round ([^>]*)>(.*?)</round>', rnd, s, flags=re.S)
    def quiz(m):
        a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        opts = ''.join(f'<button class="bt" data-v="{v}">{t}</button>' for v, t in re.findall(r'<o v="(\w)">(.*?)</o>', m.group(2), re.S))
        return (f'<div class="qitem" data-ans="{a["ans"]}" data-ok="{html.escape(a["ok"])}" data-no="{html.escape(a["no"])}"><p class="qq">{a["q"]}</p>'
                f'<div class="opts">{opts}</div><p class="fb" aria-live="polite"></p></div>')
    s = re.sub(r'<quiz ([^>]*)>(.*?)</quiz>', quiz, s, flags=re.S)
    return s

COVER = '''<div class="cover" aria-label="표지: 주판봇 USER팀과 초파리와 features팀, 가운데 심판 박사">
<div class="court">
 <div class="team u"><img class="px" data-s="robo_e16" alt="주판봇"><img class="px" data-s="asst_e01" alt="조수 하루"><img class="px" data-s="sia_e13" alt="인턴1 시아"><img class="px" data-s="moa_e01" alt="인턴2 모아"></div>
 <div class="ref"><img class="px" data-s="doc_e08" alt="심판 박사"></div>
 <div class="team b"><img class="px" data-s="fly_e09" alt="초파리 연구원"><img class="px" data-s="x1_e13" alt="X1"><img class="px" data-s="x2_e16" alt="X2"><img class="px" data-s="x3_e13" alt="X3"></div>
</div>
<div class="lab"><span class="u">주판봇 USER팀</span><span class="j">심판 · 박사</span><span class="b">초파리와 features팀</span></div>
</div>'''

TEAMS = '''<div class="teams">
<div class="teamcard u"><h4>주판봇 USER팀 — "일단 써 보고 빨리 결론!"</h4><div class="members">
<div><img data-s="robo_e16" alt="주판봇"><b>주판봇</b><small>주장 · 성급한 확신</small></div>
<div><img data-s="asst_e13" alt="조수 하루"><b>조수(하루)</b><small>수식이 어려운 질문 담당</small></div>
<div><img data-s="sia_e13" alt="인턴1 시아"><b>인턴1 시아</b><small>꼼꼼한 기록</small></div>
<div><img data-s="moa_e13" alt="인턴2 모아"><b>인턴2 모아</b><small>현장 사례 담당</small></div></div></div>
<div class="teamcard b"><h4>초파리와 features팀 — "정말 그럴까? 눌러 보고 말하자"</h4><div class="members">
<div><img data-s="fly_e09" alt="초파리 연구원"><b>초파리 연구원</b><small>주장 · 의심 담당</small></div>
<div><img data-s="x1_e13" alt="X1"><b>X1</b><small>반례 찾기</small></div>
<div><img data-s="x2_e13" alt="X2"><b>X2</b><small>숫자 확인</small></div>
<div><img data-s="x3_e13" alt="X3"><b>X3</b><small>조건 바꿔 보기</small></div></div></div>
</div>
<div class="judgecard"><img data-s="doc_e08" alt="박사"><div><b>심판 · 박사</b> — 라운드마다 두 팀의 주장을 듣고, 실험 도구로 확인한 뒤 판정합니다. 이긴 팀이 1점, 둘 다 반만 맞으면 0.5점씩입니다. 판정 전에 <b>여러분도 어느 팀이 맞을지 먼저 골라 보세요.</b> 왼쪽 아래 점수판에 내 예측 적중 수가 함께 쌓입니다.</div></div>'''

BOARD = '<div class="board" id="board" aria-live="polite"><span class="u">USER팀 <b>0</b></span><span class="b">초파리와 features팀 <b>0</b></span><span class="me">내 예측 0/0</span></div>'

def head(meta):
    t = meta['title']; d = meta['desc']; og = meta.get('og', 'og_index.jpg'); url = SITE + meta['file']
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="author" content="안상선">
<meta name="citation_title" content="{meta.get('ctitle', t)}">
<meta name="citation_author" content="안상선">
<meta name="citation_publication_date" content="2026/11/22">
<meta name="dc.title" content="{meta.get('ctitle', t)}">
<meta name="dc.creator" content="안상선">
<meta name="dc.date" content="2026-11-22">
<meta name="dc.language" content="ko">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:image" content="{SITE}assets/img/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&amp;display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
<div class="nojs" id="nojs" role="alert"><b>스크립트가 실행되지 않아 버튼·슬라이더·그림이 멈춰 있습니다.</b> 브라우저(크롬·사파리·엣지)로 <a href="{url}">{url}</a> 를 열어 주세요.</div><script>(function(){{var n=document.getElementById('nojs');if(n)n.parentNode.removeChild(n)}})();</script>
<div id="prog"></div>
'''

def footer(meta):
    return f'''<footer id="foot"><div class="wrap">
<p>글 · 안상선 (<a href="https://adminmrobo.github.io/who_am_i/who_am_i.html">https://adminmrobo.github.io/who_am_i/who_am_i.html</a>) · (주)M-Robo 대표 · 2026-11-22 · v2.0 (비전공자판 개정)</p>
<p>인용: 안상선 (2026). {meta['cite']}. 뉴런 반응 연구실, v2.0. {SITE}{meta['file']}</p>
<p>모든 계산과 그림은 이 페이지 안에서 직접 합니다(설명용 모형, 시드 고정). 외부 요청은 웹 글꼴뿐이고 브라우저 저장소를 쓰지 않습니다. 숫자는 교육용 예시이며 실제 제품·서비스의 성능을 뜻하지 않습니다.</p>
<p>캐릭터 그림: <a href="https://github.com/adminmrobo/fruitfly-lab-expressions">fruitfly-lab-expressions</a> — 캐릭터 이름·설정·그림은 저작권자의 허락 없이 사용할 수 없습니다. · <a href="https://ahnboat.xyz/">ahnboat.xyz</a></p>
</div></footer>
'''

def build(src, out):
    s = open(src, encoding='utf-8').read()
    m = re.match(r'<!--META\s*(\{.*?\})\s*-->\s*', s, re.S)
    meta = json.loads(m.group(1)); body = s[m.end():]
    body = body.replace('<cover/>', COVER).replace('<teams/>', TEAMS).replace('<board/>', BOARD)
    body = expand(body)
    page_js = ''
    pj = re.search(r'<pagejs>(.*?)</pagejs>', body, re.S)
    if pj: page_js = pj.group(1); body = body[:pj.start()] + body[pj.end():]
    keys = sorted(set(re.findall(r'data-s="(\w+)"', body)) | set(re.findall(r"face\('(\w+)'", page_js)) | set(meta.get('extra_sprites', [])))
    for k in keys:
        if k not in SPR: raise SystemExit('그림 없음: ' + k)
    sprite = 'var SPRITE=' + json.dumps({k: SPR[k] for k in keys}, separators=(',', ':')) + ';'
    nav = meta.get('nav', '')
    doc = (head(meta) + f'<nav class="top" aria-label="페이지 이동"><a class="logo" href="{meta.get('root','')}index.html">뉴런 반응 연구실</a>{nav}</nav>\n'
           + body + footer(meta) + '<div id="tip" role="tooltip"></div>\n'
           + f'<script>\n{sprite}\n{JS}\n</script>\n<script>\n{page_js}\nLAB.init();\n</script>\n</body>\n</html>\n')
    open(out, 'w', encoding='utf-8').write(doc)
    print(out, len(doc), 'sprites', len(keys))

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
