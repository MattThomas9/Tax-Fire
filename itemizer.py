# ===================================================== Itemizer ===================================================== #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Jan. 26, 2019 ============================================= #
# ==================================================================================================================== #
# ------------------------------------- Built based on IRS Form 1040 Schedule A -------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


def itemizer(medical_dental, real_estate_personal_property, other_tax_expenses, home_mortgage_interest,
             investment_interest, gifts, casualty_theft, other_itemized_deductions, federal_agi, state_tax_withholding):
    a1 = medical_dental
    a2 = federal_agi
    a3 = a2 * 0.075
    if a3 > a1:
        a4 = 0
    else:
        a4 = a1 - a3
    a5 = min(state_tax_withholding + real_estate_personal_property, 10000)
    a6 = other_tax_expenses
    a7 = a5 + a6
    a8 = home_mortgage_interest
    a9 = investment_interest
    a10 = a8 + a9
    a14 = gifts
    a15 = casualty_theft
    a16 = other_itemized_deductions
    a17 = a4 + a7 + a10 + a14 + a15 + a16
    return a17
