from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import Timer
from rest_framework.decorators import api_view
from rest_framework.response import Response

def controller_screen(request):
	if request.method == 'POST':
		duration = int(request.POST.get('duration', 300))
		Timer.objects.create(started_at=now(), duration_seconds=duration)
		return redirect('controller_screen')
	return render(request, 'controller/index.html', {})

@api_view(['GET'])
def get_timer(request):
	timer = Timer.objects.last()
	if not timer:
		return Response({'error': 'No timer found'}, status=404)
	elapsed = (now() - timer.started_at).total_seconds()
	remaining = max(timer.duration_seconds - elapsed, 0)
	return Response({
		'started_at': timer.started_at,
		'duration_seconds': timer.duration_seconds,
		'elapsed_seconds': int(elapsed),
		'remaining_seconds': int(remaining)
	})