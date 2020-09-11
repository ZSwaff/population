#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


import random
import itertools

import numpy as np


# this article says 15% of overage women are childless
# https://www.statista.com/statistics/241535/percentage-of-childless-women-in-the-us-by-age/
# then we take the distribution from this article
# https://www.statista.com/statistics/183790/number-of-families-in-the-us-by-number-of-children/
# and fudge it until the overall rate matches 1.73 from this article
#https://data.worldbank.org/indicator/SP.DYN.TFRT.IN?locations=US
child_distr = [.15, .35, .33, .10, 0, 0, .07]

init_count = 2  #15-25 per Tara + 2 family
pop = 8e9


np_cd = np.array(child_distr)
np_cumu_cd = np.array([e * i for i, e in enumerate(child_distr)])
repr_rate = np.sum(np_cumu_cd)
ints = list(range(len(child_distr)))
child_sampler = [f for i, e in enumerate(child_distr) for f in [i] * int(e * 100)]


def generation(c):
    # we assume pop and repr distr are constant and that other places make up for lower rate
    if c > 10000:
        # don't worry about randomizing, set repr rate up to 2
        return int(c/pop * c * 2 * .5 + (1 - c/pop) * c * 2)
    return sum(random.choices(ints, child_distr, k=c))


def simulate():
    c = init_count
    p = pop

    for i in itertools.count():
        c = generation(c)
        if c >= p:
            return True, i
        if c == 0:
            return False, None


def main():
    reps = 1000

    res = [simulate() for _ in range(reps)]
    succs = [e[1] for e in res if e[0]]
    print('Success: {:.2%}'.format(sum(e[0] for e in res)/reps))
    print('Mean   : {}'.format(np.mean(succs)))
    print('Median : {}'.format(np.median(succs)))
    print('75%ile : {}'.format(np.percentile(succs, 75)))



if __name__ == "__main__":
    main()
