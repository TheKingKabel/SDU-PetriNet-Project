from enum import Enum
import numpy as np
import scipy as sp


class DistributionType(Enum):
    NORM = "Normal"
    UNI = "Uniform"
    CAU = "Cauchy"
    T_D = "T-Distribution"
    F_D = "F-Distribution"
    CHI = "Chi-Square"
    EXP = "Exponential"
    WEI = "Weibull"
    LOGN = "Lognormal"
    BI_SA = "Birnbaum-Saunders (Fatigue Life)"
    GAMMA = "Gamma"
    D_EXP = "Double Exponential"
    P_NORM = "Power Normal"
    P_LOGN = "Power Lognormal"
    TU_LAMBDA = "Tukey-Lambda"
    EXT_VAL = "Extreme value Type 1"
    BETA = "Beta"

    BIN = "Binomial"
    POI = "Poisson"


def getDelay(distribution, delay: int = 0, a=0, b=0, c=0, d=0):

    if distribution == "NORM":
        return np.random.normal(a, b)

    if distribution == "UNI":
        return np.random.uniform(a, b)

    if distribution == "CAU":
        return sp.stats.cauchy.rvs(a, b)

    if distribution == "T_D":
        return sp.stats.t.rvs(a, b)

    # check
    if distribution == "F_D":
        return np.random.noncentral_f(a, b, c)

    if distribution == "CHI":
        return np.random.chisquare(a)

    if distribution == "EXP":
        return np.random.exponential(a)

    if distribution == "WEI":
        return np.random.weibull(a)

    if distribution == "LOGN":
        return np.random.lognormal(a, b)

    if distribution == "BI_SA":
        return sp.stats.fatiguelife(a, b, c)

    if distribution == "GAMMA":
        return np.random.gamma(a, b)

    if distribution == "D_EXP":
        return np.random.laplace(a, b)

    if distribution == "P_NORM":
        return sp.stats.powernorm(a, b, c)

    if distribution == "P_LOGN":
        return sp.stats.powerlognorm(a, b, c, d)

    if distribution == "TU_LAMBDA":
        return sp.stats.tukeylambda(a, b, c)

    # check
    if distribution == "EXT_VAL":
        return

    if distribution == "BETA":
        return np.random.beta(a, b)

    if distribution == "BIN":
        return np.random.binomial(a, b)

    if distribution == "POI":
        return np.random.poisson(a)
