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
        receiver_contact_id = validated_data.pop('receiver_contact_id', None)
        receiver_contact = None

        if receiver_contact_id:
            receiver_contact = Contact.objects.filter(id=receiver_contact_id).first()

        # Set initiator from request context
        interaction = Interaction.objects.create(
            initiator=self.context['request'].user,
            receiver_contact=receiver_contact,
            **validated_data
        )
        return interaction
