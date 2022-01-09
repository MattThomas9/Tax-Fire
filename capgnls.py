# ====================================== Determine Net Capital Gains or Losses ======================================= #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Jan. 27, 2019 ============================================= #
# ==================================================================================================================== #
# -------------------------------------------------------------------------------------------------------------------- #


def capgnls(long_term_capital_gains, short_term_capital_gains, long_term_capital_loss, short_term_capital_loss):
    short_term_capital_net = short_term_capital_gains + short_term_capital_loss
    long_term_capital_net = long_term_capital_gains + long_term_capital_loss
    capital_net = short_term_capital_net + long_term_capital_net
    return capital_net
