from django.core.mail import BadHeaderError
from smtplib import SMTPException
from django.utils.timezone import now
from django.core.mail import EmailMessage
from .models import Lead
from celery import shared_task
from templated_mail.mail import BaseEmailMessage
from decimal import Decimal


# @shared_task
def process_leads_for_marketing():
    """
    Fetch leads, send relevant emails, and delete followed leads.
    """
    leads = Lead.objects.filter(score__gte=40)

    for lead in leads:
        email = lead.email
        engagement = lead.engagement_level
        # Fetch product titles as a comma-separated string
        product_titles = ", ".join(lead.products.values_list("title", flat=True))

        template_name = None
        context = {"lead": lead}

        print(f"Lead: {lead.email}, Score: {lead.score}, Type: {type(lead.score)}")

        if engagement == 0 and int(lead.score) >= 40:  # Website Visit Only
            print("product_titles" + product_titles)
            print("sending mail")
            template_name = "emails/engagement_0.html"
        elif (
            engagement == 1 and int(lead.score) >= 120 and product_titles
        ):  # Product Search
            print("product_titles" + product_titles)
            print("sending mail")
            template_name = "emails/engagement_1.html"
            context["product_titles"] = product_titles
        elif (
            engagement == 2 and int(lead.score) >= 140 and product_titles
        ):  # Added to Cart
            print("product_titles" + product_titles)
            print("sending mail")
            template_name = "emails/engagement_2.html"
            context["product_titles"] = product_titles
        elif engagement == 3 and product_titles:  # Reached Payment Page
            print("product_titles" + product_titles)
            print("sending mail")
            template_name = "emails/engagement_3.html"
            context["product_titles"] = product_titles

        if template_name:
            try:
                message = BaseEmailMessage(
                    template_name=template_name,
                    context=context,
                )
                message.send([email])
                print("mail sent")
                # Remove the lead after sending email
                lead.delete()
            except (BadHeaderError, SMTPException) as e:
                print(f"Failed to send email to {email}. Error: {str(e)}")
