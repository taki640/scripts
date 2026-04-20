@echo off

for %%f in (*.png) do (
	rem Only works for 1920x1080 screenshots
	magick "%%f" -crop 950x1080+485+0 "../%%f"
)
