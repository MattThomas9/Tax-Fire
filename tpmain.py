# ============================================= Tax Planner Main Solver ============================================== #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Jan. 26, 2019 ============================================= #
# ==================================================================================================================== #
import configparser
from capgnls import capgnls
from txblstref import txblstref
from agifed import agifed
from copy import deepcopy
from itemizer import itemizer
from qdcgtax import qdcgtax
from taxtablelookup import taxtablelookup
from taxcalc import taxcalc
from refund import refund
from optrefund import optrefund
# -------------------------------------------------------------------------------------------------------------------- #
# ************************************************* Input Processing ************************************************* #
# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------- Read the main tax planner input file --------------------------------------- #
# ------------------------------------- and initialize variables with read input ------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
config = configparser.ConfigParser()
config.read('tp.inp')
detailed_print = config.get('Code Control', 'Detailed Print')
tax_year = config.getint('General Tax Information', 'Tax Year')
pay_periods = config.getint('General Tax Information', 'Number of Total Pay Periods')
current_pay_period = config.getint('General Tax Information', 'Number of Completed Pay Periods')
social_security_rate = config.getfloat('General Tax Information', 'Social Security Tax Rate (%)') / 100.0
social_security_limit = config.getfloat('General Tax Information', 'Social Security Tax Limit')
social_security_withheld = config.getfloat('General Tax Information', 'Social Security Tax Withheld')
medicare_rate = config.getfloat('General Tax Information', 'Medicare Tax Rate (%)') / 100.0
federal_filing_status = config.get('Federal Tax Information', 'Federal Filing Status')
federal_deduction_method = config.get('Federal Tax Information', 'Federal Deduction Method')
federal_standard_deduction = config.getfloat('Federal Tax Information', 'Federal Standard Deduction')
federal_exemption = config.getfloat('Federal Tax Information', 'Federal Exemption')
other_tax_total = config.getfloat('Additional Taxes', 'Total Other Taxes')
prior_year_federal_standard_deduction = config.getfloat('Prior Year Federal Tax Information',
                                                        'Prior Year Federal Standard Deduction')
number_of_states = config.getint('State Tax Information', 'Number of States Lived in')
state_abbreviations = config.get('State Tax Information', 'State Abbreviations').split()
state_deduction_method = config.get('State Tax Information', 'State Deduction Method').split()
state_standard_deduction = [float(i) for i in config.get('State Tax Information', 'State Standard Deduction').split()]
state_exemption = [float(i) for i in config.get('State Tax Information', 'State Exemption').split()]
state_additions = [float(i) for i in config.get('State Tax Information', 'State Additions').split()]
state_subtractions = [float(i) for i in config.get('State Tax Information', 'State Subtractions').split()]
do_not_file_for_state = config.get('State Tax Information', 'Do Not File Method').split()
state_do_not_file_limit = [float(i) for i in config.get('State Tax Information', 'Do Not File Limit').split()]
wages_salary_tips = [float(i) for i in config.get('Income Information', 'Wages Salary Tips').split()]
taxable_interest = [float(i) for i in config.get('Income Information', 'Taxable Interest').split()]
ordinary_dividends = [float(i) for i in config.get('Income Information', 'Total Ordinary Dividends').split()]
qualified_dividends = [float(i) for i in config.get('Income Information', 'Qualified Dividends').split()]
long_term_capital_gains = [float(i) for i in config.get('Income Information', 'Long Term Capital Gains').split()]
short_term_capital_gains = [float(i) for i in config.get('Income Information', 'Short Term Capital Gains').split()]
long_term_capital_loss = [float(i) for i in config.get('Income Information', 'Long Term Capital Losses').split()]
short_term_capital_loss = [float(i) for i in config.get('Income Information', 'Short Term Capital Losses').split()]
other_income = [float(i) for i in config.get('Income Information', 'Other Income').split()]
hsa_deduction = [float(i) for i in config.get('Adjustments to Income', 'HSA Deduction').split()]
other_adjustments = [float(i) for i in config.get('Adjustments to Income', 'Other Adjustments').split()]
prior_year_state_refund = config.getfloat('State Tax Refunds from Previous Year (1099-G)', 'Previous State Tax Refunds')
prior_year_itemized_deduction = config.getfloat('State Tax Refunds from Previous Year (1099-G)',
                                                'Previous Total Itemized Deduction')
medical_and_dental = config.getfloat('Itemized Deduction Information', 'Medical and Dental')
real_estate_personal_property = config.getfloat('Itemized Deduction Information', 'Real Estate and Personal Property')
other_tax_expenses = config.getfloat('Itemized Deduction Information', 'Other Tax Expenses')
home_mortgage_interest = config.getfloat('Itemized Deduction Information', 'Home Mortgage Interest and Points')
investment_interest = config.getfloat('Itemized Deduction Information', 'Investment Interest')
gifts = config.getfloat('Itemized Deduction Information', 'Gifts')
casualty_theft = config.getfloat('Itemized Deduction Information', 'Casualty and Theft Losses')
other_itemized_deductions = config.getfloat('Itemized Deduction Information', 'Other Itemized Deductions')
number_long_term_capital_gain_brackets = config.getint('Tax Brackets, Rates, Etc.', 'Number of LTCG Brackets')
long_term_capital_gain_brackets = [[float(i)
                                    for i in config.get('Tax Brackets, Rates, Etc.', 'LTCG Brackets and Rates').split()]
                                   [j:j+3] for j in range(0, 3 * number_long_term_capital_gain_brackets, 3)]
number_federal_brackets = config.getint('Tax Brackets, Rates, Etc.', 'Number of Federal Tax Brackets')
federal_brackets = [[float(i)
                     for i in config.get('Tax Brackets, Rates, Etc.', 'Federal Tax Brackets and Rates').split()]
                    [j:j+3] for j in range(0, 3 * number_federal_brackets, 3)]
number_state_brackets = [int(i)
                         for i in config.get('Tax Brackets, Rates, Etc.', 'Number of State Tax Brackets').split()]
state_brackets = [[[float(i) for i in config.get('Tax Brackets, Rates, Etc.', 'State Tax Brackets and Rates').split()]
                   [j:j+3] for j in range(0, 3 * sum(number_state_brackets), 3)]
                  [sum(number_state_brackets[0:k + 1]) - number_state_brackets[k]:sum(number_state_brackets[0:k + 1])]
                  for k in range(0, number_of_states)]
number_local_rates = [int(i) for i in config.get('Tax Brackets, Rates, Etc.', 'Number of Local Tax Rates').split()]
local_rates = [[float(i) for i in config.get('Tax Brackets, Rates, Etc.', 'Local Tax Rates (%)').split()]
               [sum(number_local_rates[0:j + 1]) - number_local_rates[j]:sum(number_local_rates[0:j + 1])]
               for j in range(0, number_of_states)]
case_path = "cases/" + str(tax_year) + "/"
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------- Read the federal wage input file ----------------------------------------- #
# ------------------------------------- Read the federal withholding input file -------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
config.read(case_path + 'fedwages.inp')
federal_wage_list = config.get('Federal Wage Information', 'Federal Wages').split()
total_federal_wages = sum(float(x) for x in federal_wage_list[1::3]) + sum(float(x) for x in federal_wage_list[2::3])
if round(total_federal_wages, 2) != round(sum(wages_salary_tips), 2):
    print("Warning!!! Your 'Wages Salary Tips' input is NOT the same as your"
          " Total Federal Wages calculated from the fedwages.inp file")
    print('From tp.inp file: ', round(sum(wages_salary_tips), 2))
    print('From fedwages.inp: ', round(total_federal_wages, 2))
config.read(case_path + 'fedwithholding.inp')
federal_withholding_list = config.get('Federal Withholding Information', 'Federal Withholding').split()
total_federal_withholding = sum(float(x) for x in federal_withholding_list[1::3]) + \
                            sum(float(x) for x in federal_withholding_list[2::3])
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------- Allocate space for the state wage array -------------------------------------- #
# ---------------------------------- Allocate space for the state withholding array ---------------------------------- #
# ----------------------------------------- Read the state wage input file(s) ---------------------------------------- #
# ------------------------------------- Read the state withholding input file(s) ------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
all_state_wages_list = [[] for i in range(0, number_of_states)]
all_state_withholding_list = [[] for i in range(0, number_of_states)]
for i in range(0, number_of_states):
    config.read(case_path + state_abbreviations[i] + 'wages.inp')
    all_state_wages_list[i] = config.get('State Wage Information', 'State Wages').split()
    config.read(case_path + state_abbreviations[i] + 'withholding.inp')
    all_state_withholding_list[i] = config.get('State Withholding Information', 'State Withholding'). split()
# -------------------------------------------------------------------------------------------------------------------- #
# ******************************************************************************************************************** #
# -------------------------------------------------------------------------------------------------------------------- #
# ************************************************* Main Calculation ************************************************* #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- Net Capital Determination --------------------------------------------- #
# --------------------------------------- Net Long Term Capital Determination ---------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
net_capital = round(capgnls(sum(long_term_capital_gains),
                            sum(short_term_capital_gains),
                            sum(long_term_capital_loss),
                            sum(short_term_capital_loss)), 2)
net_long_term_capital = sum(long_term_capital_gains) + sum(long_term_capital_loss)
# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------- Determine if State Refund is Taxable --------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
state_refund_taxable_portion = txblstref(prior_year_state_refund,
                                         prior_year_itemized_deduction,
                                         prior_year_federal_standard_deduction)
# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- Federal AGI Calculation ---------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
AGI_federal = agifed(net_capital,
                     wages_salary_tips,
                     taxable_interest,
                     ordinary_dividends,
                     state_refund_taxable_portion,
                     other_income,
                     hsa_deduction,
                     other_adjustments)
# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------- State AGI Calculation ----------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
total_state_wages = []
for state_wages in all_state_wages_list:
    total_state_wages.append(round(sum(float(x) for x in state_wages[1::3]) +
                                   sum(float(x) for x in state_wages[2::3]), 2))
AGI_states = []
non_resident_income_1 = []
for i in range(0, number_of_states):
    non_resident_income = deepcopy(total_state_wages)
    non_resident_income.pop(i)
    non_resident_income_1.append(deepcopy(sum(non_resident_income)))
    state_agi = (AGI_federal
                 + state_additions[i]
                 - state_subtractions[i]
                 - state_refund_taxable_portion
                 - sum(non_resident_income)
                 )
    AGI_states.append(round(state_agi, 2))
# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------- Apportionment Factors Calculation ----------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
apportionment = []
for i in range(0, number_of_states):
    if number_of_states == 1:
        apportionment.append(1.0)
    else:
        apportionment.append(AGI_states[i] / AGI_federal)
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------ Itemized Deduction Calculation ------------------------------------------ #
# -------------------------- Apportionment factors applied to state itemized deductions here ------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
total_state_withholding = []
for state_withholding in all_state_withholding_list:
    total_state_withholding.append(round(sum(float(x) for x in state_withholding[1::3]) +
                                         sum(float(x) for x in state_withholding[2::3]), 2))
federal_itemized_deduction = itemizer(medical_and_dental,
                                      real_estate_personal_property,
                                      other_tax_expenses,
                                      home_mortgage_interest,
                                      investment_interest,
                                      gifts,
                                      casualty_theft,
                                      other_itemized_deductions,
                                      AGI_federal,
                                      sum(total_state_withholding))
state_itemized_deduction = []
for i in range(0, number_of_states):
    state_itemized_deduction.append((federal_itemized_deduction - sum(total_state_withholding)) * apportionment[i])
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------ Apportionment factors applied to state standard deductions and exemptions here ------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
for i in range(0, number_of_states):
    state_standard_deduction[i] = state_standard_deduction[i] * apportionment[i]
    state_exemption[i] = state_exemption[i] * apportionment[i]
# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------- Federal Taxable Income Calculation ---------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
if federal_deduction_method.lower() == 'standard':
    taxable_income_federal = round(AGI_federal - federal_standard_deduction - federal_exemption, 2)
elif federal_deduction_method.lower() == 'itemized':
    taxable_income_federal = round(AGI_federal - federal_itemized_deduction - federal_exemption, 2)
else:
    taxable_income_federal = None
    print('STOP!!! Error in your "Federal Deduction Method" input')
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------- State Taxable Income Calculation ----------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
taxable_income_state = []
do_not_file_logic = []
for i in range(0, number_of_states):
    if do_not_file_for_state[i].lower() == 'stateagi':
        if AGI_states[i] < state_do_not_file_limit[i]:
            taxable_income_state.append(0.0)
            do_not_file_logic.append(True)
        else:
            if state_deduction_method[i].lower() == 'standard':
                taxable_income_state.append(round(AGI_states[i] - state_standard_deduction[i] - state_exemption[i], 2))
            elif state_deduction_method[i].lower() == 'itemized':
                taxable_income_state.append(round(AGI_states[i] - state_itemized_deduction[i] - state_exemption[i], 2))
            else:
                print('STOP!!! Error in your "State Deduction Method" input')
            do_not_file_logic.append(False)
    else:
        print('STOP!!! Error in your "Do Not File Method" input')
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------- Social Security and Medicare Taxable Income Calculation ------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
taxable_income_social_security = min((sum(wages_salary_tips) - sum(hsa_deduction)), social_security_limit)
taxable_income_medicare = sum(wages_salary_tips) - sum(hsa_deduction)
# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- Federal Tax Calculation ---------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
tax_rate_federal = None
for i in range(0, number_federal_brackets):
    if taxable_income_federal < federal_brackets[i][1]:
        tax_rate_federal = deepcopy(federal_brackets[i][2])
        break
qualified_dividends_capital_gains_results = qdcgtax(taxable_income_federal,
                                                    sum(qualified_dividends),
                                                    net_capital,
                                                    net_long_term_capital,
                                                    long_term_capital_gain_brackets,
                                                    federal_brackets,
                                                    number_federal_brackets)
ordinary_income_tax = qualified_dividends_capital_gains_results[0]
qualified_dividends_long_term_capital_gains_tax = qualified_dividends_capital_gains_results[1]
total_tax_federal = qualified_dividends_capital_gains_results[2] + other_tax_total
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------- State Tax Calculation ---------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
total_tax_states = []
tax_rate_states = []
for i in range(0, number_of_states):
    for j in range(0, number_state_brackets[i]):
        if taxable_income_state[i] < state_brackets[i][j][1]:
            tax_rate_states.append(deepcopy(state_brackets[i][j][2]))
            break
    if taxable_income_state[i] < 100000.0:
        total_tax_states.append(taxtablelookup(taxable_income_state[i], state_brackets[i], number_state_brackets[i]))
    else:
        total_tax_states.append(taxcalc(taxable_income_state[i], state_brackets[i], number_state_brackets[i]))
    if number_local_rates[i] > 0:
        for j in range(0, number_local_rates[i]):
            total_tax_states[i] = round(total_tax_states[i] +
                                        (taxable_income_state[i] * (local_rates[i][j] / 100.0)), 2)
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------- SS and Medicare Tax Calculation ------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
total_tax_social_security = taxable_income_social_security * social_security_rate
total_tax_medicare = taxable_income_medicare * medicare_rate
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------ Effective Tax Rate Calculation ------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
total_taxes = total_tax_federal + sum(total_tax_states) + total_tax_social_security + total_tax_medicare
total_income = (sum(wages_salary_tips)
                + sum(taxable_interest)
                + sum(ordinary_dividends)
                + net_capital
                + state_refund_taxable_portion
                + sum(other_income))
effective_tax_rate = total_taxes / total_income
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- Federal Refund Calculation -------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
refund_federal = refund(total_federal_withholding, total_tax_federal)
# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- State Refund Calculation --------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
refund_states = []
for i in range(0, number_of_states):
    refund_states.append(refund(total_state_withholding[i], total_tax_states[i]))
# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------- Social Security Refund Calculation ---------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
refund_social_security = refund(social_security_withheld, total_tax_social_security)
# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- Zero Out Federal Refund ---------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
new_federal_withholding_list = optrefund(federal_withholding_list, refund_federal, pay_periods, current_pay_period)
new_total_federal_withholding = sum(float(x) for x in new_federal_withholding_list[1::3]) + \
                                sum(float(x) for x in new_federal_withholding_list[2::3])
optimized_federal_refund = refund(new_total_federal_withholding, total_tax_federal)
# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- Zero Out State Refund(s) --------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
new_state_withholding_list = [[] for i in range(0, number_of_states)]
for i in range(0, number_of_states):
    new_state_withholding_list[i] = optrefund(all_state_withholding_list[i],
                                              refund_states[i],
                                              pay_periods,
                                              current_pay_period)
new_total_state_withholding = []
for new_state_withholding in new_state_withholding_list:
    new_total_state_withholding.append(round(sum(float(x) for x in new_state_withholding[1::3]) +
                                             sum(float(x) for x in new_state_withholding[2::3]), 2))
optimized_state_refund = []
for i in range(0, number_of_states):
    optimized_state_refund.append(refund(new_total_state_withholding[i], total_tax_states[i]))
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- Formatted Print -------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
print('{:>12s}{:>4d}{:>3s}{:>19s}'.format('___Tax_Year_', tax_year, '___', '|_____Federal_____|'), end='')
print('{:>18s}{:>18s}'.format('__Soc._Security__|', '_____Medicare____|'), end='')
for i in range(0, number_of_states):
    print('{:>7s}{:>2s}{:>7s}'.format('_______', state_abbreviations[i].upper(), '_______'), end='|')
print('')
print('{:>20s}'.format('Net Cap. Gain/Loss |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', net_capital, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>16s}'.format(' '), end='|')
print('')
if net_capital < 0.0:
    if abs(net_capital) > 3000.00:
        print('{:>20s}'.format('  Usable Cap. Loss |'), end='')
        print('{:>3s}{:>11.2f}{:>4s}'.format('$', -3000.00, '|'), end='')
        print('{:>17s}'.format(' '), end='|')
        print('{:>17s}'.format(' '), end='|')
        for i in range(0, number_of_states):
            print('{:>16s}'.format(' '), end='|')
        print('')
        print('{:>20s}'.format('Cap. Loss Carryover|'), end='')
        print('{:>3s}{:>11.2f}{:>4s}'.format('$', -(abs(net_capital) - 3000), '|'), end='')
        print('{:>17s}'.format(' '), end='|')
        print('{:>17s}'.format(' '), end='|')
        for i in range(0, number_of_states):
            print('{:>16s}'.format(' '), end='|')
        print('')
print('{:>20s}'.format('Taxable St. Refund |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', state_refund_taxable_portion, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>16s}'.format(' '), end='|')
print('')
print('{:>20s}'.format('   State Wages    |'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', total_state_wages[i], '|'), end='')
print('')
print('{:>20s}'.format('Non-resident Income|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', non_resident_income_1[i], '|'), end='')
print('')
print('{:>20s}'.format('   AGI        |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', AGI_federal, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', AGI_states[i], '|'), end='')
print('')
print('{:>20s}'.format('   Apportionment   |'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>15.4f}{:>2s}'.format(apportionment[i], ' |'), end='')
print('')
print('{:>20s}'.format(' Deduction Method  |'), end='')
print('{:>13s}{:>4s}'.format(federal_deduction_method, ' '), end='|')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>12s}{:>4s}'.format(state_deduction_method[i], ' '), end='|')
print('')
print('{:>20s}'.format(' Stn. Ded. Amount  |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', federal_standard_deduction, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', state_standard_deduction[i], '|'), end='')
print('')
print('{:>20s}'.format(' Itm. Ded. Amount  |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', federal_itemized_deduction, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', state_itemized_deduction[i], '|'), end='')
print('')
print('{:>20s}'.format(' Exemption Amount  |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', federal_exemption, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', state_exemption[i], '|'), end='')
print('')
print('{:>20s}'.format('Do Not File?    |'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>10s}{:>6s}'.format(str(do_not_file_logic[i]), ' '), end='|')
print('')
print('{:>20s}'.format('Tot. Taxable Income|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', taxable_income_federal, '|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', taxable_income_social_security, '|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', taxable_income_medicare, '|'), end='')
for i in range(0, number_of_states):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', taxable_income_state[i], '|'), end='')
print('')
print('{:>20s}'.format(' Marginal Tax Rate |'), end='')
print('{:>14.2f}{:>4s}'.format(tax_rate_federal, '% |'), end='')
print('{:>14.2f}{:>4s}'.format(social_security_rate * 100, '% |'), end='')
print('{:>14.2f}{:>4s}'.format(medicare_rate * 100, '% |'), end='')
for i in range(0, number_of_states):
    print('{:>13.2f}{:>4s}'.format(tax_rate_states[i], '% |'), end='')
print('')
print('{:>20s}'.format(' Ordinary Inc. Tax |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', ordinary_income_tax, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>16s}'.format(' '), end='|')
print('')
print('{:>20s}'.format('   QD & LTCG Tax   |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', qualified_dividends_long_term_capital_gains_tax, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>16s}'.format(' '), end='|')
print('')
print('{:>20s}'.format('  Tot. Income Tax  |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', total_tax_federal, '|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', total_tax_social_security, '|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', total_tax_medicare, '|'), end='')
for i in range(0, number_of_states):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', total_tax_states[i], '|'), end='')
print('')
print('{:>20s}'.format('   Taxes Withheld  |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', total_federal_withholding, '|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', social_security_withheld, '|'), end='')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', total_state_withholding[i], '|'), end='')
print('')
print('{:>20s}'.format('      Refunds      |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', refund_federal, '|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', refund_social_security, '|'), end='')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', refund_states[i], '|'), end='')
print('')
print('{:>20s}'.format('Effective Tax Rate |'), end='')
print('{:>14.2f}{:>4s}'.format(effective_tax_rate * 100.0, '% |'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>16s}'.format(' '), end='|')
print('')
print('{:>20s}'.format('Wthhlding Adjustmnt|'), end='')
if current_pay_period < pay_periods:
    print('{:>3s}{:>11.2f}{:>4s}'.format('$', -1.0 * (refund_federal / (pay_periods - current_pay_period)), '|'),
          end='')
else:
    print('{:>3s}{:>11.2f}{:>4s}'.format('$', 0.0, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    if current_pay_period < pay_periods:
        print('{:>2s}{:>11.2f}{:>4s}'.format('$', -1.0 * (refund_states[i] / (pay_periods - current_pay_period)), '|'),
              end='')
    else:
        print('{:>2s}{:>11.2f}{:>4s}'.format('$', 0.0, '|'), end='')
print('')
print('{:>20s}'.format('Optimized Wthhlding|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', new_total_federal_withholding, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', new_total_state_withholding[i], '|'), end='')
print('')
print('{:>20s}'.format(' Optimized Refunds |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', optimized_federal_refund, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, number_of_states):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', optimized_state_refund[i], '|'), end='')
print('')
print('')
if current_pay_period >= pay_periods:
    print('{:>43s}'.format('Federal and State Withholding for the year'))
else:
    print('{:>40s}'.format('Optimized Federal and State Withholding'))
print('{:>23s}{:>15s}{:>7}{:>12s}'.format('||', '________Federal', '_____||', '____________'), end='')
for i in range(0, number_of_states):
    if i < number_of_states - 1:
        print('{:>2s}{:>10}{:>12}'.format(state_abbreviations[i].upper(), '________||', '____________'), end='')
    if i >= number_of_states - 1:
        print('{:>2s}{:>10}'.format(state_abbreviations[i].upper(), '________||'), end='')
        print('')
for i in range(0, pay_periods):
    print('{:<4s}{:>02d}{:>17s}{:>9.2f}{:>9.2f}'.format('PP#', i + 1, 'Withholding:  ||',
                                                        float(new_federal_withholding_list[i * 3 + 1]),
                                                        float(new_federal_withholding_list[i * 3 + 2])), end='  ||')
    for j in range(0, number_of_states):
        print('{:>10.2f}{:>10.2f}'.format(float(new_state_withholding_list[j][i * 3 + 1]),
                                          float(new_state_withholding_list[j][i * 3 + 2])), end='  ||')
        if j == number_of_states - 1:
            print('')
