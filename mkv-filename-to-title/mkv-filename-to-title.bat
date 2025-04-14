@echo off

for %%f in (*.mkv) do (
    mkvpropedit "%%f" --set "title=%%~nf"
)

pause
