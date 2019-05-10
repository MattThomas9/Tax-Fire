# ================================ Determine Qualified Dividends and Capital Gains Tax =============================== #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Jan. 27, 2019 ============================================= #
# ==================================================================================================================== #
# ----------- Built based on Qualified Dividends and Capital Gain Tax Worksheet—Line 11a in IRS From 1040 ----------- #
# -------------------------------------------------------------------------------------------------------------------- #
from taxtablelookup import taxtablelookup
from taxcalc import taxcalc


def qdcgtax(tottaxinc, qualdiv, cpnet, cpltnet, brkltcg, brkfedtax, nbrkfedtax):
    a1 = tottaxinc
    a2 = qualdiv
    if (cpltnet <= 0.0) or (cpnet <= 0.0):
        a3 = 0.0
    else:
        a3 = min(cpltnet, cpnet)
    a4 = a2 + a3
    a5 = 0  # this value has something to do with Form 4952, leaving as placeholder
    if (a4 - a5) <= 0.0:
        a6 = 0.0
    else:
        a6 = a4 - a5
    if (a1 - a6) <= 0.0:
        a7 = 0.0
    else:
        a7 = a1 - a6
    a8 = brkltcg[0][1]
    a9 = min(a1, a8)
    a10 = min(a7, a9)
    a11 = a9 - a10
    a12 = min(a1, a6)
    a13 = a11
    a14 = a12 - a13
    a15 = brkltcg[1][1]
    a16 = min(a1, a15)
    a17 = a7 + a11
    if (a16 - a17) <= 0.0:
        a18 = 0.0
    else:
        a18 = a16 - a17
    a19 = min(a14, a18)
    a20 = a19 * (brkltcg[1][2] / 100)
    a21 = a11 + a19
    a22 = a12 - a21
    a23 = a22 * (brkltcg[2][2] / 100)
    if a7 < 100000.00:
        a24 = taxtablelookup(a7, brkfedtax, nbrkfedtax)
    else:
        a24 = taxcalc(a7, brkfedtax, nbrkfedtax)
    a25 = a20 + a23 + a24
    if a1 < 100000.00:
        a26 = taxtablelookup(a1, brkfedtax, nbrkfedtax)
    else:
        a26 = taxcalc(a1, brkfedtax, nbrkfedtax)
    a27 = min(a25, a26)
    areslt = [a24, a20 + a23, a27]
    return areslt
