from django.utils.text import slugify
import uuid 
from django.template.loader import get_template 
from django.conf import settings


""" Get the image to show in the page"""
def get_cloudinary_image_object(instance,
                          field_name="image",
                          as_html = False,
                          format = None,
                          width = 1200,
                          ):
    
    if not hasattr(instance, field_name):
        return ""

    image_object = getattr(instance , field_name)

    if not image_object:
        return ""
    image_options = {
        "width": width,
    }
    if format is not None:
        image_options["format"] = format

    if as_html:
        return image_object.image(**image_options)
    

    url = image_object.build_url(**image_options)
    return url
        

# video_html = """
# <video controls autoplay>
# <source src="{video_url}"
# </video>
# """




""" Get the video to show in the page"""
def get_cloudinary_video_object(instance,
                          field_name="video",
                          as_html = False,
                          width = None,
                          height = None,
                          sign_url=False,# for private videos
                          fetch_format = "auto",
                          quality = "auto",
                          controles = True,
                          autoplay = True,
                          bigPlayButton = True,
                          ):
    
    if not hasattr(instance, field_name):
        return ""

    video_object = getattr(instance , field_name)

    if not video_object:
        return ""
    video_options = {
        "sign_url":sign_url,
        "fetch_format":fetch_format,
        "quality":quality,
        "controles":controles,
        "autoplay":autoplay,
        "bigPlayButton":bigPlayButton,


    }

    if width is not None:
        video_options['width'] = width
    if height is not None:
        video_options['height'] = height
    if width and width:
        video_options['crop'] = 'limit'

    url = video_object.build_url(**video_options)
    if as_html:
        template_name = "video/snippets/embed.html"
        tmpl = get_template(template_name)
        cloud_name = settings.CLOUDINARY_CLOUD_NAME
        _html = tmpl.render({'video_url': url, 'cloud_name': cloud_name, 'base_color': "#FF2929" })
        return _html
    

    url = video_object.build_url(**video_options)
    return url
        

"""make and return the public id""" 
def get_public_id(instance, *args, **kwagrs):
    title  = instance.title
    unique_id = str(uuid.uuid4()).replace("-","")
    if not title:
        return unique_id
    slug = slugify(title)
    unique_id_short = str(uuid.uuid4()).replace("-","")[:5]

    return f'{slug}-{unique_id_short}'

  

"""make and return the prefix {that will show behind the >} public id of the image""" 
def get_prefix_public_id(instance,*args, **kwargs):

    if hasattr(instance, 'path'):
        path = instance.path
        if path.startswith('/'):
            path=path[1:]
        if path.endswith('/'):
            path=path[:-1]
        return path
    

    public_id = instance.public_id

    model_class = instance.__class__
    model_name = model_class.__name__
    model_name_slug = slugify(model_name)
    if not public_id:
        return f'{model_name_slug}'
    return f'{model_name_slug}/{public_id}'

"""make and return the display name that will show in cloudinary management website."""
def get_display_name(instance, is_video = False, is_thumbnail = False ,*args, **kwargs):

    if is_thumbnail:
        if hasattr(instance , "get_display_name"):
            return f"thumbnail - {instance.get_display_name()}"
        elif hasattr(instance, "title"):
            return f"thumbnail - {instance.title}"

        model_class = instance.__class__
        model_name = model_class.__name__
        return f'thumbnail - {model_name} upload'

    if is_video:
        if hasattr(instance , "get_display_name"):
            return f"video - {instance.get_display_name()}"
        elif hasattr(instance, "title"):
            return f"video - {instance.title}"

        model_class = model_class.__class__
        model_name = model_class.__name__
        return f'video - {model_name} upload'
    
    if hasattr(instance , "get_display_name"):
        return instance.get_display_name()
    elif hasattr(instance, "title"):
        return instance.title
    
    model_class = instance.__class__
    model_name = model_class.__name__
    return f'{model_name} upload'
  

get_thumbnail_display_name = lambda instance: get_display_name(
                                                instance,
                                                is_thumbnail=True) 

get_video_display_name = lambda instance: get_display_name(
                                                instance,
                                                is_video=True) 