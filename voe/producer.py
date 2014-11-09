companies = ['gol', 'azul']

gol_airports = ['SDU', 'CGH', 'GRU', 'REC', 'POA', 'BSB', 'CNF']
gol_block = [('SDU', 'GIG'), ('CGH', 'GRU'), ('SDU', 'GRU'), ('GIG', 'CGH')]

azul_airports = ['GIG', 'REC', 'GRU']
azul_airports = []
azul_block = []

companies_airports = {'gol': gol_airports, 'azul': azul_airports}
companies_blocks = {'gol': gol_block, 'azul': []}

def get_tasks():
    tasks = []
    for company in companies:
        done = []
        airports = companies_airports[company]
        block = companies_blocks[company]
        for from_airport in airports:
            for to_airport in airports:
                if from_airport == to_airport:
                    continue
                if (from_airport, to_airport) in block or \
                   (to_airport, from_airport) in block:
                    continue

                line = (from_airport, to_airport)
                if line in done:
                    continue

                task_definition = "{} {} {}".format(company, from_airport,
                                                    to_airport)
                done.append(line)
                done.append(line[::-1])
                tasks.append(task_definition)

    return tasks
