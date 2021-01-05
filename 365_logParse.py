import csv, json, sys
import time
import subprocess
import shlex

ip_addresses = []
output = []

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    keys = reader.__next__()
    for line in reader:

        # parse the JSON data from the event
        eventData = json.loads(line[3])

        # Get data
        date = line[0]
        source_ip = eventData['ClientIP']
        user = line[1]

        if source_ip not in ip_addresses:
            ip_addresses.append(source_ip)
            info = [user, date, source_ip]
            output.append(info)

# DONE PARSING ORIGINAL FILE; NOW CREATE NEW OUTPUT

with open('$PWD/rdel-jmart_audit_results.csv', 'wt') as f:

    csv_writer = csv.writer(f)

    # Write table headers
    csv_writer.writerow(['User', 'Date', 'IP Address', 'Country', 'State/Province', 'ISP'])

    for line in output:

        # Get GeoIP data, create and run the command
        ip = line[2]
        cmdline = shlex.split('geo -a ' + ip + ' -o all')
        geoip, stderr = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True).communicate()

        # parse the output
        country, state, city, zipcode, isp, ipaddr, extra = geoip.split('\n')

        # write to output file
        line_output = [line[0], line[1], line[2], country, state, isp]
        csv_writer.writerow(line_output)
        time.sleep(2)
