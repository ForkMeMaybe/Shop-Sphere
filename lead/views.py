from rest_framework import viewsets, status
from rest_framework.response import Response
from fuzzywuzzy import fuzz

from .models import Lead
from .serializers import LeadSerializer
from .ml import predict_lead_score  # Assuming you have this function


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get("name", "").strip().lower()
        email = data.get("email", "").strip().lower()
        message = data.get("message", "")
        engagement_level = data.get("engagement_level", 0)

        # Check if the lead already exists
        lead = Lead.objects.filter(email=email).first()
        if lead:
            # Increase the lead's score
            new_score = lead.score + predict_lead_score(engagement_level)
            lead.score = min(new_score, 100)  # Ensure it doesn't exceed 100
            lead.save()

            return Response(
                {
                    "message": "Lead already exists. Score increased.",
                    "score": lead.score,
                },
                status=status.HTTP_200_OK,
            )

        # Check for similar names using fuzzy matching
        # for existing_lead in Lead.objects.all():
        #     name_similarity = fuzz.ratio(name, existing_lead.name.lower())
        #     email_similarity = fuzz.ratio(email, existing_lead.email.lower())
        #     if name_similarity > 85 or email_similarity > 85:  # Threshold = 85
        #         return Response(
        #             {
        #                 "message": "Duplicate lead detected based on name or email similarity."
        #             },
        #             status=status.HTTP_400_BAD_REQUEST,
        #         )

        # Predict lead score for new lead
        lead_score = predict_lead_score(engagement_level)

        # Save new lead
        serializer = self.get_serializer(
            data={**data, "source": "website", "score": lead_score}
        )
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# impoate(self, request, *args, **kwargs):
#         # data = json.loads(request.body)
#         # email = data.get("email")
#
#         # Get data from request
#         data = request.data
#         name = data.get("name", "").strip().lower()
#         email = data.get("email", "").strip().lower()
#         source = data.get("source", "").strip().lower()
#         message = data.get("message", "")
#
#         # Check if the lead already exists (exact email match)
#         if Lead.objects.filter(email=email).exists():
#             return Response(
#                 {"message": "Lead with this email already exists."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         # Check for similar names using fuzzy matching
#         for lead in Lead.objects.all():
#             if fuzz.ratio(name, lead.name.lower()) > 85:  # Threshold = 85
#                 return Response(
#                     {"message": "Duplicate lead detected based on name similarity."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#
#         # Predict lead score
#         engagement_level = 1  # Default engagement level
#         lead_score = predict_lead_score(source, engagement_level)
#
#         # Perform sentiment analysis
#         sentiment = analyze_sentiment(message) if message else "Neutral"
#
#         # Add calculated fields before saving
#         serializer = self.get_serializer(
#             data={**data, "score": lead_score, "sentiment": sentiment}
#         )
#         if serializer.is_valid():
#             self.perform_create(serializer)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
