from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BoardMembers,Home
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import get_user_fields, PHOTO_LAYOUT_CHOICES
from Accounts.models import AuraInsideUser
from collections import defaultdict
from django.contrib import messages
from datetime import date, timedelta
from collections import defaultdict
from django.db.models import Count
from interactions.models import Reaction, Comment
from HRDesk.models import JobPosting 
from django.db.models import Count
from .models import Quote
import random
from datetime import timedelta
from django.utils import timezone


def home(request):
    today = date.today()
    # Get the flag
    flag = FloatingFlag.objects.filter(id=1).first()  # safe fetch
    home_content_qs = Home.objects.filter(show=True).order_by('order_no')
    grouped_content = defaultdict(list)
    today_day = date.today().day    

    for item in home_content_qs:
        field1_value = getattr(item.username, item.field1, '') if item.username and item.field1 else ''
        field2_value = getattr(item.username, item.field2, '') if item.username and item.field2 else ''
        username_str = item.username.username if item.username else ""

        grouped_content[item.content_type].append({
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "field1_name": item.field1,
            "field1_value": field1_value,
            "field2_name": item.field2,
            "field2_value": field2_value,
            "project": item.project,
            "photo": item.photo.url if item.photo else '',
            "photo_layout": item.photo_layout,
            "username": username_str,
            

        })

    # If no content_type, keys will be None, so ensure filtering or default label
    grouped_content = {k if k else "Others": v for k, v in grouped_content.items()}
    
    
    # ====================================================
    # Quotes
    # ====================================================    
    
    quotes = Quote.objects.filter(is_active=True)
    
    quote = None
    if quotes.exists():
        quote = random.choice(list(quotes))    

    # ====================================================
    # DATE CALCULATIONS
    # ====================================================
    today = date.today()
    current_month = today.month
    current_year = today.year

    # Handle January → last month = December of previous year
    if current_month == 1:
        last_month = 12
        last_month_year = current_year - 1
    else:
        last_month = current_month - 1
        last_month_year = current_year

    # ====================================================
    # 🎂 BIRTHDAYS — CURRENT MONTH
    # ====================================================
    birthday_users = AuraInsideUser.objects.filter(
        birthdate__month=current_month,
        is_active=True
    ).order_by('birthdate__day').only("first_name", "birthdate")

    # ====================================================
    # 🆕 NEW JOINEES — LAST MONTH
    # ====================================================

    
    today = timezone.now()
    last_30_days = today - timedelta(days=30)
    
    new_joinees = (
        AuraInsideUser.objects.filter(
            date_joined__range=(last_30_days, today),
            is_active=True,
        )
        .select_related("shift", "department")
        .only(
            "first_name",
            "last_name",
            "username",
            "date_joined",
            "shift__name",
            "department__name",
        )
        .order_by("-date_joined")
    )
    
    # ====================================================
    # 🎯 REACTIONS & COMMENTS COUNTS (BIRTHDAYS)
    # ====================================================

    birthday_ids = list(birthday_users.values_list("id", flat=True))

    reaction_map = {
        r["object_id"]: r["total"]
        for r in (
            Reaction.objects
            .filter(content_type="birthday", object_id__in=birthday_ids)
            .values("object_id")
            .annotate(total=Count("id"))
        )
    }

    comment_map = {
        c["object_id"]: c["total"]
        for c in (
            Comment.objects
            .filter(content_type="birthday", object_id__in=birthday_ids)
            .values("object_id")
            .annotate(total=Count("id"))
        )
    }

    for user in birthday_users:
        user.reaction_count = reaction_map.get(user.id, 0)
        user.comment_count = comment_map.get(user.id, 0)

    # ====================================================
    # 💼 CAREERS — SHOW ONLY OPEN JOBS
    # ====================================================

    
    jobs = (
        JobPosting.objects
        .filter(status="open")
        .select_related("posted_by")
        .annotate(applicant_count=Count("jobapplication"))
        .order_by("-created_at")
    )
    
    
    

    return render(request, "intranet/home.html", {
        "grouped_content": grouped_content,
        "birthday_users": birthday_users,
        "new_joinees": new_joinees,    
        "today_day": today_day,   
        "jobs": jobs,   
        "quote": quote,         
    })
    
    

def admin_list_content(request):
    content = Home.objects.all().order_by('order_no')

    content_types = Home.CONTENT_TYPES  # Use choices from model to keep in sync

    return render(request, "intranet/AdminPanel/List_Content.html", {
        'content': content,
        'users': AuraInsideUser.objects.all(),
        'user_fields': get_user_fields(),
        'photo_layouts': PHOTO_LAYOUT_CHOICES,
        'content_types': content_types,  # Make sure to send this!
    })

from django.shortcuts import render, redirect
from django.contrib import messages

def add_home_content(request):

    # ---------- POST (Save Data) ----------
    if request.method == 'POST':
        try:
            username_id = request.POST.get('username')
            if username_id == "nothing" or not username_id:
                username_id = None

            field1 = request.POST.get('field1')
            if field1 == "nothing" or not field1:
                field1 = None

            field2 = request.POST.get('field2')
            if field2 == "nothing" or not field2:
                field2 = None

            order_no = request.POST.get('order_no')
            try:
                order_no = int(order_no)
            except (TypeError, ValueError):
                order_no = 0

            Home.objects.create(
                title=request.POST.get('title'),
                photo=request.FILES.get('photo'),
                username_id=username_id,
                project=request.POST.get('project', '').strip(),
                field1=field1,
                field2=field2,
                description=request.POST.get('description', '').strip(),
                content_type=request.POST.get('content_type'),
                show=request.POST.get('show') == 'True',
                order_no=order_no,
            )

            messages.success(request, "✅ Content added successfully.")
            return redirect('Intranet:admin_list_content')

        except Exception as e:
            messages.error(request, f"❌ Error adding content: {str(e)}")

    # ---------- GET (Show Form Page) ----------
    return render(request, "intranet/AdminPanel/Add_Home_Content.html", {
        'users': AuraInsideUser.objects.all(),
        'user_fields': get_user_fields(),
        'photo_layouts': PHOTO_LAYOUT_CHOICES,
        'content_types': Home.CONTENT_TYPES,
    })


@login_required
def survey_user_response_view(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    existing_response = get_object_or_404(Response, survey=survey, user=request.user)

    return render(request, "hrdesk/survey/survey_user_response.html", {
        "survey": survey,
        "existing_response": existing_response
    })



def edit_home_content(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if not item_id or not item_id.isdigit():
            messages.error(request, "Invalid item ID.")
            return redirect('Intranet:admin_list_content')

        instance = get_object_or_404(Home, id=item_id)

        try:
            instance.title = request.POST.get('title', instance.title)
            instance.description = request.POST.get('description', instance.description)
            instance.content_type = request.POST.get('content_type', instance.content_type)

            if request.FILES.get('photo'):
                instance.photo = request.FILES['photo']

            username_id = request.POST.get('username')
            if username_id == "nothing":
                instance.username = None
            elif username_id:
                instance.username_id = username_id

            instance.project = request.POST.get('project', instance.project)

            field1 = request.POST.get('field1')
            if field1 == "nothing":
                instance.field1 = None
            elif field1:
                instance.field1 = field1

            field2 = request.POST.get('field2')
            if field2 == "nothing":
                instance.field2 = None
            elif field2:
                instance.field2 = field2

            instance.show = request.POST.get('show', str(instance.show)) == 'True'

            order_no = request.POST.get('order_no')
            if order_no and order_no.isdigit():
                instance.order_no = int(order_no)

            instance.save()
            messages.success(request, "Content updated successfully.")
        except Exception as e:
            messages.error(request, f"Error updating content: {str(e)}")

    return redirect('Intranet:admin_list_content')




def delete_home_content(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Home, id=item_id)
        item.delete()
    return redirect('Intranet:admin_list_content')



import json
from django.shortcuts import render

def org_chart(request):

    # ✅ STRICT FILTER (no empty / null allowed)
    operation_users = BoardMembers.objects.filter(chart_type='operation')
    management_users = BoardMembers.objects.filter(chart_type='management')

    def build_data(queryset):
        data = []
        allowed_ids = set(queryset.values_list('id', flat=True))  # ✅ only allowed nodes

        for emp in queryset:

            # ✅ Skip if chart_type missing (extra safety)
            if not emp.chart_type:
                continue

            # ✅ Prevent cross-chart parent linking
            parent_id = None
            if emp.manager and emp.manager.id in allowed_ids:
                parent_id = emp.manager.id

            data.append({
                'id': emp.id,
                'x': emp.name,
                'parent': parent_id,
                'attributes': {
                    'role': emp.role,
                    'photo': f"<img width='120' height='120' style='border-radius:50%' src='{emp.photo.url if emp.photo else ''}'><br>"
                }
            })

        return data

    context = {
        'org_data': json.dumps(build_data(operation_users)),
        'management_data': json.dumps(build_data(management_users)),
    }

    #return render(request, 'intranet/org_chart.html', context)
    return render(request, 'intranet/org_chart.html', context)

    # list org member
def admin_org_chart(request):
    board_members = BoardMembers.objects.select_related('manager').all()
    return render(request, "intranet/AdminPanel/Add_Board_Member.html", {
        'board_members': board_members
    })

from django.db.models import Max
import re

# ✅ ADD
@require_POST
def add_board_member(request):
    name = request.POST.get("name")
    role = request.POST.get("role")
    chart_type = request.POST.get("chart_type")
    photo = request.FILES.get("photo")
    manager_id = request.POST.get("manager")

    manager = None
    if manager_id:
        manager = get_object_or_404(BoardMembers, id=manager_id)

    # Generate ID safely
    existing_ids = BoardMembers.objects.values_list('id', flat=True)
    max_number = 0
    for eid in existing_ids:
        match = re.match(r'bm_(\d+)', str(eid))
        if match:
            max_number = max(max_number, int(match.group(1)))

    new_id = f"bm_{max_number + 1}"

    BoardMembers.objects.create(
        id=new_id,
        name=name,
        role=role,
        chart_type=chart_type,
        photo=photo,
        manager=manager
    )

    return redirect('Intranet:admin_org_chart')


# ✅ EDIT
@require_POST
def edit_board_member(request):
    member = get_object_or_404(BoardMembers, id=request.POST.get("member_id"))

    member.name = request.POST.get("name")
    member.role = request.POST.get("role")
    member.chart_type = request.POST.get("chart_type")

    manager_id = request.POST.get("manager")
    member.manager = BoardMembers.objects.get(id=manager_id) if manager_id else None

    if request.FILES.get("photo"):
        member.photo = request.FILES.get("photo")

    member.save()

    return redirect('Intranet:admin_org_chart')


# ✅ DELETE
def delete_board_member(request, member_id):
    member = get_object_or_404(
        BoardMembers,
        id=member_id
    )

    member.delete()

    return redirect('Intranet:admin_org_chart')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Gallery, GalleryGroup


from django.db.models import Prefetch


from .models import FloatingFlag

def gallery(request):
    # Get all groups and their images
    groups = GalleryGroup.objects.prefetch_related(
        Prefetch(
            "images",
            queryset=Gallery.objects.only(
                "id", "title", "description",
                "thumbnail", "image", "created_at"
            ).order_by("image")   # ✅ A → Z sorting
        )
    )

    # Get the flag

    return render(
        request,
        "intranet/gallery.html",
        {
            "groups": groups,
        }
    )

def upload_images(request):
    groups = GalleryGroup.objects.all()

    if request.method == "POST":
        group_id = request.POST.get("group")
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        files = request.FILES.getlist("images")

        if not group_id or not files:
            messages.error(request, "Please select a group and upload at least one image.")
            return redirect("Intranet:upload_images")

        group = get_object_or_404(GalleryGroup, id=group_id)

        for file in files:
            image_title = title or file.name.rsplit('.', 1)[0]

            Gallery.objects.create(
                group=group,
                title=image_title,
                description=description,
                image=file
            )

        messages.success(request, f"{len(files)} image(s) uploaded successfully.")
        return redirect("Intranet:upload_images")

    return render(
        request,
        "intranet/AdminPanel/upload_img.html",
        {"groups": groups}
    )


def delete_image(request, image_id):
    image = get_object_or_404(Gallery, id=image_id)
    if image.image:
        image.image.delete(save=False)

    image.delete()
    messages.success(request, "Image deleted successfully.")
    return redirect("Intranet:gallery")
    
    

from .models import FloatingFlag

def aura_flag(request):
    flag, _ = FloatingFlag.objects.get_or_create(id=1)

    if request.method == "POST":
        def to_float(val, default):
            try:
                return float(val)
            except (TypeError, ValueError):
                return default

        def to_int(val, default):
            try:
                return int(val)
            except (TypeError, ValueError):
                return default

        flag.title = request.POST.get("title", flag.title)
        flag.color = request.POST.get("color", flag.color)
        flag.camera_angle = to_float(request.POST.get("camera_angle"), flag.camera_angle)

        flag.width = to_float(request.POST.get("width"), flag.width)
        flag.height = to_float(request.POST.get("height"), flag.height)
        flag.pos_x = to_int(request.POST.get("pos_x"), flag.pos_x)
        flag.pos_y = to_int(request.POST.get("pos_y"), flag.pos_y)

        flag.wave_horizontal = to_float(request.POST.get("wave_horizontal"), flag.wave_horizontal)
        flag.wave_vertical = to_float(request.POST.get("wave_vertical"), flag.wave_vertical)
        flag.wave_strength = to_float(request.POST.get("wave_strength"), flag.wave_strength)
        flag.wave_speed = to_float(request.POST.get("wave_speed"), flag.wave_speed)

        if request.FILES.get("image"):
            flag.image = request.FILES["image"]

        flag.save()
        return redirect(request.path)

    return render(request, "intranet/AdminPanel/flag.html", {"flag": flag})



