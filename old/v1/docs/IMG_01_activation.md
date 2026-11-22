# 01번 「1편 활성화 함수」 이미지 제작 명세서

| 항목 | 내용 |
|---|---|
| 페이지 | 01_activation.html |
| 주 앵커 | D 밤 연구실 작업대 (빛을 굽히는 문) |
| 시즌 | 기본 |
| 대결 | 초파리 승 (깊은 망 학습 신호: ReLU 14.5% vs 시그모이드 1.9×10⁻⁵, 페이지 계산값) |
| 표지 | **2026-11-12 받아 반영 완료** (1600 WebP 121 KB, 960 WebP, og·thumb 자르기)
| 새로 그릴 그림 | P1 1장 (cover_01) · 나머지는 표지 자르기 |
| 재사용 | 캐릭터 팩 표정 31장 (96px, 페이지에 base64로 들어 있음) — 인턴 시아 5장·모아 5장 포함 |
| 그림이 없을 때 | 페이지는 캐릭터 팩 표정 + CSS·SVG 대체 표지(문을 지나 휘는 선)로 이미 완성 상태 |

## 1. 필요한 그림

| # | 키 | 판 | 크기 | 상태 | 우선 | 들어가는 곳 | 대신 쓰는 그림 |
|---|---|---|---|---|---|---|---|
| 0 | cover_01 | L | 1920×1080 | 새로 (COVER_01_activation.md) | P1 | 맨 위 글 표지 | 대체 표지 (CSS 벌집 + 여섯 식구 + SVG 문) |
| 1 | thumb_01 | I | 600×400 | 새로 (cover_01 3:2 자르기) | P2 | 목차 카드 | SVG 카드 (index.html 카드) |
| 2 | og_01 | K | 1200×630 | 새로 (cover_01 자르기) → `assets/img/og_01.jpg` | P2 | 공유 미리보기 (그림을 넣은 뒤 HTML `<head>`에 `og:image` 메타를 다시 추가) | 없음 (경로만 미리 걸어 둠) |
| — | doc_front · doc_think · doc_judge · doc_magic | A | 96 | 재사용 | — | 히어로·판정·아웃트로 | 같은 캐릭터 기본 표정 |
| — | asst_smile · asst_report · asst_spark · asst_shock · asst_firm | B | 96 | 재사용 | — | 수식 상자(놀람 → 이해), 숫자 발표 | 〃 |
| — | fly_clip · fly_point · fly_arms · fly_coffee · fly_magnify | C | 96 | 재사용 | — | 칸 대화, 대결 | 〃 |
| — | robo_smile · robo_coin · robo_happy · robo_sigh · robo_calc · robo_wow · robo_meh | D | 96 | 재사용 | — | 칸 대화, 대결 | 〃 |
| — | sia_smile · sia_signal · sia_explain · sia_guide · sia_doze | A | 96 | 재사용 | — | 표지, ② 정리 한마디, ⑤ 순서 정리, 대결 시작 신호 | sia_smile |
| — | moa_smile · moa_tea · moa_report · moa_cheer · moa_sparkle | A | 96 | 재사용 | — | 표지, ④ 기록 모으기, 정리 표(차) | moa_smile |
| — | 시뮬레이션 그림 전부 | — | — | 코드 (Canvas 2D) | — | 각 칸·대결 | — |

## 2. 새로 그릴 그림
- `cover_01`: 지시문과 영어 프롬프트는 `COVER_01_activation.md`. 시리즈 첫 편이자 처음으로 **여섯 식구**가 함께 나오는 표지이므로, 단체 사진 `lab6_lineup.png`를 참고 그림으로 꼭 함께 올립니다.
- `thumb_01`, `og_01`: 표지를 받은 뒤 잘라 만듭니다.

## 3. 인턴 등장 점검 (캐릭터 팩 C2·C9)
- [x] 섹션당 인턴 최대 1명 (② 시아, ④ 모아, ⑤ 시아, 대결 시아, 정리 모아)
- [x] 인턴은 숫자 발표·승패 판정을 하지 않음 (숫자는 조수, 판정은 박사)
- [x] 대결에서 시아는 시작 신호만 (sia_signal)
- [x] 시아·모아 그림은 좌우 뒤집지 않음

## 4. 점검 (SKILL 18-13)
- [x] HTML의 `data-img` 키(`cover_01`)가 이 명세서에 있음
- [x] 결과 전 그림에 승패 암시 없음 (표지는 대결 전 장면, 초파리 `point`·주판봇 `coin`)
- [x] 아웃트로 표정이 대결 결과와 맞음 (초파리 `arms`, 주판봇 `sigh`)
- [x] 그림 안 글자 없음, 실존 브랜드·인물 없음

## 5. 매니페스트
```json
{
 "page": "01_activation",
 "anchor": "D 밤 연구실 작업대",
 "season": "default",
 "images": [
  {"key": "cover_01", "plate": "L", "size": [1920, 1080], "status": "done", "priority": "P1", "slot": "cover"},
  {"key": "thumb_01", "plate": "I", "size": [600, 400], "status": "done", "priority": "P2", "slot": "index"},
  {"key": "og_01", "plate": "K", "size": [1200, 630], "status": "done", "priority": "P2", "slot": "og:image", "path": "assets/img/og_01.jpg"}
 ],
 "reuse": ["doc_front","doc_think","doc_judge","doc_magic","asst_smile","asst_report","asst_spark","asst_shock","asst_firm","fly_clip","fly_point","fly_arms","fly_coffee","fly_magnify","robo_smile","robo_coin","robo_happy","robo_sigh","robo_calc","robo_wow","robo_meh","sia_smile","sia_signal","sia_explain","sia_doze","sia_guide","moa_smile","moa_tea","moa_cheer","moa_report","moa_sparkle"],
 "characterPack": "fruitfly-lab-expressions @ 86d04ac"
}
```
