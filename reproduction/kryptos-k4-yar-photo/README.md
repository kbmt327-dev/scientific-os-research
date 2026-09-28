# Kryptos K4: the YAR shift and the extra L on public photos (EP-0139)

Rerun package for the Open Research Lab note
*Are the raised letters and the extra L deliberate marks or construction offsets?*

```sh
python verify_yar_photo.py   # needs numpy, under a second
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_yar.py` | The pre-registered statistic and classes for the YAR shift, ported from the author's audit script (committed there before any letter was measured) |
| `results/yar-measurements-20260927.json` | Letter bounding boxes read from two public photos, rows 13-15, columns 0-10 (pixel numbers only; no image is stored) |
| `results/yar-result-20260927.json` | The recorded residuals, classes and verdicts, with the two design errors found after measuring |
| `verify_yar_photo.py` | Recomputes residuals and classes from the measurements and prints `PASS` |
| `make_figure.py` | The Note's figure |

The photos are Jim Gillogly's `ciphermidleft.jpg` (viewed only, © Gillogly) and Carol M.
Highsmith's Library of Congress photo 2011631531 (public domain, full size through IIIF). The
package contains no image and no carved text; columns are indices within the carved row.

## Not rerun here

The measurement itself (reading edges on the photos). The extra L was not measured: no public
photo shows that tableau row whole at usable resolution.

Units: residuals are in the pre-registered pitch P, which includes the seam gap and is
1.25-1.34 times the in-plate pitch (11.7 cm), so the centimetre values use the in-plate pitch.
A rerun of the author's code, not an independent replication.
