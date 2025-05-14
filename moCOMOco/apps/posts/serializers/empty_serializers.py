from rest_framework import serializers


# 요청/응답에 별도 데이터가 필요 없는 경우 사용
class EmptySerializer(serializers.Serializer):
    pass
