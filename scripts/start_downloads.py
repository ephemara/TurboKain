import subprocess
import sys
import os

lhs_urls = [
    "http://blpd0.ssl.berkeley.edu/LHS1140/L/spliced_blc0001020304050607_guppi_57774_70844_LHS1140_0002.gpuspec.0000.fil",
    "http://blpd0.ssl.berkeley.edu/LHS1140/L/spliced_blc0001020304050607_guppi_57774_71517_LHS1140_0004.gpuspec.0000.fil"
]

baade_urls = [
    "http://blpd9.ssl.berkeley.edu/GC/AGBT19B_999_03/spliced_blc40414243444546o7o0515253545556o7o0616263646566o7o071727374757677_guppi_58702_19649_BLGCsurvey_Cband_C01_0029.gpuspec.0001.fil"
]

os.makedirs("D:/data/fil/lhs1140", exist_ok=True)
os.makedirs("D:/data/fil/baade_bulge", exist_ok=True)

with open("D:/data/fil/lhs1140/urls.txt", "w") as f:
    f.write("\n".join(lhs_urls) + "\n")

with open("D:/data/fil/baade_bulge/urls.txt", "w") as f:
    f.write("\n".join(baade_urls) + "\n")

print("URLs written to D:/data/fil/lhs1140/urls.txt and D:/data/fil/baade_bulge/urls.txt")
