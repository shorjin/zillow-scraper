call D:\code\Python\zillow\zillow\Scripts\activate.bat
cd /d D:\code\Python\zillow\zillow\zilscraper
echo Running first spider...
scrapy crawl zilspider
if %errorlevel% neq 0 (
    echo First spider failed, exiting
    exit /b %errorlevel%
)
echo First spider completed successfully!

echo Running second spider...
scrapy crawl zilsoldspider
if %errorlevel% neq 0 (
    echo Second spider failed, exiting
    exit /b %errorlevel%
)
echo Second spider completed successfully!

echo Running merge.py...
python merge.py
if %errorlevel% neq 0 (
    echo Merge failed
    exit /b %errorlevel%
)

echo All tasks completed successfully!
pause