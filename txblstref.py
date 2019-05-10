# ========================================= Taxable State Refund Determiner ========================================== #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Jan. 26, 2019 ============================================= #
# ==================================================================================================================== #
# -- Built based on State and Local Income Tax Refund Worksheet-Schedule 1, Line 10 from IRS Form 1040 Instructions -- #
# -------------------------------------------------------------------------------------------------------------------- #


def txblstref(prevrefund, prevtotalitemized, prevstnded):
    if prevstnded < prevtotalitemized:
        b = prevtotalitemized - prevstnded
        return min(prevrefund, b)
    else:
        b = 0.0
        return min(prevrefund, b)
