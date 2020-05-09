from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from settings import MAIL_LIST, SENDGRID_API_KEY, TEMPLATE_ID

sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)


def send_mail(data: dict):
    """
    {"country":"Bangladesh","cases":13770,"todayCases":636,"deaths":214,"todayDeaths":8,"recovered":2414,"active":11142,
    "critical":1,"casesPerOneMillion":84,"deathsPerOneMillion":1,"totalTests":116919,"testsPerOneMillion":710}
    :param data:
    :return:
    """
    try:
        dynamic = {
            "total_cases": data.get("cases", 0),
            "total_deaths": data.get("deaths", 0),
            "total_recovered": data.get("recovered", 0),
            "today_deaths": data.get("todayDeaths", 0),
            "affected": data.get("todayCases", 0)
        }
        for mail in MAIL_LIST:
            message = Mail(
                from_email='no-reply@vubon.me',
                to_emails=mail,
            )
            message.template_id = TEMPLATE_ID
            message.dynamic_template_data = dynamic
            res = sg.send(message)
            print(res.status_code)
    except Exception as e:
        print(e)
