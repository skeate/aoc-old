from input02 import v

v = [[int(d) for d in b.split('x')] for b in v.strip().split('\n')]

paper = 0
ribbon = 0
for [l,w,h] in v:
    paper += 2*l*w + 2*w*h + 2*l*h + min(l*w,w*h,l*h)
    ribbon += 2*min(l+w,h+w,l+h)+l*w*h
print(paper)
print(ribbon)
