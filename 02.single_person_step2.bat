.\env\python.exe single_person_step2.py
IF %ERRORLEVEL% NEQ 0 (
    echo somthing got wrong。
    PAUSE
    exit /b %ERRORLEVEL%
)