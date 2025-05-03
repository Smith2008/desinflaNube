from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

class CostView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute('SELECT date, cost FROM aws_billing ORDER BY date;')
            rows = cursor.fetchall()
        data = [{'date': r[0].isoformat(), 'cost': float(r[1])} for r in rows]
        return Response(data)
