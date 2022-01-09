# ===================================================== AGI Fed ====================================================== #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Mar. 08, 2019 ============================================= #
# ==================================================================================================================== #
# -------------------------------------------------------------------------------------------------------------------- #


def agifed(net_capital, wages_salary_tips, taxable_interest, ordinary_dividends, state_refund_taxable_portion,
           other_income, hsa_deduction, other_adjustments):
    if net_capital > 0.0:
        federal_agi = (sum(wages_salary_tips)
                       + sum(taxable_interest)
                       + sum(ordinary_dividends)
                       + net_capital
                       + state_refund_taxable_portion
                       + sum(other_income)
                       - sum(hsa_deduction)
                       - sum(other_adjustments)
                       )
    # the following code is here for a placeholder right now
    # if (net_long_term_capital > 0.0) and (net_capital > 0.0)
    # 28% Rate Gain Calculation will go here
    # Un-recaptured Section 1250 Gain Calculation will go here
    elif net_capital < 0.0:
        federal_agi = (sum(wages_salary_tips)
                       + sum(taxable_interest)
                       + sum(ordinary_dividends)
                       + -min(abs(net_capital), 3000.00)
                       + state_refund_taxable_portion
                       + sum(other_income)
                       - sum(hsa_deduction)
                       - sum(other_adjustments)
                       )
    else:
        federal_agi = (sum(wages_salary_tips)
                       + sum(taxable_interest)
                       + sum(ordinary_dividends)
                       + net_capital
                       + state_refund_taxable_portion
                       + sum(other_income)
                       - sum(hsa_deduction)
                       - sum(other_adjustments)
                       )
    return federal_agi
