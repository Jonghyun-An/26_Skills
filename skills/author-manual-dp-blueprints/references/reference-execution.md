# 기준 실행과 재현 근거

이 문서는 스킬을 추출한 실제 실행의 근거와 재발 방지 패턴이다. 새 도메인의 성능 근거로 인용하지 말고, workflow 품질과 검증 깊이의 기준으로만 사용하라.

## 사용자 지시를 실행 계약으로 바꾼 방식

| 사용자 의도 | 실제 실행 규칙 |
|---|---|
| 각 DP가 똑같이 생기지 않게 | SVG 전에 7차원 topology fingerprint를 동결하고 A/B 및 merged archetype을 portfolio 단위로 비교 |
| 1안과 2안은 양립 불가능 | 단일 authority axis, sole writer/artifact, forbidden mechanism 0, dual-writer contradiction으로 XOR 증명 |
| 한땀한땀 SVG로 | generator와 공통 skeleton 없이 후보별 XML, 좌표, path를 `apply_patch`로 직접 작성 |
| 1부터 6까지 순차적으로 | topic → A → A 검증 → B → B 검증 → compare → gate를 닫은 뒤 다음 DP 시작 |
| QA로 trade-off | 같은 input/output와 같은 QA scenario에서 gain/loss를 비교하고 accepted loss와 reversal evidence 기록 |
| 타당성·신뢰성 검증 | failure injection, semantic/XOR review, Chromium 원본 render, visual review, SHA-256 freeze 수행 |

## 기준 실행 결과

- 6개 DP × A/B/compare = 18개 hand-authored vector SVG
- 12개 candidate fingerprint와 6개 서로 다른 merged archetype
- 6개 순차 gate와 SVG/PNG 36개 frozen hash
- Chromium 1920×1080 원본 render 18개
- 최종 visual portfolio 95/100, 최저 artifact 91/100, P0=0, P1=0
- generator 및 shared coordinate skeleton 0

기준 저장소에서는 `design/manual-dp-blueprints/` 아래에 README, Decision Record, 18개 SVG, 6개 gate, 원본 render를 분리해 두었다.

## 실제 설계 순서

1. 기존 template package와 분리된 새 폴더를 만들었다.
2. 그림 전에 6개의 narrow authority axis와 neighbor boundary를 정했다.
3. 각 A/B의 sole writer, artifact, forbidden mechanism을 먼저 기록했다.
4. boundary grammar부터 failure route까지 7차원 fingerprint를 SVG 전에 동결했다.
5. A를 완성·검증한 뒤 B를 빈 캔버스에서 그렸다.
6. 병합판이 상세 topology를 보존하는지 확인했다.
7. DP gate를 닫은 뒤에만 다음 DP로 넘어갔다.
8. 마지막에 18개 원본 SVG를 portfolio 단위로 다시 비교했다.

같은 BP 슬라이드 느낌은 title, contract rail, assessment panel, QA 표라는 정보 문법에서 만들었다. 각 DP가 다르게 보이는 것은 state ownership과 failure causality가 만든 topology로 해결했다.

## 기준 topology archetype

| DP | Candidate A | Candidate B | Compare composition |
|---|---|---|---|
| DP1 | governed catalog hub와 dependency spokes | request compiler conveyor와 immutable plan store | hub versus conveyor |
| DP2 | whole-manifest barrier와 parallel fan-out | append-only prefix staircase와 terminal suffix | stacked time bands |
| DP3 | nested template/slot occupancy | constraint-variable graph와 solver loop | hierarchy versus graph bridge |
| DP4 | selected-slide surgical CAS lane | deck 2PC chamber와 participant vote fan-in | asymmetric commit radii |
| DP5 | deterministic evidence funnel | user risk workspace와 pending loop | shared case file와 security wall |
| DP6 | server event switchyard와 durable rail | browser reducer ring | ownership fault plane |

이 archetype을 새 도메인의 템플릿으로 복사하지 마라. 서로 다른 state transition과 failure shape가 어떤 시각 구조를 만드는지를 보여주는 예로만 사용하라.

## 독립 리뷰에서 실제로 발견한 결함

- connector가 label을 통과함
- flow badge가 path 또는 텍스트를 가림
- 13px 핵심 artifact text가 원본에서 약함
- 긴 canonical artifact명이 polygon 밖으로 넘침
- failure, audit, replay path가 같은 corridor를 공유해 causality가 모호함
- 축소 preview artifact를 원본 SVG 결함으로 오인할 위험

모든 수정 뒤에는 원본 SVG를 다시 렌더하고 SVG/PNG hash를 갱신했다. reduced preview가 아니라 1920×1080 원본 render를 판정 근거로 사용했다.

## 재사용 판정 기준

새 결과가 다음 조건을 만족하면 기준 실행의 방식을 재현한 것으로 본다.

- 각 후보가 독립된 sole writer와 artifact를 가진다.
- 후보가 서로를 포함하거나 fallback으로 호출하지 않는다.
- 같은 DP의 A/B topology fingerprint가 7차원 중 최소 5개 다르다.
- 전체 DP의 merged archetype이 반복되지 않는다.
- accepted loss, mitigation boundary, reversal evidence가 모두 보인다.
- 원본 render에서 P0=0, P1=0이다.
