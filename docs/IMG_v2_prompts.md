# v2.0 그림 명세와 프롬프트 (16비트 RPG 픽셀아트 · 낮의 연구실)

지금 페이지는 표지 대신 캐릭터 팩 그림으로 만든 '팀 대결 표지'를 씁니다. 아래 그림을 받으면 `assets/img/`에 넣고 각 페이지 표지에 연결합니다(받기 전에도 페이지는 그대로 동작).

## 그림 목록
| 키 | 쓰는 곳 | 크기 | 상태 |
|---|---|---|---|
| cover_v2_index | 목차 표지·공유 미리보기 | 1600×900 | 요청 전 |
| cover_v2_01 | 1부 표지 | 1600×900 | 요청 전 |
| cover_v2_02 | 2부 표지 | 1600×900 | 요청 전 |
| cover_v2_03 | 3부 표지 | 1600×900 | 요청 전 |
| cover_v2_practice | 실전 연습장 표지 | 1600×900 | 요청 전 |
| og_v2_* | 공유 미리보기 1200×630 | 1200×630 | **임시판 반영** (캐릭터 팩 그림 합성) |

만드는 순서: 목차 표지를 먼저 받아 그림체를 확인한 뒤, 그 그림을 참고 그림으로 함께 올려 나머지를 요청합니다. 캐릭터 기본 그림은 fruitfly-lab-expressions 저장소의 E13(기본 표정)을 첨부합니다.

## 공통 지시 (Genspark에 붙여 넣는 한국어)
16비트 SNES 시대 RPG 픽셀아트. 밝은 낮의 연구실, 흰 벽과 창문으로 햇빛이 들어옴. 배경은 흰색에 가깝게 밝게. 왼쪽에 파란 팀 깃발 아래 "주판봇 USER팀"(네모 화면 얼굴에 주판을 든 작은 로봇, 분홍·남색 머리 쪽진 머리의 연구 조수 하루, 흑발 긴 머리 메이드복 인턴 시아, 베이지 긴 머리 메이드복 인턴 모아), 오른쪽에 검은 팀 깃발 아래 "블랙팀"(빨간 겹눈과 흰 가운의 초파리 연구원, 검은 실루엣 캐릭터 셋: 분홍 리본 포니테일, 둥근 안경, 고양이 귀 후드), 가운데 심판석에 흰 가운과 안경의 박사. 글자는 넣지 않음.

## 편별 장면 (영어 프롬프트)
- **cover_v2_index**: `16-bit SNES era RPG pixel art, bright daytime laboratory with white walls and sunlight, two teams facing each other like a tournament stage: blue team on the left (small boxy robot with abacus, pink-and-navy haired lab assistant girl, black-haired maid intern, beige-haired maid intern), black team on the right (fruit fly researcher with red compound eyes and white coat, three cute black silhouette characters: pink ribbon ponytail, round glasses, cat-ear hood), professor with glasses and white coat as referee in the center, glowing neuron diagram on a whiteboard, no text, 16:9`
- **cover_v2_01**: `...same cast..., a giant glowing "gate" between two neurons on the whiteboard, S-shaped curve and bent line (ReLU) drawn as pixel graphs, robot pointing confidently, fruit fly squinting with doubt, no text, 16:9`
- **cover_v2_02**: `...same cast..., indoor sports day race track in the lab with four lanes, each lane labeled by a pixel icon of a curve (bent line, S curve, smooth bend), stopwatch and scoreboard, professor with a whistle, no text, 16:9`
- **cover_v2_03**: `...same cast..., a chain of meshing gears flowing right-to-left with orange arrows going backward from a "loss" bell to the first gear, blue team shaking knobs one by one, black team pulling a single lever that turns all gears, no text, 16:9`
- **cover_v2_practice**: `...same cast..., three small shops in a row inside the lab (delivery truck counter, online shop shelf, factory conveyor), characters operating control panels with green and blue knobs, no text, 16:9`

## 반영 방법
1. 받은 PNG를 `assets/img/src/`에 원본으로 두고, 1600·960 WebP와 1200×630 og 그림을 만든다.
2. 각 페이지 `<meta property="og:image">`를 새 og 그림으로 바꾸고, 표지 영역 위에 그림을 얹는다(그림이 없으면 지금의 팀 표지가 그대로 보이게).
3. `cover_manifest.json`의 상태를 "반영 완료"로 바꾼다.
