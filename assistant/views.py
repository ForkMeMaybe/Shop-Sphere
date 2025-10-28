# import boto3
# import json
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
#
#
# class AssistantChatView(APIView):
#     permission_classes = [AllowAny]  # or IsAuthenticated if you prefer
#
#     def post(self, request):
#         user_message = request.data.get("message", "")
#         session_id = request.data.get("session_id", None)
#
#         bedrock = boto3.client("bedrock-runtime")
#
#         payload = {
#             "inputText": user_message,
#             # include tool schema, conversation memory, etc. later
#         }
#
#         response = bedrock.invoke_model(
#             modelId="amazon.nova-lite-v1:0", body=json.dumps(payload)
#         )
#
#         model_output = json.loads(response["body"].read())
#         assistant_reply = model_output["outputText"]
#
#         return Response({"reply": assistant_reply})


import boto3
import json
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from botocore.config import Config


class AssistantChatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = request.data.get("message", "")

        # Configure a longer timeout for the Boto3 client
        config = Config(
            read_timeout=110, connect_timeout=60, retries={"max_attempts": 0}
        )

        # Initialize the Bedrock Agent Runtime client with the new config
        bedrock_agent_runtime = boto3.client(
            "bedrock-agent-runtime", region_name="us-east-1", config=config
        )

        # ✅ Replace with your actual Agent and Alias IDs
        agent_id = "JXRXU9WHUR"
        agent_alias_id = "BDYY2BRYHW"

        # Bedrock requires a sessionId, even if temporary
        session_id = request.data.get("session_id", str(uuid.uuid4()))
        cart_id = request.headers.get("X-Cart-ID")  # Get cart_id from request header

        session_attributes = {}
        if cart_id:
            session_attributes["cart_id"] = cart_id

        try:
            response = bedrock_agent_runtime.invoke_agent(
                agentId=agent_id,
                agentAliasId=agent_alias_id,
                sessionId=session_id,
                inputText=user_message,
                sessionState={"sessionAttributes": session_attributes},
            )

            # Stream completion output
            completion = ""
            for event in response.get("completion", []):
                if "chunk" in event and "bytes" in event["chunk"]:
                    completion += event["chunk"]["bytes"].decode("utf-8")

            return Response(
                {
                    "reply": completion.strip(),
                    "session_id": session_id,  # optional, helpful if you want to reuse it
                }
            )

        except bedrock_agent_runtime.exceptions.ResourceNotFoundException as e:
            return Response(
                {
                    "error": "Agent or alias not found. Check your IDs or region.",
                    "details": str(e),
                },
                status=404,
            )
        except Exception as e:
            return Response(
                {"error": "Failed to contact Bedrock Agent.", "details": str(e)},
                status=500,
            )
