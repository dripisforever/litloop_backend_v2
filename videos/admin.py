# from django.contrib import admin
#
# from .models import (
#     Category,
#     Comment,
#     EncodeProfile,
#     Encoding,
#     Language,
#     Media,
#     Subtitle,
#     Tag,
# )
#
#
# class CommentAdmin(admin.ModelAdmin):
#     search_fields = ["text"]
#     list_display = ["text", "add_date", "user", "media"]
#     ordering = ("-add_date",)
#     readonly_fields = ("user", "media", "parent")
#
#
# class MediaAdmin(admin.ModelAdmin):
#     search_fields = ["title"]
#     list_display = [
#         "title",
#         "user",
#         "add_date",
#         "media_type",
#         "duration",
#         "state",
#         "is_reviewed",
#         "encoding_status",
#         "featured",
#         "get_comments_count",
#     ]
#     list_filter = ["state", "is_reviewed", "encoding_status", "featured", "category"]
#     ordering = ("-add_date",)
#     readonly_fields = ("user", "tags", "category", "channel")
#
#     def get_comments_count(self, obj):
#         return obj.comments.count()
#
#     get_comments_count.short_description = "Comments count"
#
#
# class CategoryAdmin(admin.ModelAdmin):
#     search_fields = ["title"]
#     list_display = ["title", "user", "add_date", "is_global", "media_count"]
#     list_filter = ["is_global"]
#     ordering = ("-add_date",)
#     readonly_fields = ("user", "media_count")
#
#
# class TagAdmin(admin.ModelAdmin):
#     search_fields = ["title"]
#     list_display = ["title", "user", "media_count"]
#     readonly_fields = ("user", "media_count")
#
#
# class EncodeProfileAdmin(admin.ModelAdmin):
#     list_display = ("name", "extension", "resolution", "codec", "description", "active")
#     list_filter = ["extension", "resolution", "codec", "active"]
#     search_fields = ["name", "extension", "resolution", "codec", "description"]
#     list_per_page = 100
#     fields = ("name", "extension", "resolution", "codec", "description", "active")
#
#
# class LanguageAdmin(admin.ModelAdmin):
#     pass
#
#
# class SubtitleAdmin(admin.ModelAdmin):
#     pass
#
#
# class EncodingAdmin(admin.ModelAdmin):
#     pass
#
#
# admin.site.register(EncodeProfile, EncodeProfileAdmin)
# admin.site.register(Comment, CommentAdmin)
# admin.site.register(Media, MediaAdmin)
# admin.site.register(Encoding, EncodingAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Tag, TagAdmin)
# admin.site.register(Subtitle, SubtitleAdmin)
# admin.site.register(Language, LanguageAdmin)
