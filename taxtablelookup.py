# ============================================= Tax Table Lookup Routine ============================================= #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Jan. 27, 2019 ============================================= #
# ==================================================================================================================== #
# -------------------------------------------------------------------------------------------------------------------- #
from taxcalc import taxcalc


def taxtablelookup(taxblinc, taxbrk, ntaxbrk):
    if (taxblinc % 100) >= 50:
        lowerbound = taxblinc - (taxblinc % 100) + 50
    else:
        lowerbound = taxblinc - (taxblinc % 100)
    upperbound = lowerbound + 50
    lowerboundtax = taxcalc(lowerbound, taxbrk, ntaxbrk)
    upperboundtax = taxcalc(upperbound, taxbrk, ntaxbrk)
    tabletax = round((lowerboundtax + upperboundtax) / 2, 0)
    return tabletax
