from swm.business import otp as OTPBusiness


def generate_code(hex_=None):
    return OTPBusiness.generate_code(hex_)
