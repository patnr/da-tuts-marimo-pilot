"""Answer content for T1-T4, ported from notebooks/resources/answers.py.

Finding (from hands-on WASM testing): marimo renders each markdown/math
fragment through an independent KaTeX call with no shared macro namespace,
so a `\\newcommand` preamble trick (as tried in an earlier version of this
file) does not work across cells. Decision: drop the macro system entirely
and write out full LaTeX (`\\mathbf{x}`, `\\mathscr{N}`, `\\mathbb{E}`, etc.)
directly in both notebook prose and these answers.
"""

# Verbatim from resources/answers.py (MD-type entries only; TYPE tag dropped
# since it was only ever "MD" or "TXT", and TXT here just needs a code fence).
ANSWERS = {}

ANSWERS['state variables'] = r"""
- (a) Position (x, y, z), velocity (vx, vy, vz).
- (b)
    - Epidemic (SEIR):
        Susceptible (S), Exposed (E), Infectious (I), Recovered (R) populations.
    - Predator-prey (Lotka-Volterra):
        Foxes (F), Rabbits (R).
- (c) Pressure, temperature, humidity, wind components (u, v, w), at each grid point.
- (d) Pressure, fluid saturations (oil, water, gas), possibly temperature, at each grid cell.
- (e) Concentrations of chemical species, temperature.
- (f) Vehicle density, average velocity, at each road segment.
- (g) Rating value(s) for each player/team.
- (h) Asset price, volatility.

General questions:

- Usually ordering does not affect the mathematics, but it might matters for implementation (e.g., mapping variables to indices).
- No, not for plain prediction purposes, but it is often convenient to have a fixed-length vector for computational efficiency and simplicity.
- It might increases computational cost/complexity and may introduce noise or bugs.
"""

ANSWERS['model error'] = r"""
Most models could be said to be afflicted by most of the shortcomings, but here are what appears most relevant:

- (a) Laws of motion and gravity: 1, 8
- (b) Epidemic (SEIR): 3, 5, 6, 7
- (c) Weather/climate forecasting: 3, 4, 7, 9
- (d) Petroleum reservoir flow: 4, 6, 7, 9
- (e) Chemical and biological kinetics: 3, 7
- (f) Traffic flow: 2, 4, 6, 10
- (g) Sports rating: 2, 7
- (h) Financial pricing: 2, 4, 7
"""

ANSWERS['obs examples'] = r"""
- (a) Altimetry, sextants, speedometers, compass readings, accelerometers, gyroscopes, or fuel-gauges
- (b)
    - SEIR: Number of positive tests, hospitalized, or dead. Sewage analyses. Google searches for symptoms.
    - Predator-prey: loss of harvest or poultry; direct (but incomplete) counts of foxes or rabbits,
        or their tracks, or their droppings.
- (c) Local weather stations. Satellite data. Weather balloons. Each of which can measure a range of variables,
  e.g. temperature, humidity, wind speed/direction, precipitation, radiances.
- (d) Well pressure, production rates (oil, gas, water), oil/water cuts.
- (e) (Bio)chemical analyses, spectrometry, temperature readings.
- (f) Vehicle counts, speed measurements, GPS traces, traffic cameras.
- (g) Game outcomes, scores, player statistics.
- (h) Asset prices, trading volumes, volatility indices.
"""

ANSWERS['thesaurus 1'] = """
```
- Ensemble, Sample, Set of draws
- Stochastic, Random, Monte-Carlo
- Data, Measurements, Observations
```
"""

ANSWERS['thesaurus 2'] = """
```
- Statistical inference, Inverse problems, Inversion, Estimation, Regression, Fitting
- Ensemble member, Sample point, Realization, Single draw, Particle
- Quantitative belief, Probability, Relative frequency, Estimate, Information, Uncertainty, Knowledge
- Recursive, Sequential, Iterative, Serial
- Function, Operator, Model, Transform(ation), Mapping, Relation
```
"""

ANSWERS['Discussion topics 1'] = r'''
 * (a) State estimation for large systems.
 * (b) "State variables" are (potentially unknown) variables that change in time.
   By contrast, "parameters" are constant-in-time (but potentially unknown) variables.
 * (c) "Prognostic" variables are *essential* for the prediction of the dynamical system.
   As such they are to be found among $x$ (contingent on the chosen parameterisation).
   By contrast, "diagnostic" variables can be derived (computed) from the prognostic/state variables.
   For example the observations, $y$, or other non-state quantities
   such as as momentum and energy (in case the state contains the velocity),
   or precipitation (in case the state contains pressure, humidity, salinity, ...).
 * (d) In priciniple, $t(k)$ is a point in time at which we receive a new observation.
       In practice, however, we tend to accumulate observations over some amount of time,
       and only *assimilate* them at regular intervals,
       determined by the frequency with which we *wish* to launch new forecasts.
       Note that this practice complicates the theory somewhat.
 * (e) In principle it's a science. In practice...
 * (f) Abstract concept to break the problem down into smaller, *recursive*, problems.
   DAGs. Formalises the concept of hidden variables (states).
'''

ANSWERS['pdf_G1'] = """
```python
const = 1/np.sqrt(2*np.pi*sigma2)
pdf_values = const * np.exp(-0.5*(x - mu)**2/sigma2)
```
"""

ANSWERS['Riemann sums a'] = """
```python
# Midpoint rule, dx assumed constant
dx = x[1] - x[0]
mu = sum(f * x) * dx
s2 = sum(f * (x-mu)**2) * dx

# Alternatively: Right rule
dxs = np.diff(x)
mu = sum((f * x)[1:] * dxs)
s2 = sum((f * (x-mu)**2)[1:] * dxs)
```
"""

ANSWERS['pdf_U1'] = """
```python
height = 1/(b - a)
pdf_values = height * np.ones_like(x)
pdf_values[x<a] = 0
pdf_values[x>b] = 0
```
"""

ANSWERS['Gauss integrals'] = r'''
(i) Consider:
$$
\begin{align} \mathbb{E}[x]
&= \int x \, p(x) \,d x \tag{by definition} \\
&= \int x \, c \, e^{-(x-\mu)^2 / 2 \sigma^2} \,d x \tag{by definition} \\
&= \int (u + \mu) \, c \, e^{-u^2 / 2 \sigma^2} \,d u \tag{$u = x-\mu$}\\
&= \int u \, c \, e^{-u^2 / 2 \sigma^2} \,d u
\;+\;  \mu \int \, c \, e^{-u^2 / 2 \sigma^2} \,d u \tag{distribute integral}\\
&= \big[-\sigma^2 \, c \, e^{-u^2 / 2 \sigma^2}\big]^{+\infty}_{-\infty}
\;+\; \mu \, \mathbb{E}[1] \tag{integrate-by-parts + identify}
\end{align}
$$
The first term is zero. The second leaves only $\mu$, since $\mathbb{E}[1] = 1$.

(ii) Consider:
$$
\begin{align} \mathbb{E}[(x - \mu)^2]
&= \int (x - \mu)^2 \, c \, e^{-(x-\mu)^2 / 2 \sigma^2} \,d x \tag{by definition} \\
&= \int u^2 \, c \, e^{-u^2 / 2 \sigma^2} \,d u \tag{$u = x-\mu$}\\
&= \int u \, \big[ u \, c \, e^{-u^2 / 2 \sigma^2} \big] \,d u \tag{$u^2 = u\, u$} \\
&= 0 - \int (1) \big[-\sigma^2 \, c \, e^{-u^2 / 2 \sigma^2}\big] \,d u \,,  \tag{integrate by parts} \\
\end{align}
$$
where the first term was zero for the same reason as above,
and the second can again be expressed in terms of $\mathbb{E}[1] = 1$.
'''

ANSWERS['CVar in proba a'] = r'''
[Link](https://stats.stackexchange.com/a/239594)
'''

ANSWERS['CVar in proba b'] = r'''
The answer is in the link in the question,
more precisely [here](https://en.wikipedia.org/wiki/Law_of_the_unconscious_statistician#Continuous_case).

But why is the result so intuitive?
Because the formal proof is a lot of ado for nothing;
it actually involves applying (integral) change-of-variables *twice*,
thereby cancelling itself out:

- Once to derive $p_u$ from $p_x$, although
  [differently](https://en.wikipedia.org/wiki/Integration_by_substitution#Application_in_probability)
  than in part (a).
- A second time when substituting $u$ by $\phi(x)$ in the integral for the expectation.
'''

ANSWERS['Correlation extremes a'] = r"""
Recall that $p(x, y) = p(x|y) \, p(y) = p(x) \, p(y)$ by independence.
Thus,
$$ \begin{align}
\mathbb{Cov}(X, Y)
&= \int (x - \mu_x)(y - \mu_y) \, p(x, y) \, d x \, d y \\
&= \Big(\int (x - \mu_x) p(x) \, d x \Big) \Big(\int (y - \mu_y) p(y) \, d y \Big)
\,.
\end{align}
$$
But of course, $\int x \, p(x) \, d x = \mu_x$, so each integral is zero,
as is the resulting correlation.
"""

ANSWERS['RV linear algebra a'] = r"""
- By the linearity of the integral,
  $$ \mathbb{E}[a X] = \int a x \, p(x) \, d x = a \int x \, p(x) \, d x = a \, \mathbb{E}[X] $$
- By the [law of the unconscious statistician](#Exc-(optional)-–-Change-of-variables)
  $$ \mathbb{E}[X + Y] = \iint (x + y) \, p(x, y) \, d x \, d y \,. $$
  Now consider $\iint x \, p(x, y) \, d x \, d y = \int x \, p(x) \Big(\int p(y | x) d y\Big) dx$.
  The inner integral is $1$ for any $x$ and so can be ignored, leaving just $\mathbb{E}[X]$.
  Likewise, $\iint y \, p(x, y) \, d x \, d y = \mathbb{E}[Y]$.
"""

ANSWERS['Broadcasting'] = """
```python
# Cheating:
# E = rng.multivariate_normal(mu, C, N).T

# Using numpy "broadcasting"
# (would have been a lot easier if using orientation N-times-d):
# E = (mu + (L@Z).T).T

# Make mu 2d:
# mu2d = np.atleast_2d(mu).T
mu2d = mu[:, None]
# mu2d = np.tile(mu, (N, 1)).T
# mu2d = np.outer(mu, np.ones(N))
E = mu2d + L @ Z
```
"""

ANSWERS['Why Gaussian'] = r"""
What's not to love? Consider

 * The central limit theorem (CLT) and all its implications.
 * Pragmatism: Yields "least-squares problems", whose optima is given by a linear systems of equations.
 * Self-conjugate: Gaussian prior and likelihood yields Gaussian posterior.
 * Among pdfs with independent components (2 or more),
   the Gaussian is uniquely (up to scaling) rotation-invariant (symmetric).
 * Gaussians have the maximal entropy for all distributions with a given variance.
 * Gaussians are invariant to self-convolution (i.e. the addition of two random variables)
 * The Gaussian is uniquely (among densities) invariant to the Fourier transform.
 * It is the heat kernel, i.e. the [Green's function](https://en.wikipedia.org/wiki/Green%27s_function#Table_of_Green's_functions)
   of the diffusion equation: one of the fundamental PDEs.
 * Uniquely, among elliptical distributions: uncorrelated, jointly distributed, normal random variables are independent.
 * Uniquely for Gaussian sampling distribution: maximizing the likelihood for the mean simply yields the sample average.
 * Unique in that the sample mean and variance are independent if calculated from a set of independent draws.
 * For more, see [Wikipedia](https://en.wikipedia.org/wiki/Normal_distribution#Properties)
   and Chapter 7 of: [Probability theory: the logic of science (Edwin T. Jaynes)](https://books.google.com/books/about/Probability_Theory.html?id=tTN4HuUNXjgC).
"""



# --- T3 / T4 answers (ported from notebooks/resources/answers.py) ---

ANSWERS['symmetry of conjunction'] = r"""

<a href="https://en.wikipedia.org/wiki/Bayes%27_theorem#For_continuous_random_variables" target="_blank">Wikipedia</a>
"""

ANSWERS['quadrature marginalisation'] = r"""

$$ \texttt{sum(pp)*dx}
\approx \int \texttt{pp}(x) \, dx
= \int p(x) \, p(y|x) \, dx
= \int p(x,y) \, dx
= p(y) \, .
$$
"""

ANSWERS['Posterior behaviour'] = r"""

- Likelihood becomes flat.  
  Thus, the posterior is dominated by the prior,
  and becomes (in the limit) superimposed on it.
- Likelihood becomes a delta function.  
  Posterior gets dominated by the likelihood, and superimposed on it.
- It's located halfway between the prior/likelihood $\forall y$.
- It's always higher than the height of the prior and the likelihood.
  This even holds true for some interval in the mixed Gaussian-uniform cases.
- "Information-wise", the "expected" posterior entropy (and variance)
  is always smaller than that of the prior,
  but in practice (i.e. without averaging over the observations)
  we can observe that it is not necessarily the case.
    - For the uniform-uniform case, yes.
    - For the mixed case, it's not clear what scale/width means,
      but for most (any reasonable?) definitions the answer will be yes.
    - For the linear-Gaussian case, no.
- In the mixed cases: Yes. Otherwise: No.
- In fact, we'll see later that the linear-Gaussian posterior is Gaussian,
  and is therefore fully characterized by its mean and its variance.
  So we only need to compute its location and scale.
- The problem (of computing the posterior) is ill-posed:  
  The prior says there's zero probability of the truth being 
  in the region where the likelihood is not zero.
- This of course depends on the definition of "sufficient",
  but in the authors opinion $N \geq 40$ seems necessary.
"""

ANSWERS['Likelihood'] = r"""

It follows from eqn. (Obs) that $p(y|x)$ is just $p(r)$ evaluated at $r = y - \mathscr{H}(x)$,  
i.e. $\mathscr{N}(y - \mathscr{H}(x) | 0, R)$,  
i.e. $\mathscr{N}(y | \mathscr{H}(x), R)$.

PS: for the non-additive case,
i.e. more complicated combinations of $r$ and $x$,
the likelihood can be derived by applying the
[change-of-variables formula](T2%20-%20Gaussian%20distribution.ipynb#Exc-(optional)-–-Change-of-variables).
For example, multiplicative noise, i.e. $y = x r$, produces $p(y|x) = \mathscr{N}(y | 0, x^2 R)$.
"""

ANSWERS['Observation models a'] = r"""

The likelihood simply shifts/translates towards lower values by $15$.
"""

ANSWERS['what\'s forward?'] = r"""

Because estimation/inference/inverse problems
are looking for the "cause" from the "outcomes".
Of course, causality is a tricky notion.
Anyway, these problems tend to be harder,
generally because they involve solving (possibly approximately) a set of equations
rather than just computing a formula (corresponding to a forward problem).
Since $y = f(x)$ is common symbolism for formulae,
it makes sense to use the symobls $x = f^{-1}(y)$ for the estimation problem.
Note that, despite the "glorious" ideas invoked by language such as "inverse/inversion",
all techniques (known to author) still essentially come down to
some form of *fitting* to data/observations.
"""

ANSWERS['BR Gauss, a.k.a. completing the square a'] = r"""

Expanding the squares of the left hand side of eqn. (LG1),
and gathering terms in powers of $x$ yields
$$
    \frac{(x-x^{\text{f}})^2}{P^{\text{f}}} + \frac{(x-y)^2}{R}
    =  x^2 (1/P^{\text{f}} + 1/R)
    - 2 x (x^{\text{f}}/P^{\text{f}} + y/R)
    + c_1
    \,, \tag{a1}
$$
with $c_1 = (x^{\text{f}})^2/P^{\text{f}} + y^2/R$.
Now consider the right hand side of eqn. (LG1),
$$
    \frac{(x-x^{\text{a}})^2}{P^{\text{f}}} + c_2
    = x^2 / P^{\text{a}}
    - 2 x x^{\text{a}}/P^{\text{a}}
    + (x^{\text{a}})^2/P^{\text{a}}
    + c_2
    \,.
\tag{a2}
$$
where $c_2$ is constant wrt. $x$.
Both (a1) and (a2) are quadratics in $x$,
so we can equate them by requiring
$c_2 = c_1 - (x^{\text{a}})^2/P^{\text{a}}$ and
$$ \begin{align}
1/P^{\text{a}} = 1/P^{\text{f}} + 1/R \,, \tag{a3} \\\
x^{\text{a}}/P^{\text{a}} = x^{\text{f}}/P^{\text{f}} + y/R \,, \tag{a4}
\end{align}
$$
whereupon we immediately recover $P^{\text{a}}$ and $x^{\text{a}}$ of eqns. (5) and (6).

*PS: The above process is called "completing the square"
since it involves writing a quadratic polynomial as a single squared term
plus a "constant" that we add and subtract.*
"""

ANSWERS['LG BR example'] = r"""

- Eqn. (5) yields $P^{\text{a}} = \frac{1}{1/4 + 1/4} = \frac{1}{2/4} = 2$.
- Eqn. (6) yields $x^{\text{a}} = 2 \cdot (20/4 + 18/4) = \frac{20 + 18}{2} = 19$
"""

ANSWERS['BR Kalman1 algebra'] = r"""

- Multiplying eqn. (5) by $1 = \frac{P^{\text{f}} R}{P^{\text{f}} R}$ yields
  $P^{\text{a}} = \frac{P^{\text{f}} R}{P^{\text{f}} + R} = \frac{P^{\text{f}}}{P^{\text{f}} + R} R$, i.e. eqn. (8).
- We also get $P^{\text{a}} = \frac{R}{P^{\text{f}} + R} P^{\text{f}}$.
  Adding $0 = P^{\text{f}} - P^{\text{f}}$ to the numerator yields eqn. (10).
- Applying formulae (8) and (10) for $P^{\text{a}}$
  in eqn. (6) immediately produces eqn. (11).
"""

ANSWERS['KG intuition'] = r"""

Consider eqn. (9). Both nominator and denominator are strictly larger than $0$, hence $K > 0$.
Meanwhile, note that $K$ weights the observation uncertainty $(R)$
vs. the total uncertainty $(P^{\text{f}} + R)$, whence $P^{\text{f}} + R > P^{\text{f}}$, i.e. $K<1$.

Since $0<K<1$, eqn. (8) yields $P^{\text{a}} < R$,
while eqn. (10) yields $P^{\text{a}} < P^{\text{f}}$.

From eqn. (11), $x^{\text{a}} = (1-K) x^{\text{f}} + K y$.
Since $0<K<1$, we can see that $x^{\text{a}}$
is a 'convex combination' or 'weighted average'.
*For even more detail, consider the case $x^{\text{f}}<y$ and then case $y<x^{\text{f}}$.*

Because it describes how much the esimate is "dragged" from $x^{\text{f}}$ "towards" $y$.  
I.e. it is a multiplification (amplification) factor,
which French (signal processing) people like to call "gain".  
"""

ANSWERS['BR Kalman1 code'] = r"""

    KG = H*Pf / (H**2*Pf + R)
    Pa = (1 - KG*H) * Pf
    xa = xf + KG * (y - H*xf)
"""

ANSWERS['MMSE'] = r"""

Inserting $0 = \mu - \mu$ into the expression for the MSE decomposes it into the squared bias (if any)
plus the variance (of $X$ itself), which is independent of the choice of point estimate.
"""

ANSWERS['AR1'] = r"""

- The seed controls the random numbers generated via `numpy.random`
  (imported as `rnd`) that are used to generate the stochastic processes,
  i.e. the `truth` $\\{x_k\\}$ and `obsrvs` $\\{y_k\\}$.
-   - `0`: $\\{x_k\\}$ becomes [(Gaussian) white noise](https://en.wikipedia.org/wiki/White_noise#Discrete-time_white_noise).  
      But if $Q = 0$, it just becomes the constant $0$.
    - `1`: $\\{x_k\\}$ becomes a [(Gaussian) random walk](https://en.wikipedia.org/wiki/Random_walk#Gaussian_random_walk),
      a.k.a. Brownian motion a.k.a. Wiener process.  
      But if $Q=0$ it just becomes the constant $x_0$.
    - As `M` approaches 1 (from below), the process becomes more and more auto-correlated.  
      Its variance (at any given time index) also increases.  
      But if $Q=0$ then the process just decays (geometrically/exponentially) to $0$.
    - `>1`: The process becomes a divergent geometric sequence, and blows up (for any value of $Q$).
- The observations become exact (infinitely precise and accurate).
- The observations become useless, carrying no information.  
  Their variance dominates in the plot, so that it **looks** like $\\{x_k\\}$ becomes flat.
"""

ANSWERS['KF1 code'] = r"""


            # Forecast step
            xf = M * xa
            Pf = M**2 * Pa + Q
            # Analysis update step
            Pa = 1 / (1/Pf + H**2/R)
            xa = Pa * (xf/Pf + H*obsrvs[k]/R)
            # Alternatively:
            # KG = H*Pf / (H**2*Pf + R)
            # Pa = (1 - KG*H) * Pf
            # xa = xf + KG * (y - H*xf)
"""

ANSWERS['KF with bias'] = r"""

-   - If `logR_bias` $\rightarrow -\infty$ then the KF "trusts" the observations too much,
    always jumping to lie right on top of them (also assuming `H=1`).
    - The same happens for `logQ_bias` $\rightarrow +\infty$
    since then the KF has no "faith" in its predictions
    (easier to see if you comment out the line that plots the uncertainty which is now humongous).
    - If `logR_bias` $\rightarrow +\infty$ then the KF attributes no weight to the observations,
    so that only the mean model prediction matters, which is zero.
    - The same happens for `logQ_bias` $\rightarrow -\infty$, except for an initial transitory
    period during which the initial uncertainty of the KF quickly attenuates,
    after which it only trusts its mean prediction.
    - *PS: it may appear that $R$ and $Q$ simply play the opposite role
    (while adding to the complexity of the KF). However, this is only approximately true,
    and less so in more complex settings.*
- Not very long? But longer for larger $R$ or smaller $Q$.
- Even longer.
"""

ANSWERS['KF behaviour'] = r"""

- The uncertainty never reaches 0 (but decays geometrically in time).
- The dynamics always produces 0 at the next time step
  (also since there is almost no noise).
  Therefore, regardless of initial variance or observation precision,
  the KF knows exactly where the state is: at 0.
  Happily, this is reflected in its uncertainty estimate,
  i.e. variance, which is also 0.
"""

ANSWERS['Asymptotic Riccati a'] = r"""

Follows directly from eqn. (6) from both this tutorial and
[the previous one](T3%20-%20Bayesian%20inference.ipynb#Exc-–-BR-LG1).
"""

ANSWERS['Asymptotic Riccati b'] = r"""

From the previous part of the exercise,
if $\mathscr{M} = 1$ then
$1/P^{\text{a}}_k = 1/P^{\text{a}}_{k-1} + 1/R$
and so the difference $1/P^{\text{a}}_k - 1/P^{\text{a}}_{k-1}$
is always $1/R$.
In other words, $1/P^{\text{a}}_k$ grows linearly with $1/R$,
starting from $1/P^{\text{a}}_0$.
"""

ANSWERS['Asymptotic Riccati c'] = r"""

From the previous part of the exercise,
$1/P^{\text{a}}_k \xrightarrow[k \rightarrow \infty]{} +\infty$
"""

ANSWERS['Asymptotic Riccati d'] = r"""

Since $1 / \mathscr{M}^2 > 1$,
$1/P^{\text{a}}_k$ now grows quicker than
in the previous parts of the exercise,
whence the result.

Note that since this is just an inequality,
it holds also for time-dependent $\mathscr{M}_k$
as long as they're less than 1.
"""

ANSWERS['Asymptotic Riccati e'] = r"""

The fixed point $P^{\text{a}}_\infty$ should satisfy
$P^{\text{a}}_\infty = 1/\big(1/R + 1/[\mathscr{M}^2 P^{\text{a}}_\infty]\big)$,
yielding the answer.

Note that this asymptote is **not 0**!
In other words, even though the KF keeps gaining observational data/information,
this gets balanced out by the growth in error/uncertainty during the forecast.
Also note that the asymptotic state uncertainty ($P^{\text{a}}_\infty$)
is directly proportional to the observation uncertainty ($R$).
"""

ANSWERS['Asymptotes when Q>0 a'] = r"""

Again by merging the forecast and analysis steps, we get
$
1/P^a = 1/Q + 1/R
$
which immediately yields
$P^a = 1/ (1/Q + 1/R)$.
"""

ANSWERS['Asymptotes when Q>0 b'] = r"""

Multiply
$$
1/P^a = \frac{1}{P^a + Q} + 1/R
$$
by all of the denominators.
Cancel $P^a R$ from both sides.
"""

ANSWERS['Asymptotes when Q>0 c'] = r"""

As the terms including $Q$ come to dominate,
the equation tends to $P = R - \varepsilon$
with $\varepsilon \rightarrow 0^+$.

This means that if the model error is practically infinite,
then previous information is worthless,
and the uncertainty after each analysis step
equals that of the single observation.
"""

ANSWERS['Asymptotes when Q>0 d'] = r"""

If $Q \rightarrow 0$
then $P \rightarrow 0$,
so the middle term $Q P$ can be neglected,
leaving $P^2 = Q R$.

Thus, $P$ tends to zero if the model error vanishes
(as we also found previously),
but also note that $\sqrt{Q R}$ is perfectly symmetric in $R$ and $Q$.
Indeed, we'd find the same asymptote if we let $R \rightarrow +\infty$.
"""

ANSWERS['signal processing a'] = r"""

    sigproc['Wiener']   = sig.wiener(obsrvs)
"""


def get_answer(tag: str, *subtags: str) -> str:
    """Mirrors resources/answers.py:show_answer's tag/subtag matching."""
    subtag_str = "".join(subtags)
    matching = [k for k in ANSWERS if k.startswith(tag)]
    if not matching:
        raise KeyError(f"No answer found for {tag=!r}")
    parts = []
    for key in matching:
        if not subtag_str or any(key.endswith(" " + ch) for ch in subtags):
            parts.append(ANSWERS[key])
    return "\n\n---\n\n".join(p.strip() for p in parts)
