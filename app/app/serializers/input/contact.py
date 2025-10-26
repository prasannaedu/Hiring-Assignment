from rest_framework import serializers
from app.models.contact import Contact

class CreateContactInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone_number']

    def validate_phone_number(self, value):
        # Normalize phone numbers: remove spaces, dashes, etc.
        normalized = value.replace(" ", "").replace("-", "")
        if not normalized.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return normalized

    def validate(self, data):
        user = self.context['request'].user
        phone_number = data.get('phone_number')

        if Contact.objects.filter(phone_number=phone_number, created_by=user).exists():
            raise serializers.ValidationError("This contact already exists.")
        return data
