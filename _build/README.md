# 빌드 원본

- `src/*.html` — 페이지 원본. `<say>`, `<round>`, `<quiz>`, `<jt>` 같은 약식 태그를 `build.py`가 펼칩니다.
- `lab.css`, `lab.js` — 흰 배경 디자인과 공통 엔진(작은 신경망·Adam·그래프·라운드 점수판).
- `build.py` — 공통 CSS·JS와 그 페이지에 쓰인 캐릭터 그림만 넣어 단일 HTML을 만듭니다. 캐릭터 그림 묶음 `sprites.json`은 fruitfly-lab-expressions의 표정 PNG를 150px WebP로 줄여 만듭니다(용량 때문에 저장소에는 넣지 않음).
- `gen_kg.py` — 편마다 지식 색인 원본(kg/refs/meta)을 만듭니다. 조립·점검은 ai-lab-retrofit의 `retrofit.py`, `check.py`.
- `finalize.sh` — 빌드 → 지식 색인 조립 → 금지 표현 치환을 한 번에 합니다(작업 환경 경로 기준).
