#IMPORTACOES
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import plotly.figure_factory as ff
import copy

#salva o caminho dos datasets
dataset_a = "a_an_example.in.txt"
dataset_b = "b_better_start_small.in.txt"
dataset_c = "c_collaboration.in.txt"
dataset_d = "d_dense_schedule.in.txt"
dataset_e = "e_exceptional_skills.in.txt"
dataset_f = "f_find_great_mentors.in.txt"

"""# Leitura dos dados"""

def read_dataset(file_path):
    test_dataset = {
        'contributors': {},
        'projects': {},
    }
    num_c = None
    num_p = None

    with open(file_path, 'r') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):

        if i==0:
          line = lines[i].strip().split()
          num_c = int(line[0])
          num_p = int(line[0])+int(line[1])

        elif i<=num_c:
            line = lines[i].strip().split()
            contributor_name = line[0]
            contributor_numSkills = int(line[1])

            test_dataset['contributors'][contributor_name] = {
                'name': contributor_name,
                'skills': [],
                'skillsByName': {},
                'availableAt' : 0,
                'works': 0
            }

            for j in range(contributor_numSkills):
              i += 1
              num_c+=1
              num_p+=1
              line = lines[i].strip().split()

              skills = {'name': line[0], 'level': int(line[1])}
              skillsBN = {line[0] : int(line[1])}
              test_dataset['contributors'][contributor_name]['skills'].append(skills)
              test_dataset['contributors'][contributor_name]['skillsByName'].update(skillsBN)


        elif i<=num_p:
            line = lines[i].strip().split()
            project_name = line[0]
            project_numSkills = int(line[4])

            test_dataset['projects'][project_name] = {
                'name': project_name,
                'days': int(line[1]),
                'score': int(line[2]),
                'bestBefore': int(line[3]),
                'roles': [],
                'rolesByName': {}
            }

            for j in range(project_numSkills):
              i += 1
              num_c+=1
              num_p+=1
              line = lines[i].strip().split()

              roles = {'name': line[0], 'levelRequired': int(line[1])}
              rolesBN = {line[0] : int(line[1])}
              test_dataset['projects'][project_name]['roles'].append(roles)
              test_dataset['projects'][project_name]['rolesByName'].update(rolesBN)

        i += 1
    return test_dataset

dataset_A = read_dataset(dataset_a)
dataset_B = read_dataset(dataset_b)
dataset_C = read_dataset(dataset_c)
dataset_D = read_dataset(dataset_d)
dataset_E = read_dataset(dataset_e)
dataset_F = read_dataset(dataset_f)

"""# Solver"""

# Pega uma variável de conjunto de dados e retorna uma variável de solução
def solve(dataset, priority_order, contributor_order):
    plotx = [ 0 ]
    ploty = [ len(dataset['projects'].values()) ]
    for contributor in dataset['contributors'].values():
        contributor['availableAt'] = 0

    totalScore = 0
    lastDay = max(proj['bestBefore'] + proj['score'] for proj in dataset['projects'].values())

    solution = {'projects': []}
    selectedProjectNames = set()
    currentTime = 0
    projectOrder = []

    if(priority_order=="SPT"):
      for project in dataset['projects'].values():
        spt = project['days']
        projectOrder.append((spt, project['name']))
      projectOrder.sort(reverse=False)

    elif(priority_order=="LPT"):
      for project in dataset['projects'].values():
        spt = project['days']
        projectOrder.append((spt, project['name']))
      projectOrder.sort(reverse=True)

    elif(priority_order=="EDD"):
      for project in dataset['projects'].values():
        edd = project['bestBefore']
        projectOrder.append((edd, project['name']))
      projectOrder.sort(reverse=False)

    elif(priority_order=="MST"):
      for project in dataset['projects'].values():
        mst = max(0, project['days'] + project['bestBefore'])
        projectOrder.append((mst, project['name']))
      projectOrder.sort(reverse=False)

    elif(priority_order=="CR"):
      for project in dataset['projects'].values():
        cr = max(0, project['bestBefore'] // project['days'])
        projectOrder.append((cr, project['name']))
      projectOrder.sort(reverse=False)

    elif(priority_order=="SLACK"):
      for project in dataset['projects'].values():
        slack = max(0, project['bestBefore'] - currentTime - project['days'])
        projectOrder.append((slack, project['name']))
      projectOrder.sort(reverse=False)

    elif(priority_order=="MANPOWER"):
      for project in dataset['projects'].values():
        penalty = max(0, currentTime + project['days'] - project['bestBefore'])
        realScore = max(0, project['score'] - penalty)
        manpower = project['days'] * len(project['roles'])
        score = max(0, project['score'] - penalty) / manpower
        projectOrder.append((score, project['name']))
      projectOrder.sort(reverse=False)


    while True:
        projectScores = []
        for _, projectName in projectOrder:
            project = dataset['projects'][projectName]
            if project['name'] in selectedProjectNames:
                continue # não selecione um projeto duas vezes

            penalty = max(0, currentTime + project['days'] - project['bestBefore'])
            realScore = max(0, project['score'] - penalty)

            manpower = project['days'] * len(project['roles'])
            score = max(0, project['score'] - penalty) / manpower


            selectedPpl = []
            selectedContribs = set()
            rolesCanBeMentored = set()
            for roleDict in project['roles']:
                roleName = roleDict['name']
                roleLevel = roleDict['levelRequired']
                contribselect = []
                ordr = list(dataset['contributors'].values())
                random.shuffle(ordr)
                for contributor in ordr:
                  if(contributor_order=="First_to_find"):
                    if (contributor['availableAt'] <= currentTime and
                        contributor['name'] not in selectedContribs):
                        if (any(dataset['contributors'][nnn]['skillsByName'].get(roleName, 0) >= roleLevel for nnn in selectedPpl)
                            and contributor['skillsByName'].get(roleName, 0) == roleLevel - 1):
                            contribselect.append((500 - contributor['works'], contributor['name']))
                            break
                        elif contributor['skillsByName'].get(roleName, 0) == roleLevel:
                            contribselect.append((500 - contributor['works'], contributor['name']))
                        elif contributor['skillsByName'].get(roleName, 0) > roleLevel:
                            #contribselect.append((-sum(contributor['skillsByName'].values()), contributor['name']))
                            contribselect.append((  - contributor['works'] , contributor['name']))


                  elif(contributor_order=="Nearest"):
                    if (contributor['availableAt'] <= currentTime and
                        contributor['name'] not in selectedContribs):
                        if (any(dataset['contributors'][nnn]['skillsByName'].get(roleName, 0) >= roleLevel for nnn in selectedPpl)
                            and contributor['skillsByName'].get(roleName, 0) == roleLevel - 1):
                            contribselect.append((500-(roleLevel-contributor['skillsByName'].get(roleName, 0)), contributor['name']))
                        elif contributor['skillsByName'].get(roleName, 0) == roleLevel:
                            contribselect.append((500-(roleLevel-contributor['skillsByName'].get(roleName, 0)), contributor['name']))
                        elif contributor['skillsByName'].get(roleName, 0) > roleLevel:
                            contribselect.append((-sum(contributor['skillsByName'].values()), contributor['name']))

                  elif(contributor_order=="Farest"):
                    if (contributor['availableAt'] <= currentTime and
                        contributor['name'] not in selectedContribs):
                        if (any(dataset['contributors'][nnn]['skillsByName'].get(roleName, 0) >= roleLevel for nnn in selectedPpl)
                            and contributor['skillsByName'].get(roleName, 0) == roleLevel - 1):
                            contribselect.append((500+(roleLevel-contributor['skillsByName'].get(roleName, 0)), contributor['name']))
                        elif contributor['skillsByName'].get(roleName, 0) == roleLevel:
                            contribselect.append((500+(roleLevel-contributor['skillsByName'].get(roleName, 0)), contributor['name']))
                        elif contributor['skillsByName'].get(roleName, 0) > roleLevel:
                            contribselect.append((-sum(contributor['skillsByName'].values()), contributor['name']))

                if len(contribselect) == 0:
                    # Não encontrou um colaborador adequado nesta data
                    score = -1
                    break
                else:
                    bestContribScore, bestContribName = max(contribselect)
                    selectedPpl.append(bestContribName)
                    selectedContribs.add(bestContribName)

                    for role in project['roles']:
                        roleName = role['name']
                        roleLevel = role['levelRequired']
                        if dataset['contributors'][bestContribName]['skillsByName'].get(roleName,0) >= roleLevel:
                            rolesCanBeMentored.add(roleName)

            projectScores.append((score, realScore, project['name'], selectedPpl))
            if score > 0:
                # Encontrou uma pontuação válida
                # Como estamos verificando diminuindo a pontuação esperada, podemos quebrar agora
                break

        if(len(projectScores)!=0):
          bestScore, bestRealScore, bestProjectName, bestAlloc = max(projectScores)
          ##################################print(f'Melhor pontuacao do projeto: {bestScore:.2f} / {bestRealScore}. Total {totalScore}')
        else:
          bestScore, bestRealScore, bestProjectName, bestAlloc = (-1,-1,-1,-1)

        if bestScore > 0:
            totalScore += bestRealScore
            ##################################print(f"{len(dataset['projects']) - len(selectedProjectNames)} projetos faltantes.")
            bestProject = dataset['projects'][bestProjectName]
            for name, role in zip(bestAlloc, bestProject['roles']):
                contributor = dataset['contributors'][name]
                contributor['availableAt'] = currentTime + bestProject['days']
                contributor['works'] = contributor['works'] + 1

                # Level up
                contributorSkill = contributor['skillsByName'].get(role['name'], 0)
                if contributorSkill <= role['levelRequired']:
                    assert contributorSkill >= role['levelRequired'] - 1
                    contributor['skillsByName'][role['name']] = contributorSkill + 1

            projectSol = {
                'name': bestProjectName,
                'roles': bestAlloc,
                'startTime': currentTime
            }
            #print(projectSol)
            solution['projects'].append(projectSol)
            selectedProjectNames.add(bestProjectName)

        if bestScore <= 0:
            # Avance no tempo

            earliestStep = lastDay
            for contributor in dataset['contributors'].values():
                if contributor['availableAt'] > currentTime:
                    earliestStep = min(earliestStep, contributor['availableAt'])
            currentTime = earliestStep
            plotx.append(currentTime)
            ploty.append(len(dataset['projects']) - len(selectedProjectNames))
            ##################################print(f'Avança no tempo para {currentTime}/{lastDay}')
            if currentTime >= lastDay:
                break

    maxday = lastDay
    len_incompleted_projects = len(dataset['projects']) - len(selectedProjectNames)
    incompleted_projects = {key: value for key, value in dataset['projects'].items() if key not in selectedProjectNames}


    return incompleted_projects, maxday, solution, totalScore, plotx, ploty

"""# Impressão dos gráficos"""

def imprime(p_x, p_y):
    plt.figure(figsize=(20, 5))
    plt.bar([str(x) for x in p_x], p_y)
    plt.ylim(0, p_y[0])
    #plt.xlabel('X-axis Label')
    #plt.ylabel('Y-axis Label')
    #ax.margins(x=0)
    plt.title("Dia x Projetos Incompletos")
    plt.margins(x=0)
    plt.xticks(rotation=270)

    plt.show()


def plota_graficos(dataset, incompleted_projects, maxday, solution, totalScore, plotx, ploty, priority_order, contributor_order):
    trocas_c = 0
    trocas_p = 0
    for projectName in incompleted_projects:
        project = dataset['projects'][projectName]
        selectedPpl = []
        selectedContribs = set()
        rolesCanBeMentored = set()
        missing_roles = []
        for roleDict in project['roles']:
          roleName = roleDict['name']
          roleLevel = roleDict['levelRequired']
          contribselect = []
          ordr = list(dataset['contributors'].values())
          for contributor in ordr:
            if (contributor['name'] not in selectedContribs):
                if (any(dataset['contributors'][nnn]['skillsByName'].get(roleName, 0) >= roleLevel for nnn in selectedPpl)
                    and contributor['skillsByName'].get(roleName, 0) == roleLevel - 1):
                    contribselect.append((1000, contributor['name']))
                    break
                elif contributor['skillsByName'].get(roleName, 0) == roleLevel:
                    contribselect.append((500, contributor['name']))
                elif contributor['skillsByName'].get(roleName, 0) > roleLevel:
                    contribselect.append((-sum(contributor['skillsByName'].values()), contributor['name']))

          if len(contribselect) == 0:
              maximum = 0
              for contributor in ordr:
                if contributor['skillsByName'].get(roleName, 0) > maximum:
                  maximum = contributor['skillsByName'].get(roleName, 0)
              missing_roles.append((projectName, roleName, "roleLevel:", roleLevel, "max_value_found:", maximum))
              if (maximum>=roleLevel):
                trocas_c+=1
              else:
                trocas_p+=1
          else:
              bestContribScore, bestContribName = max(contribselect)
              selectedPpl.append(bestContribName)
              selectedContribs.add(bestContribName)

              for role in project['roles']:
                  roleName = role['name']
                  roleLevel = role['levelRequired']
                  if dataset['contributors'][bestContribName]['skillsByName'].get(roleName,0) >= roleLevel:
                      rolesCanBeMentored.add(roleName)
        print(len(missing_roles))
        for mr in missing_roles:
          print(mr)
    if(True):
      print("Poderia fazer", trocas_c, "trocas da ordem de contribuidores")
      print("Poderia fazer", trocas_p, "trocas da ordem dos projetos")
      xxx = []
      yyy = []
      ordr = list(dataset['contributors'].values())
      for contributor in ordr:
        xxx.append(contributor['name'])
        yyy.append(contributor['works'])

      plt.figure(figsize=(20, 5))
      plt.bar(xxx, yyy)
      #plt.ylim(0, p_y[0])
      #plt.xlabel('X-axis Label')
      #plt.ylabel('Y-axis Label')
      #ax.margins(x=0)
      plt.title("Numero de vezes que cada contribuidor foi selecionado para"+contributor_order)
      plt.margins(x=0)
      plt.xticks(rotation=270)

      plt.show()



##################################
##################################
##################################

datasets = [ read_dataset(dataset_b) ]
instance = [ "B" ]

solutions = []
scores = []

priority_order = [ "SPT", "LPT", "EDD", "MST", "CR", "SLACK", "MANPOWER"]

contributor_order = [ "First_to_find", "Nearest", "Farest"]

# for data, PO in zip(datasets, priority_order, strict=False):
for i in range(len(instance)):
  for j in priority_order:
    for k in contributor_order:
      ip, maxd, solution, totalScore, plotx, ploty = solve(datasets[i], j, k)
      solutions.append((ip, maxd, instance[i], k, j, totalScore))
      print((len(ip), maxd, instance[i], k, j, totalScore))
      imprime(plotx, ploty)
      plota_graficos(datasets[i], ip, maxd, solution, totalScore, plotx, ploty, j, k)

#for i in solutions:
#  print(i)

dataset_x = dataset_a
instance = "A"

priority_order = [ "SPT", "LPT", "EDD", "MST", "CR", "SLACK", "MANPOWER"]

contributor_order = [ "First_to_find", "Nearest", "Farest"]

num_times = 3

for _ in range(num_times):
    solutions = []
    for j in priority_order:
        for k in contributor_order:
            ip, maxd, solution, totalScore, plotx, ploty = solve(read_dataset(dataset_x), j, k)
            solutions.append((ip, maxd, read_dataset(dataset_x), k, j, totalScore))
            #print((len(ip), maxd, instance, k, j, totalScore))
            #imprime(plotx, ploty)
            #plota_graficos(datasets[i], ip, maxd, solution, totalScore, plotx, ploty, j, k)

    solutions.sort(key=lambda a: a[-1], reverse = True)
    for sol in solutions:
        print((len(sol[0]), sol[1], instance, sol[3], sol[4], sol[-1]))
    print()

dataset_x = dataset_b
instance = "B"

priority_order = [ "SPT", "LPT", "EDD", "MST", "CR", "SLACK", "MANPOWER"]

contributor_order = [ "First_to_find", "Nearest", "Farest"]

num_times = 3

for _ in range(num_times):
    solutions = []
    for j in priority_order:
        for k in contributor_order:
            ip, maxd, solution, totalScore, plotx, ploty = solve(read_dataset(dataset_x), j, k)
            solutions.append((ip, maxd, read_dataset(dataset_x), k, j, totalScore))
            #print((len(ip), maxd, instance, k, j, totalScore))
            #imprime(plotx, ploty)
            #plota_graficos(datasets[i], ip, maxd, solution, totalScore, plotx, ploty, j, k)

    solutions.sort(key=lambda a: a[-1], reverse = True)
    for sol in solutions:
        print((len(sol[0]), sol[1], instance, sol[3], sol[4], sol[-1]))
    print()

dataset_x = dataset_c
instance = "C"

priority_order = [ "SPT", "LPT", "EDD", "MST", "CR", "SLACK", "MANPOWER"]

contributor_order = [ "First_to_find", "Nearest", "Farest"]

num_times = 3

for _ in range(num_times):
    solutions = []
    for j in priority_order:
        for k in contributor_order:
            ip, maxd, solution, totalScore, plotx, ploty = solve(read_dataset(dataset_x), j, k)
            solutions.append((ip, maxd, read_dataset(dataset_x), k, j, totalScore))
            #print((len(ip), maxd, instance, k, j, totalScore))
            #imprime(plotx, ploty)
            #plota_graficos(datasets[i], ip, maxd, solution, totalScore, plotx, ploty, j, k)

    solutions.sort(key=lambda a: a[-1], reverse = True)
    for sol in solutions:
        print((len(sol[0]), sol[1], instance, sol[3], sol[4], sol[-1]))
    print()





