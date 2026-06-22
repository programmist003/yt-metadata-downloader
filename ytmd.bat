@echo off
setlocal
pushd "%~dp0"
where python >nul 2>&1
if errorlevel 1 (
  echo Python is not found in PATH.
  pause
  popd
  endlocal
  exit /b 1
)
python "src\main.py" %*
popd
endlocal
