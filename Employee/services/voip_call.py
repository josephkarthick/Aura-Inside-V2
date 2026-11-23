
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def initiate_employee_call(request):

    # Fetch all VoIP accounts assigned to the logged-in employee
    voip_records = (
        request.user.voip_accounts
        .select_related("vendor")
        .all()
        .order_by("vendor__name", "id")
    )

    voip_accounts = []

    for record in voip_records:

        login_url = (record.url_webrtc or "").strip()

        # Normalize login URL
        if login_url and not login_url.startswith(
            ("http://", "https://")
        ):
            login_url = f"https://{login_url}"

        voip_accounts.append({
            "id": record.id,
            "vendor": record.vendor.name.upper().strip(),
            "login_url": login_url,
            "username": record.username,
            "password": record.password,
            "company_code": record.company_code,
            "callback_number": record.callback_number,
            "domain": record.domain,
            "tenant_id": record.tenant_id,
        })

    # No VoIP accounts
    if not voip_accounts:

        return render(
            request,
            "Employee/Voip/voip_login_details.html",
            {
                "voip_accounts": [],
                "message": (
                    "You don't have a VoIP account assigned. "
                    "Please contact the IT team."
                ),
            },
        )

    # Render all accounts
    context = {
        "voip_accounts": voip_accounts,
    }

    return render(
        request,
        "Employee/Voip/voip_login_details.html",
        context,
    )
