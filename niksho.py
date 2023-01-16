import os
import re
import shodan
import subprocess

# read list of websites from a file
with open('websites.txt', 'r') as f:
    websites = f.readlines()

# initialize Shodan client
SHODAN_API_KEY = "YOUR_API_KEY"
api = shodan.Shodan(SHODAN_API_KEY)

# loop through list of websites and run Nikto scan
for website in websites:
    website = website.strip()
    print(f'Running Nikto scan on {website}')
    try:
        output = subprocess.run(['nikto', '-h', website], capture_output=True, text=True)
        with open(f'{website}_nikto_output.txt', 'w') as f:
            f.write(output.stdout)
        print(f'Nikto scan complete for {website}')

        # extract IP from Nikto output
        ip = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', output.stdout)
        if ip:
            ip = ip.group()
            print(f'IP for {website} is {ip}')
            # run Shodan scan on extracted IP
            print(f'Running Shodan scan on {ip}')
            try:
                host = api.host(ip)
                with open(f'{website}_shodan_output.txt', 'w') as f:
                    f.write(str(host))
            except shodan.APIError as e:
                print(f'Error: {e}')
            print(f'Shodan scan complete for {website}')
        else:
            print(f'Skipping shodan scan for {website} as no IP found')
    except Exception as e:
        print(f'Error running Nikto on {website}: {e}')
