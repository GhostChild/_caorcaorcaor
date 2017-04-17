import sys
import vapoursynth as vs

core = vs.get_core()
s=core.ffms2.Source(r"f:\clip1.mp4")
s.set_output()
