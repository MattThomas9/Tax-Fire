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
idetprnt = config.get('Code Control', 'Detailed Print')
ntaxyear = config.getint('General Tax Information', 'Tax Year')
numpayps = config.getint('General Tax Information', 'Number of Total Pay Periods')
ipayperd = config.getint('General Tax Information', 'Number of Completed Pay Periods')
txrtoasd = config.getfloat('General Tax Information', 'Social Security Tax Rate (%)') / 100.0
oasdlimt = config.getfloat('General Tax Information', 'Social Security Tax Limit')
sstxwhld = config.getfloat('General Tax Information', 'Social Security Tax Withheld')
txrtmedi = config.getfloat('General Tax Information', 'Medicare Tax Rate (%)') / 100.0
ifilstat = config.get('Federal Tax Information', 'Federal Filing Status')
ifeddedm = config.get('Federal Tax Information', 'Federal Deduction Method')
fedstndd = config.getfloat('Federal Tax Information', 'Federal Standard Deduction')
fedexmat = config.getfloat('Federal Tax Information', 'Federal Exemption')
totothtx = config.getfloat('Additional Taxes', 'Total Other Taxes')
prefedsd = config.getfloat('Prior Year Federal Tax Information', 'Prior Year Federal Standard Deduction')
numstate = config.getint('State Tax Information', 'Number of States Lived in')
istateab = config.get('State Tax Information', 'State Abbreviations').split()
istadedm = config.get('State Tax Information', 'State Deduction Method').split()
stastndd = [float(i) for i in config.get('State Tax Information', 'State Standard Deduction').split()]
staexmat = [float(i) for i in config.get('State Tax Information', 'State Exemption').split()]
stateadd = [float(i) for i in config.get('State Tax Information', 'State Additions').split()]
statesub = [float(i) for i in config.get('State Tax Information', 'State Subtractions').split()]
wgsaltip = [float(i) for i in config.get('Income Information', 'Wages Salary Tips').split()]
taxabint = [float(i) for i in config.get('Income Information', 'Taxable Interest').split()]
totordiv = [float(i) for i in config.get('Income Information', 'Total Ordinary Dividends').split()]
qualdivd = [float(i) for i in config.get('Income Information', 'Qualified Dividends').split()]
cpgainlt = [float(i) for i in config.get('Income Information', 'Long Term Capital Gains').split()]
cpgainst = [float(i) for i in config.get('Income Information', 'Short Term Capital Gains').split()]
cplosslt = [float(i) for i in config.get('Income Information', 'Long Term Capital Losses').split()]
cplossst = [float(i) for i in config.get('Income Information', 'Short Term Capital Losses').split()]
otherinc = [float(i) for i in config.get('Income Information', 'Other Income').split()]
hsadedct = [float(i) for i in config.get('Adjustments to Income', 'HSA Deduction').split()]
otheradj = [float(i) for i in config.get('Adjustments to Income', 'Other Adjustments').split()]
prestref = config.getfloat('State Tax Refunds from Previous Year (1099-G)', 'Previous State Tax Refunds')
preitded = config.getfloat('State Tax Refunds from Previous Year (1099-G)', 'Previous Total Itemized Deduction')
expnsmed = config.getfloat('Itemized Deduction Information', 'Medical and Dental')
expnsrel = config.getfloat('Itemized Deduction Information', 'Real Estate and Personal Property')
expnstxo = config.getfloat('Itemized Deduction Information', 'Other Tax Expenses')
expnsmor = config.getfloat('Itemized Deduction Information', 'Home Mortgage Interest and Points')
expnsinv = config.getfloat('Itemized Deduction Information', 'Investment Interest')
expnsgif = config.getfloat('Itemized Deduction Information', 'Gifts')
expnscas = config.getfloat('Itemized Deduction Information', 'Casualty and Theft Losses')
expnsoth = config.getfloat('Itemized Deduction Information', 'Other Itemized Deductions')
nltcgbrk = config.getint('Tax Brackets, Rates, Etc.', 'Number of LTCG Brackets')
brkltcgr = [[float(i) for i in config.get('Tax Brackets, Rates, Etc.', 'LTCG Brackets and Rates').split()]
            [j:j+3] for j in range(0, 3 * nltcgbrk, 3)]
nfdtxbrk = config.getint('Tax Brackets, Rates, Etc.', 'Number of Federal Tax Brackets')
brkfedtx = [[float(i) for i in config.get('Tax Brackets, Rates, Etc.', 'Federal Tax Brackets and Rates').split()]
            [j:j+3] for j in range(0, 3 * nfdtxbrk, 3)]
nsttxbrk = [int(i) for i in config.get('Tax Brackets, Rates, Etc.', 'Number of State Tax Brackets').split()]
brkstatx = [[[float(i) for i in config.get('Tax Brackets, Rates, Etc.', 'State Tax Brackets and Rates').split()]
             [j:j+3] for j in range(0, 3 * sum(nsttxbrk), 3)]
            [sum(nsttxbrk[0:k+1])-nsttxbrk[k]:sum(nsttxbrk[0:k+1])] for k in range(0, numstate)]
nloctaxr = [int(i) for i in config.get('Tax Brackets, Rates, Etc.', 'Number of Local Tax Rates').split()]
taxrlocl = [[float(i) for i in config.get('Tax Brackets, Rates, Etc.', 'Local Tax Rates (%)').split()]
            [sum(nloctaxr[0:j+1])-nloctaxr[j]:sum(nloctaxr[0:j+1])] for j in range(0, numstate)]
icase = "cases/" + str(ntaxyear) + "/"
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------- Read the federal wage input file ----------------------------------------- #
# ------------------------------------- Read the federal withholding input file -------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
config.read(icase + 'fedwages.inp')
wagefedl = [[float(i) for i in config.get('Federal Wage Information', 'Federal Wages').split()]
            [j:j+3] for j in range(0, 3 * numpayps, 3)]
ytdfdwag = sum(sum([wagefedl[i][1:] for i in range(0, numpayps)], []))
if round(ytdfdwag, 2) != round(sum(wgsaltip), 2):
    print("Warning!!! Your 'Wages Salary Tips' input is NOT the same as your"
          " YTD Federal Wages calculated from the fedwages.inp file")
    print('From tp.inp file: ', round(sum(wgsaltip), 2))
    print('From fedwages.inp: ', round(ytdfdwag, 2))
config.read(icase + 'fedwithholding.inp')
wthldfed = [[float(i) for i in config.get('Federal Withholding Information', 'Federal Withholding').split()]
            [j:j+3] for j in range(0, 3 * numpayps, 3)]
ytdfdwhl = sum(sum([wthldfed[i][1:] for i in range(0, numpayps)], []))
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------- Allocate space for the state wage array -------------------------------------- #
# ---------------------------------- Allocate space for the state withholding array ---------------------------------- #
# ----------------------------------------- Read the state wage input file(s) ---------------------------------------- #
# ------------------------------------- Read the state withholding input file(s) ------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
wagestat = [[] for i in range(0, numstate)]
wthldsta = [[] for i in range(0, numstate)]
for i in range(0, numstate):
    config.read(icase + istateab[i] + 'wages.inp')
    wagestat[i] = [[float(j) for j in config.get('State Wage Information', 'State Wages').split()]
                   [k:k+3] for k in range(0, 3 * numpayps, 3)]
    config.read(icase + istateab[i] + 'withholding.inp')
    wthldsta[i] = [[float(j) for j in config.get('State Withholding Information', 'State Withholding'). split()]
                   [k:k+3] for k in range(0, 3 * numpayps, 3)]
# -------------------------------------------------------------------------------------------------------------------- #
# ******************************************************************************************************************** #
# -------------------------------------------------------------------------------------------------------------------- #
# ************************************************* Main Calculation ************************************************* #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- Net Capital Determination --------------------------------------------- #
# --------------------------------------- Net Long Term Capital Determination ---------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
capnet = round(capgnls(sum(cpgainlt), sum(cpgainst), sum(cplosslt), sum(cplossst)), 2)
capltnet = sum(cpgainlt) + sum(cplosslt)
# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------- Determine if State Refund is Taxable --------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
txblprtnofstref = txblstref(prestref, preitded, prefedsd)
# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- Federal AGI Calculation ---------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
fedrlagi = agifed(capnet, wgsaltip, taxabint, totordiv, txblprtnofstref, otherinc, hsadedct, otheradj)
# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------- State AGI Calculation ----------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
ytdstwag = []
for x in wagestat:
    dude = 0
    for y in x:
        dude += sum(y[1:])
    ytdstwag.append(round(dude, 2))
stateagi = []
nonresinc1 = []
for i in range(0, numstate):
    nonresinc = deepcopy(ytdstwag)
    nonresinc.pop(i)
    nonresinc1.append(deepcopy(sum(nonresinc)))
    stagi = (fedrlagi
             + stateadd[i]
             - statesub[i]
             - txblprtnofstref
             - sum(nonresinc)
             )
    stateagi.append(round(stagi, 2))
# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------- Apportionment Factors Calculation ----------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
apprtnmt = []
for i in range(0, numstate):
    if numstate == 1:
        apprtnmt.append(1.0)
    else:
        apprtnmt.append(stateagi[i] / fedrlagi)
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------ Itemized Deduction Calculation ------------------------------------------ #
# -------------------------- Apportionment factors applied to state itemized deductions here ------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
ytdstwhl = []
for x in wthldsta:
    dude = 0
    for y in x:
        dude += sum(y[1:])
    ytdstwhl.append(round(dude, 2))
feditmded = itemizer(expnsmed, expnsrel, expnstxo, expnsmor, expnsinv, expnsgif, expnscas, expnsoth, fedrlagi,
                     sum(ytdstwhl))
staitmded = []
for i in range(0, numstate):
    staitmded.append((feditmded - sum(ytdstwhl)) * apprtnmt[i])
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------ Apportionment factors applied to state standard deductions and exemptions here ------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
for i in range(0, numstate):
    stastndd[i] = stastndd[i] * apprtnmt[i]
    staexmat[i] = staexmat[i] * apprtnmt[i]
# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------- Federal Taxable Income Calculation ---------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
if ifeddedm.lower() == 'standard':
    fedtaxinc = round(fedrlagi - fedstndd - fedexmat, 2)
elif ifeddedm.lower() == 'itemized':
    fedtaxinc = round(fedrlagi - feditmded - fedexmat, 2)
else:
    fedtaxinc = None
    print('STOP!!! Error in your "Federal Deduction Method" input')
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------- State Taxable Income Calculation ----------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
stataxinc = []
for i in range(0, numstate):
    if istadedm[i].lower() == 'standard':
        stataxinc.append(round(stateagi[i] - stastndd[i] - staexmat[i], 2))
    elif istadedm[i].lower() == 'itemized':
        stataxinc.append(round(stateagi[i] - staitmded[i] - staexmat[i], 2))
    else:
        print('STOP!!! Error in your "State Deduction Method" input')
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------- Social Security and Medicare Taxable Income Calculation ------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
socstaxinc = min((sum(wgsaltip) - sum(hsadedct)), oasdlimt)
medctaxinc = sum(wgsaltip) - sum(hsadedct)
# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- Federal Tax Calculation ---------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
fedmartaxrate = None
for i in range(0, nfdtxbrk):
    if fedtaxinc < brkfedtx[i][1]:
        fedmartaxrate = deepcopy(brkfedtx[i][2])
        break
qdcgrslt = qdcgtax(fedtaxinc, sum(qualdivd), capnet, capltnet, brkltcgr, brkfedtx, nfdtxbrk)
fedinclessqdcgtax = qdcgrslt[0]
qdltcgtax = qdcgrslt[1]
fedtax = qdcgrslt[2] + totothtx
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------- State Tax Calculation ---------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
statetax = []
stamartaxrate = []
for i in range(0, numstate):
    for j in range(0, nsttxbrk[i]):
        if stataxinc[i] < brkstatx[i][j][1]:
            stamartaxrate.append(deepcopy(brkstatx[i][j][2]))
            break
    if stataxinc[i] < 100000.0:
        statetax.append(taxtablelookup(stataxinc[i], brkstatx[i], nsttxbrk[i]))
    else:
        statetax.append(taxcalc(stataxinc[i], brkstatx[i], nsttxbrk[i]))
    if nloctaxr[i] > 0:
        for j in range(0, nloctaxr[i]):
            statetax[i] = round(statetax[i] + (stataxinc[i] * (taxrlocl[i][j] / 100.0)), 2)
# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------- SS and Medicare Tax Calculation ------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
socsectax = socstaxinc * txrtoasd
medcartax = medctaxinc * txrtmedi
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------ Effective Tax Rate Calculation ------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
totaxes = fedtax + sum(statetax) + socsectax + medcartax
totincm = (sum(wgsaltip)
           + sum(taxabint)
           + sum(totordiv)
           + capnet
           + txblprtnofstref
           + sum(otherinc))
efftxrt = totaxes / totincm
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- Federal Refund Calculation -------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
refunfed = refund(ytdfdwhl, fedtax)
# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- State Refund Calculation --------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
refunsta = []
for i in range(0, numstate):
    refunsta.append(refund(ytdstwhl[i], statetax[i]))
# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------- Social Security Refund Calculation ---------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
refunssc = refund(sstxwhld, socsectax)
# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- Zero Out Federal Refund ---------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
wthldfednew = optrefund(wthldfed, refunfed, numpayps, ipayperd)
ytdfdwhlnew = sum(sum([wthldfednew[i][1:] for i in range(0, numpayps)], []))
optrefunfed = refund(ytdfdwhlnew, fedtax)
# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- Zero Out State Refund(s) --------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
wthldstanew = [[] for i in range(0, numstate)]
for i in range(0, numstate):
    wthldstanew[i] = optrefund(wthldsta[i], refunsta[i], numpayps, ipayperd)
ytdstwhlnew = []
for x in wthldstanew:
    dude = 0
    for y in x:
        dude += sum(y[1:])
    ytdstwhlnew.append(round(dude, 2))
optrefunsta = []
for i in range(0, numstate):
    optrefunsta.append(refund(ytdstwhlnew[i], statetax[i]))
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- Formatted Print -------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
print('{:>12s}{:>4d}{:>3s}{:>19s}'.format('___Tax Year ', ntaxyear, '___', '|_____Federal_____|'), end='')
print('{:>18s}{:>18s}'.format('__Soc. Security__|', '_____Medicare____|'), end='')
for i in range(0, numstate):
    print('{:>7s}{:>2s}{:>7s}'.format('_______', istateab[i].upper(), '_______'), end='|')
print('')
print('{:>20s}'.format('Net Cap. Gain/Loss |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', capnet, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>16s}'.format(' '), end='|')
print('')
if capnet < 0.0:
    if abs(capnet) > 3000.00:
        print('{:>20s}'.format('  Usable Cap. Loss |'), end='')
        print('{:>3s}{:>11.2f}{:>4s}'.format('$', -3000.00, '|'), end='')
        print('{:>17s}'.format(' '), end='|')
        print('{:>17s}'.format(' '), end='|')
        for i in range(0, numstate):
            print('{:>16s}'.format(' '), end='|')
        print('')
        print('{:>20s}'.format('Cap. Loss Carryover|'), end='')
        print('{:>3s}{:>11.2f}{:>4s}'.format('$', -(abs(capnet) - 3000), '|'), end='')
        print('{:>17s}'.format(' '), end='|')
        print('{:>17s}'.format(' '), end='|')
        for i in range(0, numstate):
            print('{:>16s}'.format(' '), end='|')
        print('')
print('{:>20s}'.format('Taxable St. Refund |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', txblprtnofstref, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>16s}'.format(' '), end='|')
print('')
print('{:>20s}'.format('   State Wages    |'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', ytdstwag[i], '|'), end='')
print('')
print('{:>20s}'.format('Non-resident Income|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', nonresinc1[i], '|'), end='')
print('')
print('{:>20s}'.format('   AGI        |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', fedrlagi, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', stateagi[i], '|'), end='')
print('')
print('{:>20s}'.format('   Apportionment   |'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>15.4f}{:>2s}'.format(apprtnmt[i], ' |'), end='')
print('')
print('{:>20s}'.format(' Deduction Method  |'), end='')
print('{:>13s}{:>4s}'.format(ifeddedm, ' '), end='|')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>12s}{:>4s}'.format(istadedm[i], ' '), end='|')
print('')
print('{:>20s}'.format(' Stn. Ded. Amount  |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', fedstndd, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', stastndd[i], '|'), end='')
print('')
print('{:>20s}'.format(' Itm. Ded. Amount  |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', feditmded, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', staitmded[i], '|'), end='')
print('')
print('{:>20s}'.format(' Exemption Amount  |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', fedexmat, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', staexmat[i], '|'), end='')
print('')
print('{:>20s}'.format('Tot. Taxable Income|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', fedtaxinc, '|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', socstaxinc, '|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', medctaxinc, '|'), end='')
for i in range(0, numstate):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', stataxinc[i], '|'), end='')
print('')
print('{:>20s}'.format(' Marginal Tax Rate |'), end='')
print('{:>14.2f}{:>4s}'.format(fedmartaxrate, '% |'), end='')
print('{:>14.2f}{:>4s}'.format(txrtoasd*100, '% |'), end='')
print('{:>14.2f}{:>4s}'.format(txrtmedi*100, '% |'), end='')
for i in range(0, numstate):
    print('{:>13.2f}{:>4s}'.format(stamartaxrate[i], '% |'), end='')
print('')
print('{:>20s}'.format(' Ordinary Inc. Tax |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', fedinclessqdcgtax, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>16s}'.format(' '), end='|')
print('')
print('{:>20s}'.format('   QD & LTCG Tax   |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', qdltcgtax, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>16s}'.format(' '), end='|')
print('')
print('{:>20s}'.format('  Tot. Income Tax  |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', fedtax, '|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', socsectax, '|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', medcartax, '|'), end='')
for i in range(0, numstate):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', statetax[i], '|'), end='')
print('')
print('{:>20s}'.format('   Taxes Withheld  |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', ytdfdwhl, '|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', sstxwhld, '|'), end='')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', ytdstwhl[i], '|'), end='')
print('')
print('{:>20s}'.format('      Refunds      |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', refunfed, '|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', refunssc, '|'), end='')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', refunsta[i], '|'), end='')
print('')
print('{:>20s}'.format('Effective Tax Rate |'), end='')
print('{:>14.2f}{:>4s}'.format(efftxrt * 100.0, '% |'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>16s}'.format(' '), end='|')
print('')
print('{:>20s}'.format('Wthhlding Adjustmnt|'), end='')
if ipayperd < numpayps:
    print('{:>3s}{:>11.2f}{:>4s}'.format('$', -1.0 * (refunfed / (numpayps - ipayperd)), '|'), end='')
else:
    print('{:>3s}{:>11.2f}{:>4s}'.format('$', 0.0, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    if ipayperd < numpayps:
        print('{:>2s}{:>11.2f}{:>4s}'.format('$', -1.0 * (refunsta[i] / (numpayps - ipayperd)), '|'), end='')
    else:
        print('{:>2s}{:>11.2f}{:>4s}'.format('$', 0.0, '|'), end='')
print('')
print('{:>20s}'.format('Optimized Wthhlding|'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', ytdfdwhlnew, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', ytdstwhlnew[i], '|'), end='')
print('')
print('{:>20s}'.format(' Optimized Refunds |'), end='')
print('{:>3s}{:>11.2f}{:>4s}'.format('$', optrefunfed, '|'), end='')
print('{:>17s}'.format(' '), end='|')
print('{:>17s}'.format(' '), end='|')
for i in range(0, numstate):
    print('{:>2s}{:>11.2f}{:>4s}'.format('$', optrefunsta[i], '|'), end='')
print('')
print('')
if ipayperd >= numpayps:
    print('{:>43s}'.format('Federal and State Withholdings for the year'))
else:
    print('{:>40s}'.format('Optimized Federal and State Withholdings'))
print('{:>23s}{:>15s}{:>7}{:>12s}'.format('||', '________Federal', '_____||', '____________'), end='')
for i in range(0, numstate):
    if i < numstate - 1:
        print('{:>2s}{:>10}{:>12}'.format(istateab[i].upper(), '________||', '____________'), end='')
    if i >= numstate - 1:
        print('{:>2s}{:>10}'.format(istateab[i].upper(), '________||'), end='')
        print('')
for i in range(0, numpayps):
    print('{:<4s}{:>02d}{:>17s}{:>9.2f}{:>9.2f}'.format('PP#', i+1, 'Withholding:  ||',
          wthldfednew[i][1], wthldfednew[i][2]), end='  ||')
    for j in range(0, numstate):
        print('{:>10.2f}{:>10.2f}'.format(wthldstanew[j][i][1], wthldstanew[j][i][2]), end='  ||')
        if j == numstate - 1:
            print('')
