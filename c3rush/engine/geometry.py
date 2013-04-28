

def in_rect(xy, rpos, rdim):
	return rpos[0] <= xy[0] <= rpos[0] + rdim[0] and rpos[1] <= xy[1] <= rpos[1] + rdim[1]
