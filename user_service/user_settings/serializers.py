from rest_framework import serializers
from user_service.user_settings.models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = '__all__'
    
    def deleteAccount(self):
        self.instance.deleteAccount()