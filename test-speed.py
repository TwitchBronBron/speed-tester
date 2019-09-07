import gc
import time
import json
import os
import speedtest

secondsBetweenTests = 600  # 10 minutes


# create the csv file if it doesn't already exist
f = None
if not os.path.exists('results.csv'):
    f = open('results.csv', 'w+')
    f.writelines(
        'Server ID,Sponsor,Server Name,Timestamp,Ping,Download (Megabits/second),Upload (Megabits/second),Share,Client IP Address'
    )
    f.flush()
else:
    f = open('results.csv', 'a+')


def doTest(runNumber):
    print('----------- Test ' + str(runNumber) + ' ---------------')

    servers = []
    threads = None
    print('initializing speed test')
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()

    print('testing download speed')
    s.download(threads=threads)

    print('testing upload speed')
    s.upload(threads=threads, pre_allocate=False)

    s.results.share()
    result = s.results.dict()

    download = result['download'] / 1000000
    upload = result['upload'] / 1000000
    print (' ')
    print('Download = ' + str(download))
    print('Upload = ' + str(upload))
    print('Ping = ' + str(result['ping']))
    print(' ')

    print('writing results to csv')
    csvLine = ','.join(map(str, [
        result['server']['id'],
        '"' + result['server']['sponsor'] + '"',
        '"' + result['server']['name'] + '"',
        result['timestamp'],
        result['ping'],
        download,
        upload,
        result['share'],
        result['client']['ip']
    ]))
    f.writelines('\n' + csvLine)
    f.flush()
    # clean up some variables
    del result
    del csvLine
    del servers
    del threads
    del s
    gc.collect()


runNumber = 0
# loop forever
while True:
    runNumber = runNumber + 1
    doTest(runNumber)

    print('sleeping for ' + str(secondsBetweenTests) + ' seconds')
    print(' ')
    time.sleep(secondsBetweenTests)
