# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.24.0",
#     "numpy",
#     "scipy",
#     "matplotlib",
# ]
# ///
import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full", css_file="custom.css")


@app.cell
async def _():
    import marimo as mo
    from answers_data import show_answer
    from notebook_utils import hookup
    from T2 import app as _t2_app
    _t2 = await _t2_app.embed()  # runs T2.py itself and gives access to its variables
    pdf_G1 = _t2.defs["pdf_G1"]
    pdf_U1 = _t2.defs["pdf_U1"]
    bounds = _t2.defs["bounds"]
    grid1d = _t2.defs["grid1d"]
    mean_and_var = _t2.defs["mean_and_var"]
    dx = grid1d[1] - grid1d[0]
    import numpy as np
    import matplotlib.pyplot as plt
    _ = plt.ion()  # named to avoid auto-displaying plt.ion()'s ExitStack repr
    return mo, hookup, show_answer, pdf_G1, pdf_U1, bounds, dx, grid1d, mean_and_var, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # T3 - Bayes' rule and inference

    The previous tutorial (T2) studied the Gaussian probability density function (pdf), defined in 1D by:
    $$ \large \mathscr{N}(x \mid \mu, \sigma^2) = (2 \pi \sigma^2)^{-1/2} e^{-(x-\mu)^2/2 \sigma^2} \,,\tag{G1} $$
    which we implemented and tested alongside the uniform distribution.

    <mark><font size="-1">
    Migration note: T2's `pdf_G1`, `pdf_U1`, `bounds`, `grid1d`, `mean_and_var` were
    originally pulled in via `import_from_nb("T2", (...))` -- a hack that imports another
    notebook's jupytext mirror as if it were a module. Here they come from marimo's own
    `app.embed()` API: `from T2 import app` then `await app.embed()` actually *runs*
    T2.py (the same notebook you already worked through) and exposes its variables via
    `.defs`, rather than pulling from a separately-maintained, never-seen module.
    </font></mark>
    """)
    return


@app.cell
def _(pdf_G1, pdf_U1):
    pdfs = dict(N=pdf_G1, U=pdf_U1)
    return (pdfs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *We no longer use uppercase to distinguish random variables from their outcomes (an unfortunate consequence of the myriad of notations to keep track of)!*

    Now that we have reviewed some probability, we can turn to statistical inference and estimation.
    In particular, we will focus on **Bayes' rule**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Migration note: raw `<details>` HTML (as used for "optional reading" asides
    # in the original notebooks) silently suppresses KaTeX math rendering for any
    # $...$ inside it -- confirmed by isolated testing, a general marimo limitation,
    # not specific to this content. `mo.accordion` renders correctly instead (math
    # works in both its title and body), so all such asides that contain math are
    # converted to it here.
    mo.accordion({
        "In the Bayesian approach, uncertain knowledge (i.e. belief) about some unknown ($x$) is quantified through probability ... (optional reading 🔍)": mo.md(r"""
    For example, what is the temperature at the surface of Mercury (at some given point and time)?
    Not many people know the answer. Perhaps you say $500^{\circ} C, \, \pm \, 20$.
    But that's hardly anything compared to you real uncertainty, so you revise that to $\pm \, 1000$.
    But then you're allowing for temperature below absolute zero, which you of course don't believe is possible.
    You can continue to refine the description of your uncertainty.
    Ultimately (in the limit) the complete way to express your belief is as a *distribution*
    (essentially just a list) of plausibilities for all possibilities.
    Furthermore, the only coherent way to reason in the presence of such uncertainty
    is to obey the laws of probability (Jaynes, 2003).
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Bayes' rule** is the fundamental tool for inference: it tells us how to condition/merge/assimilate/update our beliefs based on data/observation ($y$).
    For *continuous* random variables $x$ and $y$, Bayes' rule reads:
    $$
    \large
    \color{red}{\overset{\mbox{Posterior}}{p(\color{black}{x|y})}} = \frac{\color{blue}{\overset{\mbox{  Prior  }}{p(\color{black}{x})}} \, \color{green}{\overset{\mbox{ Likelihood}}{p(\color{black}{y|x})}}}{\color{gray}{\underset{\mbox{Constant wrt. x}}{p(\color{black}{y})}}} \,. \tag{BR} \\[1em]
    $$

    #### Exc – Bayes' rule derivation

    Derive eqn. (BR) from the definition of conditional pdfs.
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("symmetry of conjunction")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It is hard to overstate the simplicity of Bayes' rule, eqn. (BR): it consists merely of scalar multiplication and division.
    However, our goal is to compute the function $p(x|y)$ for **all values of $x$**.
    Thus, upon discretization, eqn. (BR) becomes the multiplication of two *arrays* of values (followed by normalization):
    """)
    return


@app.cell
def _(np):
    def Bayes_rule(prior_values, lklhd_values, dx):
        prod = prior_values * lklhd_values         # pointwise multiplication
        posterior_values = prod/(np.sum(prod)*dx)  # normalization
        return posterior_values
    return (Bayes_rule,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc (optional) – BR normalization

    Show that the normalization in `Bayes_rule()` amounts to (approximately) the same as dividing by $p(y)$.
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("quadrature marginalisation")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In fact, since $p(y)$ is implicitly known in this way,
    we often omit it, simplifying Bayes' rule (eqn. BR) to

    $$ p(x|y) \propto p(x) \, p(y|x) \,.  \tag{BR2} $$

    Do we even need to care about $p(y)$ at all? In practice, all we need to know is how much more likely one value of $x$ (or an interval around it) is compared to another.
    Normalization is only necessary because of the *convention* that all densities integrate to $1$.
    However, for large models, we can usually only afford to evaluate $p(y|x)$ at a few points (of $x$), so the integral for $p(y)$ can only be roughly approximated. In such settings, estimating the normalization factor becomes an important question too.

    ### Interactive illustration

    The code below shows Bayes' rule in action.
    """)
    return


@app.cell(hide_code=True)
def _(bounds, mo, pdfs):
    # A `mo.ui.dictionary` bundles several widgets into one variable: `.value`
    # gives back a dict of their values, so the consumer cell can just do
    # `Bayes1(**controls.value)` -- much less boilerplate than one variable
    # (and one return-tuple entry) per widget. Not displayed here -- the
    # plotting cell below displays the widgets and the figure together.
    controls = mo.ui.dictionary({
        "y": mo.ui.slider(start=bounds[0], stop=bounds[1], step=1, value=9.0, show_value=True, label="y"),
        "logR": mo.ui.slider(start=-3, stop=5, step=.5, value=1.0, show_value=True, label="logR"),
        "prior_kind": mo.ui.dropdown(options=list(pdfs), value="N", label="prior_kind"),
        "lklhd_kind": mo.ui.dropdown(options=list(pdfs), value="N", label="lklhd_kind"),
    })
    return (controls,)


@app.cell
def _(Bayes_rule, Bayes_rule_LG1, controls, grid1d, hookup, mean_and_var, pdf_G1, pdfs, plt):
    def Bayes1(y, logR, lklhd_kind, prior_kind):
        R = 4**logR
        xf = 10
        Pf = 4**2

        # (Ref. later exercise)
        def H(x):
            return 1*x + 0

        x = grid1d
        prior_vals = pdfs[prior_kind](x, xf, Pf)
        lklhd_vals = pdfs[lklhd_kind](y, H(x), R)
        postr_vals = Bayes_rule(prior_vals, lklhd_vals, grid1d[1] - grid1d[0])

        def plot(x, y, c, lbl):
            plt.fill_between(x, y, color=c, alpha=.3, label=lbl)

        plt.figure(figsize=(8, 4))
        plot(x, prior_vals, 'blue'  , f'Prior, {prior_kind}(x | {xf:.4g}, {Pf:.4g})')
        plot(x, lklhd_vals, 'green' , f'Lklhd, {lklhd_kind}({y:<3}| H(x), {R:.4g})')
        plot(x, postr_vals, 'red'   , 'Postr, pointwise: ?(x | %4.2g, %4.2g)' % mean_and_var(postr_vals, x))

        # Migration note: the original used a try/except NameError here, since on a
        # single top-to-bottom run `Bayes_rule_LG1` (defined later in the notebook)
        # wouldn't exist yet on the first pass. marimo's reactive graph resolves cell
        # execution order by *data* dependency, not file position, so `Bayes_rule_LG1`
        # is already defined by the time this cell runs -- the purple parametric curve
        # below is simply always shown, rather than only after a later manual re-run.
        H_lin = H(xf)/xf # a simple linear approximation of H(x)
        xa, Pa = Bayes_rule_LG1(xf, Pf, y, H_lin, R)
        label = f'Postr, parametric: N(x | {xa:4.2g}, {Pa:4.2g})'
        postr_vals_G1 = pdf_G1(x, xa, Pa)
        plt.plot(x, postr_vals_G1, 'purple', label=label)

        plt.ylim(0, 0.6)
        plt.legend(loc="upper left", prop={'family': 'monospace'})
        return plt.gca()

    hookup(controls, Bayes1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The illustration uses a

    - prior $p(x) = \mathscr{N}(x|x^f, P^f)$ with (fixed) mean and variance, $x^f= 10$, $P^f=4^2$
      (but you can of course change these in the code above)
    - likelihood $p(y|x) = \mathscr{N}(y|x, R)$, whose parameters are set by the interactive sliders.

    We are now dealing with three (!) separate distributions,
    which introduces a lot of symbols to keep track of – a necessary evil for later.

    #### Exc – `Bayes1` properties

    This exercise serves to make you acquainted with how Bayes' rule blends information.

    Move the sliders to animate it, and answer the following.

    - What happens to the posterior when $R \rightarrow \infty$ ?
    - What happens to the posterior when $R \rightarrow 0$ ?
    - Move $y$ around. What is the posterior's location (mean/mode) when $R$ equals the prior variance?
    - Can you say something universally valid (for any $y$ and $R$) about the height of the posterior pdf?
    - Does the posterior scale (width) depend on $y$?
       *Optional*: What does this mean information-wise?
    - Consider the shape (ignoring location & scale) of the posterior. Does it depend on $R$ or $y$?
    - Can you see a shortcut to computing this posterior rather than having to do the pointwise multiplication?
    - For the case of two uniform distributions: What happens when you move the prior and likelihood too far apart? Is the fault of the implementation, the math, or the problem statement?
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("Posterior behaviour")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## With forward (observation) models

    In general, the observation $y$ is not a "direct" measurement of $x$, as above,
    but rather some transformation, i.e. function of $x$,
    which is called **observation/forward model**, $\mathscr{H}$.
    Examples include:

    - $\mathscr{H}(x) = x + 273$ for a thermometer reporting °C, while $x$ is the temperature in °K.
    - $\mathscr{H}(x) = 10 x$ for a ruler using mm, while $x$ is stored as cm.
    - $\mathscr{H}(x) = \log(x)$ for litmus paper (pH measurement), where $x$ is the molar concentration of hydrogen ions.
    - $\mathscr{H}(x) = |x|$ for bicycle speedometers (measuring rpm, i.e. Hall effect sensors).
    - $\mathscr{H}(x) = 2 \pi h \, x^2$ if observing inebriation (drunkenness), and the unknown, $x$, is the radius of the beer glasses.

    Of course, the linear and logarithmic transformations are hardly worthy of the name "model", since they merely change the scale of measurement, and so could be trivially done away with. But doing so is not necessary, and they will serve to illustrate some important points.

    In addition, measurement instruments always (at least for continuous variables) have limited accuracy,
    i.e. there is an **measurement noise/error** corrupting the observation. For simplicity, this noise is usually assumed *additive*, so that the observation, $y$, is related to the true state, $x$, by
    $$
    y = \mathscr{H}(x) + r \,, \;\; \qquad \tag{Obs}
    $$
    and $r \sim \mathscr{N}(0, R)$ for some variance $R>0$.
    Then the likelihood is $p(y|x) = \mathscr{N}(y| \mathscr{H}(x), R) \,.$ (Lklhd)

    #### Exc (optional) – The likelihood

    Derive the expression (Lklhd) for the likelihood.
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("Likelihood")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc – Obs. model gallery

    Consider the following observation models.

    - (a) $\mathscr{H}(x) = x + 15$.
    - (b) $\mathscr{H}(x) = 2 x$.
    - (c) $\mathscr{H}(x) = (x-5)^2$.
      - Explain how negative values of $y$ are possible.
    - (d) Try $\mathscr{H}(x) = |x|$.

    In each case, describe how and why you'd expect the likelihood to change (as compared to $\mathscr{H}(x) = x$).
    Then verify your answer by implementing `H` in the interactive Bayes' rule illustration above.
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("Observation models", "a")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It is important to appreciate that the likelihood, and its role in Bayes' rule, does not perform any "inversion". It simply quantifies how well each $x$ fits the data, in terms of its weighting. This approach also inherently handles the fact that multiple values of $x$ may be plausible.

    #### Exc (optional) – "why inverse"

    Laplace called "statistical inference" the reasoning of "inverse probability" (1774). You may also have heard of "inverse problems" in reference to similar problems, but without a statistical framing. In view of this, why do you think we use $x$ for the unknown, and $y$ for the known/given data?
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("what's forward?")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Linear-Gaussian Bayes' rule (1D)

    To address this computational difficulty, we can take a more analytical ("pen-and-paper") approach: instead of computing the full posterior, we compute only its parameters (mean and (co)variance).
    This is straightforward in the linear-Gaussian case, i.e. when $\mathscr{H}$ is linear (just a number). For readability, the unknown, $x$, is colored.

    - Given the prior of $p(\color{darkorange}{x}) = \mathscr{N}(\color{darkorange}{x} \mid x^{\text{f}}, P^{\text{f}})$
    - and a likelihood $p(y|\color{darkorange}{x}) = \mathscr{N}(y \mid \mathscr{H} \color{darkorange}{x},R)$,
    - $\implies$ posterior $p(\color{darkorange}{x}|y) = \mathscr{N}(\color{darkorange}{x} \mid x^{\text{a}}, P^{\text{a}}) \,,$

    where, in the 1-dimensional/univariate/scalar (multivariate is discussed in T5) case:

    $$
    \begin{align}
      P^{\text{a}} &= 1/(1/P^{\text{f}} + \mathscr{H}^2/R) \,, \tag{5} \\\
      x^{\text{a}} &= P^{\text{a}} (x^{\text{f}}/P^{\text{f}} + \mathscr{H} y/R) \,.  \tag{6}
    \end{align}
    $$

    <mark><font size="-1">
    Migration note: marimo's markdown renderer doesn't process multi-line
    math (single-$ or $$) when it's nested inside a list item's continuation
    lines -- confirmed by testing. The bulleted "posterior" line and the
    (5)/(6) equation block are kept as a single-line bullet plus a
    non-list paragraph, rather than one multi-line list item, to work around
    this.
    </font></mark>

    The proof is in the following exercise.

    #### Exc – BR-LG1

    Consider the following identity, where $P^{\text{a}}$ and $x^{\text{a}}$ are given by eqns. (5) and (6).
    $$
    \frac{(\color{darkorange}{x}-x^{\text{f}})^2}{P^{\text{f}}} + \frac{(\mathscr{H} \color{darkorange}{x}-y)^2}{R} \quad =
    \quad \frac{(\color{darkorange}{x} - x^{\text{a}})^2}{P^{\text{a}}} + \frac{(y - \mathscr{H} x^{\text{f}})^2}{R + P^{\text{f}}} \,, \tag{LG1}
    $$
    Notice that the left hand side (LHS) is the sum of *two* squares with $\color{darkorange}{x}$,
    but the RHS only contains *one*.

    - (a) Actually derive the first term of the RHS of (LG1), i.e. eqns. (5) and (6).
      *Hint: you can simplify the task by first "hiding" $\mathscr{H}$*
    - (b) *Optional*: Derive the full RHS (i.e. also the second term).
    - (c) Show that $p(\color{darkorange}{x}|y) = \mathscr{N}(\color{darkorange}{x} \mid x^{\text{a}}, P^{\text{a}})$
      using part (a), Bayes' rule (BR2), and the Gaussian pdf (G1).
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("BR Gauss, a.k.a. completing the square", "a")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc – Temperature example

    The statement $x = \mu \pm \sigma$ is *sometimes* used
    as a shorthand for $p(x) = \mathscr{N}(x \mid \mu, \sigma^2)$. Suppose

    - you think the temperature $x = 20°C \pm 2°C$,
    - a thermometer yields the observation $y = 18°C \pm 2°C$.

    Show that your posterior is $p(x|y) = \mathscr{N}(x \mid 19, 2)$
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("LG BR example")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following implements the linear-Gaussian Bayes' rule (eqns. 5 and 6).
    Note that its inputs and outputs are not arrays (as in `Bayes_rule()`), but simply scalar numbers: the means, variances, and $\mathscr{H}$.
    """)
    return


@app.cell
def _():
    def Bayes_rule_LG1(xf, Pf, y, H, R):
        Pa = 1 / (1/Pf + H**2/R)
        xa = Pa * (xf/Pf + H*y/R)
        return xa, Pa
    return (Bayes_rule_LG1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc – Gaussianity as an approximation

    - (a) Again, try the various $\mathscr{H}$ from the above "Obs. model gallery" exercise in the interactive Bayes' rule illustration.
      For which $\mathscr{H}$ does `Bayes_rule_LG1()` reproduce `Bayes_rule()`?
    - (b) For simplicity, revert back to the identity for $\mathscr{H}$.
      Then run the cell below, which fits distributions from `scipy`'s library of distributions
      so as to respect `mu` and `sig2` and adds them to the pdfs in the dropdown menus of the widget
      (upon re-running its cell). Try them out for the likelihood, and answer the following.
      Which ones

      - Are skewed (or at least asymmetric) ?
      - Have excess kurtosis (tails heavier than for the Gaussian) ?
      - Produces a posterior variance that increases with the distance prior-observation ?
        *PS: this one (the Student's) is frequently used
        to increase the robustness of the (ensemble) Kalman filter,
        or estimate the "inflation" factor.*
    """)
    return


@app.cell
def _(pdfs):
    import scipy.stats as ss
    for _dist in [
      ss.chi2(df=3),
      ss.beta(a=5, b=2),
      ss.anglit(),
      ss.t(df=3),
    ]:
        def _pdf_fitted(x, mu, sigma2, dist=_dist):
            import numpy as _np
            mean, var = dist.stats(moments='mv')
            ratio = _np.sqrt(var / sigma2)
            u = ratio * (x - mu) + mean
            return ratio * dist.pdf(u)
        pdfs[_dist.dist.name + str(_dist.kwds)] = _pdf_fitted
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc (optional) – Gain algebra

    Show that eqn. (5) can be written as
    $$ P^{\text{a}} = K R / \mathscr{H} \,,    \tag{8} $$
    where
    $$ K = \frac{\mathscr{H} P^{\text{f}}}{\mathscr{H}^2 P^{\text{f}} + R} \,,    \tag{9} $$
    is called the "Kalman gain".

    Then shown that eqns. (5) and (6) can be written as
    $$
    \begin{align}
        P^{\text{a}} &= (1-K \mathscr{H}) P^{\text{f}} \,,  \tag{10} \\\
      x^{\text{a}} &= x^{\text{f}} + K (y- \mathscr{H} x^{\text{f}}) \tag{11} \,,
    \end{align}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("BR Kalman1 algebra")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc (optional) – Gain intuition

    Let $\mathscr{H} = 1$ for simplicity.

    - (a) Show that $0 < K < 1$ since $0 < P^{\text{f}}, R$.
    - (b) Show that $P^{\text{a}} < P^{\text{f}}, R$.
    - (c) Show that $x^{\text{a}}$ is in the interval $(x^{\text{f}}, y)$.
    - (d) Why do you think $K$ is called a "gain"?
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("KG intuition")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc – BR with Gain

    Re-define `Bayes_rule_LG1` so to as to use eqns. 9-11. Remember to re-run the cell. Verify that you get the same plots as before.
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("BR Kalman1 code")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc (optional) – optimalities

    In contrast to orthodox statistics,
    Bayes' rule (BR) does not attempt to produce a single estimate/value of $x$.
    It merely states how to update our quantitative belief (weighted possibilities) in light of new data.
    As such, barring any approximations (such as using `Bayes_rule_LG1` outside the linear-Gaussian case),
    the (full) posterior will be **optimal** from the perspective of any proper scoring rule.

    *But if you must* pick a single point value estimate $\widehat{x}$
    then you should **decide** on it by optimising (with respect to $\widehat{x}$)
    the expectation (with respect to $x$) of some utility/loss function,
    i.e. $\mathbb{E}\, \text{Loss}(x - \widehat{x})$.
    For instance, if the posterior pdf happens to be symmetric
    (as in the linear-Gaussian context above),
    and your loss function is convex and symmetric,
    then the mean/median will be optimal (Lehmann & Casella, 1998, Corollary 7.19).
    More specifically, for any given distribution of $x$,
    the optimal Bayes estimator is:

    - the mode if $\text{Loss}(d) = \begin{cases} 0 & \text{if } d = 0 \\ 1 & \text{otherwise} \end{cases}$
    - the median if $\text{Loss}(d) = |d|$
    - the mean if $\text{Loss}(d) = d^2$

    The last case (squared-error loss) is most commonly used,
    and the resulting estimator is sometimes called
    the minimum mean-square error (MMSE) estimator.
    *Prove that the MMSE is indeed the mean of the distribution!*
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("MMSE")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    However, it is not generally easy to find the posterior mean, median, or mode,
    so the above optimalities are mainly useful in the linear-Gaussian case,
    where they justify a preference for $x^{\text{a}}$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "It is possible to drop the linear-Gaussian assumption and still claim optimality for $x^{\\text{a}}$ of eqns. (6) and (11) as the best (min. variance), linear, unbiased, estimate (BLUE ... 🔍).": mo.md(r"""
    The result requires reformulating the prior
    as "background" zero-mean noise onto the (non-random) $x$,
    whose outcome was the prior mean, $x^{\text{f}}$, and whose covariance is $P^{\text{f}}$.
    Then, by explicit augmentation (i.e. pseudo-obs: $[y, x^{\text{f}}]$) one recovers the linear regression problem
    of the celebrated Gauss-Markov theorem, generalized by Aitken to the case of correlated noise.
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All in all, the intuitive idea of **considering the mean of $p(x)$ as the point
    estimate** has good theoretical foundations.

    ## Summary

    Bayesian inference quantifies uncertainty (in $x$) using probability.
    Bayes' rule tells us how to update this belief based on data or observation ($y$).
    It is simply a reformulation of conditional probability.
    Observation can be "inverted" using Bayes' rule,
    in the sense that all possibilities for $x$ are weighted.
    While technically simple, Bayes' rule requires many pointwise multiplications.
    But if Gaussianity can be assumed, it reduces to just two formulae.

    ### Next: [T4 - Time series filtering](../T4/T4.html)

    ### References

    - **Jaynes (2003)**:
      Edwin T. Jaynes, "Probability theory: the logic of science", 2003.
    - **Lehmann & Casella (1998)**:
      "Theory of Point Estimation", 1998.
    - **Pötscher & Preinerstorfer (2024)**:
      Benedikt M. Pötscher and David Preinerstorfer, "A Comment on: 'A Modern Gauss-Markov Theorem'", Econometrica, 2024.
    """)
    return


if __name__ == "__main__":
    app.run()
