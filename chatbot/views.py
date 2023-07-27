from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from dotenv import load_dotenv
import openai
import os
from .models import Conversation
from .serializers import CoversationSerializer

User = get_user_model()

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class ChatView(APIView):

    throttle_classes = [UserRateThrottle]

    # def get(self, request, pk, *args, **kwargs):
    #     # 로그인 후 특정 유저의 챗 봇 대화 가져오기
    #     conversations = Conversation.objects.get(pk=pk) # user_id
    #     # JSON 형태로 대화내역 나열 후 전송
    #     serialized_conversations = CoversationSerializer(conversations, many=True) # 직렬화
    #     return Response(serialized_conversations.data)

    def post(self, request, *args, **kwargs):
        # 유저의 질문 가져오기
        prompt = request.data.get('prompt')
        if prompt:
            # 이전 대화 기록 가져오기 -> get 이 필요가 없음. 채팅화면은 프론트에서 해줄테니깐
            session_conversations = request.session.get('conversations', [])
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

            conversation = Conversation(prompt=prompt, response=response)
            conversation.save()

            # 대화 기록에 새로운 응답 추가
            session_conversations.append({'prompt': prompt, 'response': response})
            request.session['conversations'] = session_conversations
            request.session.modified = True

            return Response(status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)