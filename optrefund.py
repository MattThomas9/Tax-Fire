# ================================================= Optimize Refund ================================================== #
# ============================================== Developer: Matt Thomas ============================================== #
# ============================================ Build Date: Feb. 01, 2019 ============================================= #
# ==================================================================================================================== #
# -------------------------------------------------------------------------------------------------------------------- #
from copy import deepcopy


def optrefund(withholding, refund, number_pay_periods, current_pay_period):
    withholding_new = deepcopy(withholding)
    if current_pay_period < number_pay_periods:
        withholding_adjustment = refund / (number_pay_periods - current_pay_period)
        for i in range(current_pay_period, number_pay_periods):
            withholding_new[i*3+1] = round(float(withholding[i * 3 + 1]) - withholding_adjustment, 2)
    return withholding_new
