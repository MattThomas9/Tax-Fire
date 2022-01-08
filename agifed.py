# ===================================================== AGI Fed ====================================================== #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Mar. 08, 2019 ============================================= #
# ==================================================================================================================== #
# -------------------------------------------------------------------------------------------------------------------- #


def agifed(netcapital, wagsaltip, taxblint, totordnrydiv, taxblstateref, otherincome, hsadeduction, otheradjmt):
    if netcapital > 0.0:
        fedagi = (sum(wagsaltip)
                  + sum(taxblint)
                  + sum(totordnrydiv)
                  + netcapital
                  + taxblstateref
                  + sum(otherincome)
                  - sum(hsadeduction)
                  - sum(otheradjmt)
                  )
    # the following code is here for a placeholder right now
    # if (net_long_term_capital > 0.0) and (net_capital > 0.0)
    # 28% Rate Gain Calculation will go here
    # Unrecaptured Section 1250 Gain Calculation will go here
    elif netcapital < 0.0:
        fedagi = (sum(wagsaltip)
                  + sum(taxblint)
                  + sum(totordnrydiv)
                  + -min(abs(netcapital), 3000.00)
                  + taxblstateref
                  + sum(otherincome)
                  - sum(hsadeduction)
                  - sum(otheradjmt)
                  )
    else:
        fedagi = (sum(wagsaltip)
                  + sum(taxblint)
                  + sum(totordnrydiv)
                  + netcapital
                  + taxblstateref
                  + sum(otherincome)
                  - sum(hsadeduction)
                  - sum(otheradjmt)
                  )
    return fedagi
