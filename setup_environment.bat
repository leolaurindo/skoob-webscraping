@echo off
conda create --name skoob_scrap python -y

conda activate skoob_scrap

pip install -r requirements.txt

echo Environment setup completed.

echo Remember to download the chrome driver and google chrome
echo For Google Chrome, visit: https://www.google.com/intl/pt-BR/chrome/
echo For Chrome Driver, visit: https://googlechromelabs.github.io/chrome-for-testing/

pause