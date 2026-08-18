# DA-tuts marimo pilot

A pilot conversion of 4 of the 9 [DA-tutorials](https://github.com/nansencenter/DA-tutorials)
notebooks (T1&ndash;T4) from Jupyter/Colab to [marimo](https://marimo.io) &mdash;
evaluating marimo as a durable, self-contained replacement for Colab.

## Inspect what students would see

`docs/` is a pre-built, self-contained, **editable and re-runnable** WASM
export (`--mode edit`) &mdash; no server, no install, no login. Serve it
locally and open in a browser:

```
python -m http.server --directory docs
```

then visit `http://localhost:8000`. After opening a notebook, cells don't
auto-run (a marimo WASM quirk) &mdash; press Cmd/Ctrl+K, type "run all", Enter.

## Source

- `T1.py`&ndash;`T4.py` &mdash; the marimo notebooks (plain Python, PEP 723 inline
  dependencies at the top of each file).
- `answers_data.py` &mdash; ported exercise answers (41 of the repo's 140).
- `public/` &mdash; media assets (image/video) referenced by T1.

## Edit live

```
uv venv .venv && source .venv/bin/activate
uv pip install "marimo>=0.24.0" numpy scipy matplotlib
marimo edit
```

## Known limitations (pilot, not production)

- Only T1&ndash;T4 are converted; T5&ndash;T9 remain.
- T1's DAPPER/EnKF example section is removed for now: `dapper==1.7.3` fails
  to install inside the WASM/Pyodide export (a `dill` version-pin conflict) --
  everything else in T1 runs fine.
- Cross-notebook navigation (the `docs/index.html` landing page) is hand-built
  for this pilot; marimo has no built-in multi-notebook site feature.
- T3 imports directly from T2 via marimo's `App.embed()` API (runs T2.py and
  reads its `.defs`) rather than a separately-maintained module &mdash; the
  intended long-term pattern for T5/T7/T8 (which depend on T2) and T5 (which
  also depends on T3).
- Cells meant to be hidden (answer reveals, widget setup) render as a
  translucent, read-only code preview rather than being fully invisible, in
  this editable (`--mode edit`) export &mdash; a known, currently-open marimo
  limitation ([marimo#5244](https://github.com/marimo-team/marimo/issues/5244)).
  The alternative, `--mode run`, hides code cleanly but isn't editable at
  all, so this pilot prioritizes editability.
