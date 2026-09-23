# Script to generate kain/core/waterfall.kn with embedded assets
import sys

with open("_tmp/font_8x12.hex") as f:
    fhex = f.read().strip()
with open("_tmp/turbo.hex") as f:
    thex = f.read().strip()
with open("_tmp/inferno.hex") as f:
    ihex = f.read().strip()

print(f"Loaded assets: Font {len(fhex)} chars, Turbo {len(thex)} chars, Inferno {len(ihex)} chars")
