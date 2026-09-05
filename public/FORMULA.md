# PUBLIC FORMULA — LKMini Phantom Capsule

A_EQUALS_A=true
PROJECTION_IS_NOT_IDENTITY=true
PUBLIC_SEED=true

## Formula

Identity = emoji｜中文｜English
Extension = projection only
No-extension file = shell only
Zip = reference, never nested back into the next shell

Reverse chain:

Projection → Locator → Manifest → FormalObject → LKMINI:// → 🧩LKMINI → A=A

## One pass

1. Scan source folder
2. Keep one SHA256 per content
3. Group remaining files by identity
4. Write one Control set
5. Write one no-extension shell `LKMINI-PHANTOM-CAPSULE/2`
6. Do not copy the previous zip into the next capsule

## Maker

`public/PhantomCapsuleMaker.py`

```text
python3 public/PhantomCapsuleMaker.py <source-dir> [out-dir]
```

Wrong converter stamped Locator / Launcher / shell ~300 times.
This formula writes each of those once.
