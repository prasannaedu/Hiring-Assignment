from rest_framework import serializers
from app.models.interaction import Interaction
from app.serializers.output.user import UserOutputSerializer
from app.serializers.output.contact import ContactOutputSerializer


class InteractionOutputSerializer(serializers.ModelSerializer):
    initiator = UserOutputSerializer(read_only=True)
    receiver_user = UserOutputSerializer(read_only=True, allow_null=True)
    receiver_contact = ContactOutputSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Interaction
        fields = (
            'id',
            'initiator',
            'receiver_user',
            'receiver_contact',
            'type',
            'timestamp',
            'metadata',
        )
