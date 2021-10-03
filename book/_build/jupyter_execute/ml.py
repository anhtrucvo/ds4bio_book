#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/smart-stats/ds4bio_book/blob/main/book/ml.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
# 
# # Maximum Likelihood
# 
# How do we get the loss function that we use for logistic regression? It relies on a statistical argument called maximum likelihood (ML). Sadly, ML is used to be represent maximum likelihood and machine learning, both important topics in data science. So you'll just kind of have to get used to which one is being used via the context. 
# 
# To figure out maximum likelihood, let's consider a bunch of coin flips, each with their own probability of a head. Say 
# 
# $$
# p_i = P(Y_i = 1 | x_i) ~~~ 1 - p_i = P(Y_i = 0 | x_i)
# $$
# 
# Here, we write $~| x_i$ in the probability statement to denote that the probability may depend on the realized value of some variable that also depends on $i$, $X_i$, which is denoted as $x_i$. So, for a context, think $Y_i$ is event that person $i$ has hypertension and $x_i$ their smoking consumption in pack years. We'd like to estimate the probability that someone has hypertension given their pack years.
# 
#  We could write this more compactly as:
# 
# $$
# P(Y_i = j | x_i) = p_i ^ j (1 - p_i)^{1-j} ~~~ j \in \{0, 1\}.
# $$
# 
# Consider a dataset, $Y_1, \ldots, Y_n$ and $x_1, \ldots, x_n$. Consider a sequence of potential observed values of the $Y_i$, say $y_1, \ldots, y_n$ where each $y_i$ is 0 or 1. Then, using our formula:
# 
# $$
# P(Y_i = y_i | x_i) = p_i ^ {y_i} (1 - p_i)^{1-y_i}
# $$
# 
# This is the (perhaps?) unfortunate notation that statisticians use, $Y_i$ for the conceptual value of a variable and $y_i$ for a realized value or number that we could plug in. This equation is just the probability of one $y_i$. This is why I'm using a lowercase $x_i$ for the variables we're conditioning on. Perhaps if I was being more correct, I would write something like $P(Y_i = y_i ~|~ X_i = x_i)$, but I find that adds too much notation. 
# 
# What about all of them jointly? If the coin flips are independent, a statistical way of saying unrelated, then the probabilities multiply. So the **joint** probability of our data in this case is 
# 
# $$
# P(Y_1 = y_1, \ldots, Y_n = y_n ~|~ x_1, \ldots, x_n)
# = \prod_{i=1}^n p_i ^ {y_i} (1 - p_i)^{1-y_i}
# $$
# 
# This model doesn't say much, there's nothing to tie these probabilities together. In our example, all we could do is estimate the probability of hypertension for a bunch of people with exactly the same pack years. There's no **parsimony** so to speak. It seems logical that groups with nearly the same pack years should have similar probabilities, or even better that they vary smoothly with pack years. Our logistic regression model does this.
# 
# 
# Consider again, our logistic regression model:
# 
# $$
# \mathrm{logit}(p_i) = \beta_0 + \beta_1 x_i
# $$
# 
# Now we have a model that relates the probabilities to the $x_i$ in a smooth way. This implies that if we plot $x_i$ versus $\mathrm{logit}(p_i)$ we have a line and if we plot $x_i$ versus $p_i$ it looks like a sigmoid. So, under this model, what is our joint probability?
# 
# $$
# P(Y_1 = y_1, \ldots, Y_n = y_n ~|~ x_1, \ldots, x_n)
# = \prod_{i=1}^n p_i ^ {y_i} (1 - p_i)^{1-y_i}
# = \prod_{i=1}^n \left(\frac{e^{\beta_0 + \beta_1 x_i}}{1 + e^{\beta_0 + \beta_1 x_i}}\right)^{y_i}
# \left(\frac{1}{1 + e^{\beta_0 + \beta_1 x_i}}\right)^{1-y_i}
# $$
# 
# We can work around with this a bit to get
# 
# $$
# \exp\left\{\beta_0 \sum_{i=1}^n y_i + \beta_1 \sum_{i=1}^n y_i x_i\right\}\times \prod_{i=1}^n \left(\frac{1}{1 + e^{\beta_0 + \beta_1 x_i}}\right)
# $$
# 
# Notice, interestingly, this only depends on $n$, $\sum_{i=1}^n y_i$ and $\sum_{i=1}^n y_i x_i$. These are called the **sufficient statistics**, since we don't actually need to know the individual data points, just these quantities. (Effectively
# these quantities can be turned into the proportion of Ys that are one and the correlation between the Ys and Xs.) Plug in these quantities and this equation spits out the joint probability of that particular sequence of 0s and 1s for the Ys given this particular collection of Xs. Of course, we can't actually do this, because we don't know $\beta_0$ or $\beta_1$.
# 
# The statistician Fisher got around this problem using maximum likelihood. The principle is something like this. Pick the values of $\beta_0$ and $\beta_1$ that make the data that we actually observed most probable. This seems like a good idea, since the data that we observed must be at least somewhat probable (since we observed it). When you take the joint probability and plug in the actual Ys and Xs that we observed and view it as a function of $\beta_0$ and $\beta_1$, it's called a **likelihood**. So a likelihood is the joint probability with the observed data plugged in and maximum likelihood finds the values of the parameters that makes the data
# that we observed most likely.
# 
# Let's consider that for our problem. Generally, since sums are more convenient than producs, we take the natural logarithm. Then, this works out to be:
# 
# $$
# \beta_0 \sum_{i=1}^n y_i + \beta_1 \sum_{i=1}^n y_i x_i - \sum_{i=1}^n \log\left(1 + e^{\beta_0 + \beta_1 x_i}\right)
# $$
# 
# This is the function that sklearn maximizes over $\beta_1$ and $\beta_0$ to obtain the estimates. There's quite a few
# really good properties of maximum likelihood, which is why we use it.
# 
# 

# ## Linear regression
# 
# You might be surprised to find out that linear regression can also be cast as a likelihood problem. Consider an instance where we assume that the $Y_i$ are Gaussian with a mean equal to $\beta_0 + \beta_1 x_i$ and variance $\sigma^2$. What that means is that the probability that $Y_i$ lies betweens the points $A$ and $B$ is governed by the equation
# 
# $$
# P(Y_i \in [A, B) ~|~ x_i) = \int_A^B \exp\left\{ -(y_i - \beta_0 - \beta_1 x_i)^2 / 2\sigma^2 \right\} dy_i
# $$
# 
# Letting $A=-\infty$ and taking the derivative with respect to $B$, we obtain the density function, sort of the 
# probability on an infintessimally small interval:
# 
# $$
# \exp\left\{ -(y_i - \beta_0 - \beta_1 x_i)^2 / 2\sigma^2 \right\}
# $$
# 
# Uses the density evaluated at the observed data, the joint likelihood assuming independence is:
# 
# $$
# \prod_{i=1}^n \exp\left\{ -(y_i - \beta_0 - \beta_1 x_i)^2 / 2\sigma^2 \right\}
# = \exp\left\{ -\sum_{i=1}^n (y_i - \beta_0 - \beta_1 x_i)^2 / 2\sigma^2 \right\}
# $$
# 
# Since it's more convenient to deal with logs we get that the joint log likelihood is
# 
# $$
# - \sum_{i=1}^n (y_i - \beta_0 - \beta_1 x_i)^2 / 2\sigma^2 
# $$
# 
# Since minimizing the negative is the same as maximizing this, and the constants of proportionality are irrelevant for maximizing for $\beta_1$ and $\beta_0$, we get that maximum likelihood for these parameters minimizes
# 
# $$
# \sum_{i=1}^n (y_i - \beta_0 - \beta_1 x_i)^2
# $$
# 
# which is the same thing we minimized to obtain our least squares regression estimates.
