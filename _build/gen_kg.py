#!/usr/bin/env python3
"""편마다 kg.json·refs.json·meta.json을 만든다 (ai-lab-retrofit 6장 형식)."""
import json, os, re
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kg')
os.makedirs(OUT, exist_ok=True)
T = lambda x: 'lab:topic/' + x

REFS = {
 'goodfellow2016deep': ('book', 'Deep Learning', [('Goodfellow','Ian'),('Bengio','Yoshua'),('Courville','Aaron')], 2016, 'MIT Press'),
 'glorot2010understanding': ('paper-conference', 'Understanding the difficulty of training deep feedforward neural networks', [('Glorot','Xavier'),('Bengio','Yoshua')], 2010, 'AISTATS'),
 'nair2010rectified': ('paper-conference', 'Rectified linear units improve restricted Boltzmann machines', [('Nair','Vinod'),('Hinton','Geoffrey E.')], 2010, 'ICML'),
 'glorot2011deep': ('paper-conference', 'Deep sparse rectifier neural networks', [('Glorot','Xavier'),('Bordes','Antoine'),('Bengio','Yoshua')], 2011, 'AISTATS'),
 'hendrycks2016gelu': ('article', 'Gaussian Error Linear Units (GELUs)', [('Hendrycks','Dan'),('Gimpel','Kevin')], 2016, 'arXiv:1606.08415'),
 'elfwing2018sigmoid': ('article-journal', 'Sigmoid-weighted linear units for neural network function approximation in reinforcement learning', [('Elfwing','Stefan'),('Uchibe','Eiji'),('Doya','Kenji')], 2018, 'Neural Networks'),
 'shazeer2020glu': ('article', 'GLU Variants Improve Transformer', [('Shazeer','Noam')], 2020, 'arXiv:2002.05202'),
 'devlin2019bert': ('paper-conference', 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding', [('Devlin','Jacob'),('Chang','Ming-Wei'),('Lee','Kenton'),('Toutanova','Kristina')], 2019, 'NAACL'),
 'he2015delving': ('paper-conference', 'Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification', [('He','Kaiming'),('Zhang','Xiangyu'),('Ren','Shaoqing'),('Sun','Jian')], 2015, 'ICCV'),
 'kingma2015adam': ('paper-conference', 'Adam: A Method for Stochastic Optimization', [('Kingma','Diederik P.'),('Ba','Jimmy')], 2015, 'ICLR'),
 'rumelhart1986learning': ('article-journal', 'Learning representations by back-propagating errors', [('Rumelhart','David E.'),('Hinton','Geoffrey E.'),('Williams','Ronald J.')], 1986, 'Nature'),
 'he2016deep': ('paper-conference', 'Deep Residual Learning for Image Recognition', [('He','Kaiming'),('Zhang','Xiangyu'),('Ren','Shaoqing'),('Sun','Jian')], 2016, 'CVPR'),
 'pascanu2013difficulty': ('paper-conference', 'On the difficulty of training recurrent neural networks', [('Pascanu','Razvan'),('Mikolov','Tomas'),('Bengio','Yoshua')], 2013, 'ICML'),
 'salimans2017evolution': ('article', 'Evolution Strategies as a Scalable Alternative to Reinforcement Learning', [('Salimans','Tim'),('Ho','Jonathan'),('Chen','Xi'),('Sidor','Szymon'),('Sutskever','Ilya')], 2017, 'arXiv:1703.03864'),
 'hinton2022forward': ('article', 'The Forward-Forward Algorithm: Some Preliminary Investigations', [('Hinton','Geoffrey')], 2022, 'arXiv:2212.13345'),
 'chen2016training': ('article', 'Training Deep Nets with Sublinear Memory Cost', [('Chen','Tianqi'),('Xu','Bing'),('Zhang','Chiyuan'),('Guestrin','Carlos')], 2016, 'arXiv:1604.06174'),
 'lillicrap2020backpropagation': ('article-journal', 'Backpropagation and the brain', [('Lillicrap','Timothy P.'),('Santoro','Adam'),('Marris','Luke'),('Akerman','Colin J.'),('Hinton','Geoffrey')], 2020, 'Nature Reviews Neuroscience'),
 'breiman2001random': ('article-journal', 'Random Forests', [('Breiman','Leo')], 2001, 'Machine Learning'),
}

def page(slug, number, title, about, refs, items, edges, quizzes, sims, basis):
    nodes = []; E = []
    def N(i, t, ko, en, anc, lv=2, d=None, fam='nn-basics', cov='explained', src=None):
        n = {'id': i, 'type': t, 'label': {'ko': ko, 'en': en}, 'page': slug, 'anchor': anc, 'level': lv, 'status': 'known',
             'confidence': 'high', 'coverage': cov, 'family': fam, 'match': [], 'domain': ['ai']}
        if d: n['definition'] = {'ko': d}
        if src: n['source'] = [{'ref': r, 'loc': ''} for r in src]
        nodes.append(n)
    for it in items: N(*it)
    for (i, ko, anc, target) in sims:
        N(i, 'Simulation', ko, ko, anc, 1); E.append((target, 'demonstratedBy', i, anc))
    for (i, ko, anc, target) in quizzes:
        N(i, 'QuizItem', ko, ko, anc, 1); E.append((i, 'assesses', target, anc))
    for r in refs:
        typ, ttl, au, yr, ct = REFS[r]
        N('lab:work/' + r, 'Work', f'{au[0][0]}{" 외" if len(au) > 1 else ""} ({yr}) {ct}', ttl, '#export', 2)
    for n in nodes:
        if n['type'] == 'Claim':
            for s in n.get('source', []): E.append((n['id'], 'assertedIn', 'lab:work/' + s['ref'], n['anchor']))
    E += edges
    kg = {'version': '1.0', 'page': slug, 'nodes': nodes,
          'edges': [{'s': s, 'p': 'lab:' + p, 'o': o, 'anchor': a, 'confidence': 'high'} for (s, p, o, a) in E]}
    R = []
    for r in refs:
        typ, ttl, au, yr, ct = REFS[r]
        sup = [n['id'] for n in nodes if n['type'] == 'Claim' and any(s['ref'] == r for s in n.get('source', []))]
        R.append({'id': r, 'type': typ, 'title': ttl, 'author': [{'family': f, 'given': g} for f, g in au], 'issued': {'date-parts': [[yr]]},
                  'container-title': ct, 'lab': {'work': 'lab:work/' + r, 'role': 'primary' if r in basis else 'background', 'supports': sup, 'locs': [],
                  'verified': {'title': True, 'author': True, 'year': True, 'container': True, 'pages': False, 'doi': False},
                  'checkedBy': '저자가 알려진 서지 정보로 작성 (쪽수·DOI 대조 안 함)', 'checkedSource': 'page'}})
    meta = {'title': title, 'number': number, 'series': '뉴런 반응 연구실', 'about': about, 'basedOn': basis, 'educationalLevel': '입문',
            'creator': [{'name': '안상선', 'role': 'author'}], 'contributor': [{'name': 'AI 보조 제작', 'role': 'assistant'}],
            'date': '2026-11-22', 'version': '2.0', 'language': ['ko'], 'license': '', 'url': 'https://adminmrobo.github.io/neuron_reaction/' + slug + '.html',
            'registry': 'KG_00_registry 0.2', 'learningResourceType': 'interactive explainer', 'seeAlso': '',
            'suggestedCitation': f'안상선 (2026). {title}. 뉴런 반응 연구실 {number}, v2.0.'}
    d = os.path.join(OUT, slug); os.makedirs(d, exist_ok=True)
    for n_, o in (('kg.json', kg), ('refs.json', R), ('meta.json', meta)):
        json.dump(o, open(os.path.join(d, n_), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(slug, len(nodes), 'nodes', len(kg['edges']), 'edges')

# ---------- 1부 ----------
C = 'lab:concept/'; M = 'lab:method/'; L = 'lab:limitation/'; AN = 'lab:analogy/'; CL = 'lab:claim/'; Q = 'lab:question/'
page('01_activation', '1부', '활성화 함수 — 뉴런의 반응을 정하는 문',
 [T('activation-function'), M+'relu', M+'sigmoid', M+'softmax'],
 ['goodfellow2016deep','glorot2010understanding','nair2010rectified','glorot2011deep','hendrycks2016gelu','elfwing2018sigmoid','shazeer2020glu','devlin2019bert'],
 [(C+'weighted-sum','Concept','가중합 z','weighted sum','#lv1',1,'입력에 중요도(가중치)를 곱해 더하고 편향을 더한 합계 점수.'),
  (C+'bias','Term','편향','bias','#lv1',1,'입력과 상관없는 기본 성향.'),
  (C+'nonlinearity','Concept','비선형성(굽은 관계)','nonlinearity','#lv2',2,'곱하고 더하기만으로는 만들 수 없는 굽은 관계.'),
  (C+'linear-collapse','Concept','선형 층의 합성은 직선','composition of linear layers is linear','#lv2',2,'일차함수를 합성해도 일차함수라서, 문 없이 쌓은 층은 직선 하나와 같다.'),
  (M+'sigmoid','Method','시그모이드','sigmoid','#lv3',2,'σ(z)=1/(1+e^(−z)), 값 0~1, 기울기 최대 0.25.'),
  (M+'tanh','Method','tanh','hyperbolic tangent','#lv3',2,'값 −1~1의 S자, 기울기 최대 1.'),
  (C+'saturation','Concept','포화','saturation','#lv3',2,'z가 아주 크거나 작아 곡선이 평평해지고 기울기가 0에 가까워지는 구간.'),
  (M+'relu','Method','ReLU','rectified linear unit','#lv4',2,'max(0, z). 양수 쪽 기울기 1, 음수 쪽 0.'),
  (M+'leaky-relu','Method','Leaky ReLU','leaky ReLU','#lv4',2,'음수 쪽에 0.01배를 흘리는 ReLU.'),
  (L+'dead-neuron','Limitation','멈춘(죽은) 뉴런','dead neuron','#lv4',2,'합계가 늘 음수라 기울기가 0이어서 학습되지 않는 ReLU 뉴런.'),
  (M+'gelu','Method','GELU','Gaussian error linear unit','#lv5',3,'z × 통과 비율(정규분포 누적). 최저 약 −0.17.','nn-basics','mentioned'),
  (M+'silu','Method','SiLU','sigmoid linear unit','#lv5',3,'z × σ(z). 최저 약 −0.28.','nn-basics','mentioned'),
  (M+'softmax','Method','소프트맥스','softmax','#lv5',2,'점수를 e^z로 바꿔 합이 1인 비율로 만든다.'),
  (C+'logit','Term','로짓(점수)','logit','#lv5',2,'마지막 문을 지나기 전의 점수.'),
  (C+'output-activation-choice','Concept','마지막 문 고르기','choosing the output activation','#lv5',2,'숫자는 그대로, 예·아니오와 태그 여러 개는 시그모이드, 하나 고르기는 소프트맥스.'),
  (C+'gradient-signal-depth','Concept','깊은 망의 학습 신호','gradient signal through depth','#duel',2,'끝 층의 기울기가 첫 층까지 남는 비율.'),
  (L+'line-only','Limitation','문 없이 쌓으면 직선뿐','linear only','#lv2',2),
  (L+'saturation-vanish','Limitation','양 끝 포화로 신호 소실','saturation kills gradient','#lv3',2),
  (L+'softmax-single','Limitation','소프트맥스는 정답 하나를 가정','single-label assumption','#lv5',2),
  (AN+'umbrella','Analogy','우산 챙기기 판단 ↔ 뉴런 하나','umbrella decision','#lv1',1),
  (AN+'ruler','Analogy','곧은 자 이어 붙이기 ↔ 선형 층 쌓기','straight rulers','#lv2',1),
  (AN+'speaker','Analogy','스피커 최대 볼륨 ↔ 포화','speaker volume','#lv3',1),
  (AN+'faucet','Analogy','수도꼭지·새는 꼭지 ↔ ReLU·Leaky ReLU','faucet','#lv4',1),
  (AN+'bowls','Analogy','메뉴에 맞는 그릇 ↔ 마지막 문','bowls','#lv5',1),
  (CL+'relu-simple-fast','Claim','ReLU는 계산이 단순하고 깊은 망 학습을 쉽게 했다','ReLU eases deep training','#lv4',2,None,'nn-basics','mentioned',['nair2010rectified','glorot2011deep']),
  (CL+'bert-gelu','Claim','BERT 같은 트랜스포머 언어모델은 GELU를 쓴다','BERT uses GELU','#lv5',3,None,'nn-basics','mentioned',['devlin2019bert','hendrycks2016gelu']),
  (CL+'swiglu','Claim','최근 공개 언어모델 다수는 SwiGLU를 쓴다','recent LLMs use SwiGLU','#lv5',3,None,'nn-basics','mentioned',['shazeer2020glu','elfwing2018sigmoid']),
  (CL+'relu-deep-signal','Claim','숨은 층 10개에서 ReLU는 첫 층에 약 32%, 시그모이드는 0.0001% 미만이 남는다(이 페이지 모형)','ReLU preserves more gradient','#duel',2,None,'nn-basics','explained',['glorot2010understanding']),
  ('lab:metric/first-layer-ratio','Metric','첫 층까지 남은 학습 신호 비율','first-layer gradient ratio','#duel',2),
  ('lab:dataset/ad-orders-toy','Dataset','광고비·주문 수 설명용 데이터(시드 7, 24점)','toy ad-orders data','#lv2',1),
  (CL+'sigmoid-max','Claim','시그모이드 기울기의 최댓값은 0.25(z=0)','max slope of sigmoid is 1/4','#lv3',2,None,'nn-basics','explained',['goodfellow2016deep']),
  (Q+'which-hidden','Question','숨은 층의 문은 과제와 모델 크기에 따라 어떻게 고를까?','How to choose hidden activations?','#sum',3)],
 [(C+'weighted-sum','broader',T('weights-and-biases'),'#lv1'),(C+'bias','broader',T('weights-and-biases'),'#lv1'),
  (C+'nonlinearity','broader',T('activation-function'),'#lv2'),(C+'linear-collapse','broader',T('mlp'),'#lv2'),
  (M+'sigmoid','broader',T('activation-function'),'#lv3'),(M+'tanh','broader',T('activation-function'),'#lv3'),(C+'saturation','broader',T('activation-function'),'#lv3'),
  (M+'relu','broader',T('activation-function'),'#lv4'),(M+'leaky-relu','broader',T('activation-function'),'#lv4'),(L+'dead-neuron','broader',T('activation-function'),'#lv4'),
  (M+'gelu','broader',T('activation-function'),'#lv5'),(M+'silu','broader',T('activation-function'),'#lv5'),(M+'softmax','broader',T('activation-function'),'#lv5'),
  (C+'logit','broader',T('loss-function'),'#lv5'),(C+'output-activation-choice','broader',T('activation-function'),'#lv5'),
  (C+'gradient-signal-depth','broader',T('backpropagation'),'#duel'),(L+'line-only','broader',T('mlp'),'#lv2'),(L+'saturation-vanish','broader',T('backpropagation'),'#lv3'),(L+'softmax-single','broader',T('activation-function'),'#lv5'),
  (C+'weighted-sum','prerequisiteOf',C+'linear-collapse','#lv2'),(C+'linear-collapse','prerequisiteOf',M+'sigmoid','#lv3'),(M+'sigmoid','prerequisiteOf',M+'relu','#lv4'),(M+'relu','prerequisiteOf',C+'output-activation-choice','#lv5'),
  (C+'linear-collapse','hasLimitation',L+'line-only','#lv2'),(L+'line-only','addressedBy',T('activation-function'),'#lv2'),
  (M+'sigmoid','hasLimitation',L+'saturation-vanish','#lv3'),(L+'saturation-vanish','addressedBy',M+'relu','#lv4'),
  (M+'relu','hasLimitation',L+'dead-neuron','#lv4'),(L+'dead-neuron','addressedBy',M+'leaky-relu','#lv4'),
  (M+'softmax','hasLimitation',L+'softmax-single','#lv5'),(L+'softmax-single','addressedBy',M+'sigmoid','#lv5'),
  (M+'tanh','contrastsWith',M+'sigmoid','#lv3'),(M+'gelu','contrastsWith',M+'silu','#lv5'),(M+'softmax','contrastsWith',M+'sigmoid','#lv5'),(M+'relu','contrastsWith',M+'sigmoid','#duel'),
  (C+'logit','partOf',C+'output-activation-choice','#lv5'),(M+'softmax','partOf',C+'output-activation-choice','#lv5'),
  (AN+'umbrella','analogyOf',C+'weighted-sum','#lv1'),(AN+'ruler','analogyOf',C+'linear-collapse','#lv2'),(AN+'speaker','analogyOf',C+'saturation','#lv3'),(AN+'faucet','analogyOf',M+'leaky-relu','#lv4'),(AN+'bowls','analogyOf',C+'output-activation-choice','#lv5'),
  (C+'saturation','relatedTo',L+'saturation-vanish','#lv3'),
  (CL+'relu-simple-fast','supports',M+'relu','#lv4'),(CL+'bert-gelu','supports',M+'gelu','#lv5'),(CL+'swiglu','supports',M+'silu','#lv5'),(CL+'relu-deep-signal','supports',C+'gradient-signal-depth','#duel'),
  (C+'gradient-signal-depth','evaluatedBy','lab:metric/first-layer-ratio','#duel'),(C+'nonlinearity','evaluatedOn','lab:dataset/ad-orders-toy','#lv2'),
  (T('activation-function'),'raises',Q+'which-hidden','#sum'),(CL+'sigmoid-max','supports',C+'saturation','#lv3'),(C+'saturation','broader',T('activation-function'),'#lv3')],
 [('lab:quiz/p01-lv1-1','뉴런 계산 순서','#lv1',C+'weighted-sum'),('lab:quiz/p01-lv2-1','문 없이 10층','#lv2',C+'linear-collapse'),('lab:quiz/p01-lv3-1','포화 위치','#lv3',C+'saturation'),
  ('lab:quiz/p01-lv4-1','Leaky ReLU의 역할','#lv4',M+'leaky-relu'),('lab:quiz/p01-lv5-1','배송 시간의 마지막 문','#lv5',C+'output-activation-choice'),('lab:quiz/p01-lv5-2','태그 여러 개','#lv5',M+'sigmoid')],
 [('lab:sim/p01-neuron','도구 1 뉴런 하나 계산기','#lv1',C+'weighted-sum'),('lab:sim/p01-fit','도구 2 곡선 따라 그리기','#lv2',C+'nonlinearity'),('lab:sim/p01-sat','도구 3 포화 관찰기','#lv3',C+'saturation'),
  ('lab:sim/p01-dead','도구 4 멈춘 뉴런 살리기','#lv4',L+'dead-neuron'),('lab:sim/p01-out','도구 5 마지막 문 고르기','#lv5',C+'output-activation-choice'),('lab:sim/p01-duel','대결 학습 신호 측정기','#duel',C+'gradient-signal-depth'),
  ('lab:sim/p01-compare','도구 6 문 모양 비교판','#sum',T('activation-function'))],
 ['goodfellow2016deep'])

# ---------- 2부 ----------
page('02_reaction_race', '2부', '연구실 반응속도 대회 — 빠른 문, 끝까지 전하는 문, 정확히 배우는 문',
 [M+'relu', M+'gelu', M+'he-init', M+'adam', C+'seed-variance'],
 ['he2015delving','kingma2015adam','glorot2010understanding','hendrycks2016gelu','elfwing2018sigmoid','goodfellow2016deep'],
 [(C+'fair-comparison','Concept','공정한 비교 조건','fair comparison','#rule',1,'같은 데이터·구조·출발점·학습 방법에서 재야 비교가 된다.','evaluation'),
  (C+'compute-cost','Concept','문의 계산 비용','activation compute cost','#lv1',2,'지수 계산이 들어간 문은 비교 한 번인 ReLU보다 무겁다.'),
  (M+'relu','Method','ReLU','rectified linear unit','#cast',2,'max(0, z).'),(M+'tanh','Method','tanh','hyperbolic tangent','#cast',2,'−1~1 S자.'),
  (M+'gelu','Method','GELU','Gaussian error linear unit','#cast',2,'z × 통과 비율.'),(M+'silu','Method','SiLU','sigmoid linear unit','#cast',2,'z × σ(z).'),
  (M+'he-init','Method','He 출발 가중치','He initialization','#lv2',2,'가중치를 분산 2/n으로 뽑아 ReLU가 줄이는 신호를 보충한다.','nn-basics'),
  (M+'std-init','Method','표준 1/n 출발 가중치','1/n initialization','#lv2',2,'분산 1/n으로 뽑는 방법.','nn-basics'),
  (C+'gradient-signal-depth','Concept','첫 층까지 전해지는 학습 신호','gradient signal through depth','#lv2',2,'끝 층 대비 첫 층 기울기 크기 비율.'),
  (L+'vanish-explode','Limitation','신호 소실·폭발','vanishing/exploding gradients','#lv2',2),
  (M+'adam','Method','Adam','Adam optimizer','#lv3',2,'최근 기울기의 평균 방향을 평균 크기로 나눠 걸음을 고르게 맞추는 최적화 방법.','optimization'),
  (M+'gd','Method','일반 경사하강','gradient descent','#lv3',2,'학습률 × 기울기만큼 움직인다.','optimization'),
  (L+'small-gradient-slow','Limitation','기울기가 작으면 일반 경사하강은 거의 멈춤','slow with small gradients','#lv3',2,None,'optimization'),
  (C+'test-accuracy','Concept','시험 정확도','test accuracy','#lv3',1,'학습에 쓰지 않은 데이터로 잰 정확도.','evaluation'),
  (C+'seed-variance','Concept','시드에 따른 흩어짐','seed variance','#lv4',2,'출발 난수가 바뀌면 결과가 흔들린다. 평균과 범위를 함께 본다.','evaluation'),
  (L+'single-run','Limitation','한 번 잰 기록은 운과 실력을 구분 못 함','single-run limitation','#lv4',2,None,'evaluation'),
  ('lab:metric/time-1m','Metric','100만 번 계산 시간','time per 1M evaluations','#lv1',1),('lab:metric/first-layer-ratio','Metric','첫 층 신호 비율','first-layer gradient ratio','#lv2',2),
  ('lab:metric/steps-to-95','Metric','95% 도달 걸음 수','steps to 95% test accuracy','#lv3',2),
  ('lab:dataset/spiral','Dataset','나선 데이터(점 160개)','two spirals','#lv3',1),('lab:dataset/moons','Dataset','초승달 데이터','two moons','#lv4',1),
  (AN+'checkout','Analogy','계산대 줄 ↔ 계산 속도','checkout line','#lv1',1),(AN+'whisper','Analogy','말 전하기 놀이 ↔ 출발 가중치','telephone game','#lv2',1),
  (AN+'hiker','Analogy','보폭을 조절하는 등산객 ↔ Adam','hiker','#lv3',1),(AN+'season','Analogy','한 경기와 시즌 성적 ↔ 시드 재경기','season record','#lv4',1),
  (CL+'he-2n','Claim','He 출발 가중치는 분산 2/n으로 ReLU 망의 신호 크기를 유지한다','He init keeps variance','#lv2',2,None,'nn-basics','explained',['he2015delving']),
  (CL+'adam-scale','Claim','Adam은 기울기 크기로 나눠 걸음을 맞춘다','Adam normalizes step size','#lv3',2,None,'optimization','explained',['kingma2015adam']),
  (CL+'sigmoid-vanish','Claim','시그모이드 깊은 망은 학습 신호가 사라진다','sigmoid nets vanish','#lv2',2,None,'nn-basics','explained',['glorot2010understanding']),
  (CL+'gelu-def','Claim','GELU는 z에 정규분포 누적 비율을 곱한 문이다','GELU definition','#cast',2,None,'nn-basics','mentioned',['hendrycks2016gelu']),
  (CL+'silu-def','Claim','SiLU는 z에 시그모이드(z)를 곱한 문이다','SiLU definition','#cast',2,None,'nn-basics','mentioned',['elfwing2018sigmoid']),
  (CL+'test-split','Claim','일반화는 학습에 쓰지 않은 시험 데이터로 잰다','evaluate on held-out data','#lv3',1,None,'evaluation','explained',['goodfellow2016deep']),
  (Q+'best-activation','Question','"가장 좋은 문"은 어떤 기준·조건에서 말할 수 있나?','Which activation is best, under which conditions?','#duel',3)],
 [(C+'fair-comparison','broader',T('reproducibility'),'#rule'),(C+'compute-cost','broader',T('activation-function'),'#lv1'),
  (M+'relu','broader',T('activation-function'),'#cast'),(M+'tanh','broader',T('activation-function'),'#cast'),(M+'gelu','broader',T('activation-function'),'#cast'),(M+'silu','broader',T('activation-function'),'#cast'),
  (M+'he-init','broader',T('weights-and-biases'),'#lv2'),(M+'std-init','broader',T('weights-and-biases'),'#lv2'),(C+'gradient-signal-depth','broader',T('backpropagation'),'#lv2'),(L+'vanish-explode','broader',T('backpropagation'),'#lv2'),
  (M+'adam','broader',T('momentum-adam'),'#lv3'),(M+'gd','broader',T('gradient-descent'),'#lv3'),(L+'small-gradient-slow','broader',T('gradient-descent'),'#lv3'),
  (C+'test-accuracy','broader',T('data-splitting'),'#lv3'),(C+'seed-variance','broader',T('reproducibility'),'#lv4'),(L+'single-run','broader',T('reproducibility'),'#lv4'),
  (C+'fair-comparison','prerequisiteOf',C+'compute-cost','#lv1'),(C+'compute-cost','prerequisiteOf',C+'gradient-signal-depth','#lv2'),(C+'gradient-signal-depth','prerequisiteOf',M+'adam','#lv3'),(M+'adam','prerequisiteOf',C+'seed-variance','#lv4'),
  (C+'gradient-signal-depth','hasLimitation',L+'vanish-explode','#lv2'),(L+'vanish-explode','addressedBy',M+'he-init','#lv2'),
  (M+'gd','hasLimitation',L+'small-gradient-slow','#lv3'),(L+'small-gradient-slow','addressedBy',M+'adam','#lv3'),
  (C+'test-accuracy','hasLimitation',L+'single-run','#lv4'),(L+'single-run','addressedBy',C+'seed-variance','#lv4'),
  (M+'he-init','contrastsWith',M+'std-init','#lv2'),(M+'adam','contrastsWith',M+'gd','#lv3'),(M+'relu','contrastsWith',M+'gelu','#lv1'),(M+'tanh','contrastsWith',M+'silu','#lv2'),
  (C+'compute-cost','evaluatedBy','lab:metric/time-1m','#lv1'),(C+'gradient-signal-depth','evaluatedBy','lab:metric/first-layer-ratio','#lv2'),(M+'adam','evaluatedBy','lab:metric/steps-to-95','#lv3'),
  (M+'relu','evaluatedOn','lab:dataset/spiral','#lv3'),(C+'seed-variance','evaluatedOn','lab:dataset/moons','#lv4'),
  (AN+'checkout','analogyOf',C+'compute-cost','#lv1'),(AN+'whisper','analogyOf',M+'he-init','#lv2'),(AN+'hiker','analogyOf',M+'adam','#lv3'),(AN+'season','analogyOf',C+'seed-variance','#lv4'),
  (CL+'he-2n','supports',M+'he-init','#lv2'),(CL+'adam-scale','supports',M+'adam','#lv3'),(CL+'sigmoid-vanish','supports',L+'vanish-explode','#lv2'),
  (C+'fair-comparison','raises',Q+'best-activation','#duel'),(CL+'gelu-def','supports',M+'gelu','#cast'),(CL+'silu-def','supports',M+'silu','#cast'),(CL+'test-split','supports',C+'test-accuracy','#lv3'),(C+'test-accuracy','partOf',C+'fair-comparison','#lv3')],
 [('lab:quiz/p02-lv1-1','ReLU가 가벼운 이유','#lv1',C+'compute-cost'),('lab:quiz/p02-lv2-1','He가 2/n인 이유','#lv2',M+'he-init'),
  ('lab:quiz/p02-lv3-1','시험 데이터로 재는 이유','#lv3',C+'test-accuracy'),('lab:quiz/p02-lv4-1','평균 차이와 흩어짐','#lv4',C+'seed-variance')],
 [('lab:sim/p02-speed','도구 1 문 속도 측정기','#lv1',C+'compute-cost'),('lab:sim/p02-signal','도구 2 학습 신호 전달 레인','#lv2',C+'gradient-signal-depth'),
  ('lab:sim/p02-race','도구 3 학습 경주장','#lv3',M+'adam'),('lab:sim/p02-seeds','도구 4 시드 재경기표','#lv4',C+'seed-variance'),('lab:sim/p02-board','도구 5 종합 점수판','#duel',C+'fair-comparison')],
 ['he2015delving','kingma2015adam'])

# ---------- 3부 ----------
page('03_backprop', '3부', '역전파 — 학습 신호가 거꾸로 건너가는 길',
 [T('backpropagation'), C+'chain-rule', M+'numerical-gradient', T('residual-connections')],
 ['rumelhart1986learning','goodfellow2016deep','he2016deep','pascanu2013difficulty','salimans2017evolution','hinton2022forward','chen2016training','lillicrap2020backpropagation','breiman2001random'],
 [(C+'loss','Concept','손실','loss','#lv1',1,'예측이 정답에서 틀린 정도. 여기서는 오차 제곱의 평균.'),
  (C+'gradient','Concept','기울기','gradient','#lv1',1,'손잡이를 조금 돌렸을 때 손실이 바뀌는 방향과 크기.','optimization'),
  (M+'gradient-descent','Method','경사하강법','gradient descent','#lv1',1,'기울기 반대 방향으로 학습률만큼 움직인다.','optimization'),
  (M+'numerical-gradient','Method','흔들어 보기(수치 미분)','numerical (finite-difference) gradient','#lv2',2,'손잡이를 ±h만큼 바꿔 손실 변화 ÷ 2h로 기울기를 어림한다.','optimization'),
  (L+'cost-scales-with-params','Limitation','흔들기 비용은 손잡이 수에 비례(약 2N번)','cost scales with parameter count','#lv2',2,None,'optimization'),
  (C+'gradient-check','Concept','기울기 검사','gradient checking','#lv2',2,'역전파 기울기를 흔들어 보기 값과 비교해 검산한다.'),
  (C+'chain-rule','Concept','연쇄법칙','chain rule','#lv3',2,'이어진 계산의 변화 비율은 단계별 비율의 곱이다.','math'),
  (C+'computational-graph','Concept','계산 그래프','computational graph','#lv3',2,'곱하기·문·손실을 상자로 이은 계산 흐름.'),
  (C+'reuse','Concept','뒤에서 구한 기울기 재사용','reuse of upstream gradients','#lv3',2,'앞 층 기울기는 뒤에서 구한 값에 곱 하나를 더해 얻는다.'),
  (M+'autodiff','Method','자동 미분','automatic differentiation','#lv3',3,'프로그램이 앞으로 계산을 기록해 두고 거꾸로 계산을 자동으로 한다.','nn-basics','mentioned'),
  (L+'vanish-explode','Limitation','기울기 소실·폭발','vanishing/exploding gradients','#lv4',2,'비율의 곱이 길어지면 0으로 사라지거나 끝없이 커진다.'),
  (M+'residual','Method','지름길(잔차 연결)','residual connection','#lv4',3,'층을 건너뛰는 길을 더해 층마다 비율을 1 + 조금으로 만든다.','vision'),
  (M+'grad-clip','Method','기울기 자르기','gradient clipping','#lv4',3,'너무 큰 기울기에 상한을 둔다.','optimization'),
  (C+'differentiable','Concept','미분 가능','differentiability','#lv5',2,'모든 단계에서 기울기를 정할 수 있다는 조건.','math'),
  (L+'memory-cost','Limitation','중간값 저장으로 메모리를 많이 씀','memory cost of backprop','#lv5',3),
  (M+'checkpointing','Method','다시 계산하며 메모리 아끼기','gradient checkpointing','#lv5',4,None,'systems','mentioned'),
  (M+'decision-tree','Method','의사결정나무','decision tree','#lv5',2,'질문으로 나누는 계단 모양 모델. 역전파를 쓰지 않는다.','classical'),
  (M+'evolution-strategies','Method','진화 전략·무작위 탐색','evolution strategies / random search','#lv5',3,'점수만 보고 손잡이를 바꿔 보며 고친다.','optimization','mentioned'),
  (M+'random-search','Method','무작위 바꿔 보기','random search','#duel',2,'손잡이 전체를 살짝 무작위로 바꿔 보고 좋아지면 채택.','optimization'),
  (Q+'brain-backprop','Question','뇌는 역전파를 하는가?','Does the brain do backprop?','#lv5',4),
  (AN+'shower','Analogy','샤워기 온도 맞추기 ↔ 경사하강','shower knob','#lv1',1),(AN+'remote','Analogy','리모컨 버튼 하나씩 눌러 보기 ↔ 흔들어 보기','remote control','#lv2',1),
  (AN+'gears','Analogy','맞물린 톱니바퀴 ↔ 연쇄법칙','gears','#lv3',1),(AN+'photocopy','Analogy','복사본의 복사본 ↔ 기울기 소실','photocopy','#lv4',1),(AN+'navigation','Analogy','지도가 있을 때의 내비게이션 ↔ 역전파의 조건','navigation','#lv5',1),
  ('lab:metric/compute-budget','Metric','계산 예산(앞으로 계산 횟수)','compute budget','#duel',2),('lab:dataset/delivery-toy','Dataset','거리·배송 시간 설명용 데이터','toy delivery data','#lv1',1),
  (CL+'rumelhart','Claim','1986년 러멜하트·힌턴·윌리엄스 논문이 역전파를 신경망 학습법으로 널리 알렸다','Rumelhart et al. popularized backprop','#why',2,None,'nn-basics','mentioned',['rumelhart1986learning']),
  (CL+'resnet','Claim','잔차 연결(ResNet)로 층을 100개 넘게 쌓을 수 있게 됐다','ResNet enables very deep nets','#lv4',3,None,'vision','mentioned',['he2016deep']),
  (CL+'clip-explode','Claim','기울기 폭발에는 기울기 자르기를 쓴다','clipping for exploding gradients','#lv4',3,None,'optimization','mentioned',['pascanu2013difficulty']),
  (CL+'es-alternative','Claim','진화 전략은 미분 없이도 쓸 수 있는 대안이다','ES as alternative','#lv5',3,None,'optimization','mentioned',['salimans2017evolution']),
  (CL+'brain-debate','Claim','뇌가 역전파를 그대로 하는지는 논쟁 중이고 대안 학습법이 연구된다','brain and backprop debated','#lv5',4,None,'neuro','mentioned',['lillicrap2020backpropagation','hinton2022forward']),
  (CL+'checkpoint','Claim','중간값 일부를 버리고 다시 계산해 메모리를 아낀다','sublinear memory','#lv5',4,None,'systems','mentioned',['chen2016training']),
  (CL+'trees-no-backprop','Claim','랜덤 포레스트 같은 나무 모델은 기울기 없이 학습한다','tree ensembles without gradients','#lv5',2,None,'ensemble','mentioned',['breiman2001random']),
  (CL+'bp-wins-budget','Claim','같은 예산에서 역전파가 흔들기·무작위보다 손실을 더 낮춘다(이 페이지 모형)','backprop wins under equal budget','#duel',2,None,'optimization','explained',['goodfellow2016deep'])],
 [(C+'loss','broader',T('loss-function'),'#lv1'),(C+'gradient','broader',T('gradient-descent'),'#lv1'),(M+'gradient-descent','broader',T('gradient-descent'),'#lv1'),
  (M+'numerical-gradient','broader',T('calculus-optimization-math'),'#lv2'),(L+'cost-scales-with-params','broader',T('backpropagation'),'#lv2'),(C+'gradient-check','broader',T('backpropagation'),'#lv2'),
  (C+'chain-rule','broader',T('calculus-optimization-math'),'#lv3'),(C+'computational-graph','broader',T('backpropagation'),'#lv3'),(C+'reuse','broader',T('backpropagation'),'#lv3'),(M+'autodiff','broader',T('backpropagation'),'#lv3'),
  (L+'vanish-explode','broader',T('backpropagation'),'#lv4'),(M+'residual','broader',T('residual-connections'),'#lv4'),(M+'grad-clip','broader',T('gradient-descent'),'#lv4'),
  (C+'differentiable','broader',T('calculus-optimization-math'),'#lv5'),(L+'memory-cost','broader',T('backpropagation'),'#lv5'),(M+'checkpointing','broader',T('backpropagation'),'#lv5'),
  (M+'decision-tree','broader',T('decision-tree'),'#lv5'),(M+'evolution-strategies','broader',T('policy-gradient'),'#lv5'),(M+'random-search','broader',T('gradient-descent'),'#duel'),
  (C+'loss','prerequisiteOf',C+'gradient','#lv1'),(C+'gradient','prerequisiteOf',M+'numerical-gradient','#lv2'),(M+'numerical-gradient','prerequisiteOf',C+'chain-rule','#lv3'),(C+'chain-rule','prerequisiteOf',L+'vanish-explode','#lv4'),(L+'vanish-explode','prerequisiteOf',C+'differentiable','#lv5'),
  (M+'numerical-gradient','hasLimitation',L+'cost-scales-with-params','#lv2'),(L+'cost-scales-with-params','addressedBy',T('backpropagation'),'#lv3'),
  (T('backpropagation'),'hasLimitation',L+'vanish-explode','#lv4'),(L+'vanish-explode','addressedBy',M+'residual','#lv4'),(L+'vanish-explode','addressedBy',M+'grad-clip','#lv4'),
  (T('backpropagation'),'hasLimitation',L+'memory-cost','#lv5'),(L+'memory-cost','addressedBy',M+'checkpointing','#lv5'),
  (M+'numerical-gradient','contrastsWith',T('backpropagation'),'#lv2'),(M+'random-search','contrastsWith',T('backpropagation'),'#duel'),(M+'decision-tree','contrastsWith',T('backpropagation'),'#lv5'),
  (C+'computational-graph','partOf',C+'chain-rule','#lv3'),(C+'reuse','partOf',C+'chain-rule','#lv3'),(C+'gradient-check','partOf',M+'numerical-gradient','#lv2'),
  (AN+'shower','analogyOf',M+'gradient-descent','#lv1'),(AN+'remote','analogyOf',M+'numerical-gradient','#lv2'),(AN+'gears','analogyOf',C+'chain-rule','#lv3'),(AN+'photocopy','analogyOf',L+'vanish-explode','#lv4'),(AN+'navigation','analogyOf',C+'differentiable','#lv5'),
  (CL+'rumelhart','supports',T('backpropagation'),'#why'),(CL+'resnet','supports',M+'residual','#lv4'),(CL+'clip-explode','supports',M+'grad-clip','#lv4'),(CL+'es-alternative','supports',M+'evolution-strategies','#lv5'),
  (CL+'brain-debate','supports',Q+'brain-backprop','#lv5'),(CL+'checkpoint','supports',M+'checkpointing','#lv5'),(CL+'trees-no-backprop','supports',M+'decision-tree','#lv5'),(CL+'bp-wins-budget','supports',T('backpropagation'),'#duel'),
  (T('backpropagation'),'evaluatedBy','lab:metric/compute-budget','#duel'),(M+'gradient-descent','evaluatedOn','lab:dataset/delivery-toy','#lv1'),(C+'differentiable','raises',Q+'brain-backprop','#lv5')],
 [('lab:quiz/p03-lv1-1','기울기 +5일 때 방향','#lv1',M+'gradient-descent'),('lab:quiz/p03-lv2-1','흔들기 계산 횟수','#lv2',L+'cost-scales-with-params'),
  ('lab:quiz/p03-lv3-1','톱니바퀴 비율','#lv3',C+'chain-rule'),('lab:quiz/p03-lv4-1','비율 1.5, 20층','#lv4',L+'vanish-explode'),('lab:quiz/p03-lv5-1','역전파의 조건','#lv5',C+'differentiable')],
 [('lab:sim/p03-knob','도구 1 손잡이 하나 맞추기','#lv1',M+'gradient-descent'),('lab:sim/p03-cost','도구 2 흔들기 vs 역전파 비용','#lv2',M+'numerical-gradient'),
  ('lab:sim/p03-graph','도구 3 계산 그래프 따라가기','#lv3',C+'chain-rule'),('lab:sim/p03-chain','도구 4 곱셈 줄','#lv4',L+'vanish-explode'),
  ('lab:sim/p03-chooser','도구 5 방법 고르기 판정기','#lv5',C+'differentiable'),('lab:sim/p03-duel','대결 계산 예산 대결장','#duel',T('backpropagation'))],
 ['rumelhart1986learning','goodfellow2016deep'])
