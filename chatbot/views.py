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


class ChatView(APIView):
    permission_classes = [IsAuthenticated] # 인증된 사용자만 접근 가능
    throttle_classes = [UserRateThrottle] # 사용자 요청 속도 제한 설정

    def post(self, request, *args, **kwargs):
        # 유저의 질문 가져오기
        prompt = request.data.get('prompt')
        if prompt:
            # 이전 대화 기록 가져오기
            user = request.user
            session_conversations = user.conversation.all()
            previous_conversations = "\n".join([f"User: {c['prompt']}\nAI: {c['response']}" for c in session_conversations])
            prompt_with_previous = f"{previous_conversations}\nUser: {prompt}\nAI:"

            model_engine = "text-davinci-003"
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt_with_previous,
                max_tokens=1024,
                n=5,
                stop=None,
                temperature=0.5,
            )
            response = completions.choices[0].text.strip()

            conversation = Conversation(questioner=user, prompt=prompt, response=response)
            conversation.save()

            # 대화 기록에 새로운 응답 추가 더이상 필요하지 않음. 위의 conversation.save() 로 데이터베이스에 대화 기록이 저장되기 때문

            # session_conversations.append({'prompt': prompt, 'response': response})
            # request.session['conversations'] = session_conversations
            # request.session.modified = True

            return Response(status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)