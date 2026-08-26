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
app = marimo.App(
    width="full",
    layout_file="layouts/T2.slides.json",
    css_file="custom.css",
)


@app.cell
def _():
    import marimo as mo
    from answers_data import show_answer
    from notebook_utils import hookup
    import numpy as np
    import scipy as sp
    import numpy.linalg as la
    import numpy.random as rnd
    import matplotlib.pyplot as plt
    plt.ion()
    rnd.seed(3000)
    return hookup, la, mo, np, plt, rnd, show_answer, sp


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # T2 - The Gaussian (Normal) distribution

    We begin by reviewing the most useful of probability distributions.
    But first, let's refresh some basic theory.

    ## Probability essentials

    As stated by James Bernoulli (1713) and elucidated by [Laplace (1812)](#references):

    > The Probability ($\mathbb{P}$) for an event ($E$) is the ratio of the number of cases favorable to it ($|E|$), to the number of all
    > cases possible ($|\Omega|$) when nothing leads us to expect that any one of these cases should occur more than any other,
    > which renders them, for us, equally possible:

    $$ \mathbb{P}(E) = \frac{|E|}{|\Omega|} $$

    It follows that for two events, $A, B$, the probability of *both* occurring is that of their intersection:
    $\mathbb{P}(A \cap B)$, while the probability of *either (or)* is obtained by their union $\mathbb{P}(A \cup B)$.
    The *conditional* probability of $A$ given $B$ restricts our attention (count)
    to cases where $B$ occurs: $\mathbb{P}(A | B) = \frac{\mathbb{P}(A \cap B)}{\mathbb{P}(B)}$.

    #### Exc (optional) – By definition, not axiom

    - (a) Show that $0 \le \mathbb{P}(E) \le 1$, with the boundaries attained if $E=\emptyset$ or $E=\Omega$.
    - (b) Assuming $E_i \cap E_j = \emptyset$ for $i \neq j$, i.e. that the events are (pairwise) disjoint,
      show that $\mathbb{P}(\bigcup_i E_i) = \sum_i \mathbb{P}(E_i)$.
    - (c) For general (non-disjoint) events/sets $A, B$,
      express $\mathbb{P}(A \cup B)$ in terms of $\mathbb{P}(A)$, $\mathbb{P}(B)$, and $\mathbb{P}(A \cap B)$.
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("By definition, not axiom")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Rather than "*did* event $E$ occur or not?",
    a **random variable** conveniently enables the question "*what* was the value of $X$?"
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Migration note: raw `<details>` HTML silently suppresses KaTeX math rendering
    # for any $...$ inside it -- see T3's equivalent note. `mo.accordion` renders
    # correctly instead, so this aside (whose body contains math) uses it here.
    mo.accordion({
        'This question pre-supposes the existence of one, and only one outcome, a "structure" that brings to mind *functions*... (optional reading 🔍)': mo.md(r"""
    Indeed, formally, $X$ is defined as a function on (the sample space of)
    some underlying *probability space* (like that of $A, B$ above).
    But since each possible value $x$ constitutes a disjoint event,
    $X$ itself induces a new probability space
    (though not Laplacian, since cases no longer equally probable),
    allowing us to forget about the underlying one.
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A random variable takes *numeric* values, so it can be sorted, averaged, and transformed.
    The probabilities associated with each *outcome*, $x$, form a **distribution**.
    If $X$ is *discrete* (the set $\{x_i\}$ is countable), the distribution can be summarized by
    the probability *mass* function (**pmf**) $p_X(x) := \mathbb{P}(X{=}x)$,
    which is essentially a mapping (table) of outcomes to probabilities,
    written $p(x)$ if contextually unambiguous.
    Similarly, $p(x, y) = \mathbb{P}(X{=}x \cap Y{=}y)$ is a 2D table of the **joint** probabilities of $X$ and $Y$.
    **Independence** means $p(x, y) = p(x) \, p(y)$ for all possible $x, y$.

    #### Exc (optional) – conditional and marginal

    Show that

    - (a) $p(x | y) = \frac{p(x,y)}{p(y)}$, where $p(x|y)$ is defined similarly to $p(x, y)$ above.
    - (b) The *marginal* pmf, $p(x)$, can be recovered from the joint pmf, $p(x, y)$, by summing over all $y$.
    - (c) *Independence* can equivalently be stated as $p(x|y) = p(x)$ (or the other way around).
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("pmf identities")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc – Try it out

    Consider the joint pmf $p(x,y)$ given by the table below.

    - (a) Is it a valid pmf?
    - (b) Compute $p(x)$ and $p(y)$.
    - (c) Compute $p(y \mid x{=}0)$.
    - (d) Are $X$ and $Y$ independent?

    $$
    \begin{array}{c|ccc}
    x \diagdown\, y & 0 & 1 & 2 \\ \hline
    0 & 0.10 & 0.15 & 0.25 \\
    1 & 0.20 & 0.05 & 0.25
    \end{array}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("pmf test")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will mainly be concerned with **continuous** random variables,
    whose possible values are *uncountable* (e.g. all of $\mathbb{R}$),
    so that the above counting definition of probability no longer applies.
    Instead, the distribution of such an $X$ can be characterised by
    a probability *density* function (**pdf**, analogous to the pmf), $p(x) \ge 0$,
    which integrates to $1$ (but unlike a pmf, the pdf $p(x)$ itself may exceed $1$).
    Then

    $$\mathbb{P}(X \in [a, b]) := \int_a^b p(x) \, d x \,,$$

    satisfies the above axioms by calculus (rather than counting).
    Moreover, the above pmf definitions and identities carry over to the pdf, with sums becoming integrals,
    as can be shown by replacing $\mathbb{P}(X{=}x)$ by $p(x) \, \delta x$
    and taking limits (assuming sufficient regularity).

    The **sample average** of draws from a random variable $X$
    is denoted with an overhead bar:
    $$ \bar{x} := \frac{1}{N} \sum_{n=1}^{N} x_n \,. $$
    The *law of large numbers (LLN)* states that, as $N \to \infty$,
    the sample average of independent draws
    converges to the **expected value** (sometimes called the **mean**):
    $$ \mathbb{E}[X] ≔ \int x \, p(x) \, d x \,, $$
    where the (omitted) domain of integration is *all values of $x$*.

    ## The univariate (a.k.a. 1-dimensional, scalar) Gaussian

    If $X$ is Gaussian (also known as "Normal"), we write
    $X \sim \mathscr{N}(\mu, \sigma^2)$, or $p(x) = \mathscr{N}(x \mid \mu, \sigma^2)$,
    where the parameters $\mu$ and $\sigma^2$ are called the mean and variance
    (for reasons that will become clear below).
    The Gaussian pdf, for $x \in (-\infty, +\infty)$, is
    $$ \large \mathscr{N}(x \mid \mu, \sigma^2) = (2 \pi \sigma^2)^{-1/2} e^{-(x-\mu)^2/2 \sigma^2} \, . \tag{G1} $$

    Run the cell below to define a function to compute the pdf (G1) using the `scipy` library.
    """)
    return


@app.cell
def _(np, sp):
    def pdf_G1(x, mu, sigma2):
        "Univariate Gaussian pdf"
        pdf_values = sp.stats.norm.pdf(x, loc=mu, scale=np.sqrt(sigma2))
        return pdf_values

    return (pdf_G1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Computers typically represent functions *numerically* by their values at a set of grid points (nodes),
    an approach called ***discretization***.
    """)
    return


@app.cell
def _(np):
    bounds = -20, 30
    N = 201                          # num of grid points
    grid1d = np.linspace(*bounds, N)  # grid
    dx = grid1d[1] - grid1d[0]       # grid spacing
    return bounds, grid1d


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Feel free to return here later and change the grid resolution to see how
    it affects the cells below (after re-running them).

    The following code plots the Gaussian pdf.

    <mark><font size="-1">
    Migration note: the original used `@interact(mu=bounds, sigma=(.1,10,1))` from a
    custom ipywidgets wrapper. Below, the two `mo.ui.slider`s are defined in their own
    cell, and the plotting cell reads their `.value` reactively -- no decorator, no
    custom layout DSL. The trailing "ghost" history of previous curves (`pdf_hist`) is
    kept in a separate, slider-independent cell precisely so it persists across
    reactive re-runs instead of being reset to `[]` every time a slider moves.
    </font></mark>
    """)
    return


@app.cell(hide_code=True)
def _(bounds, mo):
    controls = mo.ui.dictionary({
        "mu": mo.ui.slider(start=bounds[0], stop=bounds[1], value=0, step=1, show_value=True, label="mu"),
        "sigma": mo.ui.slider(start=.1, stop=10, value=5, step=1, show_value=True, label="sigma"),
    })
    return (controls,)


@app.cell
def _():
    pdf_hist = []  # Deliberately NOT depending on the sliders (see note above).
    return (pdf_hist,)


@app.cell
def _(bounds, controls, grid1d, hookup, pdf_G1, pdf_hist, plt):
    def _plot_pdf(mu, sigma):
        plt.figure(figsize=(6, 2))
        colors = plt.get_cmap('hsv')([(k - len(pdf_hist)) % 9 / 9 for k in range(9)])
        plt.xlim(*bounds)
        plt.ylim(0, .2)
        pdf_hist.insert(0, pdf_G1(grid1d, mu, sigma**2))
        for density_values, color in zip(pdf_hist, colors):
            plt.plot(grid1d, density_values, c=color)
        return plt.gca()

    hookup(controls, _plot_pdf)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc – Parameter impact on the density

    Experiment with `mu` and `sigma` to answer these questions:

    - How does the pdf curve change when `mu` changes? (Several options may be correct or incorrect)
    <details style="border: 1px solid #aaaaaa; border-radius: 4px; padding: 0.5em 0.5em 0;">
    <summary style="font-weight: normal; font-style: italic; margin: -0.5em -0.5em 0; padding: 0.5em;">
      Click to view options 🔍
    </summary>

      1. It changes the curve into a uniform distribution.
      1. It changes the width of the curve.
      1. It shifts the peak of the curve to the left or right.
      1. It changes the height of the curve.
      1. It transforms the curve into a binomial distribution.
      1. It makes the curve wider or narrower.
      1. It modifies the skewness (asymmetry) of the curve.
      1. It causes the curve to expand vertically while keeping the width the same.
      1. It translates the curve horizontally.
      1. It alters the kurtosis (peakedness) of the curve.
      1. It rotates the curve around the origin.
      1. It makes the curve a straight line.
    </details>

    - How does the pdf curve change when you increase `sigma`?
      Refer to the same options as the previous question.
    - In a few words, describe the shape of the Gaussian pdf curve.
      Does this remind you of anything? *Hint: it should be clear as a bell!*

    #### Exc – Implementation

    Change the implementation of `pdf_G1` so that it does not use `scipy`, but instead uses your own code (with `numpy` only). Re-run all of the above cells and check that you get the same plots as before.
    *Hint: `**` is the exponentiation/power operator, but $e^x$ is more efficiently computed with `np.exp(x)`*
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("pdf_G1")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc – Derivatives

    Recall $p(x) = \mathscr{N}(x \mid \mu, \sigma^2)$ from eqn. (G1).
    Use pen, paper, and calculus to answer the following questions,
    which will help you remember some key properties of the distribution.

    - (i) Find $x$ such that $p(x) = 0$.
    - (ii) Where is the location of the **mode (maximum)** of the density?
      I.e. find $x$ such that $\frac{d p}{d x}(x) = 0$.
      *Hint: begin by writing $p(x)$ as $c e^{- J(x)}$ for some $J(x)$.*
    - (iii) Where is the **inflection point**? I.e. where $\frac{d^2 p}{d x^2}(x) = 0$.
    - (iv) *Optional*: Some forms of *sensitivity analysis* (typically for non-Gaussian $p$) consist in estimating/approximating the Hessian, i.e. $\frac{d^2 \log p}{d x^2}$. Explain what this has to do with *uncertainty quantification*.

    #### Exc (optional) – Change of variables

    Let $U = \phi(X)$ for some monotonic function $\phi$,
    and let $p_x$ and $p_u$ be their probability density functions (pdf).

    - (a): Show that $p_u(u) = p_x\big(\phi^{-1}(u)\big) \frac{1}{|\phi'(u)|}$,
    - (b): Show that you don't need to derive the density of $u$ in order to compute its expectation, i.e. that
      $$ \mathbb{E}[U] = \int  \phi(x) \, p_x(x) \, d x ≕ \mathbb{E}[\phi(x)] \,, $$
      *PS: this result is [pretty intuitive](https://en.wikipedia.org/wiki/Law_of_the_unconscious_statistician),
      and also holds for non-injective transformations, $\phi$,
      as well as functions of multiple random variables.*
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("CVar in proba")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc (optional) – Integrals

    Recall $p(x) = \mathscr{N}(x \mid \mu, \sigma^2)$ from eqn. (G1). Abbreviate it as $c = (2 \pi \sigma^2)^{-1/2}$.
    Use pen, paper, and calculus to show that

    - (i) the first parameter, $\mu$, indicates its **mean**, i.e. that $\mu = \mathbb{E}[X] \,.$
      *Hint: you can rely on the result of (iii)*
    - (ii) the second parameter, $\sigma^2>0$, indicates its **variance**,
      i.e. that $\sigma^2 = \mathbb{Var}(X) \mathrel{≔} \mathbb{E}[(X-\mu)^2] \,.$
      *Hint: use $x^2 = x x$ to enable integration by parts.*
    - (iii) $c$ is indeed the right normalizing constant, i.e. that
      $$ E[1] = 1 \,. $$
      *Hint: Neither Bernoulli nor Laplace managed this,
      until [Gauss (1809)](#references) did by first deriving $(E[1])^2$.
      Here is a nice [video demonstration by 3Blue1Brown](https://www.youtube.com/watch?v=cy8r7WSuT1I&t=3m52s).*
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("Gauss integrals")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc (optional) – Riemann sums

    Recall that integrals (for example for the mean and variance)
    compute an "area under the curve".
    On a discrete grid, integrals can be approximated using the [Trapezoidal rule](https://en.wikipedia.org/wiki/Riemann_sum#Trapezoidal_rule).

    - (a) Replace `np.trapezoid` below with your own implementation (using `sum()`).
    - (b) Use `np.trapezoid` to compute the probability that a scalar Gaussian $X$ lies within $1$ standard deviation of its mean.
      *Hint: the numerical answer you should find is $\mathbb{P}(X \in [\mu {-} \sigma, \mu {+} \sigma]) \approx 68\%$.*
    """)
    return


@app.cell
def _(grid1d, np, pdf_G1):
    def mean_and_var(pdf_values, grid):
        f, x = pdf_values, grid
        mu_ = np.trapezoid(f * x, x)
        s2 = np.trapezoid(f * (x - mu_) ** 2, x)
        return mu_, s2

    mean_and_var(pdf_G1(grid1d, mu=0, sigma2=2**2), grid1d)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("Riemann sums", "a")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc – The uniform distribution

    Below is the pdf of the [uniform/flat/box distribution](https://en.wikipedia.org/wiki/Uniform_distribution_(continuous))
    for a given mean and variance.

    - Use `mean_and_var()` to verify `pdf_U1` (as is).
    - Replace `_G1` with `_U1` in the code generating the above interactive plot.
    - Why are the walls (ever so slightly) inclined?
    - Write your own implementation below, and check that it reproduces the `scipy` version already in place.
    """)
    return


@app.cell
def _(np, sp):
    def pdf_U1(x, mu, sigma2):
        a = mu - np.sqrt(3 * sigma2)
        b = mu + np.sqrt(3 * sigma2)
        pdf_values = sp.stats.uniform(loc=a, scale=(b - a)).pdf(x)
        # Your own implementation:
        # height = ...
        # pdf_values = height * np.ones_like(x)
        # pdf_values[x<a] = ...
        # pdf_values[x>b] = ...
        return pdf_values

    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("pdf_U1")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The multivariate (i.e. vector) Gaussian

    A *multivariate* random variable, i.e. a **vector**, is simply a collection of scalar variables (on the same probability space).
    Its distribution is the *joint* distribution of its components.
    The pdf of the multivariate Gaussian $\mathbf{X}$ (for any dimension $\ge 1$) is

    $$
    \large \mathscr{N}(\mathbf{x} \mid \mathbf{\mu}, \mathbf{\Sigma}) =
    |2 \pi \mathbf{\Sigma}|^{-1/2} \, \exp\Big(-\frac{1}{2}\|\mathbf{x}-\mathbf{\mu}\|^2_\mathbf{\Sigma} \Big) \,, \tag{GM}
    $$
    which is very similar to the univariate (scalar) case (G1),
    but with $|.|$ representing the matrix determinant,
    and $\|.\|_\mathbf{W}$ representing the weighted 2-norm: $\|\mathbf{x}\|^2_\mathbf{W} = \mathbf{x}^T \mathbf{W}^{-1} \mathbf{x}$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "$\\mathbf{W}$ must be symmetric-positive-definite (SPD) because ... (optional reading 🔍)": mo.md(r"""
    - The norm (a quadratic form) is invariant to any asymmetry in the weight matrix.
    - The density (GM) would not be integrable (over $\mathbb{R}^{d}$) unless $\mathbf{x}^{\mathsf{T}} \mathbf{\Sigma}^{-1} \mathbf{x} > 0$ for all $\mathbf{x} \neq \mathbf{0}$.
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Moreover, [as above](#exc-optional-integrals), it can be shown that

    - $\mathbf{\mu} = \mathbb{E}[\mathbf{X}]$,
    - $\mathbf{\Sigma} = \mathbb{E}[(\mathbf{X}-\mu)(\mathbf{X}-\mu)^{\mathsf{T}}]  =: \mathbb{Cov}(\mathbf{X})$.

    As such, $\mathbf{\Sigma}$ is called the **covariance matrix**,
    whose individual elements are individual covariances,
    $\Sigma_{i,j} = \mathbb{E}[(X_i-\mu_i)(X_j-\mu_j)] =: \mathbb{Cov}(X_i, X_j)$,
    and – on the diagonal – variances: $\Sigma_{i,i} = \mathbb{Var}(X_i)$.

    The following implements the pdf (GM).
    """)
    return


@app.cell
def _(la, np):
    def weighted_norm22(points, cov):
        "Computes the weighted norm of each vector (a row in `points`)."
        W = la.inv(cov)  # NB: replace by la.solve() in real applications!
        return np.sum((points @ W) * points, axis=-1)

    def pdf_GM(x, mu, Sigma):
        "pdf – Gaussian, Multivariate: N(x | mu, Sigma) for each x."
        c = np.sqrt(la.det(2 * np.pi * Sigma))
        return 1 / c * np.exp(-0.5 * weighted_norm22(x - mu, Sigma))

    return (pdf_GM,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The norm implementation is a bit tricky because it uses `@` (matrix multiplication), `*` (array, i.e. element-wise multiplication) and `axis=-1` (sum along the last dimension) to enable inputting the entire lattice/grid at once without shape manipulation.
    """)
    return


@app.cell
def _(grid1d, np):
    grid2d = np.dstack(np.meshgrid(grid1d, grid1d))
    grid2d.shape
    return (grid2d,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following code plots the pdf as contour (level) curves.

    <mark><font size="-1">
    Migration note: the original code guarded the optional scatter overlay with
    `if seed and 'sample_GM' in globals()`, because in a linear-execution notebook
    `sample_GM` is only defined *after* this cell, textually. marimo builds its
    dependency graph from actual variable references (not cell position), so simply
    referencing `sample_GM` below makes marimo schedule its defining cell first,
    automatically -- the `globals()` existence check is no longer needed at all.
    </font></mark>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    controls2 = mo.ui.dictionary({
        "corr": mo.ui.slider(start=-1, stop=1, step=.001, value=0.7, show_value=True, label="corr"),
        "std_x": mo.ui.slider(start=1e-5, stop=10, value=1, step=.1, show_value=True, label="std_x"),
        "seed": mo.ui.slider(start=0, stop=9, step=1, value=0, show_value=True, label="seed"),
    })
    return (controls2,)


@app.cell
def _(controls2, grid1d, grid2d, hookup, la, np, pdf_GM, plt, sample_GM):
    def _plot_pdf_G2(corr, std_x, seed):
        mu = 0
        var_x = std_x**2
        var_y = 1
        cv_xy = np.sqrt(var_x * var_y) * corr

        C = 25 * np.array([[var_x, cv_xy],
                            [cv_xy, var_y]])

        density_values = pdf_GM(grid2d, mu=mu, Sigma=C)

        plt.figure(figsize=(4, 4))
        plt.contour(grid1d, grid1d, density_values, cmap="plasma",
                    levels=np.linspace(1e-4, 1 / np.sqrt(la.det(2 * np.pi * C)), 11))

        if seed:
            plt.scatter(*sample_GM(mu, C=C, N=100, rng=seed))

        plt.axis('equal')
        return plt.gca()

    hookup(controls2, _plot_pdf_G2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that the code defines the covariance `cv_xy` from the input ***correlation*** `corr`.
    This is a coefficient (number),
    defined for any two random variables $X$ and $Y$ (not necessarily Gaussian) as
    $$ \rho[X,Y]=\frac{\mathbb{Cov}[X,Y]}{\sigma_x \sigma_y} \,. $$
    Equivalently, it is the covariance between the *standardized* variables,
    i.e. $\rho[X,Y] = \mathbb{Cov}[X / \sigma_x, Y / \sigma_y]$.
    It quantifies (defines) the ***linear dependence*** between $X$ and $Y$,
    as illustrated by the following exercises.

    #### Exc – Correlation influence

    How do the contours look? Try to understand why. Cases:

    - (a) correlation=0.
    - (b) correlation=0.99.
    - (c) correlation=0.5. (Note that we've used `plt.axis('equal')`).
    - (d) correlation=0.5, but with non-equal variances.

    Finally (optional): why does the code "crash" when `corr = +/- 1`? Is this a good or a bad thing?

    More generally, it can be shown that $\rho^2$ is the proportion of the variance of $Y$
    captured/explained by a simple linear regression from $X$.

    #### Exc (optional) – Correlation extremes

    Show that

    - (a) $\rho[X,Y] = 0$ if $X$ and $Y$ are independent.
    - (b) $\rho = 1$ if $Y = a X$ for some $a > 0$.
    - (c) $\rho = -1$ if $Y = a X$ for some $a < 0$.

    Otherwise, it can be shown by Cauchy-Schwarz, that $-1\leq \rho \leq 1$.
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("Correlation extremes", "a")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc – Correlation game

    [Play](http://guessthecorrelation.com/) until you get a score (gold coins) of 5 or more.

    #### Exc – Correlation disambiguation

    - What's the difference between correlation and covariance (in a single sentence)?
    - What's the difference between non-zero (C) correlation (or covariance) and (D) dependence?
      *Hint: consider this [image](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient#/media/File:Correlation_examples2.svg).*
      - Does $C \Rightarrow D$ or the converse?
      - What about the negation, $\neg D \Rightarrow \neg C$, or its converse?*
      - What about the (jointly) Gaussian case?
    - Does correlation (or dependence) imply causation?
    - Suppose $x$ and $y$ have non-zero correlation, but neither one causes the other.
      Does information about $y$ give you information about $x$?

    #### Exc – Arithmetics of random variables

    - (a) Prove the linearity of the expectation operator:
      $\mathbb{E}[a X + Y] = a \mathbb{E}[X] + \mathbb{E}[Y]$.
    - (b) Thereby, show that $\mathbb{Var}[ a  X + Y ] = a^2 \mathbb{Var} [X] + \mathbb{Var} [Y]$
      if $X$ and $Y$ are independent.
    - (c) Similarly, prove:
      $\mathbb{Cov}[ \mathbf{A} \, \mathbf{X} + \mathbf{Y} ] = \mathbf{A} \, \mathbb{Cov} [\mathbf{X}] \, \mathbf{A}^{\mathsf{T}} + \mathbb{Cov}[\mathbf{Y}]$ if $\mathbf{X}$ and $\mathbf{Y}$ are independent.
    - (d – *optional*) If $X$ and $Y$ are Gaussian, then so is $X + Y$.
      Proof in the next tutorial. Meanwhile watch the [`3blue1brown` video](https://www.youtube.com/watch?v=d_qvLDhkg00&t=266s&ab_channel=3Blue1Brown).
    - (e) Let $\mathbf{Z} \sim \mathscr{N}(\mathbf{0}, \mathbf{I})$,  where $\mathbf{I}$ is the identity matrix.
      Show that each component, $Z_i$, is independent of all others.
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("RV linear algebra", "a")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc – Gaussian (multivariate) sampling

    Pseudo-random samples of $Z_i\sim \mathscr{N}(0, 1)$
    can be generated on any modern computer using one of [these algorithms](https://en.wikipedia.org/wiki/Normal_distribution#Computational_methods).
    As shown above, the "transformation" $\mathbf{X} = \mathbf{L} \mathbf{Z} + \mu$
    yields $\mathbf{X} \sim \mathscr{N}(\mu, \mathbf{C})$,
    which can be used to sample with a desired mean and covariance, $\mathbf{C} = \mathbf{L}^{}\mathbf{L}^T$.
    Indeed, the code below samples $N$ realizations of $\mathbf{X}$,
    and assembles them as columns in an "ensemble matrix", $\mathbf{E}$.
    But `for` loops are slow in Python (and Matlab).
    Replace it with something akin to `E = mu + L@Z`.
    *Hint: this snippet will fail because it's trying to add a vector to a matrix.*
    """)
    return


@app.cell
def _(np, rnd):
    def sample_GM(mu=0, L=None, C=None, N=1, reg=0, rng=rnd):
        if isinstance(rng, int):
            rng = rnd.default_rng(seed=rng)

        if L is None:
            from numpy.linalg import cholesky
            if reg:
                C = C + reg * np.eye(len(C))
            L = cholesky(C)

        d = len(L)
        Z = rng.standard_normal((N, d)).T

        if np.isscalar(mu):
            mu = mu * np.ones(d)

        # Using a loop ("slow"):
        E = np.zeros((d, N))
        for n in range(N):
            E[:, n] = mu + L @ Z[:, n]

        return E

    return (sample_GM,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Go back up to the interactive illustration of the 2D Gaussian distribution and re-run its cell to check (eyeball measure) your implementation.
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("Broadcasting")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Exc (optional) – Gaussian ubiquity

    Why are we so fond of the Gaussian assumption?
    """)
    return


@app.cell(hide_code=True)
def _(show_answer):
    show_answer("Why Gaussian")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    The Normal/Gaussian distribution is bell-shaped.
    Its parameters are the mean and the variance.
    In the multivariate case, the mean is a vector,
    while the second parameter becomes a covariance *matrix*,
    whose off-diagonal elements represent scaled correlation factors,
    which measure *linear* dependence.

    ### Next: [T3 - Bayes' rule and inference](../T3/T3.html)

    ### References

    - **Laplace (1812)**: P. S. Laplace, "Théorie Analytique des Probabilités", 1812.
    - **Gauss (1809)**: Gauss, C. F. (1809). *Theoria Motus Corporum Coelestium in Sectionibus Conicis Solem Ambientium*. Specifically, Book II, Section 3, Art. 177-179, where he presents the method of least squares (which will be very relevant to us) and its probabilistic justification based on the normal distribution of errors.
    """)
    return


if __name__ == "__main__":
    app.run()
