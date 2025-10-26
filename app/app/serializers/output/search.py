from rest_framework import serializers
from app.models.user import User
from app.models.contact import Contact
from app.models.scam import ScamRecord
from app.serializers.output.contact import ContactOutputSerializer

class SearchOutputSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()
    spammed_by_count = serializers.SerializerMethodField()
    phone_number = serializers.CharField()

    def get_name(self, obj):
        return obj.get_full_name() if hasattr(obj, 'get_full_name') else f"{getattr(obj, 'first_name', '')} {getattr(obj, 'last_name', '')}".strip()

    def get_is_registered(self, obj):
        return isinstance(obj, User)

    def get_spammed_by_count(self, obj):
        phone_number = getattr(obj, 'phone_number', None)
        if phone_number:
            return ScamRecord.objects.filter(phone_number=phone_number).count()
        return 0


class SearchDetailsUserOutputSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    spammed_by_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'full_name', 'spammed_by_count', 'email', 'phone_number')

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_spammed_by_count(self, obj):
        return ScamRecord.objects.filter(phone_number=obj.phone_number).count()
