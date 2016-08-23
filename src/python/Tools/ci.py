#!/illumina/development/haplocompare/hc-virtualenv/bin/python
# coding=utf-8
#
# Copyright (c) 2010-2016 Illumina, Inc.
# All rights reserved.
#
# This file is distributed under the simplified BSD license.
# The full text can be found here (and in LICENSE.txt in the root folder of
# this distribution):
#
# https://github.com/Illumina/licenses/blob/master/Simplified-BSD-License.txt


from __future__ import division
from math import log1p

import numpy as np
import scipy.stats as stats


def jeffreysCI(x, n, alpha=0.05):
    '''Modified Jeffreys confidence interval for binomial proportions:
    Brown, Cai and DasGupta: Interval Estimation for a Binomial Proportion.
    2001, doi:10.1214/ss/1009213286'''

    p = x / n
    beta = stats.distributions.beta(x+0.5, n-x+0.5)

    # lower bound
    if x == n:
        lower = (alpha/2)**(1/n)
    elif x <= 1:
        lower = 0.0
    else:
        lower = beta.ppf(alpha/2)

    # upper bound
    if x == 0:
        upper = 1-(alpha/2)**(1/n)
    elif x >= n-1:
        upper = 1.0
    else:
        upper = beta.isf(alpha/2)

    # avoid values outside the unit range due to potential numerical inaccuracy
    lower = max(lower, 0.0)
    upper = min(upper, 1.0)

    return (p, lower, upper)


binomialCI = np.vectorize(jeffreysCI)