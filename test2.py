import os, subprocess,re
a=subprocess.check_output("netsh wlan show profile", shell=True, universal_newlines=True)
lines=a.split("\n")
user_profiles = []

for line in lines:
    if re.match(r'\s+All User Profile\s+:\s+(.+)', line):
        match = re.match(r'\s+All User Profile\s+:\s+(.+)', line)
        user_profile = match.group(1)
        user_profiles.append(user_profile)
print("Select the user profile index for which you want to check the password:")
sl = 1
for profile in user_profiles:
    print(str(sl)+". "+profile)
    sl+=1
userInput = int(input("Enter the index for which you want to check the password: "))
print(user_profiles[userInput-1])
passInfo = subprocess.check_output("netsh wlan show profile "+user_profiles[userInput-1]+" key=clear")
passInfo = passInfo.decode().split('\n')
password = None

for line in passInfo:
    if "Key Content" in line:
        password = line.split(":")[-1].strip()
print("Password:", password)