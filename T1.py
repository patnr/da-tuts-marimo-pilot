# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.24.0",
#     "numpy",
#     "matplotlib",
# ]
# ///
import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    from answers_data import show_answer

    return mo, show_answer


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # T1 - Introduction

    *Copyright (c) 2020, Patrick N. Raanes*

    This tutorial series introduces *data assimilation (DA)*, beginning with basic mathematical concepts and culminating in your own implementation of the EnKF.
    Alternatively, the article by [Wikle and Berliner (2007)](#References) is short and nice,
    while the book by [Asch, Bocquet, and Nodet (2016)](#References) is rigorous and detailed.

    ## Jupyter

    The "document" you're currently reading is a *marimo notebook*
    (originally: a *Jupyter notebook*).
    It consists of a sequence of **cells**, which can be either code (Python) or text (markdown).
    For example, try editing the cell below (double-click it)
    to insert your name, and running it.
    """)
    return


@app.cell
def _():
    name = "Batman"
    print("Hello world! I'm " + name)
    for i, c in enumerate(name):
        print(i, c)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Knowing these **keyboard shortcuts** will help you work more efficiently:

    | Navigate                      | Edit              | Exit           | Run                              | Run & go to next                  |
    |-------------------------------|-------------------|----------------|----------------------------------|-----------------------------------|
    | <kbd>↓</kbd> and <kbd>↑</kbd> | <kbd>Enter</kbd>  | <kbd>Esc</kbd> | <kbd>Ctrl</kbd>+<kbd>Enter</kbd> | <kbd>Shift</kbd>+<kbd>Enter</kbd> |

    Each notebook connects to a background **session (kernel/runtime/interpreter)** of Python.
    marimo notebooks are *reactive*: unlike classic Jupyter, all code cells in a given notebook
    are connected by their actual variable dependencies (not just cell position), and marimo
    automatically re-runs every cell that depends on something you changed -- so, unlike Jupyter,
    "I ran cells out of order and now nothing matches" mostly stops being possible.

    <mark><font size="-1">
    Migration note: the original tutorial's first code cell was a Colab-bootstrap
    (<code>!wget ... | bash</code>) that pip-installed requirements and copied the repo's
    <code>notebooks/</code> folder into the Colab runtime. marimo notebooks need no such step --
    dependencies are just declared once for the whole notebook (e.g. inlined
    <code>/// script</code> metadata, or a venv like this pilot's), so this hack disappears entirely.
    </font></mark>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Python

    There is a huge amount of libraries available in **Python**, including the popular `scipy` and `matplotlib` packages, both with the essential `numpy` library at their core. They're usually abbreviated `sp`, `mpl` (and `plt`), and `np`. Try them out by running the following cell.
    """)
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    plt.ion()

    a = np.arange(10)  # Alternatively: np.array([0,1,2,3,4,5,6,7,8,9])
    I = 2 * np.eye(10)  # Alternatively: np.diag(2*np.ones(10))

    print("Indexing examples:")
    print("a        =", a)
    print("a[3]     =", a[3])
    print("a[1:3]   =", a[0:3])
    print("a[-1]    =", a[-1])
    print("I[:3]    =", I[:3], sep="\n")

    print("\nLinear algebra examples:")
    print("100+a =", 100 + a)
    print("I@a   =", I @ a)
    print("I*a   =", I * a, sep="\n")

    plt.title("Plotting example")
    plt.ylabel("i $x^2$")
    for _i in range(4):
        plt.plot(_i * a**2, label="i = %d" % _i)
    plt.legend()
    plt.gca()
    return np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    These tutorials require that you are able to understand the above code, but not much beyond that.
    Some exercises will ask you to do some programming, but understanding the pre-written code is also important.
    The interesting parts of the code can all be found in the notebooks themselves
    (as opposed to being hidden away via imports).
    Beware, however, that it is not generally production-ready.
    For example, it overuses global variables, and is lacking in vectorisation,
    generally for the benefit of terseness and simplicity.

    ## Dynamical and observational models

    What is a ***model***?
    In the broadest sense, a model is a *simplified representation* of something.
    Whether it be some laws of nature, or comprising of a set of empirical or statistical relations,
    the underlying aim is usually that of making **predictions** of some sort.
    A convenient language for this purpose is mathematics,
    in which case the model consists of a set of equations, often differential.

    We will mainly be concerned with models of **dynamical systems**, meaning *stuff that changes in time*.
    The "stuff", denoted $\mathbf{x}_k$ for time index $k$, will be referred to as ***state*** variables/vectors.
    Regardless of sophistication or how many PhDs worked on coding it up as a computer simulation program,
    the ***dynamical model*** will henceforth be represented simply as the *function* $\mathscr{M}_k$
    that **forecasts** (predicts) the state at time $k+1$ from $\mathbf{x}_k$.

    Examples include

    - (a) Laws of motion and gravity (Newton, Einstein)
    - (b) Epidemic (SEIR) and predator-prey (Lotka-Volterra)
    - (c) Weather/climate forecasting (Navier–Stokes + thermodynamics + ideal gas law + radiation + cloud microphysics + BCs)
    - (d) Petroleum reservoir flow (Multiphase Darcy's law + ...)
    - (e) Chemical and biological kinetics (Arrhenius, Michaelis-Menten, Mass Action Law)
    - (f) Traffic flow (Lighthill-Whitham-Richards)
    - (g) Sports rating (Elo, Glicko, TrueSkill)
    - (h) Financial pricing (Black-Scholes)

    **Exc (optional) – state variables:**

    - For the above model examples above that you are familiar with, list the elements of the state variable.

    - Generally speaking, do you think
      - the ordering of the elements/components matters?
      - the state vector needs to be of fixed length, or can it change over time?
      - it is problematic if we include more variables than needed?
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("state variables")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A model is usually assessed in terms of (some measure of) skill of prediction,
    as expressed by the following maxim.

    > All models are wrong, but some are useful – [George E. P. Box](https://en.wikipedia.org/wiki/All_models_are_wrong)

    **Exc (optional) – model error:**
    For each of model examples above, select the shortcomings (below) that seem relevant.

    1. Inaccurate at relatively high speeds
    1. Extreme events do not conform to statistical assumptions
    1. Assumes closed systems, ignoring external influences,
       except for poorly specified boundary conditions and forcings
    1. Assumes equilibrium or steady-state when systems are inherently dynamic
    1. Lack of demographic and/or geographic resolution.
    1. Continuity is an approximation
    1. Oversimplification of complex interactions and feedbacks
    1. Incompatibility with quantum dynamics
    1. Insufficient spatial or temporal resolution upon discretization
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("model error")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Taking the quoted advice to heart, in data assimilation it is common to assume that
    the difference between the true evolution and that suggested by the model alone is explained
    by a random (stochastic) noise term, $\mathbf{q}_k$, with a known distribution, i.e.

    $$ \mathbf{x}_{k+1} = \mathscr{M}_k(\mathbf{x}_k) + \mathbf{q}_k \,. \tag{DynMod} $$

    However, a good model (i.e. $\mathbf{q} \approx 0$) is not enough to ensure good predictions, because

    > Garbage in, garbage out ([GIGO](https://en.wikipedia.org/wiki/Garbage_in,_garbage_out))

    In other words, we also need accurate initial conditions,
    i.e. a good estimate of $\mathbf{x}_k$.
    This is known as the ***forecast initialisation*** problem.
    It may seem obvious and trifling if $\mathbf{x}_k$ is some experimental condition that is
    completely in our control, or if $\mathbf{x}_k$ is a computable steady-state condition of the system
    (to wit, typically in both cases, $k=0$).
    But it is not so easy to determine $\mathbf{x}_k$ when it is the state of an ongoing, constantly-evolving process,
    and/or if we have only very limited observations of it.
    For example, consider the case of numerical weather prediction (NWP).
    Clearly, in order to launch the numerical simulator (model), $\mathscr{M}_k$,
    to forecast (predict) *tomorrow*'s weather,
    we initially need to know *today*'s state of the atmosphere (wind, pressure, density and temperature)
    at each grid point in the model.
    Yet despite the vast increase in data since the advent of weather satellites in the 1970s,
    most parts of the globe are (at any given moment) unobserved.
    Moreover, the ***measurement/observation data*** available to us, $\mathbf{y}_k$, are not generally a "direct observation"
    of quantities in the state vector, but rather some function, i.e. model thereof, $\mathscr{H}_{\!k}$
    (in the case of satellite radiances: an integral along the vertical column at some lat/long location,
    or even a more complicated radiative transfer model).
    Finally, since any measurement is somewhat imprecise,
    we include an observation noise, $\mathbf{r}_k$, in our conception of the measuring process, i.e.

    $$ \mathbf{y}_k = \mathscr{H}_{\!k}(\mathbf{x}_k) + \mathbf{r}_k \,. \tag{ObsMod} $$

    **Exc (optional) – observation examples:**
    For each of the above dynamical model examples, suggest 1 or more observation kinds (i.e. what will $\mathbf{y}$ consist of?).
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("obs examples")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data + Models = ❤️

    The above complications make the forecast initialisation problem daunting.
    Fortunately we have another source of information on $\mathbf{x}_k$: yesterday's (or the previous) forecast.
    As we will see, using it as a "prior" in the estimation of $\mathbf{x}_k$ will implicitly
    incorporate the information from *previous* observations, $\mathbf{y}_1, \ldots, \mathbf{y}_{k-1}$,
    on top of the "incoming" one, $\mathbf{y}_k$.
    Thus, model forecasts help out the data, $\mathbf{y}_k$, in the estimation of $\mathbf{x}_k$,
    which in turn improve the forecast of $\mathbf{x}_{k+1}$, and so on in a *virtuous cycle* of improved estimation and prediction (❤️).

    The *cyclic* computational procedure outlined above for the sequence of forecast initialisation problems is known as **filtering**.
    More generally, the theory of **state estimation** (a.k.a. **sequential inference**)
    also includes the techniques of **smoothing** (the estimation of *earlier* states)
    and – as an add-on – the estimation of parameters (uncertain/unknown quantities that do *not* change in time).
    State estimation can be said to generalize [time series estimation](https://www.google.no/books/edition/Time_Series_Analysis_by_State_Space_Meth/XRCu5iSz_HwC)
    and [signal processing](https://ocw.mit.edu/courses/6-011-introduction-to-communication-control-and-signal-processing-spring-2010/0009cae26d5218d6ebae14297d111325_MIT6_011S10_chap04.pdf),
    by allowing for multivariate, hidden states (partially observed, or only through the operator $\mathscr{H}$),
    and adding the sophistication (and computational burden) of the predictive model $\mathscr{M}$.

    The most famous state estimation technique is the ***Kalman filter (KF)***,
    which was developed to steer the Apollo mission rockets to the moon.
    To wit, in guidance systems, the *state variable* (vector) consists of at least 6 elements: 3 for the current position and 3 for velocity, whose trajectories we wish to track in time. More sophisticated systems can also include acceleration and/or angular quantities. The *dynamical model* then consists of the fact that displacement is the time integral of the velocity, while the velocity is the integral of acceleration, which can be determined from Newton/Einstein's laws of gravity as well and the steering controls of the vessel. The noisy *observations* can come from altimetry, sextants, speedometers, compass readings, accelerometers, gyroscopes, or fuel-gauges. The essential point is that we have an *observational model* predicting the observations from the state. For example, the altimeter model is simply the function that selects the $z$ coordinate from the state vector, while the force experienced by an accelerometer can be modelled by Newton's second law of motion.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Migration note: the original placed this <img align="right" ...> tag
    # inline within the surrounding markdown paragraph, floating beside the
    # text. mo.image() doesn't support float-beside-text layout, so this pilot
    # promotes it to its own cell -- a minor layout-fidelity loss to flag.
    mo.image(
        src="public/DA_bridges.jpg",
        width=400,
        caption='DA "bridges" data and models. Source: AICS-Riken.',
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the context of *large* dynamical systems, especially in geoscience (climate, ocean, hydrology, petroleum)
    state estimation is known as **data assimilation** (DA),
    and is seen as a "bridge" between data and models,
    as illustrated above (source: [AICS-Riken](https://aics.riken.jp/en)).
    For example, in weather applications, the dynamical model is an atmospheric fluid-mechanical simulator, the state variable consists of the fields of pressure, humidity, and wind quantities discretized on a grid,
    and the observations may come from satellite or weather stations.

    But when the KF was first proposed for DA (specifically, weather forecasting), the idea seemed ludicrous due to
    several technical challenges in DA compared to "classic" state estimation:

    - size of data and models;
    - nonlinearity of models;
    - sparsity and inhomogeneous-ness of data.

    Some of these challenges may be recognized in the video below. Can you spot them?
    """)
    return


@app.cell
def _(mo):
    # Migration note: the original `envisat_video()` helper manually
    # base64-encoded the mp4 and wrote a raw <video> HTML tag (to sidestep
    # the fact that Jupyter/Colab can't otherwise embed local video files).
    # marimo's `mo.video()` does exactly that encoding step natively --
    # this hack disappears into a single builtin call.
    mo.vstack([
        mo.video(src="public/darc_envisat_analyses.mp4", width=580),
        mo.md("""
        Illustration of DA for the ozone layer in 2002.<br><br>
        LEFT: Satellite data (i.e. all that is observed).
        RIGHT: Simulation model with assimilated data.<br><br>
        Could you have perceived the
        [splitting of the ozone hole](http://dx.doi.org/10.1175/JAS-3337.1)
        only from the satellite data?<br><br>
        Attribution: William A. Lahoz, DARC.
        """),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The ensemble Kalman filter (EnKF)

    The EnKF is a Monte-Carlo formulation of the KF
    resulting in a simple and versatile method for DA,
    that manages (to some extent) to deal with the above challenges in DA.
    For those familiar with the method of 4D-Var, **further advantages of the EnKF** include it being:

    - Non-invasive: the models are treated as black boxes, and no explicit Jacobian is required.
    - Bayesian:
      - provides ensemble of possible realities;
        - arguably the most practical form of "uncertainty quantification";
        - ideal way to initialize "ensemble forecasts";
      - uses "flow-dependent" background covariances in the analysis.
    - Embarrassingly parallelizable:
      - distributed across realizations for model forecasting;
      - distributed across local domains for observation analysis.

    ## DAPPER example

    This tutorial builds on the underlying package, [DAPPER](https://github.com/nansencenter/DAPPER), made for academic research in DA and its dissemination. At the end of these tutorials, you should be able to reproduce (from the ground up) this type of experiment.

    <mark><font size="-1">
    Migration note: this section (running a small `DAPPER/example_1.py`-style
    EnKF experiment) is temporarily removed from this pilot. `dapper==1.7.3`
    fails to install in marimo's WASM/Pyodide export -- a version-pin conflict
    (`dapper` requires `dill>=0.4.1`, Pyodide ships `dill==0.3.8`, and
    micropip's default install mode won't upgrade an already-installed
    package). This is a cheap fix on the DAPPER side (relax or test the pin
    against 0.3.8), not attempted here; until then, this section is dropped so
    the rest of the notebook runs cleanly.
    </font></mark>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Vocabulary exercises

    **Exc – Word association:**
    Group the words below into 3 groups of similar meaning.

    `Sample, Random, Measurements, Ensemble, Data, Stochastic, Monte-Carlo, Observations, Set of draws`
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("thesaurus 1")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - "The answer" is given from the perspective of DA. Do you agree with it?
    - Can you describe the (important!) nuances between the similar words?

    **Exc (optional) – Word association 2:**
    Also group (and nuance!) these words, by filling in the `x`s in the list below.

    `Inverse problems, Operator, Sample point, Transform(ation), Knowledge, Relation, Probability, Mapping, Particle, Sequential, Inversion, Realization, Relative frequency, Information, Iterative, Estimate, Estimation, Single draw, Serial, Regression, Model, Fitting, Uncertainty`

    - Statistical inference, x, x, x, x, x
    - Ensemble member, x, x, x, x
    - Quantitative belief, x, x, x, x, x, x
    - Recursive, x, x, x
    - Function, x, x, x, x, x
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("thesaurus 2")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exc (optional) – intro discussion:** Prepare to discuss the following questions. Use any tool at your disposal.

    - (a) What is DA?
    - (b) What is the difference between "state variables" and "parameters"?
    - (c) What are "prognostic" variables?
      How do they differ from "diagnostic" variables?
    - (d) $k$ is the time index, but what determines the times they correspond to?
    - (e) Is DA a science, an engineering art, or a dark art?
    - (f) What is the point of "Hidden Markov Models"?
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("Discussion topics 1")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Next: T2 - Gaussian distribution

    <a name="References"></a>

    ### References

    - **Wikle and Berliner (2007)**:
      C. K. Wikle and L. M. Berliner, "A Bayesian tutorial for data assimilation", Physica D, 2007.
    - **Asch, Bocquet, and Nodet (2016)**:
      Mark Asch, Marc Bocquet, and Maëlle Nodet, "Data assimilation: methods, algorithms, and applications", 2016.
    """)
    return


if __name__ == "__main__":
    app.run()
