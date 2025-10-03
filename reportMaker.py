import csv

print("Report Maker")

def read_csv(filename):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        return list(reader)
def format_percent(value, useColor = True, invert = False):
    color = ('🔴 ' if value<0.0 else '🟢 ') if useColor else ''
    return color + "{:.1f}".format(value) + " %"


def gen_md_table(rows1, rows2, threshold, details):
    header = ['M','N','K','Speedup']
    if details:
        header+=['L2 hitrate diff','t1(us)', 't2(us)', 'TFlops/s']
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
        time_diff = 100.0*(t1-t2)/t1
        hit_rate_diff = 100.0*(tcc2-tcc1)/tcc1
        
        if (not filter or abs(time_diff)>threshold):
            r = [str(m),str(n),str(k), 
                format_percent(time_diff)
                ]
            if details:
                flops = m*n*k*2/t2/1e3
                r+=[format_percent(hit_rate_diff, False), str(t1),str(t2),"{:.0f}".format(flops)]

            print('| ' + ' | '.join(r) + ' |')

# file1 = read_csv('10_02_25_without_change_gfx950/summary_static_f16.csv')
# file2 = read_csv('10_02_25_with_change_gfx950/summary_static_f16.csv')
# file1 = read_csv('10_02_25_without_change_gfx950/summary_dynamic_f16.csv')
# file2 = read_csv('10_02_25_with_change_gfx950/summary_dynamic_f16.csv')

file1 = read_csv('10_02_25_without_change_gfx950/summary_dynamic_f8E4M3FN.csv')
file2 = read_csv('10_02_25_with_change_gfx950/summary_dynamic_f8E4M3FN.csv')


file1_16 = file1[:]
file2_16 = file2[:]

gen_md_table(file1_16,file2_16, threshold=0, details=True)
