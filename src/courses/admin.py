from django.contrib import admin

"""html format to display image and any html element"""
from django.utils.html import format_html

from cloudinary import CloudinaryImage
import courses.helper as helper

from .models import Course, Lesson

class LessonsInLine(admin.StackedInline):
    model= Lesson
    fields = ["public_id","title", "description","display_desc", "can_preview" ,"status", "thumbnail", "video", "display_image","display_video"]

    readonly_fields = ["display_desc","public_id","last_update", "created_at","display_image", "display_video"]
    extra = 0

    def display_image(self, obj,  *args, **kwargs):
        """display the thumbnail in lesson admin"""
        url = helper.get_cloudinary_image_object(obj, field_name='thumbnail', as_html=False, width= 300)
        return format_html(f"<img src='{url}' />" )  

    def display_video(self, obj,  *args, **kwargs):
        """display the video in lesson admin"""
        video_embed_html = helper.get_cloudinary_video_object(obj,
                                                field_name='video',
                                                width= 550,
                                                height=550,
                                                as_html=True)
        return video_embed_html
        

    def display_desc(self, obj,  *args, **kwargs):
        """display the description in lesson admin"""
        text = obj.description
        return format_html(f"<h1>{text}</h1>")


    
    display_image.short_description = "Current Image"
    display_desc.short_description = "Current Description"
  


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [
        LessonsInLine,
    ]
    list_display = ["title", "status", "access"]
    list_filter = ['status', 'access']
    fields = ["public_id","title", "description","display_desc", "status", "image", "access", "display_image"]
    readonly_fields = ["public_id","display_image", "display_desc","last_update", "created_at"]



    def display_image(self, obj,  *args, **kwargs):
        """display the image in Course admin"""
        url = helper.get_cloudinary_image_object(obj, field_name="image", as_html=False, width= 300)
        return format_html(f"<img src='{url}' />" )
        

    def display_desc(self, obj,  *args, **kwargs):
        """display the description in Course admin"""
        text = obj.description
        return format_html(f"<h1>{text}</h1>") 

    display_image.short_description = "Current Image"
    display_desc.short_description = "Current Description"



# Register your models here.
# admin.site.register(Course, CourseAdmin)