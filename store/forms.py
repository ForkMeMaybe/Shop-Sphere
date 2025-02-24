from django import forms
from .models import ProductImage


class ProductImageForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False
    )  # Add an upload field (not stored in DB)

    class Meta:
        model = ProductImage
        fields = [
            "image_file"
        ]  # Do not include `image_blob` since we manually handle it

    def save(self, commit=True):
        """Convert uploaded image to BLOB before saving"""
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get("image_file")

        if image_file:
            instance.image_blob = image_file.read()  # Convert to binary and store in DB

        if commit:
            instance.save()

        return instance
