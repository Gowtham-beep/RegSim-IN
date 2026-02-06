def payout(**kwargs):
    """
    Minimal stub for example scripts.
    In real services this would enqueue/execute a payout.
    """
    return {
        "payment": kwargs,
    }


def process():
    payout(
        amount=45000,
        vendor_type="contractor",
        tds_deducted=False
    )
