# ============================================== Tax Calculator Routine ============================================== #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Jan. 27, 2019 ============================================= #
# ==================================================================================================================== #
# -------------------------------------------------------------------------------------------------------------------- #


def taxcalc(taxable_income, tax_brackets, number_tax_brackets):
    c = []
    tax = 0.0
    for i in range(0, number_tax_brackets):
        if i == 0:
            c.append(0.0)
        else:
            c.append(c[i - 1] + (tax_brackets[i - 1][1] - tax_brackets[i - 1][0]) * (tax_brackets[i - 1][2] / 100))
        if taxable_income <= tax_brackets[i][1]:
            tax = c[i] + (taxable_income - tax_brackets[i][0]) * (tax_brackets[i][2] / 100)
            break
    return tax
