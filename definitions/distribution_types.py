from enum import Enum
import scipy as sp


class DistributionType(Enum):
    NORM = "Normal"
    UNI = "Uniform"
    CAU = "Cauchy"
    T_D = "T-Distribution"
    F_D = "F-Distribution"
    CHI = "Chi-Square"
    EXP = "Exponential"
    WEI_MIN = "Weibull (Minimum Extreme Value)"
    WEI_MAX = "Weibull (Maximum Extreme Value)"
    LOGN = "Lognormal"
    BI_SA = "Birnbaum-Saunders (Fatigue Life)"
    GAMMA = "Gamma"
    D_EXP = "Double Exponential"
    P_NORM = "Power Normal"
    P_LOGN = "Power Lognormal"
    TU_LAMBDA = "Tukey-Lambda"
    GEV = "Generalized Extreme Value"
    BETA = "Beta"
    BIN = "Binomial"
    POI = "Poisson"


def getDelay(distribution, a=0.0, b=1.0, c=0.0, d=0.0):

    if distribution == "NORM":
        return abs(sp.stats.norm.rvs(a, b))

    if distribution == "UNI":
        return abs(sp.stats.uniform.rvs(a, b))

    if distribution == "CAU":
        return abs(sp.stats.cauchy.rvs(a, b))

    if distribution == "T_D":
        return abs(sp.stats.t.rvs(a, b))

    if distribution == "F_D":
        return abs(sp.stats.f.rvs(a, b, c, d))

    if distribution == "CHI":
        return abs(sp.stats.chi2.rvs(a, b, c))

    if distribution == "EXP":
        return abs(sp.stats.expon.rvs(a, b))

    if distribution == "WEI_MIN":
        return abs(sp.stats.weibull_min.rvs(a, b, c))

    if distribution == "WEI_MAX":
        return abs(sp.stats.weibull_max.rvs(a, b, c))

    if distribution == "LOGN":
        return abs(sp.stats.lognorm.rvs(a, b, c))

    if distribution == "BI_SA":
        return abs(sp.stats.fatiguelife.rvs(a, b, c))

    if distribution == "GAMMA":
        return abs(sp.stats.gamma.rvs(a, b, c))

    if distribution == "D_EXP":
        return abs(sp.stats.laplace.rvs(a, b))

    if distribution == "P_NORM":
        return abs(sp.stats.powernorm.rvs(a, b, c))

    if distribution == "P_LOGN":
        return abs(sp.stats.powerlognorm.rvs(a, b, c, d))

    if distribution == "TU_LAMBDA":
        return abs(sp.stats.tukeylambda.rvs(a, b, c))

    if distribution == "GEV":
        return abs(sp.stats.genextreme.rvs(a, b, c))

    if distribution == "BETA":
        return abs(sp.stats.beta.rvs(a, b, c, d))

    if distribution == "BIN":
        return abs(sp.stats.binom.rvs(a, b, c))

    if distribution == "POI":
        return abs(sp.stats.poisson.rvs(a, b))
