from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Timer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import timedelta, timezone as dt_timezone

def controller_screen(request):
	if request.method == 'POST':
		action = request.POST.get('action')
		now_utc = timezone.now()  # aware UTC datetime
		if action == 'end':
			Timer.objects.create(started_at=now_utc, duration_seconds=0)
		elif action == 'schedule_end':
			now_utc = timezone.now()
			now_local = timezone.localtime(now_utc)
			target_local = now_local.replace(hour=21, minute=45, second=0, microsecond=0)
			if target_local <= now_local:
				target_local += timedelta(days=1)
			# Convert local-aware datetime to UTC
			target_utc = target_local.astimezone(dt_timezone.utc)
			duration = (target_utc - now_utc).total_seconds()
			Timer.objects.create(started_at=now_utc, duration_seconds=int(max(duration, 0)))
		else:
			duration = int(request.POST.get('duration', 300))
			Timer.objects.create(started_at=now_utc, duration_seconds=duration)

		return redirect('controller_screen')
	return render(request, 'controller/index.html', {})

@api_view(['GET'])
def get_timer(request):
	timer = Timer.objects.last()
	if not timer:
		return Response({'error': 'No timer found'}, status=404)
	now_utc = timezone.now()
	elapsed = (now_utc - timer.started_at).total_seconds()
	remaining = max(timer.duration_seconds - elapsed, 0)
	ending_at = timer.started_at + timedelta(seconds=timer.duration_seconds)
	return Response({
		'started_at': timer.started_at,
		'ending_at': ending_at,
		'duration_seconds': timer.duration_seconds,
		'elapsed_seconds': int(elapsed),
		'remaining_seconds': int(remaining)
	})