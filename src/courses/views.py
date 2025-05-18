from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse

from . import services
from . import helper
from .models import PublishStatus

# Create your views here.


def course_list_view(request):
    
    queryset = services.get_published_and_coming_soon_courses() 
    
    template_name = "courses/list.html"
    context = {
        'object_list': queryset.order_by("status")
    }
    
    

    if request.htmx:
        template_name = "courses/snippets/list_display.html"
        context["queryset"] = queryset.filter(status=PublishStatus.PUBLISHED)[:3]

    

    return render(request, template_name, context)

def course_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404
    
    lesson_query = services.get_course_lessons(course_obj)

    context = {
        "object": course_obj,
        "lessons_query": lesson_query
    }

    return render(request, 'courses/detail.html', context)

def lesson_detail_view(request, lesson_id=None, course_id=None, *args, **kwargs):

    lesson_obj = services.get_lesson_detail(course_id=course_id, lesson_id=lesson_id)
    

    if lesson_obj is None:
        raise Http404
    
    email_id_exists = request.session.get('email_id')
    if lesson_obj.requires_email and not email_id_exists:
        request.session["next_url"] = request.path
        return render(request,"courses/email_require.html",{})
    
    template_name = "courses/lesson-coming-soon.html"
        
    context = {
        'object': lesson_obj
    }
 
    if not lesson_obj.is_coming_soon and lesson_obj.has_video:
        """ The lesson is published, Go forward & video is available"""

        template_name = "courses/lesson.html"
        video_embed_html = helper.get_cloudinary_video_object(
            lesson_obj,
            field_name='video',
            width= 1250,
            as_html=True)
        context['video_embed'] = video_embed_html




    return render(request, template_name ,context )