
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST

from .models import FloatingFlag


def is_flag_admin(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_flag_admin)


def flag_list(request):
    flags = FloatingFlag.objects.all().order_by("-created_at")

    return render(
        request,
        "Floating_Flag/Admin/flag_list.html",
        {"flags": flags}
    )


@login_required
@user_passes_test(is_flag_admin)
def flag_create(request):

    if request.method == "POST":

        flag = FloatingFlag()

        flag.title = request.POST.get("title", "").strip()
        flag.color = request.POST.get("color", "#ffffff")
        flag.position_type = request.POST.get("position_type", "top_right")

        flag.width = int(request.POST.get("width", 600))
        flag.height = int(request.POST.get("height", 300))

        flag.pos_x = float(request.POST.get("pos_x", 50))
        flag.pos_y = float(request.POST.get("pos_y", 10))

        flag.camera_angle = float(request.POST.get("camera_angle", 0))
        flag.wave_horizontal = float(request.POST.get("wave_horizontal", 0.5))
        flag.wave_vertical = float(request.POST.get("wave_vertical", 0.3))
        flag.wave_strength = float(request.POST.get("wave_strength", 0.4))
        flag.wave_speed = float(request.POST.get("wave_speed", 0.5))

        flag.animation_direction = request.POST.get(
            "animation_direction", "both"
        )

        flag.animation_enabled = request.POST.get("animation_enabled") == "on"

        flag.z_index = int(request.POST.get("z_index", 999))

        flag.show_close_button = request.POST.get("show_close_button") == "on"
        flag.auto_close = request.POST.get("auto_close") == "on"

        flag.auto_close_seconds = int(
            request.POST.get("auto_close_seconds", 10)
        )

        flag.is_active = request.POST.get("is_active") == "on"

        flag.start_date = request.POST.get("start_date") or None
        flag.end_date = request.POST.get("end_date") or None

        if request.FILES.get("image"):
            flag.image = request.FILES["image"]

        flag.save()

        messages.success(request, "Floating flag created successfully.")
        return redirect("Floating_Flag:flag_list")

    return render(
        request,
        "Floating_Flag/Admin/flag_settings.html",
        {"flag": None}
    )


@login_required
@user_passes_test(is_flag_admin)
def flag_edit(request, pk):

    flag = get_object_or_404(FloatingFlag, pk=pk)

    if request.method == "POST":

        flag.title = request.POST.get("title", flag.title).strip()
        flag.color = request.POST.get("color", flag.color)

        flag.position_type = request.POST.get(
            "position_type", flag.position_type
        )

        flag.width = int(request.POST.get("width", flag.width))
        flag.height = int(request.POST.get("height", flag.height))

        flag.pos_x = float(request.POST.get("pos_x", flag.pos_x))
        flag.pos_y = float(request.POST.get("pos_y", flag.pos_y))

        flag.camera_angle = float(
            request.POST.get("camera_angle", flag.camera_angle)
        )

        flag.wave_horizontal = float(
            request.POST.get("wave_horizontal", flag.wave_horizontal)
        )

        flag.wave_vertical = float(
            request.POST.get("wave_vertical", flag.wave_vertical)
        )

        flag.wave_strength = float(
            request.POST.get("wave_strength", flag.wave_strength)
        )

        flag.wave_speed = float(
            request.POST.get("wave_speed", flag.wave_speed)
        )

        flag.animation_direction = request.POST.get(
            "animation_direction", flag.animation_direction
        )

        flag.animation_enabled = (
            request.POST.get("animation_enabled") == "on"
        )

        flag.z_index = int(request.POST.get("z_index", flag.z_index))

        flag.show_close_button = (
            request.POST.get("show_close_button") == "on"
        )

        flag.auto_close = request.POST.get("auto_close") == "on"

        flag.auto_close_seconds = int(
            request.POST.get("auto_close_seconds", flag.auto_close_seconds)
        )

        flag.is_active = request.POST.get("is_active") == "on"

        flag.start_date = request.POST.get("start_date") or None
        flag.end_date = request.POST.get("end_date") or None

        if request.FILES.get("image"):
            flag.image = request.FILES["image"]

        flag.save()

        messages.success(request, "Flag settings updated successfully.")
        return redirect("Floating_Flag:flag_edit", pk=flag.pk)

    return render(
        request,
        "Floating_Flag/Admin/flag_settings.html",
        {"flag": flag}
    )


@login_required
@user_passes_test(is_flag_admin)
@require_POST
def flag_save_position(request, pk):

    flag = get_object_or_404(FloatingFlag, pk=pk)

    try:
        pos_x = float(request.POST.get("pos_x"))
        pos_y = float(request.POST.get("pos_y"))

        if not (0 <= pos_x <= 100 and 0 <= pos_y <= 100):
            raise ValueError

        flag.pos_x = pos_x
        flag.pos_y = pos_y
        flag.position_type = "custom"

        flag.save(update_fields=[
            "pos_x",
            "pos_y",
            "position_type",
            "updated_at"
        ])

        messages.success(request, "Flag position saved.")

    except (TypeError, ValueError):
        messages.error(request, "Invalid flag position.")

    return redirect("Floating_Flag:flag_edit", pk=pk)


@login_required
@user_passes_test(is_flag_admin)
@require_POST
def flag_delete(request, pk):

    flag = get_object_or_404(FloatingFlag, pk=pk)
    flag.delete()

    messages.success(request, "Floating flag deleted.")

    return redirect("Floating_Flag:flag_list")
