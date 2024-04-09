# create a loop that loops through the list ove rand over
frames = ["frame1", "frame2", "frame3", "frame4"]

x = 0
print(frames[x])
x+=1
print(frames[x])
x+=1
print(frames[x])
x+=1
print(frames[x])
x+=1
firstFrame = x%len(frames)
print(firstFrame)