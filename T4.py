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
app = marimo.App(width="full", css_file="custom.css")


@app.cell
def _():
    import marimo as mo
    from answers_data import show_answer
    import numpy as np
    import numpy.random as rnd
    import matplotlib.pyplot as plt
    _ = plt.ion()  # named to avoid auto-displaying plt.ion()'s ExitStack repr
    return mo, np, plt, rnd, show_answer


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # T4 - Time series filtering

    Before exploring the full (multivariate) Kalman filter (KF),
    let's first consider scalar but time-dependent (temporal/sequential) problems.

    Consider the scalar, stochastic process $\{x_k\}$,
    generated for sequentially increasing time index $k$ by

    $$ x_{k+1} = \mathscr{M}_k x_k + q_k \,. \tag{DynMod} $$

    For our present purposes, the **dynamical "model"** $\mathscr{M}_k$ is simply a known number.
    Suppose we get observations $\{y_k\}$ as in:

    $$ y_k = \mathscr{H}_k x_k + r_k \,, \tag{ObsMod} $$

    The noises and $x_0$ are assumed to be independent of each other and across time
    (i.e., $\varepsilon_k$ is independent of $\varepsilon_l$ for $k \neq l$),
    and Gaussian with known parameters:
    $$
    x_0 \sim \mathscr{N}(x^{\text{a}}_0, P^{\text{a}}_0),\quad
    q_k \sim \mathscr{N}(0, Q_k),\quad
    r_k \sim \mathscr{N}(0, R_k) \,.
    $$

    ## Example problem: AR(1)

    For simplicity (though the KF does not require these assumptions),
    suppose that $\mathscr{M}_k = \mathscr{M}$, i.e., it is constant in time.
    Then $\{x_k\}$ forms a so-called order-1 auto-regressive process.
    Similarly, we drop the time dependence (subscript $k$) from $\mathscr{H}_k, Q_k, R_k$.
    The code below simulates a random realization of this process.
    """)
    return


@app.cell
def _(np, rnd):
    # Use H=1 so that it makes sense to plot data on the same axes as the state.
    H = 1

    # Initial estimate
    xa0 = 0   # mean
    Pa0 = 10  # variance

    def simulate(nTime, xa, Pa, M, H, Q, R):
        """Simulate synthetic truth (x) and observations (y)."""
        x = xa + np.sqrt(Pa)*rnd.randn()        # Draw initial condition
        truths = np.zeros(nTime)                # Allocate
        obsrvs = np.zeros(nTime)                # Allocate
        for k in range(nTime):                  # Loop in time
            x = M * x + np.sqrt(Q)*rnd.randn()  # Dynamics
            y = H * x + np.sqrt(R)*rnd.randn()  # Measurement
            truths[k] = x                       # Assign
            obsrvs[k] = y                       # Assign
        return truths, obsrvs

    return H, Pa0, simulate, xa0


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following code plots the process. *You don't need to read or understand it*.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # A `mo.ui.dictionary` bundles several widgets into one variable: `.value`
    # gives back a dict of their values, so the consumer cell can just do
    # `exprmt(**controls.value)` -- much less boilerplate than one variable
    # (and one return-tuple entry) per widget. Not displayed here -- the
    # plotting cell below displays the widgets and the figure together.
    controls = mo.ui.dictionary({
        "seed": mo.ui.slider(start=1, stop=12, step=1, value=4, show_value=True, label="seed"),
        "nTime": mo.ui.slider(start=0, stop=100, step=1, value=50, show_value=True, label="nTime"),
        "M": mo.ui.slider(start=0, stop=1.03, step=.01, value=0.97, show_value=True, label="M"),
        "logR": mo.ui.slider(start=-9, stop=9, step=1, value=1, show_value=True, label="logR"),
        "logQ": mo.ui.slider(start=-9, stop=9, step=1, value=1, show_value=True, label="logQ"),
        "logR_bias": mo.ui.slider(start=-9, stop=9, step=1, value=0, show_value=True, label="logR_bias"),
        "logQ_bias": mo.ui.slider(start=-9, stop=9, step=1, value=0, show_value=True, label="logQ_bias"),
        "analyses_only": mo.ui.checkbox(value=False, label="analyses_only"),
    })
    return (controls,)


@app.cell
def _(H, KF, Pa0, controls, mo, np, plt, rnd, simulate, xa0):
    def exprmt(seed, nTime, M, logR, logQ, analyses_only, logR_bias, logQ_bias):
        R, Q, Q_bias, R_bias = 4.0**np.array([logR, logQ, logQ_bias, logR_bias])

        rnd.seed(seed)
        truths, obsrvs = simulate(nTime, xa0, Pa0, M, H, Q, R)

        plt.figure(figsize=(9, 6))
        kk = 1 + np.arange(nTime)
        plt.plot(kk, truths, 'k' , label='True state ($x$)')
        plt.plot(kk, obsrvs, 'g*', label='Noisy obs ($y$)', ms=9)

        try:
            estimates, variances = KF(nTime, xa0, Pa0, M, H, Q*Q_bias, R*R_bias, obsrvs)
            if analyses_only:
                plt.plot(kk, estimates[:, 1], label=r'Kalman$^a$ ± 1$\sigma$')
                plt.fill_between(kk, *cInterval(estimates[:, 1], variances[:, 1]), alpha=.2)
            else:
                kk2 = kk.repeat(2)
                plt.plot(kk2, estimates.flatten(), label=r'Kalman ± 1$\sigma$')
                plt.fill_between(kk2, *cInterval(estimates, variances), alpha=.2)
        except NameError:
            pass

        plt.xlabel('Time index (k)')
        plt.legend(loc='upper left')
        plt.axhline(0, c='k', lw=1, ls='--')
        return plt.gca()

    mo.vstack([
        mo.hstack(list(controls.values()), wrap=True, justify="start"),
        exprmt(**controls.value),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <mark><font size="-1">
    Migration note: `cInterval` (a plotting helper for +/- 1-sigma confidence intervals) is
    ported directly below rather than imported from `resources/__init__.py`, since that
    module also carries the Colab-detection and other repo-wide setup this pilot isn't
    replicating. Also note `KF` is only defined in a *later* cell in this notebook -- as in
    T3, marimo's dependency graph resolves this by data dependency, not file position, so the
    `try/except NameError` below is dead code once `KF` exists; it's kept only because the
    exercise text still asks the student to "define KF, then re-run this cell" as a discrete
    step, even though marimo would already show a (nonsensical, since as-yet unimplemented)
    KF trace immediately.
    </font></mark>
    """)
    return


@app.function
def cInterval(mu, sigma2, flat=True):
    """Compute +/- 1-sigma (std.dev.) confidence/credible intervals (CI)."""
    import numpy as np
    s1 = np.sqrt(sigma2)
    a = mu - s1
    b = mu + s1
    if flat:
        return a.flatten(), b.flatten()
    return a, b


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exc – AR1 properties:** Answer the following.

    - What does `seed` control?
    - Explain what happens when `M=0`. Also consider $Q \rightarrow 0$.
      Can you give a name to this `truth` process?
      What about when `M=1`?
      Describe the general nature of the process as `M` changes from 0 to 1.
      What about when `M>1`?
    - What happens when $R \rightarrow 0$ ?
    - What happens when $R \rightarrow \infty$ ?
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("AR1")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The (univariate) Kalman filter (KF)

    Now we have a random variable that evolves in time, that we can *pretend* is unknown,
    in order to estimate (or "track") it.
    From above,
    $p(x_0) = \mathscr{N}(x_0 | x^{\text{a}}_0, P^{\text{a}}_0)$ with given parameters.
    We also know that $x_k$ evolves according to eqn. (DynMod).
    Therefore, as shown in the T2 exercise on algebra with random variables,
    $p(x_1) = \mathscr{N}(x_1 | x^{\text{f}}_1, P^{\text{f}}_1)$, with
    $$
    \begin{align}
    x^{\text{f}}_k &= \mathscr{M} \, x^{\text{a}}_{k-1} \tag{5} \\
    P^{\text{f}}_k &= \mathscr{M}^2 \, P^{\text{a}}_{k-1} + Q \tag{6}
    \end{align}
    $$

    Formulae (5) and (6) are called the **forecast step** of the KF.
    But when $y_1$ becomes available (according to eqn. (ObsMod)),
    we can update/condition our estimate of $x_1$, i.e., compute the posterior,
    $p(x_1 | y_1) = \mathscr{N}(x_1 \mid x^{\text{a}}_1, P^{\text{a}}_1)$,
    using the formulae we developed for Bayes' rule with Gaussian distributions (T3).

    $$
    \begin{align}
      P^{\text{a}}_k &= 1/(1/P^{\text{f}}_k + \mathscr{H}^2/R) \,, \tag{7} \\\
      x^{\text{a}}_k  &= P^{\text{a}}_k (x^{\text{f}}/P^{\text{f}}_k + \mathscr{H} y_k/R) \,.  \tag{8}
    \end{align}
    $$

    This is called the **analysis step** of the KF.
    We can subsequently apply the same two steps again
    to produce forecast and analysis estimates for the next time index, $k+1$.
    Note that if $k$ is a date index, then "yesterday's forecast becomes today's prior".

    In the case of linearity and Gaussianity,
    the KF of eqns. (5)-(8) computes the *exact* Bayesian pdfs for $x_k$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Migration note: see T3's equivalent note -- raw `<details>` HTML suppresses
    # KaTeX math rendering, so this "optional reading" aside is a `mo.accordion` here.
    mo.accordion({
        "But even without these assumptions, a general (abstract) Bayesian recursive procedure can still be formulated  ... (optional reading 🔍)": mo.md(r"""
    The following does relies only on the ("hidden Markov model") assumptions.

    - The analysis "assimilates" $y_k$ according to Bayes' rule to compute $p(x_k | y_{1:k})$,
    where $y_{1:k} = y_1, \ldots, y_k$ is shorthand notation.
    $$
    p(x_k | y_{1:k}) \propto p(y_k | x_k) \, p(x_k | x_{1:k-1}) \,.
    $$
    - The forecast "propagates" the uncertainty (i.e. density) according to the Chapman-Kolmogorov equation
    to produce $p(x_{k+1}| y_{1:k})$.
    $$
    p(x_{k+1} | y_{1:k}) = \int p(x_{k+1} | x_k) \, p(x_k | y_{1:k}) \, d x_k \,.
    $$

    The above recursive procedure, called ***filtering***, always computes $p(x_l | y_{1:k})$ with $l \geq k$.
    I.e. a filtering estimate only builds on *past* information.
    Recursive formulations are available, with ensemble formulations reviewed by Raanes (2016).
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc – Implementation

    Below is a very rudimentary sequential estimator (not the KF!), which essentially just does "persistence" forecasts and sets the analysis estimates to the value of the observations (*which is only generally possible in this linear, scalar case*). Run its cell to define it, and then re-run the above interactive animation cell. Then:

    - Implement the KF properly by replacing the forecast and analysis steps below. *Re-run the cell.*
    - Try implementing the analysis step both in the "precision" and "gain" forms.
    """)
    return


@app.cell
def _(np):
    def KF(nTime, xa, Pa, M, H, Q, R, obsrvs):
        """Kalman filter. PS: (xa, Pa) should be input with *initial* values."""
        ############################
        # TEMPORARY IMPLEMENTATION #
        ############################
        estimates = np.zeros((nTime, 2))
        variances = np.zeros((nTime, 2))
        for k in range(nTime):
            # Forecast step
            xf = xa
            Pf = Pa
            # Analysis update step
            Pa = R / H**2
            xa = obsrvs[k] / H
            # Assign
            estimates[k] = xf, xa
            variances[k] = Pf, Pa
        return estimates, variances

    return (KF,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc – KF behaviour

    - Set `logQ` to its minimum, and `M=1`.
      We established in Exc "AR1" that the true states are now constant in time (but unknown).
      How does the KF fare in estimating it?
      Does its uncertainty variance ever reach 0?
    - What is the KF uncertainty variance in the case of `M=0`?
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("KF behaviour")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc – Temporal convergence

    In general, $\mathscr{M}$, $\mathscr{H}$, $Q$, and $R$ depend on time, $k$
    (often to parameterize exogenous/outside factors/forces/conditions),
    and there are no limit values that the KF parameters converge to.
    But, we assumed that they are all stationary.
    In addition, suppose $Q=0$ and $\mathscr{H} = 1$.
    Show that

    - (a) $1/P^{\text{a}}_k = 1/(\mathscr{M}^2 P^{\text{a}}_{k-1}) + 1/R$,
      by combining the forecast and analysis equations for the variance.
    - (b) $1/P^{\text{a}}_k = 1/P^{\text{a}}_0 + k/R$, if $\mathscr{M} = 1$.
    - (c) $P^{\text{a}}_{\infty} = 0$, if $\mathscr{M} = 1$.
    - (d) $P^{\text{a}}_{\infty} = 0$, if $\mathscr{M} < 1$.
    - (e) $P^{\text{a}}_{\infty} = R (1-1/\mathscr{M}^2)$, if $\mathscr{M} > 1$.
      *Hint: Look for the fixed point of the recursion of part (a).*
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("Asymptotic Riccati", "a")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exc (optional) – Temporal CV, part 2:**
    Now we don't assume that $Q$ is zero. Instead

    - (a) Suppose $\mathscr{M} = 0$. What does $P^{\text{a}}_k$ equal?
    - (b) Suppose $\mathscr{M} = 1$. Show that $P^{\text{a}}_\infty$
      satisfies the quadratic equation: $0 = P^2 + Q P - Q R$.
      Thereby, without solving the quadratic equation, show that
      - (c) $P^{\text{a}}_\infty \rightarrow R$ (from below) if $Q \rightarrow +\infty$.
      - (d) $P^{\text{a}}_\infty \rightarrow \sqrt{ Q R}$ (from above) if $Q \rightarrow 0^+$.
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("Asymptotes when Q>0")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc (optional) – Analytic simplification in the case of an unknown constant

    - Note that in case $Q = 0$,
    then $x_{k+1} = \mathscr{M}^k x_0$.
    - So if $\mathscr{M} = 1$, then $x_k = x_0$, so we are estimating an unknown *constant*,
    and can drop its time index subscript.
    - For simplicity, assume $\mathscr{H} = 1$, and $P^a_0 \rightarrow +\infty$.
    - Then $p(x | y_{1:k}) \propto \exp \big\{- \sum_l \| y_l - x \|^2_R / 2 \big\} = \mathscr{N}(x | \bar{y}, R/k )$, which again follows by completing the square.
    - In words, the (accumulated) posterior mean is the sample average,
      $\bar{y} = \frac{1}{k}\sum_l y_l$,
      and the variance is that of a single observation divided by $k$.

    Show that this is the same posterior that the KF recursions produce.
    *Hint: while this is straightforward for the variance,
    you will probably want to prove the mean using induction.*

    #### Exc – Impact of biases

    Re-run the above interactive animation to set the default control values. Answer the following

    - `logR_bias`/`logQ_bias` control the (multiplicative) bias in $R$/$Q$ that is fed to the KF.
      What happens when the KF "thinks" the measurement/dynamical error
      is (much) smaller than it actually is?
      What about larger?
    - Re-run the animation to get default values.
      Set `logQ` to 0, which will make the following behaviour easier to describe.
      In the code, add 20 to the initial `xa` **given to the KF**.
      How long does it take for it to recover from this initial bias?
    - Multiply `Pa` **given to the KF** by 0.01. What about now?
    - Remove the previous biases.
      Instead, multiply `M` **given to the KF** by 2, and observe what happens.
      Try the same, but dividing `M` by 2.
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("KF with bias")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Alternative methods

    When it comes to (especially univariate) time series analysis,
    the Kalman filter (KF) is not the only option.
    For example, **signal processing** offers several alternative filters.
    Indeed, the word "filter" in the KF comes from that domain,
    where it originally referred to removing high-frequency noise,
    since this often leads to a better estimate of the signal.
    We will not review signal processing theory here,
    but challenge you to make use of what `scipy` already has to offer.

    #### Exc – signal processing

    Run the following cell to import and define some more tools.
    """)
    return


@app.cell
def _(np):
    import scipy as sp
    import scipy.signal as sig

    def nrmlz(x):
        return x / x.sum()

    def trunc(x, n):
        return np.pad(x[:n], (0, len(x)-n))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now try to "filter" the `obsrvs` to produce estimates of `truth`.
    For each method, add your estimate ("filtered signal" in signal processing parlance)
    to the `sigproc` dictionary in the interactive animation cell,
    using an appropriate name/key (this will automatically include it in the plot).
    Use

    - (a) `sig.wiener`.
      *PS: this is a direct ancestor of the KF*.
    - (b) a moving average, for example `sig.windows.hamming`.
      *Hint: you may also want to use `sig.convolve`*.
    - (c) a low-pass filter using `np.fft`.
      *Hint: you may also want to use the above `trunc` function.*
    - (d) The `sig.butter` filter.
      *Hint: apply with `sig.filtfilt`.*
    - (e) not really a signal processing method: `sp.interpolate.UnivariateSpline`

    The answers should be considered examples, not the uniquely right way.

    <mark><font size="-1">
    Migration note: the original wired `sigproc` results back into the interactive `exprmt`
    plot via a shared, mutable dict that the student edits in-place. That pattern doesn't
    map cleanly onto marimo's reactive model (a cell mutating a dict defined in an earlier
    cell doesn't trigger a re-run of cells that already read it) -- the exercise stands as a
    standalone coding task in this pilot, without automatically feeding into the animation
    above. Wiring it back in reactively (e.g. an explicit `sigproc` cell feeding a redrawn
    plot) is a small, known follow-up, not attempted here.
    </font></mark>
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("signal processing", "a")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    But for the above problem (which is linear-Gaussian!),
    the KF is guaranteed (on average, in the long run, in terms of mean square error)
    to outperform any other method.
    We will see cases later (in full-blown state estimation)
    where the difference is much clearer,
    and indeed it might not even be clear how to apply signal processing methods.
    However, the KF has an unfair advantage: we are giving it a lot of information
    about the problem (`M, H, R, Q`) that the signal processing methods do not have.
    Therefore, those methods typically require a good deal of tuning
    (but in practice, so does the KF, since `Q` and `R` are rarely well determined).

    ## Summary

    The Kalman filter (KF) can be derived by applying linear-Gaussian assumptions
    to a sequential inference problem.
    Generally, the uncertainty never converges to 0,
    and the performance of the filter depends entirely on
    accurate system parameters (models and error covariance matrices).

    As a subset of state estimation (i.e., the KF), we can do classical time series estimation
    (wherein state-estimation is called the state-space approach).
    Moreover, DA methods produce uncertainty quantification, which is usually more obscure with time series analysis methods.

    ### Next: T5 - Multivariate Kalman filter

    ### References

    - **Raanes (2016)**:
      Patrick N. Raanes, "On the ensemble Rauch-Tung-Striebel smoother and its equivalence to the ensemble Kalman smoother", Quarterly Journal of the Royal Meteorological Society, 2016.
    """)
    return


if __name__ == "__main__":
    app.run()
