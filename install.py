import subprocess, os, time

USERNAME =    os.getlogin()
LOCAL    =  f"C:\\Users\\{USERNAME}\\AppData\\Local\\Programs\\Python\\Python38\\Scripts\\pip.exe"
GLOBAL   =   "C:\\Program Files\\Python38\\Lib\\Scripts\\pip.exe"
ROAMING  =  f"C:\\Users\\{USERNAME}\\AppData\\Roaming\\Python\\Python38\\Scripts\\pip.exe"


print('Waiting For Response From Python ...')
while True:
    pip_exists =  os.path.exists(LOCAL)  or  os.path.exists(GLOBAL)  or  os.path.exists(ROAMING)
    if pip_exists:
        break

time.sleep(3)
print('Done')

print('Installing RX Language ...')
subprocess.getoutput('pip install rx7')
print('Done')

print('Installing Requirements Packages ...')
Requirements=['colored', 'psutil', 'requests', 'pyautogui', 'keyboard',
              'mouse', 'pyscreeze', 'whois', 'win10toast']
Total = len(Requirements)

for i,Package in enumerate(Requirements, 1):
    print(f'\rInstalling Packages: |{i*"█"}{(Total-i)*" "}| {i}/{Total}', end='')
    subprocess.getoutput(f'pip install {Package}')
print()
print('Done')
