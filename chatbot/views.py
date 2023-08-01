from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from rest_framework.authentication import TokenAuthentication
from dotenv import load_dotenv
import openai
import os
from .models import Conversation
from .serializers import CoversationSerializer

User = get_user_model()

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

class ChatList(APIView):
    permission_classes = [IsAuthenticated] # 인증된 사용자만 접근 가능

    def get(self, request, *args, **kwargs):
        session_conversations = Conversation.objects.filter(questioner=request.user).order_by('-asked_at')
        previous_conversations = "\n".join([f"Asked at: {c.asked_at.strftime('%Y-%m-%d %H:%M')}\nUser: {c.prompt}\nAI: {c.response}" for c in session_conversations])
        return Response(previous_conversations)


class ChatView(APIView):
    # 인증된 사용자만 접근 가능
    permission_classes = [IsAuthenticated] 
    # 사용자 요청 속도 제한 설정
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        # 유저의 질문 가져오기
        prompt = request.data.get('prompt')

        if prompt:
            prompt_with_previous = f"User: {prompt}\nAI:"
            print(prompt_with_previous)
            model_engine = "text-davinci-003"
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt_with_previous,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            response = completions.choices[0].text.strip()

            conversation = Conversation(questioner=request.user, prompt=prompt, response=response)
            conversation.save()

            return Response(completions, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)