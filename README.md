# 뉴런 반응 연구실 — 신경망 칸은 어떻게 반응하고 배울까

신경망의 칸(뉴런)이 곱하고 더한 값을 함수에 통과시켜 넘기는 '반응'을, 빠른지·끝까지 전해지는지·정확히 배우는지로 나눠 **직접 돌려 보며** 배우는 비전공자용 해설 시리즈입니다. 박사 · 조수(하루) · 초파리 연구원 · 주판봇과 인턴 시아 · 모아가 진행합니다. [텐서 연구실](https://github.com/adminmrobo/what_is_tensor)에서 이어집니다.

- **바로 보기 (GitHub Pages):** https://adminmrobo.github.io/neuron_reaction/
- 글 · 안상선 ((주)M-Robo 대표) · 2026-11-12 · v1.0 · [저자 소개](https://adminmrobo.github.io/who_am_i/who_am_i.html)

## 차례

| 편 | 페이지 | 핵심 질문 | 다루는 것 | 대결 |
|---|---|---|---|---|
| 목차 | [index.html](index.html) | — | 시리즈 안내, 배우는 길 | — |
| 01편 | [활성화 함수](01_activation.html) | 직선뿐인 층 사이에 무엇을 끼워야 곡선을 배울까? | 선형 층의 합성, 시그모이드·tanh와 포화, ReLU·Leaky ReLU와 죽은 칸, GELU·SiLU, 출력 칸(소프트맥스·로짓) | 깊은 망의 학습 신호 → 초파리 승 |
| 특별편 | [연구실 반응속도 대회](sp1_reaction_race.html) | 반응을 속도와 정확도로 나누면 어떤 함수가 무엇에 강할까? | 계산 속도(기기 실측), 학습 신호 전달력(3D 레인, He·1/n 출발 가중치), 학습 속도·정확도(나선 분류, Adam), 3D 종합 무대 | 종목마다 1위가 다름 (선수 박사·시아·조수·모아, 심판 초파리, 점수판 주판봇) |
| 02편 | 역전파 (준비 중) | 학습 신호는 층을 어떻게 거꾸로 건너갈까? | 역전파를 쓸 때와 안 쓸 때, 쓰는 이유, 실제 사례 | — |

## 페이지에 들어 있는 것
- **시뮬레이션:** 모든 그림과 계산(최소제곱 맞춤, 기울기 전달, 작은 신경망 학습)을 페이지 안에서 직접 합니다. 데이터는 시드를 고정한 설명용 모형입니다. 특별편의 순발력 종목만 읽는 사람의 기기에서 실제 시간을 잽니다.
- **비전공자판 구성:** 처음 오신 분께 3줄 요약, 칸마다 "왜 이 방법을 쓰나" 상자와 조수가 대신 묻는 수식 상자(학교 수학 연결, 숫자로 한 번 해 보기), 칸 대화, 코드는 접기 상자에만.
- **학습 도우미:** 용어 말풍선, 확인 퀴즈(01편 10문항, 특별편 6문항), 진행 막대.
- **지식 색인·꾸러미:** 편마다 개념 그래프 검색과, 온톨로지(JSON-LD·Turtle·CSV)·참고문헌(CSL-JSON·BibTeX·RIS)을 ZIP으로 내려받는 섹션.
- 파일 하나로 동작하며, 외부 요청은 웹 글꼴(Google Fonts)뿐입니다. 브라우저 저장소를 쓰지 않습니다.

## 저장소 구조
```
index.html                    시리즈 목차
cover_manifest.json           표지·그림 목록 (ahnboat lab 표지 현황판이 읽음)
assets/img/                   표지 WebP(1600·960), 공유 미리보기 og_*.jpg, 목차 썸네일, src/ 원본
01_activation.html            01편 활성화 함수
sp1_reaction_race.html        특별편 연구실 반응속도 대회
docs/COVER_*.md               편별 글 표지 지시문 (Genspark에 붙여 넣는 한국어 지시 + 영어 프롬프트)
docs/IMG_*.md                 편별 이미지 제작 명세서와 매니페스트
docs/REVIEW.md                페르소나 감사 결과와 보완 과제
data/kg_*.json                편별 지식 그래프·참고문헌·페이지 서지 (꾸러미 원본)
```

## 표지 그림 현황
| 키 | 상태 | 파일 | 지시문 |
|---|---|---|---|
| cover_01 (목차 표지 겸용) | 반영 완료 2026-11-12 | assets/img/cover_01.webp (1600·960), og_01.jpg, og_index.jpg, thumb_01.webp | docs/COVER_01_activation.md |
| cover_SP1 | 반영 완료 2026-11-12 | assets/img/cover_SP1.webp (1600·960), og_SP1.jpg, thumb_SP1.webp | docs/COVER_sp1_reaction_race.md |

원본 PNG는 `assets/img/src/`에 있습니다. 그림 파일을 못 찾으면(예: HTML만 따로 열 때) 각 페이지는 CSS·캐릭터 팩 대체 표지를 그대로 보여 줍니다. 표지 목록은 `cover_manifest.json`(현황판 연결용)에 있습니다.

## 출처와 참고
- Goodfellow, I., Bengio, Y., Courville, A. (2016). *Deep Learning*. MIT Press.
- Glorot, X., Bengio, Y. (2010). Understanding the difficulty of training deep feedforward neural networks. *AISTATS*.
- He, K. 외 (2015). Delving Deep into Rectifiers. *ICCV*.
- Hendrycks, D., Gimpel, K. (2016). Gaussian Error Linear Units (GELUs). arXiv:1606.08415.
- Elfwing, S., Uchibe, E., Doya, K. (2018). Sigmoid-weighted linear units ... *Neural Networks*, 107.
- 그 밖의 문헌과 쪽수·DOI 확인 필요 목록은 각 편 바닥글과 꾸러미 섹션에 있습니다.
- 개념 구성에 참고한 인포그래픽: @eeanimation "Why Activation Functions?", "Sigmoid & Tanh", "ReLU & Leaky ReLU", "GELU, SiLU & Output Choices". 그림은 옮기지 않고 새로 그렸으며, 원자료와 다르게 적은 곳(SiLU 최저점 등)은 01편에 밝혔습니다.
- 캐릭터 그림: [fruitfly-lab-expressions](https://github.com/adminmrobo/fruitfly-lab-expressions)

## 인용
안상선 (2026). 뉴런 반응 연구실 (01편, 특별편), v1.0. https://adminmrobo.github.io/neuron_reaction/

## 라이선스
저자가 정할 예정입니다. 정하기 전에는 개인 학습 목적의 열람만 허용합니다. 캐릭터 이름·설정·그림은 저작권자 허락 없이 사용할 수 없습니다.
