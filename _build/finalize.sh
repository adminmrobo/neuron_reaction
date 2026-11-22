#!/bin/bash
# 빌드 → 지식 색인 조립 → 금지 표현 치환
set -e
cd /home/claude/build
RS=/root/.claude/skills/synced/5c4cdcbd-c458-458b-abad-45cd67676395_f15a0a16-6ee9-44d8-9ec7-5b168737f051/ai-lab-retrofit
python3 gen_kg.py >/dev/null
for p in 01:01_activation 02:02_reaction_race 03:03_backprop index:index; do s=${p%%:*}; o=${p##*:}; python3 build.py src/$s.html out/$o.html >/dev/null; done
python3 build.py src/practice.html out/practice/index.html >/dev/null
for o in 01_activation 02_reaction_race 03_backprop; do
  python3 $RS/tools/retrofit.py out/$o.html --kg kg/$o/kg.json --refs kg/$o/refs.json --meta kg/$o/meta.json --backbone $RS/data/backbone_ai.json -o out/$o.kg.html >/dev/null
  python3 $RS/tools/check.py out/$o.html out/$o.kg.html --backbone $RS/data/backbone_ai.json --registry $RS/data/KG_00_registry.json --report kg/$o/check_report.md >/dev/null
  grep -A0 '^## 오류' kg/$o/check_report.md
  python3 - out/$o.kg.html <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
for a,b in [('사다리 경로','개념 순서 경로'),('사다리 사슬','개념 순서 사슬'),('// 칸 수 계산','// 항목 수 계산'),('(빈칸으로 둠)','(공란으로 둠)'),('loc 칸이','loc 항목이')]: s=s.replace(a,b)
open(p,'w').write(s)
PY
done
echo built
