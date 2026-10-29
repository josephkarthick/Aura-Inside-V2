
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .models import Reaction, Comment


@login_required
@require_POST
@csrf_protect
def add_reaction(request):
    reaction = request.POST.get("reaction")
    content_type = request.POST.get("content_type")
    object_id = request.POST.get("object_id")

    if not all([reaction, content_type, object_id]):
        return JsonResponse({
            "success": False,
            "message": "Missing reaction details."
        }, status=400)

    existing = Reaction.objects.filter(
        user=request.user,
        content_type=content_type,
        object_id=object_id
    ).first()

    if existing:
        if existing.reaction == reaction:
            existing.delete()
            action = "removed"
        else:
            existing.reaction = reaction
            existing.save()
            action = "updated"
    else:
        Reaction.objects.create(
            user=request.user,
            reaction=reaction,
            content_type=content_type,
            object_id=object_id,
        )
        action = "added"

    count = Reaction.objects.filter(
        content_type=content_type,
        object_id=object_id
    ).count()

    return JsonResponse({
        "success": True,
        "action": action,
        "count": count
    })


@login_required
@require_POST
@csrf_protect
def add_comment(request):
    text = (request.POST.get("text") or "").strip()
    content_type = request.POST.get("content_type")
    object_id = request.POST.get("object_id")

    if not all([text, content_type, object_id]):
        return JsonResponse({
            "success": False,
            "message": "Missing comment details."
        }, status=400)

    comment = Comment.objects.create(
        user=request.user,
        text=text,
        content_type=content_type,
        object_id=object_id,
    )

    count = Comment.objects.filter(
        content_type=content_type,
        object_id=object_id
    ).count()

    return JsonResponse({
        "success": True,
        "count": count,
        "comment_id": comment.id
    })


def interaction_details(request):
    content_type = request.GET.get("content_type")
    object_id = request.GET.get("object_id")

    reactions = Reaction.objects.filter(
        content_type=content_type,
        object_id=object_id
    ).select_related("user")

    comments = Comment.objects.filter(
        content_type=content_type,
        object_id=object_id
    ).select_related("user")

    return JsonResponse({
        "reactions": [
            {
                "user": r.user.get_full_name(),
                "type": r.reaction
            }
            for r in reactions
        ],
        "comments": [
            {
                "user": c.user.get_full_name(),
                "comment": c.text
            }
            for c in comments
        ]
    })
