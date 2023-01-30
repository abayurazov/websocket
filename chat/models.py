import json

from channels.layers import get_channel_layer
from django.db import models
from django.contrib.auth.models import User

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.TextField()
    is_active = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        print("--------SAVE ISHLADI---------")

        channel_layer = get_channel_layer()
        notification_obj = Notification.objects.filter(is_active=True).count()

        data = {'count': notification_obj, 'current_notification': self.notification}

        async_to_sync(channel_layer.group_send)(
            'test_consumer_group', {
                'type': 'send_notification',
                'value': json.dumps(data)
            }
        )

        super(Notification, self).save(*args, **kwargs)
