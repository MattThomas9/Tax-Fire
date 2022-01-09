# ================================ Determine Qualified Dividends and Capital Gains Tax =============================== #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Jan. 27, 2019 ============================================= #
# ==================================================================================================================== #
# ----------- Built based on Qualified Dividends and Capital Gain Tax Worksheet—Line 16 in IRS From 1040 ------------- #
# -------------------------------------Version: Tax Year 2021 1040 Instructions--------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
from taxtablelookup import taxtablelookup
from taxcalc import taxcalc


def qdcgtax(total_taxable_income, qualified_dividends, net_capital, net_long_term_capital,
            long_term_capital_gain_brackets, federal_brackets, number_federal_brackets):
    line_1 = total_taxable_income
    line_2 = qualified_dividends
    if (net_long_term_capital <= 0.0) or (net_capital <= 0.0):
        line_3 = 0.0
    else:
        line_3 = min(net_long_term_capital, net_capital)
    line_4 = line_2 + line_3
    if (line_1 - line_4) <= 0.0:
        line_5 = 0.0
    else:
        line_5 = line_1 - line_4
    line_6 = long_term_capital_gain_brackets[0][1]
    line_7 = min(line_1, line_6)
    line_8 = min(line_5, line_7)
    line_9 = line_7 - line_8
    line_10 = min(line_1, line_4)
    line_11 = line_9
    line_12 = line_10 - line_11
    line_13 = long_term_capital_gain_brackets[1][1]
    line_14 = min(line_1, line_13)
    line_15 = line_5 + line_9
    if (line_14 - line_15) <= 0.0:
        line_16 = 0.0
    else:
        line_16 = line_14 - line_15
    line_17 = min(line_12, line_16)
    line_18 = line_17 * (long_term_capital_gain_brackets[1][2] / 100.0)
    line_19 = line_9 + line_17
    line_20 = line_10 - line_19
    line_21 = line_20 * (long_term_capital_gain_brackets[2][2] / 100.0)
    if line_5 < 100000.0:
        line_22 = taxtablelookup(line_5, federal_brackets, number_federal_brackets)
    else:
        line_22 = taxcalc(line_5, federal_brackets, number_federal_brackets)
    line_23 = line_18 + line_21 + line_22
    if line_1 < 100000.0:
        line_24 = taxtablelookup(line_1, federal_brackets, number_federal_brackets)
    else:
        line_24 = taxcalc(line_1, federal_brackets, number_federal_brackets)
    line_25 = min(line_23, line_24)
    return [line_22, line_18 + line_21, line_25]
