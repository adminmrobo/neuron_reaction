# 뉴런 반응 연구실 — 뉴런은 어떻게 반응하고 배울까 (비전공자판 v2.0)

신경망의 뉴런이 곱하고 더한 숫자를 '문'(활성화 함수)에 통과시키는 이유, 문끼리 겨루는 법, 틀린 만큼 거꾸로 고치는 역전파를 **직접 돌려 보며** 배우는 해설 시리즈입니다. 주판봇 USER팀(주판봇 · 조수 하루 · 인턴1 시아 · 인턴2 모아)과 블랙팀(초파리 연구원 · X1 · X2 · X3)이 라운드마다 겨루고, 박사가 심판을 봅니다. [텐서 연구실](https://github.com/adminmrobo/what_is_tensor)에서 이어집니다.

- **바로 보기 (GitHub Pages):** https://adminmrobo.github.io/neuron_reaction/
- 글 · 안상선 ((주)M-Robo 대표) · 2026-11-22 · v2.0 · [저자 소개](https://adminmrobo.github.io/who_am_i/who_am_i.html)

## 차례
| 편 | 페이지 | 핵심 질문 | 실험 도구 | 라운드 |
|---|---|---|---|---|
| 목차 | [index.html](index.html) | — | — | — |
| 1부 | [활성화 함수](01_activation.html) | 곱하고 더한 숫자를 그대로 넘기면 안 될까? | 뉴런 계산기, 곡선 따라 그리기, 포화 관찰기, 멈춘 뉴런 살리기, 마지막 문 고르기, 문 모양 비교판 + 대결 측정기 | 6 |
| 2부 | [연구실 반응속도 대회](02_reaction_race.html) | "가장 좋은 문"은 무엇으로 재느냐에 따라 바뀔까? | 속도 측정기, 신호 전달 레인(He), 학습 경주장(Adam), 시드 재경기표, 종합 점수판 | 4 + 종합 |
| 3부 | [역전파](03_backprop.html) | 손잡이가 수백만 개인데 어느 쪽으로 돌릴지 어떻게 알까? | 손잡이 하나 맞추기, 흔들기 vs 역전파 비용, 계산 그래프, 곱셈 줄, 방법 고르기 판정기 + 예산 대결장 | 6 |
| 마지막 장 | [실전 연습장](practice/index.html) | 배운 것을 현장에 놓으면? | 배송 회사 · 쇼핑몰 · 공장 시뮬레이터, 미션 9개 | — |

예전 판(v1.1, 2026-11-12)은 [old/v1](old/v1/index.html)에 그대로 있습니다. 예전 주소 `sp1_reaction_race.html`은 새 2부로 이동합니다.

## v2.0에서 바뀐 것
- "어렵다"는 의견을 반영해 1·2부를 비전공자판 연구실 스킬(ai-lab-explainer-plain)로 처음부터 다시 썼습니다. 단계마다 "왜 이 방법을 쓰나" 상자, 조수가 대신 묻는 수식 상자(학교 수학 연결 · 숫자로 한 번 해 보기), 일상·현장 비유, 단계 대화, 확인 퀴즈, AI 판단 코너.
- 진행 방식: 주판봇 USER팀 대 블랙팀의 라운드 대결, 박사 심판. 판정 전에 독자가 먼저 예측하고 점수판에 적중 수가 쌓입니다.
- 흰 배경(낮의 연구실)과 실험 도구 20개. 3부 역전파와 실전 연습장 새로 작성.
- 페르소나 감사 결과와 반영 내역: [docs/REVIEW.md](docs/REVIEW.md) · 강의자용 가이드: [docs/TEACHING_GUIDE.md](docs/TEACHING_GUIDE.md)

## 저장소 구조
```
index.html                    시리즈 목차
01_activation.html            1부 활성화 함수
02_reaction_race.html         2부 연구실 반응속도 대회
03_backprop.html              3부 역전파
practice/index.html           마지막 장 실전 연습장 (#delivery #shop #factory)
sp1_reaction_race.html        예전 2부 주소 → 새 2부로 이동
kg/{편}/                       지식 색인 원본(kg.json·refs.json·meta.json)과 점검 보고서
assets/img/                   공유 미리보기 og_v2_*.jpg (임시판), 예전 표지
docs/                         감사 보고서, 강의자용 가이드, 그림 명세·프롬프트(IMG_v2_prompts.md)
old/v1/                       예전 판 페이지·지시문·데이터
_build/                       페이지 원본(src/)과 빌드 스크립트 (공통 엔진 lab.js·lab.css)
cover_manifest.json           표지·그림 목록 (ahnboat lab 표지 현황판이 읽음)
```

## 페이지에 들어 있는 것
- 모든 그림과 계산(최소제곱 맞춤, 작은 신경망의 앞으로·거꾸로 계산, Adam 학습, 흔들어 보기 기울기)을 페이지 안에서 직접 합니다. 데이터는 시드를 고정한 설명용 모형이고, 2부 종목 ①만 읽는 사람의 기기에서 실제 시간을 잽니다.
- 파일 하나로 동작하며 외부 요청은 웹 글꼴뿐입니다. 브라우저 저장소를 쓰지 않습니다.
- 편마다 지식 색인(개념 그래프 검색)과 온톨로지·서지 꾸러미(JSON-LD·Turtle·CSV, CSL-JSON·BibTeX·RIS)를 ZIP으로 내려받을 수 있습니다.

## 표지 그림 현황
| 키 | 상태 | 비고 |
|---|---|---|
| og_v2_index · 01 · 02 · 03 | 임시판 반영 (2026-11-22) | 캐릭터 팩 그림을 합성한 공유 미리보기 |
| cover_v2_index · 01 · 02 · 03 · practice | 요청 전 | 16비트 RPG 픽셀아트, 낮의 연구실 — [docs/IMG_v2_prompts.md](docs/IMG_v2_prompts.md) |
| cover_01 · cover_SP1 (v1) | 보관 | old/v1 페이지에서 사용 |

## 출처와 참고
- Goodfellow, I., Bengio, Y., Courville, A. (2016). *Deep Learning*. MIT Press.
- Rumelhart, D. E., Hinton, G. E., Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*.
- Glorot, X., Bengio, Y. (2010). Understanding the difficulty of training deep feedforward neural networks. *AISTATS*.
- Nair, V., Hinton, G. E. (2010). Rectified linear units improve restricted Boltzmann machines. *ICML*.
- He, K. 외 (2015). Delving Deep into Rectifiers. *ICCV*. · He, K. 외 (2016). Deep Residual Learning for Image Recognition. *CVPR*.
- Kingma, D. P., Ba, J. (2015). Adam: A Method for Stochastic Optimization. *ICLR*.
- Hendrycks, D., Gimpel, K. (2016). Gaussian Error Linear Units (GELUs). arXiv:1606.08415.
- Pascanu, R. 외 (2013), Salimans, T. 외 (2017), Chen, T. 외 (2016), Lillicrap, T. P. 외 (2020), Hinton, G. (2022) — 전체 목록은 각 편의 꾸러미 섹션에 있습니다.
- 캐릭터 그림: [fruitfly-lab-expressions](https://github.com/adminmrobo/fruitfly-lab-expressions)

## 인용
안상선 (2026). 뉴런 반응 연구실 (1부·2부·3부·실전 연습장), v2.0. https://adminmrobo.github.io/neuron_reaction/

## 라이선스
저자가 정할 예정입니다. 정하기 전에는 개인 학습 목적의 열람만 허용합니다. 캐릭터 이름·설정·그림은 저작권자 허락 없이 사용할 수 없습니다.
