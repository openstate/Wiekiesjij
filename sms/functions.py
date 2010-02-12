from elections.models import Council
from utils.emails import send_email
from sms.models import get_credit
def credit_left():
    councils_credit = 0
    over_drawn = 0

    for council in Council.objects.all():
        if council.election_instances:
            councils_credit_left = council.credit_left()
            councils_credit = councils_credit + council.credit
            if councils_credit_left < 0:
                over_drawn = over_drawn - councils_credit_left

    credit_left = get_credit()

    margin = credit_left - councils_credit - over_drawn

    if margin < 0:
        message = 'WARINING: Accepte has not enough credit bought. Currently Accepte has %s credits left. Councils have reserved: %s. %s credits have not been reserved. Total (Acceptes credits - reserver - non_reserved): %s' %(str(credit_left), str(councils_credit), str(over_drawn),str(margin))

        send_email(
                'Credits Negative -- IMPORTANT',
                'info@wiekiesjij.nl',
                'bmcmahon@gmail.com',
                {'message': message },
                {'plain': 'elections/credits_low.txt'},
        )

        return False
    elif margin < 2000:

        message = 'Accepte may not have enough credit bought. Currently Accepte has %s credits left. Councils have reserved: %s. %s credits have not been reserved. Total (Acceptes credits - reserver - non_reserved): %s' %(str(credit_left), str(councils_credit), str(over_drawn),str(margin))

     
        send_email(
                    'Credits Low',
                    'info@wiekiesjij.nl',
                    'bmcmahon@gmail.com',
                    {'message': message },
                    {'plain': 'elections/credits_low.txt'},
        )


    else:
        pass
    return True