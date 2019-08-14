with open('fails.txt') as fail:
    fails = fail.readlines()

fail_ids = []

for f in fails:
    fail_ids.append(f.split('.')[2].strip())

with open('reun_files_big.txt', 'w') as w:
    counter = 1
    with open('bigfiles.txt') as big:
        for b in big.readlines():
            if b.split(' ')[0] in fail_ids:
                w.write('{} {}'.format(counter, b.split(' ')[1]))
                counter += 1
