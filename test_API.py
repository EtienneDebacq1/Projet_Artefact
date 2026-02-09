import requests
import time
import math

#simple example with robot moving clockwise along a cercle at 1m from center starting at PI/2 with PI/16 steps
#we post a marker ID found each time the robot enters a new sector

def get_sector(angle):
	angle = int(angle * 180 / math.pi)
	angle = angle % 360
	if angle<=45:
		return 'B'
	if angle<=90:
		return 'A'
	if angle<=135:
		return 'H'
	if angle<=180:
		return 'G'
	if angle<=225:
		return 'F'
	if angle<=270:
		return 'E'
	if angle<=315:
		return 'D'
	if angle<=360:
		return 'C'
	return 'Error'


rsp = requests.get('http://localhost:8080/api/list')
print('Marker list is ' + rsp.text)


dist=100 #at 1m from the center
prev_angle=0
angle=8
inner=0
marker_id=6
runs=30
while runs > 0:
	angle -= 1
	x = int(100 * math.cos( angle * math.pi / 16))
	y = int(100 * math.sin( angle * math.pi / 16 ))
	runs = runs - 1
	requests.post('http://localhost:8080/api/pos?x='+str(x)+'&y='+str(y))
	if angle % 4 == 3:
		final_angle = angle * math.pi / 16
		while final_angle < 0:
			final_angle = final_angle + math.pi*2

		sector = get_sector(final_angle)
		print('sending for angle ' + str(int(180*final_angle/math.pi)) + ' sector ' + sector)

		requests.post('http://localhost:8080/api/marker?id='+str(marker_id)+'&sector='+sector+'&inner='+str(inner))
		marker_id = marker_id + 1
		if inner:
			inner = 0
		else:
			inner = 1
	time.sleep(1)