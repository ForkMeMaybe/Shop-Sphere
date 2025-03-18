from rest_framework import viewsets, status
from rest_framework.response import Response
from fuzzywuzzy import fuzz
from .models import Lead, Product
from .serializers import LeadSerializer
from .ml import predict_lead_score  # Assuming you have this function


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        email = data.get("email", "").strip().lower()
        engagement_level = data.get("engagement_level", 0)
        product_ids = data.get("products", [])  # List of product IDs

        # Find existing lead with same email and engagement level
        lead = Lead.objects.filter(
            email=email, engagement_level=engagement_level
        ).first()
        if lead:
            new_score = lead.score + predict_lead_score(engagement_level)
            lead.score = new_score
            lead.save()

            # Associate new products if provided
            if product_ids:
                lead.products.add(*Product.objects.filter(id__in=product_ids))

            return Response(
                {
                    "message": "Lead already exists. Score increased.",
                    "score": lead.score,
                },
                status=status.HTTP_200_OK,
            )

        # Predict lead score for new lead
        lead_score = predict_lead_score(engagement_level)

        # Create new lead
        serializer = self.get_serializer(
            data={**data, "source": "website", "score": lead_score}
        )
        if serializer.is_valid():
            lead = serializer.save()

            # Associate products
            if product_ids:
                lead.products.add(*Product.objects.filter(id__in=product_ids))

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
