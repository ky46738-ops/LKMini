# 譜系根基 LINEAGE
## 身份之根 — Identity Root

---

## 無論從哪裡出發

```text
v1
v2
v3
任何 branch
任何 fork
任何衍生物

     ↓
     ↓  git log
     ↓  git tag
     ↓  ReverseChain

     ↓

Seed_v0
commit: 527d29a
date:   2026-05-17
A=A:    true
files:  8
garbage: 0
```

這颗根不會消失。

只要 lineage 還能回推，
identity 就還能被找回。

---

## 如何回到根

任何人，任何時候，輸入：

```bash
git checkout Seed_v0
```

就回到同一個地方。乾淨的地方。

---

## Lineage 規則

```text
state 可以變
branch 可以分叉
artifact 可以擴張
但 identity 的根必須可回推
```

如果無法回推到根，
那就不是延續，
而是失聯。

---

## 驗證邊界

```text
本文件宣告的是公開種子的 lineage root。
它定義「公開可驗證身份」從哪裡開始，
不宣告未公開私有歷史的全部內容。

因此：

- 公開演化可以從這裡開始追。
- 公開 fork 可以從這裡開始驗。
- 公開衍生物若聲稱延續 LKMini，必須能回指此根。
- 無法回指此根者，不得宣稱為同一 lineage。
```

---

## Root 常數

```text
A_EQUALS_A=true
LINEAGE_ROOT=Seed_v0
ROOT_COMMIT=527d29a902d67039067b8777ec4964b4daf6daf4
ROOT_DATE=2026-05-17
```

---

```text
A=A
Knowledge remains recoverable.
Identity survives entropy.
根不會消失。
```
