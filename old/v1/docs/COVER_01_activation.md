# 표지 지시문 — 1편 활성화 함수 — 계산 결과에 굽이를 넣는 문

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_01 · L (16:9, 가로 1920 이상) |
| 장소 (앵커) | D 생활·현장 — 밤 연구실 작업대 |
| 주제 은유 | 왼쪽에서 들어오는 곧은 파란 빛줄기가 가운데의 작은 보라색 문(아치)을 지나면서 초록 곡선으로 휘어져 나간다 |
| 여섯 식구 포즈 | 박사: 가운데 뒤, 한 손으로 문을 가리킴 / 조수(하루): 오른쪽 앞, 빈 기록판에 휘어진 선을 따라 그림 / 초파리: 왼쪽, 오른쪽을 보며 곧은 빛줄기를 의심스럽게 가리킴 / 주판봇: 오른쪽, 왼쪽을 보며 주판알을 들어 보임 / 인턴 시아: 맨 왼쪽 뒤, 앞치마 앞에 두 손을 모으고 조용히 지켜봄 / 인턴 모아: 맨 오른쪽 뒤, 분홍 찻잔을 두 손으로 들고 미소 |
| 대체 글 (alt) | 여섯 식구가 곧은 빛줄기가 작은 문을 지나 곡선으로 휘어 나오는 장면을 지켜보는 표지 |
| 앞 표지와 다른 점 | 텐서 연구실 4장(풀리는 큐브와 등고선 바닥) → 뉴런 반응 연구실 1편(빛을 굽히는 문). 인턴 시아·모아가 처음으로 표지에 등장 |

**참고 이미지 (함께 올리기):** 여섯 캐릭터 기본 그림 6장 (기준: GitHub `adminmrobo/fruitfly-lab-expressions`, 주판봇은 v2 기준 그림, 인턴은 `images/sia/E13`, `images/moa/E13`). 여섯 식구 단체 사진 `images/_sheets/lab6_lineup.png`를 함께 올리면 키 비율이 맞습니다(박사 1.00 · 조수 0.90 · 시아 0.88 · 모아 0.84 · 주판봇 0.72 · 초파리 0.41).

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- 비율 16:9, 가로 1920px 이상
- 첨부한 참고 이미지의 여섯 캐릭터(박사, 조수, 초파리 연구원, 주판봇, 인턴 시아, 인턴 모아)를 같은 그림체·같은 외형으로, 여섯 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 어둡고 단순하게
아래 영어 프롬프트를 그대로 써 줘.

Website top cover illustration, wide 16:9.
Match the art style, proportions and colors of the attached reference images exactly
(if there are no reference images: 16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights).
Cozy night laboratory mood, purple light, soft magenta and green fluorescent accents.
Scene: a straight beam of pale blue light enters from the left, passes through a small glowing purple arch-shaped gate standing on a workbench in the center, and comes out on the right as a smooth green curve that bends down and then rises.
All six characters together, height order doctor ≥ girl > maid with black hair > maid with beige hair > robot > fruit fly:
the doctor at the back center pointing at the gate with one hand; the girl at the front right tracing the green curve on a blank board; the fruit fly on the left facing right, pointing suspiciously at the straight blue beam; the robot on the right facing left, holding up a shiny abacus bead;
the black-haired maid at the far left back, hands folded in front of her apron, quietly watching; the beige-haired maid at the far right back, holding a pink teacup with both hands and smiling.
Character details: doctor = chibi scientist with thin teal rectangular glasses, black hair with one white streak and a short tied-back ponytail, white lab coat over black vest and tie; girl = girl researcher with long pink hair in two round buns and a navy streak, blue eyes, white lab coat over a lavender hoodie and jeans; fruit fly = anthropomorphic fruit fly researcher with big red compound eyes, black body, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings; robot = boxy beige retro CRT-monitor robot with a dark green screen face and mint pixel eyes, short antenna topped with an abacus bead, grey segmented arms and two tank treads;
black-haired maid = young woman with waist-length straight jet-black hair and side-swept bangs, no hair accessory, grey eyes, small silver drop earrings, long-sleeved charcoal black maid dress with a large grey bow and an ankle-length white frilled apron;
beige-haired maid = young woman with long ash-beige hair with wavy ends, white frilled maid headband and a small white ribbon above her left ear, amber eyes, white shirt with a red-and-navy plaid ribbon tie, camel knit cardigan, white frilled apron, black skirt.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom); keep the bottom-left corner dark and simple; the light falls on the gate and the curve.
Mood: curious, friendly rivalry, the moment before the result.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

**고칠 때 (같은 대화에서):** `Same six characters, same art style and composition. Change only: {고칠 점}. Still no text.`

**받은 뒤:** SKILL 18-15 절차 — 16:9·글자·여섯 캐릭터·키 순서·시아(머리 장식 없음)·모아(흰 머리띠 + 왼쪽 귀 위 리본) 확인 → WebP 1600×900(220 KB 이하)·960×540 → `01_activation.html`의 `<!-- lab-cover -->` 블록 안 `data-img="cover_01"` 자리에 반영. `og_01.jpg`(1200×630)는 표지에서 잘라 `assets/img/`에 넣습니다(페이지의 og:image가 이 경로를 가리킴).
