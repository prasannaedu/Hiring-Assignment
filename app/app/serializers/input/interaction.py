from rest_framework import serializers
from app.models.interaction import Interaction
from app.models.contact import Contact


class InteractionSerializer(serializers.ModelSerializer):
    receiver_contact_id = serializers.UUIDField(required=False, write_only=True)

    class Meta:
        model = Interaction
        fields = ['id', 'receiver_contact_id', 'type', 'metadata', 'timestamp']
        read_only_fields = ['id', 'timestamp']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required to record interaction.")

        receiver_contact_id = validated_data.pop('receiver_contact_id', None)
        receiver_contact = None

        if receiver_contact_id:
            receiver_contact = Contact.objects.filter(id=receiver_contact_id).first()
            if not receiver_contact:
                raise serializers.ValidationError({"receiver_contact_id": "Invalid contact ID."})

        return Interaction.objects.create(
            initiator=request.user,
            receiver_contact=receiver_contact,
            **validated_data
        )


class SpamReportCreateSerializer(serializers.Serializer):
    contact_id = serializers.UUIDField()

    def validate_contact_id(self, value):
        if not Contact.objects.filter(id=value).exists():
            raise serializers.ValidationError("Contact not found.")
        return value
