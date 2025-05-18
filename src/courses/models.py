from django.db import models

from django.utils.text import slugify 
import uuid

import courses.helper as helper
from cloudinary.models import CloudinaryField

from django.utils import timezone


helper.cloudinary_init()

"""
 - Courses:
	- Title
	- Description
	- Thumbnail/Image
	- Access:
		- Anyone
		- Email required
        - Purchase required
		- User required (n/a)
	- Status: 
		- Published
		- Coming Soon
		- Draft

"""

# def get_public_id(instance, *args, **kwagrs):
#     title  = instance.title
#     unique_id = str(uuid.uuid4()).replace("-","")
#     if not title:
#         return unique_id
#     slug = slugify(title)
#     unique_id_short = str(uuid.uuid4()).replace("-","")[:5]

#     return f'courses/{slug}-{unique_id_short}'

  


# def get_prefix_public_id(instance,*args, **kwargs):

#     if hasattr(instance, 'path'):
#         path = instance.path
#         if path.startswith('/'):
#             path=path[1:]
#         if path.endswith('/'):
#             path=path[:-1]
#         return path
#     public_id = instance.public_id

#     model_class = instance.__class__
#     model_name = model_class.__name__
#     model_name_slug = slugify(model_name)
#     if not public_id:
#         return f'{model_name_slug}'
#     return f'{model_name_slug}/{public_id}'


# def get_display_name(instance, is_video = False, is_thumbnail = False ,*args, **kwargs):

#     if is_thumbnail:
#         if hasattr(instance , "get_display_name"):
#             return f"thumbnail - {instance.get_display_name()}"
#         elif hasattr(instance, "title"):
#             return f"thumbnail - {instance.title}"

#         model_class = instance.__class__
#         model_name = model_class.__name__
#         return f'thumbnail - {model_name} upload'

#     if is_video:
#         if hasattr(instance , "get_display_name"):
#             return f"video - {instance.get_display_name()}"
#         elif hasattr(instance, "title"):
#             return f"video - {instance.title}"

#         model_class = model_class.__class__
#         model_name = model_class.__name__
#         return f'video - {model_name} upload'
    
#     if hasattr(instance , "get_display_name"):
#         return instance.get_display_name()
#     elif hasattr(instance, "title"):
#         return instance.title
    
#     model_class = instance.__class__
#     model_name = model_class.__name__
#     return f'{model_name} upload'
  

# get_thumbnail_display_name = lambda instance: get_display_name(
#                                                 instance,
#                                                 is_thumbnail=True) 

# get_video_display_name = lambda instance: get_display_name(
#                                                 instance,
#                                                 is_video=True) 


class AccessRequirement(models.TextChoices):
    ANYONE = 'any', 'Anyone'
    EMAIL_REQUIRED = 'email_required', 'Email required'

class PublishStatus(models.TextChoices):
    PUBLISHED = 'publish', 'Published'
    COMING_SOON = 'soon', 'Coming Soon'
    DRAFT = 'draft', 'Draft'

def handle_uplaod(instance, filename):
    return f"{filename}"

class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null = True)
    public_id = models.CharField(max_length=120, null=True, blank=True, db_index= True)
    # image = models.ImageField(upload_to=handle_uplaod, blank=True, null=True)
    image = CloudinaryField(
        "image",
        null = True,
        public_id_prefix = helper.get_prefix_public_id,
        display_name = helper.get_display_name,
        tags = ["course", "thumbnail"]
        )
    access = models.CharField(
        max_length=20,
        choices=AccessRequirement.choices,
        default= AccessRequirement.EMAIL_REQUIRED
    )
    status = models.CharField(
        max_length=20,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT
    )  
    created_at = models.DateTimeField(auto_now_add=True)  
    last_update = models.DateTimeField(auto_now=True)

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
    
    @property
    def image_admin_url(self):
        if not self.image:
            return ""
        
        image_options = {
            "width": 400
        }
        
 

        url = self.image.build_url(**image_options)

        return url
    
    @property
    def is_coming_soon(self):
        return self.status == PublishStatus.COMING_SOON
            

    def save(self,*args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = helper.get_public_id(self)
        super().save(args, kwargs)



    def get_absolute_url(self):
        return self.path
    
    def get_display_name(self):
        return f"{self.title} - Course"
    

    def get_thumbnail(self):
        if not self.image:
            return None
        return helper.get_cloudinary_image_object(self, field_name="image", as_html=False, width= 300)
    
    def get_display_image(self):
        if not self.image:
            return None
        return helper.get_cloudinary_image_object(self, field_name="image", as_html=False, width= 1700)

    @property
    def path(self):
        return f'/courses/{self.public_id}'

  
    # def image_admin_thumbnail(self, as_html = False, width = 500):
    #     if not self.image:
    #         return ""
        
    #     image_options = {
    #         "width": width
    #     }

    #     if as_html:
    #         #CloudinaryImage(str(self.image)).image(**image_options) same with
    #         return self.image.image(**image_options)
    #     #CloudinaryImage(str(self.image)).build_url(**image_options) same with
    #     url = self.image.build_url(**image_options)
    #     return url         
        

    # def image_admin_detail(self, as_html = False, width = 750):
    #         if not self.image:
    #             return ""
            
    #         image_options = {
    #             "width": width
    #         }

    #         if as_html:
    #             #CloudinaryImage(str(self.image)).image(**image_options) same with
    #             return self.image.image(**image_options)
    #         #CloudinaryImage(str(self.image)).build_url(**image_options) same with
    #         url = self.image.build_url(**image_options)
    #         return url   
        



    def __str__(self):
        return self.title
    

"""
- Lessons
    - Title
    - Description
    - Video
    - Status: Published, Coming Soon, Draft
"""

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=120, null=True, blank=True, db_index= True)
    thumbnail = CloudinaryField(
                "image",
                blank = True,
                null = True,
                public_id_prefix = helper.get_prefix_public_id,
                display_name = helper.get_thumbnail_display_name,
                tags= ["thumbnail", "lesson"]
                )
    video = CloudinaryField(
            "video",
            blank = True,
            null = True,
            resource_type= "video",
            public_id_prefix = helper.get_prefix_public_id,
            display_name = helper.get_video_display_name,
            tags= ["video", "lesson"],
            type = 'private',
            )
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(default=True,
        help_text="If user does not have access to the course, can they see this?")
    
    status = models.CharField(
        max_length=20,
        choices=PublishStatus.choices,
        default=PublishStatus.PUBLISHED
    )   
    created_at = models.DateTimeField(auto_now_add=True)  
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-last_update"]

    def save(self,*args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = helper.get_public_id(self)
        super().save(args, kwargs)


    def get_absolute_url(self):
        return self.path
    
        

        
    @property
    def path(self):
        course_path = self.course.path
        if course_path.endswith('/'):
            course_path = course_path[:-1]
        return f'{course_path}/lessons/{self.public_id}'

    def get_display_name(self):
        return f"{self.title} - {self.course.get_display_name()}"
    
    def get_thumbnail(self):
        width = 300
        if self.thumbnail:
            return helper.get_cloudinary_image_object(self, field_name="thumbnail", as_html=False, width= width)
        elif self.video:
            return helper.get_cloudinary_image_object(self, field_name="video",format="jpg", as_html=False, width= width)
        
        return None
    
    @property
    def is_coming_soon(self):
        return self.status == PublishStatus.COMING_SOON
    
    @property
    def has_video(self):
        return self.video is not None
    
    @property
    def requires_email(self):
        return self.course.access == AccessRequirement.EMAIL_REQUIRED

    def __str__(self):
        return self.title

    