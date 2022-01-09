# ========================================= Taxable State Refund Determiner ========================================== #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Jan. 26, 2019 ============================================= #
# ==================================================================================================================== #
# -- Built based on State and Local Income Tax Refund Worksheet-Schedule 1, Line 10 from IRS Form 1040 Instructions -- #
# -------------------------------------------------------------------------------------------------------------------- #


def txblstref(prior_year_refund, prior_year_itemized_deduction, prior_year_federal_standard_deduction):
    if prior_year_federal_standard_deduction < prior_year_itemized_deduction:
        b = prior_year_itemized_deduction - prior_year_federal_standard_deduction
        return min(prior_year_refund, b)
    else:
        b = 0.0
        return min(prior_year_refund, b)
