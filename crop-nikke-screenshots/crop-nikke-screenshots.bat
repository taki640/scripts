@echo off

for %%f in (*.png) do (
	rem Only works for 1920x1080 screenshots
	set /p ="%%f... " <NUL
	magick "%%f" -crop 950x1080+485+0 "../%%f"
	echo Done.
)
