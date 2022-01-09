# ============================================= Tax Table Lookup Routine ============================================= #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Jan. 27, 2019 ============================================= #
# ==================================================================================================================== #
# -------------------------------------------------------------------------------------------------------------------- #
from taxcalc import taxcalc


def taxtablelookup(taxable_income, tax_brackets, number_tax_brackets):
    if (taxable_income % 100) >= 50:
        lower_bound = taxable_income - (taxable_income % 100) + 50
    else:
        lower_bound = taxable_income - (taxable_income % 100)
    upperbound = lower_bound + 50
    lower_bound_tax = taxcalc(lower_bound, tax_brackets, number_tax_brackets)
    upper_bound_tax = taxcalc(upperbound, tax_brackets, number_tax_brackets)
    table_tax = round((lower_bound_tax + upper_bound_tax) / 2, 0)
    return table_tax
