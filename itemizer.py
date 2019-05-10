# ===================================================== Itemizer ===================================================== #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Jan. 26, 2019 ============================================= #
# ==================================================================================================================== #
# ------------------------------------- Built based on IRS Form 1040 Schedule A -------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


def itemizer(expmed, exprel, exptxo, expmor, expinv, expgif, expcas, expoth, fedagi, staxwh):
    a1 = expmed
    a2 = fedagi
    a3 = a2 * 0.075
    if a3 > a1:
        a4 = 0
    else:
        a4 = a1 - a3
    a5 = min(staxwh + exprel, 10000)
    a6 = exptxo
    a7 = a5 + a6
    a8 = expmor
    a9 = expinv
    a10 = a8 + a9
    a14 = expgif
    a15 = expcas
    a16 = expoth
    a17 = a4 + a7 + a10 + a14 + a15 + a16
    return a17