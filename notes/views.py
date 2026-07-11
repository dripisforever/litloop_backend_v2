import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Count
from notes.models import Page, Block, BlockTable, PageTag
from users.auth_utils import jwt_required_testable

# ── Pages ──────────────────────────────────────────

@csrf_exempt
@jwt_required_testable
def list_pages(request):
    pages = Page.objects.filter(author=request.user)
    data = [p.to_dict() for p in pages]
    return JsonResponse(data, safe=False)


@csrf_exempt
@jwt_required_testable
def create_page(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")
    try:
        data = json.loads(request.body)
        title = data.get("title", "").strip() or ""
        parent_id = data.get("parent_id")
        parent = Page.objects.get(id=parent_id, author=request.user) if parent_id else None
        page = Page.objects.create(title=title, author=request.user, parent=parent)
        return JsonResponse(page.to_dict(), status=201)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Page.DoesNotExist:
        return JsonResponse({"error": "Parent page not found"}, status=404)


@csrf_exempt
@jwt_required_testable
def get_page(request, page_id):
    page = get_object_or_404(Page, id=page_id, author=request.user)
    data = page.to_dict()
    blocks = page.blocks.all().prefetch_related('table_data')
    data["blocks"] = [b.to_dict() for b in blocks]
    return JsonResponse(data)


@csrf_exempt
@jwt_required_testable
def update_page(request, page_id):
    if request.method != "PUT":
        return HttpResponseBadRequest("Invalid method")
    try:
        page = Page.objects.get(id=page_id, author=request.user)
        data = json.loads(request.body)
        if "title" in data:
            page.title = data["title"].strip() or ""
        page.save()
        return JsonResponse(page.to_dict())
    except Page.DoesNotExist:
        return JsonResponse({"error": "Page not found"}, status=404)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")


@csrf_exempt
@jwt_required_testable
def delete_page(request, page_id):
    if request.method != "DELETE":
        return HttpResponseBadRequest("Invalid method")
    try:
        page = Page.objects.get(id=page_id, author=request.user)
        page.delete()
        return JsonResponse({"message": "Page deleted"})
    except Page.DoesNotExist:
        return JsonResponse({"error": "Page not found"}, status=404)


# ── Blocks ──────────────────────────────────────────

@csrf_exempt
@jwt_required_testable
def create_block(request, page_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")
    try:
        page = Page.objects.get(id=page_id, author=request.user)
        data = json.loads(request.body)
        block_type = data.get("type", "text")
        content = data.get("content", "")
        order = data.get("order", page.blocks.count())
        block = Block.objects.create(page=page, type=block_type, content=content, order=order)
        if block_type == "table":
            BlockTable.objects.create(
                block=block,
                columns=data.get("table_data", {}).get("columns", ["Column 1", "Column 2"]),
                rows=data.get("table_data", {}).get("rows", [["", ""]]),
            )
        return JsonResponse(block.to_dict(), status=201)
    except Page.DoesNotExist:
        return JsonResponse({"error": "Page not found"}, status=404)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")


@csrf_exempt
@jwt_required_testable
def update_block(request, block_id):
    if request.method != "PUT":
        return HttpResponseBadRequest("Invalid method")
    try:
        block = Block.objects.get(id=block_id, page__author=request.user)
        data = json.loads(request.body)
        if "content" in data:
            block.content = data["content"]
        if "order" in data:
            block.order = data["order"]
        block.save()
        return JsonResponse(block.to_dict())
    except Block.DoesNotExist:
        return JsonResponse({"error": "Block not found"}, status=404)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")


@csrf_exempt
@jwt_required_testable
def delete_block(request, block_id):
    if request.method != "DELETE":
        return HttpResponseBadRequest("Invalid method")
    try:
        block = Block.objects.get(id=block_id, page__author=request.user)
        block.delete()
        return JsonResponse({"message": "Block deleted"})
    except Block.DoesNotExist:
        return JsonResponse({"error": "Block not found"}, status=404)


# ── Table Blocks ────────────────────────────────────

@csrf_exempt
@jwt_required_testable
def update_block_table(request, block_id):
    if request.method != "PUT":
        return HttpResponseBadRequest("Invalid method")
    try:
        block = Block.objects.get(id=block_id, page__author=request.user, type='table')
        data = json.loads(request.body)
        table_data, _ = BlockTable.objects.get_or_create(block=block)
        if "columns" in data:
            table_data.columns = data["columns"]
        if "rows" in data:
            table_data.rows = data["rows"]
        table_data.save()
        return JsonResponse(block.to_dict())
    except Block.DoesNotExist:
        return JsonResponse({"error": "Table block not found"}, status=404)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")


# ── Tags ────────────────────────────────────────────

@csrf_exempt
@jwt_required_testable
def list_tags(request, page_id):
    page = get_object_or_404(Page, id=page_id, author=request.user)
    data = [t.to_dict() for t in page.tags.all()]
    return JsonResponse(data, safe=False)


@csrf_exempt
@jwt_required_testable
def add_tag(request, page_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")
    try:
        page = Page.objects.get(id=page_id, author=request.user)
        data = json.loads(request.body)
        name = data.get("name", "").strip().lower()
        if not name:
            return JsonResponse({"error": "Tag name is required"}, status=400)
        tag, created = PageTag.objects.get_or_create(page=page, name=name)
        return JsonResponse(tag.to_dict(), status=201)
    except Page.DoesNotExist:
        return JsonResponse({"error": "Page not found"}, status=404)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")


@csrf_exempt
@jwt_required_testable
def delete_tag(request, tag_id):
    if request.method != "DELETE":
        return HttpResponseBadRequest("Invalid method")
    try:
        tag = PageTag.objects.get(id=tag_id, page__author=request.user)
        tag.delete()
        return JsonResponse({"message": "Tag deleted"})
    except PageTag.DoesNotExist:
        return JsonResponse({"error": "Tag not found"}, status=404)


@csrf_exempt
@jwt_required_testable
def search_by_tags(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")
    try:
        data = json.loads(request.body)
        tag_names = data.get("tags", [])
        if not tag_names:
            return JsonResponse([], safe=False)
        tag_names = [t.strip().lower() for t in tag_names]
        pages = Page.objects.filter(
            author=request.user,
            tags__name__in=tag_names
        ).annotate(
            match_count=Count('id')
        ).filter(match_count__gte=len(tag_names)).distinct()
        return JsonResponse([p.to_dict() for p in pages], safe=False)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
