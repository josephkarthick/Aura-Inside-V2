from django.http import HttpResponse
from django.utils.html import escape


def initiate(voip_record):

    domain = (voip_record.domain or "").strip()

    if not domain:
        return HttpResponse(
            "SKYFALL domain is not configured for this employee.",
            status=400
        )

    # Add HTTPS if protocol is not already present
    if not domain.startswith(("http://", "https://")):
        domain = "https://" + domain

    # SKYFALL Extension Login URL
    login_url = f"{domain.rstrip('/')}/index.php/site/login"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SKYFALL Login</title>
    </head>

    <body>

        <form id="skyfall-login"
              action="{escape(login_url)}"
              method="post">

            <!-- Login Type -->
            <input type="hidden"
                   name="LoginForm[acc_type]"
                   value="EXTENSION_LOGIN">

            <!-- Extension Username -->
            <input type="hidden"
                   name="LoginForm[username]"
                   value="{escape(
                       voip_record.cdr_id
                       or voip_record.username
                       or ''
                   )}">

            <!-- Password -->
            <input type="hidden"
                   name="LoginForm[password]"
                   value="{escape(
                       voip_record.password
                       or ''
                   )}">

            <!-- Reseller -->
            <input type="hidden"
                   name="LoginForm[reseller_id]"
                   value="0">

            <!-- Tenant ID -->
            <input type="hidden"
                   name="LoginForm[cmp_id]"
                   value="{escape(
                       voip_record.tenant_id
                       or ''
                   )}">

            <!-- Captcha -->
            <input type="hidden"
                   name="LoginForm[applyCaptcha]"
                   value="0">

        </form>

        <script>
            document.getElementById("skyfall-login").submit();
        </script>

    </body>
    </html>
    """

    return HttpResponse(html)