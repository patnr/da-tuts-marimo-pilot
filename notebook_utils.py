"""Shared display helpers for the marimo notebooks."""
import marimo as mo


# TODO: this can probably be significantly improved
# as it was sloppily generated based on `interact()`
# which itself is a little sloppy.
def hookup(controls, plot_fn, *, top=None, right=None, bottom=None, left=None,
           wrap=False, justify="start"):
    """Bundle a mo.ui.dictionary's widgets around the plot they drive.

    With no side arguments (the common case), all controls go on top:
        hookup(controls, plot_fn)
    is equivalent to:
        mo.vstack([mo.hstack(list(controls.values()), wrap=wrap, justify=justify),
                   plot_fn(**controls.value)])

    To place specific controls elsewhere, pass `top`/`right`/`bottom`/`left` as
    `True` (claim all controls not yet claimed by an earlier side), a
    comma-separated string of `controls` keys, or a list of keys, e.g.:
        hookup(controls, plot_fn, bottom="seed,analyses_only", right=["logR"])
    Controls not claimed by any side default to `top`.

    Unlike `resources/__init__.py:interact` (the ipywidgets analogue this is
    modeled on), groups are flat (no nested sub-boxes) and per-widget styling
    isn't supported -- not needed for this notebook's widget counts.
    """
    remaining = dict(controls.items())

    def pop(labels):
        if not labels:
            return []
        if labels is True:
            ww = list(remaining.values())
            remaining.clear()
            return ww
        if isinstance(labels, str):
            labels = [s.strip() for s in labels.split(",")]
        return [remaining.pop(key) for key in labels]

    on = {side: pop(labels) for side, labels in
          dict(top=top, right=right, bottom=bottom, left=left).items()}
    on["top"] += list(remaining.values())  # unclaimed controls default to top

    out = plot_fn(**controls.value)
    if on["left"] or on["right"]:
        out = mo.hstack(
            [w for w in (mo.vstack(on["left"]) if on["left"] else None,
                         out,
                         mo.vstack(on["right"]) if on["right"] else None)
             if w is not None],
            justify=justify,
        )

    rows = [mo.hstack(on["top"], wrap=wrap, justify=justify)] if on["top"] else []
    rows.append(out)
    if on["bottom"]:
        rows.append(mo.hstack(on["bottom"], wrap=wrap, justify=justify))
    return mo.vstack(rows)
