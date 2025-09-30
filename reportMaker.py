import csv

print("Report Maker")

def read_csv(filename):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        return list(reader)
def format_percent(value, useColor = True):
    color = ('🔴 ' if value>0.0 else '🟢 ') if useColor else ''
    return color + "{:.1f}".format(value) + " %"


def gen_md_table(rows1, rows2, threshold, details):
    header = ['M','N','K','L2 hitrate diff','time diff']
    if details:
        header+=['t1', 't2', 'flops']
    print('| ' + ' | '.join(header) + ' |')
    print('| ' + ' | '.join(['---'] * len(header)) + ' |')
    for index in range(len(rows1)):
        r1 = rows1[index]
        r2 = rows2[index]
        m = int(r1.get('M', ''))
        n = int(r1.get('N', ''))
        k = int(r1.get('K', ''))
        t2 = float(r2.get('time_ns',0))
        t1 = float(r1.get('time_ns',0))
        tcc2 = float(r2.get('TCC_HIT_RATE',0))
        tcc1 = float(r1.get('TCC_HIT_RATE',0))
        time_diff = 100.0*(t2-t1)/t1
        hit_rate_diff = 100.0*(tcc2-tcc1)/tcc1
        
        if (not filter or abs(time_diff)>threshold):
            r = [str(m),str(n),str(k), 
                format_percent(hit_rate_diff, False),
                format_percent(time_diff)
                ]
            if details:
                flops = m*n*k*2/t2/1e3
                r+=[str(t1),str(t2),"{:.0f}".format(flops)]

            print('| ' + ' | '.join(r) + ' |')

file1 = read_csv('file1.csv')
file2 = read_csv('file2.csv')

file1_16 = file1[:]
file2_16 = file2[:]

gen_md_table(file1_16,file2_16, threshold=8, details=False)
