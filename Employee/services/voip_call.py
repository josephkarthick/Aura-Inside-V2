from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def initiate_employee_call(request):

    voip_record = request.user.voip_accounts.first()

    # No VoIP account
    if not voip_record:
        return render(
            request,
            "Employee/Voip/voip_login_details.html",
            {
                "has_account": False,
                "message": (
                    "You don't have a VoIP account assigned. "
                    "Please contact the IT team."
                ),
            },
        )

    vendor = voip_record.vendor.name.upper().strip()

    login_url = (voip_record.url_webrtc or "").strip()

    if login_url and not login_url.startswith(("http://", "https://")):
        login_url = f"https://{login_url}"

    context = {
        "has_account": True,
        "vendor": vendor,
        "login_url": login_url,
        "username": voip_record.username,
        "password": voip_record.password,
        "company_code": voip_record.company_code,
    }

    return render(
        request,
        "Employee/Voip/voip_login_details.html",
        context,
    )