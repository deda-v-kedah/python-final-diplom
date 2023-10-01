from django.db.models.signals import post_save
from django.dispatch import receiver

from my_diplom_app.models import User
# from my_diplom_app.views import send
from my_diplom_app.tasks import send



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    user = User.objects.get(username=instance)
    if created:
        
        send.delay('Регистрация успешна', 
f'Здравствуйте, {user.last_name}! \
Если вы получили это письмо, \
значит вы зарегистрировались: "там-то там-то"\n\n\
Ваш логин: {instance}\n\n\
Спасибо =>\n\n\n\
Если вы ни где не регестрировались, просто закройте это сообщение.',
             [user.email])


