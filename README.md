# DA-tuts marimo pilot

A pilot conversion of 4 of the 9 [DA-tutorials](https://github.com/nansencenter/DA-tutorials)
notebooks (T1&ndash;T4) from Jupyter/Colab to [marimo](https://marimo.io) &mdash;
evaluating marimo as a durable, self-contained replacement for Colab.

## Inspect what students would see

`site/` is a pre-built, self-contained WASM export &mdash; no server, no
install, no login. Serve it locally and open in a browser:

```
python -m http.server --directory site
```

then visit `http://localhost:8000`.

## Source

- `T1.py`&ndash;`T4.py` &mdash; the marimo notebooks (plain Python, PEP 723 inline
  dependencies at the top of each file).
- `answers_data.py` &mdash; ported exercise answers (41 of the repo's 140).
- `public/` &mdash; media assets (image/video) referenced by T1.

## Edit live

```
uv venv .venv && source .venv/bin/activate
uv pip install "marimo>=0.24.0" numpy scipy matplotlib "dapper==1.7.3"
marimo edit
```

## Known limitations (pilot, not production)

- Only T1&ndash;T4 are converted; T5&ndash;T9 remain.
- T1's `dapper` import currently fails inside the WASM/Pyodide export (a
  `dill` version-pin conflict) &mdash; everything else in T1 runs fine.
- Cross-notebook navigation (the `site/index.html` landing page) is hand-built
  for this pilot; marimo has no built-in multi-notebook site feature.
- T3 imports directly from T2 via marimo's `App.embed()` API (runs T2.py and
  reads its `.defs`) rather than a separately-maintained module &mdash; the
  intended long-term pattern for T5/T7/T8 (which depend on T2) and T5 (which
  also depends on T3).
