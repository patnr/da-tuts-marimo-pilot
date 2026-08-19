"""Shared display helpers for the marimo notebooks."""
import marimo as mo


def linkup(controls, plot_fn, *, wrap=False, justify="start"):
    """Bundle a mo.ui.dictionary's widgets with the plot they drive.

    Equivalent to:
        mo.vstack([mo.hstack(list(controls.values()), wrap=wrap, justify=justify),
                   plot_fn(**controls.value)])
    """
    return mo.vstack([
        mo.hstack(list(controls.values()), wrap=wrap, justify=justify),
        plot_fn(**controls.value),
    ])
