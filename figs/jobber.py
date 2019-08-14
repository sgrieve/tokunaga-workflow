with open('job.sh') as j:
    job = j.readlines()

with open('build-figs.sh') as a:
    a.readline()
    commands = a.readlines()

job_name = job[3].strip()

for i, c in enumerate(commands):
    if len(c) > 1:
        job[-1] = c
        job[3] = job_name + str(i) + '\n'

        with open('job-{}.sh'.format(i), 'w') as w:
            for jb in job:
                w.write(jb)
