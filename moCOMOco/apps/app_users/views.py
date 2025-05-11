from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserDetailSerializer, UserUpdateSerializer, PositionSerializer,
)

# Position 매핑
POSITION_NAMES = {
    1: "백엔드(BE)",
    2: "프론트엔드(FE)",
    3: "풀스택(FS)",
    4: "DB관리자(DBA)"
}

def _update_user_position(user, position):
    """사용자 포지션 업데이트 헬퍼 함수"""
    if position not in POSITION_NAMES:
        raise ValueError("유효하지 않은 포지션 값입니다.")
    user.position = position
    user.position_name = POSITION_NAMES[position]
    user.save()

def _prepare_position_response(user, position_value):
    """포지션 응답 데이터 준비 헬퍼 함수 (중복 코드 제거)"""
    _update_user_position(user, position_value)
    return {
        'user_id': user.id,
        'position_id': user.position,
        'position_name': user.position_name,
    }

class UserDetailView(APIView):
    """현재 사용자 정보 조회 API 뷰"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # self를 사용하므로 static 메서드로 변환하지 않음
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        # self를 사용하므로 static 메서드로 변환하지 않음
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserDetailSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # self를 사용하므로 static 메서드로 변환하지 않음
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PositionView(APIView):
    """사용자 포지션 관리 API 뷰"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # self를 사용하므로 static 메서드로 변환하지 않음
        serializer = PositionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 중복 코드를 헬퍼 함수로 대체
            response_data = _prepare_position_response(
                request.user,
                serializer.validated_data['position']
            )
            return Response(response_data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        # self를 사용하므로 static 메서드로 변환하지 않음
        serializer = PositionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 중복 코드를 헬퍼 함수로 대체
            response_data = _prepare_position_response(
                request.user,
                serializer.validated_data['position']
            )
            return Response(response_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)