import boto3
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class AssistantChatView(APIView):
    permission_classes = [AllowAny]  # or IsAuthenticated if you prefer

    def post(self, request):
        user_message = request.data.get("message", "")
        session_id = request.data.get("session_id", None)

        bedrock = boto3.client("bedrock-runtime")

        payload = {
            "inputText": user_message,
            # include tool schema, conversation memory, etc. later
        }

        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",  # Example
            body=json.dumps(payload)
        )

        model_output = json.loads(response["body"].read())
        assistant_reply = model_output["outputText"]

        return Response({"reply": assistant_reply})
