import csv
import copy
import numpy as np
from random import random, sample, choice
import os
import random
import schedule_improvement as aco2
import time
import numpy as np

import numpy as np
import pandas as pd
c=[]
c1=[]
tt1 = time.time()

nd_activity_num=120
duration=[]
rsl=[]
rc=[]
pa=[]
d=[]
activity=[]
cities=[]
popm = 1
total_schedule = 5000
def clean():
    global c,c1,duration,rsl,rc,pa,d,activity,cities,popm
    c = []
    c1 = []
    duration = []
    rsl = []
    rc = []
    pa = []
    d = []
    activity = []
    cities = []
    popm = 1


def convertdayplantoactschedule(d):
    def sortsecond(a):
        return a[1]
    c = list(range(len(duration)))
    c = np.array(c) + 1
    c = list(c)
    e = list(zip(c, d))
    # print(e)
    e.sort(key=sortsecond)
    temppopulation = []
    for i in range(len(e)):
        temppopulation.append(e[i][0])
    return temppopulation


def detectviloation(x):
    violation = 0
    for i in range(len(x)):
        if list(set(pa[x[i] - 1]) & set(x[i:])) == []:
            continue
        else:
            violation = violation + 1
    return violation

def detectviloation1(x):
    violation = 0
    for i in range(len(x)):
        if list(set(pa[x[i] - 1]) & set(x[i:])) == []:
            continue
        else:
            violation = violation + 1
            break
    return violation

def verifysequence(a):
    b = a
    for i in range(len(a)):
        if list(set(pa[a[i] - 1]) & set(a[i:])) == []:
            continue
        else:
            s = list(set(pa[a[i] - 1]) & set(a[i:]))
            s1 = choice(s)
            temp = a[i]
            s2 = a.index(s1)
            b[i] = s1
            b[s2] = temp
    return b


def feasiblesequnce(b):
    vi = detectviloation(b)
    while vi != 0:
        b = verifysequence(b)
        vi = detectviloation(b)
    return b


def h(x):
    if x >= 0:
        return 1
    else:
        return 0






def constraint(ind, x, alb, aub, rsl):
    t2 = list(range(aub + 1))
    t3 = np.array(t2)
    t4 = t3[alb:]
    # print("t4",t4)
    sumd10 = []

    for i in t4:
        d0 = []
        for j in range(len(ind)):
            # print(rc[x[j] - 1][0])
            d0.append(   (h(i - ind[j]) - h(i - ind[j] - duration[x[j] - 1]))    * ( rc[x[j] - 1][0]) )  # zero reprents  the first resource constraint
        # print("d0",d0)
        sumd10.append(sum(d0))
    # print(sumd13)
    # print(np.array(sumd10)-1)
    d00 = []
    # print(np.array(sumd13))
    for k in (np.array(sumd10) - rsl[0]):
        if k > 0:
            d00.append(k)

    sumd11 = []
    for i in t4:
        d1 = []
        for j in range(len(ind)):
            d1.append((h(i - ind[j]) - h(i - ind[j] - duration[x[j] - 1])) * (
                rc[x[j] - 1][1]))  # zero reprents  the first resource constraint
        # print("d3",d3)
        sumd11.append(sum(d1))
    # print(sumd13)
    # print(np.array(sumd10)-1)
    d01 = []
    # print(np.array(sumd13))
    for k in (np.array(sumd11) - rsl[1]):
        if k > 0:
            # print(i)
            d01.append(k)

    sumd12 = []
    for i in t4:
        d2 = []
        for j in range(len(ind)):
            d2.append((h(i - ind[j]) - h(i - ind[j] - duration[x[j] - 1])) * (
                rc[x[j] - 1][2]))  # zero reprents  the first resource constraint
        # print("d3",d3)
        sumd12.append(sum(d2))
    # print(sumd13)
    # print(np.array(sumd10)-1)
    d02 = []
    # print(np.array(sumd13))
    for k in (np.array(sumd12) - rsl[2]):
        if k > 0:
            # print(i)
            d02.append(k)

    sumd13 = []
    for i in t4:
        d3 = []
        for j in range(len(ind)):
            d3.append((h(i - ind[j]) - h(i - ind[j] - duration[x[j] - 1])) * (
                rc[x[j] - 1][3]))  # zero reprents  the first resource constraint
        sumd13.append(sum(d3))
    d03 = []
    for k in (np.array(sumd13) - rsl[3]):
        if k > 0:
            d03.append(k)
    tsum = (sum(d00) + sum(d01) + sum(d02) + sum(d03))
    return tsum


def settingdate(b4):
    print("ssgs possible....",b4)
    actes = np.zeros(len(duration), int)
    parallel = []
    successor = []
    for i in range(len(duration)):
        if i == 0:
            actes[i] = 0
        else:
            if b4[i - 1] in pa[b4[i] - 1]:
                ta = list((b4[i - 1], b4[i]))
                successor.append(ta)
                paact = []
                for o1 in b4[:i + 1]:
                    if o1 in pa[b4[i] - 1]:
                        paact.append(o1)
                paact1 = []
                ind = []
                tempb4 = b4[:i + 1]
                for m1 in range(len(tempb4)):
                    ind.append(actes[b4.index(tempb4[m1])])
                for o2 in range(len(paact)):
                    paact1.append(ind[b4.index(paact[o2])] + duration[paact[o2] - 1])
                # print("paact1",paact1)
                paalb = max(paact1)
                tempb4 = b4[:i]
                # print("tempb4", tempb4)
                tempaub = []
                for k in range(len(tempb4)):
                    # print("ssss",b4.index(tempb4[k]))
                    # print("sss",actef[b4.index(tempb4[k])])
                    tempaub.append(actes[b4.index(tempb4[k])] + duration[(tempb4[k]) - 1])
                aub = max(tempaub)
                # ind = []
                # for m1 in range(len(tempb4)):
                # ind.append(actes[b4.index(tempb4[m1])])
                ind[i] = paalb
                # print("ind", ind)
                alb1 = paalb
                # print(i, "alb1", alb1)
                while constraint(ind, b4[:i + 1], paalb, aub, rsl) != 0:
                    alb1 = alb1 + 1
                    ind[i] = alb1
                    actes[i] = alb1
                # print("again", alb1)
                for n1 in range(len(ind)):
                    actes[n1] = ind[n1]

            else:
                # print("parallel",b4[i-1],b4[i])
                ta = list((b4[i - 1], b4[i]))
                # print("ta",ta)
                parallel.append(ta)
                tempalb = []
                for j in range(len(pa[b4[i] - 1])):
                    # print("ss",pa[b4[i]-1][j])
                    if pa[b4[i] - 1][j] == 0:
                        alb = 0
                    else:
                        # print("testindex",b4.index(pa[b4[i]-1][j]))
                        # print(actes[b4.index(pa[b4[i]-1][j])])
                        # print([b4.index(pa[b4[i]-1][j])])
                        tempalb.append(actes[b4.index(pa[b4[i] - 1][j])] + duration[b4[b4.index(pa[b4[i] - 1][j])] - 1])
                if len(tempalb) == 0:
                    alb = 0
                else:
                    alb = max(tempalb)
                # print("alb",alb)
                tempb4 = b4[:i + 1]
                # print("tempb4",tempb4)
                tempaub = []
                for k in range(len(tempb4)):
                    # print("ssss",b4.index(tempb4[k]))
                    # print("sss",actef[b4.index(tempb4[k])])
                    tempaub.append(actes[b4.index(tempb4[k])] + duration[(tempb4[k]) - 1])
                aub = max(tempaub)
                # print("sy",alb,aub)
                # print("i",i,tempb4)
                ind = []
                for m in range(len(tempb4)):
                    ind.append(actes[b4.index(tempb4[m])])
                ind[i] = alb
                # print("ind",ind)
                alb1 = alb
                # print(i,"alb1",alb1)
                while constraint(ind, b4[:i + 1], alb, aub, rsl) != 0:
                    alb1 = alb1 + 1
                    ind[i] = alb1
                    actes[i] = alb1
                # print("again",alb1)
                for n in range(len(ind)):
                    actes[n] = ind[n]
    return list(actes)


def converttodayplan(d, actsch):
    def sortsecond(a):
        return a[1]

    e = list(zip(d, actsch))
    # print(e)
    e.sort(key=sortsecond)
    temppopulation = []
    for i in range(len(e)):
        temppopulation.append(e[i][0])
    return temppopulation


def transfer(ind):
    b4 = ind
    b4act = convertdayplantoactschedule(b4)
    # print("b4",b4)
    # print("b4act",b4act)
    b4fact = feasiblesequnce(b4act)
    # print("b4actfea",b4act)

    # print("b4fact",b4fact)
    b4date = settingdate(b4fact)
    # print("b4date",b4date)
    ind11 = converttodayplan(b4date, b4fact)
    # print(ind11)
    return ind11, b4fact


def schedule_transger_date(mutationunit):
    print(mutationunit)
    mutationunit = feasiblesequnce(mutationunit)
    b4date = settingdate(mutationunit)
    # print(b4date)
    ind11 = converttodayplan(b4date, mutationunit)
    return ind11


def pc(ind):  # use to replace pc constraints.

    for i in range(len(ind)):
        if  ind[i] <0:
            ind[i]=0
        else:
            ind[i] = int(ind[i])
    for i in range(len(pa)):
        for j in range(len(pa[i])):
            tempv = ind[i]
            if pa[i][j] == 0:
                ind[i] =tempv
            if pa[i][j] != 0:
                if ind[i] <= ind[pa[i][j] - 1] + duration[pa[i][j] - 1]:
                    ind[i] = ind[pa[i][j] - 1] + duration[pa[i][j] - 1]
    return ind


def h(x):
    if x >= 0:
        return 1
    else:
        return 0

def rsconstraint(ind):
    t2 = max(list(np.array(ind) + np.array(duration)))
    pc(ind)
    # print("t2",t2)
    tsum = constraint(ind, cities, 0, t2, rsl)

    return tsum


def schedule(ind):
    #pc(ind)
    t2 = ind[-1]
    #max(list(np.array(ind) + np.array(duration)))
    #t2 = t2 + rsconstraint(ind)

    return t2


def genind():
    offspring = []
    for kk in range(len(duration)):
        ad1=int(np.random.uniform(0, sum(duration) - duration[kk]))
        offspring.append(ad1)

    offspring[0] = 0
    # print(offspring)
    pc(offspring)

    # offspring=transfer(offspring)
    return offspring


def correctind(x):
    tempk = []
    for j2 in range(len(x)):
        if x[j2] == "NaN":
            x[j2] = 0
        if x[j2] < 0:
            x[j2] = 0
        if x[j2] > sum(duration):
            x[j2] = sum(duration) - duration[j2]
        tempk.append(int(x[j2]))
    tempk[np.argmin(tempk)] = 0
    pc(tempk)
    return tempk


def genpop():
    population = []
    for i in range(popm):  # this number is important
        entity = genind()
        population.append(entity)
    return population




def fitness(population, schedule):
    v1 = []
    for i in range(len(population)):
        v1.append(schedule(population[i]))
    return v1


t3 = []


def compare(x1, x2):
    if schedule(x1) < schedule(x2):
        x1 = x1
    else:
        x1 = x2
    return x1


def multi():
    mult = []
    for i in range(len(duration)):
        mult.append(choice([-1, 1]))
    return mult


def chaos():
    x = 0.298
    chaosequence = []
    for i in range(10000):
        x = 4 * x * (1 - x)
        chaosequence.append(x)
    return chaosequence


chaosequence = chaos()


def genrand():
    randnum = sample(chaosequence, len(duration))
    return randnum


upbound = []
for i in range(len(duration)):
    upbound.append(sum(duration) - duration[i])


def mutation():
    x2 = list(np.array(upbound) * np.array(genrand()))
    x2 = correctind(x2)
    # x2=transfer(x2)
    return x2



def correctind(x):
    tempk = []
    for j2 in range(len(x)):
        if x[j2] == "NaN":
            x[j2] = 0
        if x[j2] < 0:
            x[j2] = 0
        if x[j2] > sum(duration):
            x[j2] = sum(duration) - duration[j2]
        tempk.append(int(x[j2]))
    pc(tempk)
    return tempk


def crossover(x1, x3):
    rand = genrand()
    x1son1 = list(np.array(x1) - rand * (np.array(x1) - x3))
    x1son2 = list(np.array(x3) + rand * (np.array(x1) - x3))
    x1son1 = correctind(x1son1)
    x1son2 = correctind(x1son2)
    x1 = compare(x1, x1son1)
    x1 = compare(x1, x1son2)
    return x1


def bestcount(t3):
    n = 0
    for i in t3:
        if i == min(t3):
            n = n + 1
    return n


def sortsecond(a):
    return a[1]


def paixu(population):
    # print("selectpopu",population)
    value1 = fitness(population, schedule)
    # print(value1)
    a = list(zip(population, value1))
    a.sort(key=sortsecond)
    temppopulation = []
    for i in range(len(a)):
        temppopulation.append(a[i][0])
    return temppopulation


def selection(population):
    # print("selectpopu",population)
    value1 = fitness(population, schedule)
    a = list(zip(population, value1))
    a.sort(key=sortsecond)
    temppopulation = []
    for i in range(len(a)):
        temppopulation.append(a[i][0])
    populationsort = temppopulation[:3]
    #populationsort=populationsort+temppopulation[-1:]
    # populationsort=populationsort

    # print("selectpopusort",populationsort)
    return populationsort

def selection1(population):
    #print("selectpopu",population)
    value1 = fitness(population, schedule)
    a = list(zip(population, value1))
    a.sort(key=sortsecond)
    temppopulation = []
    for i in range(len(a)):
        temppopulation.append(a[i][0])
    populationsort = temppopulation[:popm]
    populationsort=populationsort+temppopulation[-1:]
    # populationsort=populationsort

    #print("selectpopusort",populationsort)
    return populationsort

def stardardact(population, xbest):
    n = 1
    population[-n], tempp = transfer(population[-n])
    while schedule(population[-n]) >= schedule(xbest):
        n = n + 1
        population[-n], tempp = transfer(population[-n])
        if n == 3:
            break
    return population


def correctomit(ind):
    citycopy = copy.deepcopy(cities)
    for i in range(len(ind)):
        for j in range(len(ind)):
            if ind[i] == citycopy[j]:
                citycopy[j] = 0
    citycopy1 = []
    for k in citycopy:
        if k != 0:
            citycopy1.append(k)
    citycopy = citycopy1
    for g in range(len(cities)):
        n = 0
        for e in range(len(ind)):
            if ind[e] == cities[g]:
                n = n + 1
                if n >= 2:
                    tempva = choice(citycopy)
                    ind[e] = tempva
                    citycopy.remove(tempva)
    return ind
def sosmutation(x):
    k = copy.deepcopy(x)
    posi1 = sample(cities, 2)
    # print(posi1)
    posi1 = list(np.array(posi1) - 1)
    # print(posi1)
    k4 = copy.deepcopy(k)
    k4[posi1[0]] = k[posi1[1]]
    k4[posi1[1]] = k[posi1[0]]
    return k4


def actforwardonestep(x):
    k = copy.deepcopy(x)
    posi1 = sample(cities, 2)
    # print(posi1)
    posi1 = list(np.array(posi1) - 1)
    # print(posi1)
    k4 = copy.deepcopy(k)
    k4[posi1[0]] = k[posi1[1]]
    k4[posi1[1]] = k[posi1[0]]
    k4 = feasiblesequnce(k4)
    return k4
def mutatiaontimes(x, n):
    tempmut = copy.deepcopy(x)
    for i in range(n):
        tempmut = minus1day(tempmut)
    return tempmut

def hunpairealnumber(x):
    xiao = int(np.random.uniform(2, len(duration) - 3))
    mid=int(np.random.uniform(xiao+1, len(duration) - 2))
    z0=x[xiao:mid]    #print("z0",z0)
    z=copy.deepcopy(z0)
    random.shuffle(z)
    if z0==x[xiao:mid]:
        son1 = x[:xiao] + z + x[mid:]
    pc(son1)
    return son1

def swap(x):
    xiao = int(np.random.uniform(2, len(duration) - 3))
    #print("xiao",xiao)
    da=int(np.random.uniform(xiao, len(duration) - 2))
    #print("da",da)
    position=int(np.random.uniform(1, min(len(duration) - da,da-xiao)))
    #print("position",position)
    son1 = x[:xiao] + x[da:da+position] + x[xiao+position:da] + x[xiao:xiao+position]+x[da+position:]
    #print("len",len(son1))
    pc(son1)
    return son1
def swap_activity(x):
    xiao = int(np.random.uniform(2, len(duration) - 3))
    #print("xiao",xiao)
    da=int(np.random.uniform(xiao, len(duration) - 2))
    #print("da",da)
    position=int(np.random.uniform(1, min(len(duration) - da,da-xiao)))
    #print("position",position)
    son1 = x[:xiao] + x[da:da+position] + x[xiao+position:da] + x[xiao:xiao+position]+x[da+position:]
    #print("len",len(son1))
    son1=feasiblesequnce(son1)
    return son1


def soscrossover(x):
    newpopulation = []
    # print("len(x)",len(x))
    for i in range(len(x)):
        p1 =x[i]
        p2 = sample(x, 1)[0]
        # print("p2",p2)
        while p2 == p1:
            #p2=choice(randomwalkgroup(p1))
            if np.random.uniform()<0.9:
                p2 = twopont_realnumbcross(p2)
                #p2 = randomwalkgroup(p1)
                #p2=threepoint_realnumbcross(p1)
                #p2=gagenind()
            else:
                #p2= hunpai_realnumber(p1)
                p2 = choice([swap(p2),genind(),hunpai_realnumber(p2),threepoint_realnumbcross(p2)])
                #p2 = swap(p1)
        randpos = choice(cities) - 1
        son1 = p1[:randpos] + p2[randpos:]
        son2 = p2[:randpos] + p1[randpos:]
        son3 = hunpai_realnumber(p1)
        son4=threepoint_realnumbcross(p1)
        son5=twopont_realnumbcross(p1)
        pc(son5)
        #son4 = p1[randpos:] + p2[:randpos]
        pc(son1)
        pc(son2)
        #pc(son3)
        #pc(son4)
        newpopulation.append(p1)
        newpopulation.append(son1)
        newpopulation.append(son2)
        z=minus1day(p1)
        pc(z)
        newpopulation.append(minus1day(z))
        newpopulation.append(son3)
        newpopulation.append(son4)
        newpopulation.append(son5)
        p3=swap(p1)
        newpopulation.append(p3)
        # print("sum_newpopulation",len(newpopulation))
    return newpopulation


def mutationalternative(x):
    xiao = np.random.randint(2, int(len(cities) - 1) / 3)
    da = np.random.randint(xiao, len(cities) - 1)
    son1 = x[:xiao] + x[da:] + x[xiao:da]
    son1 = correctomit(son1)
    son1 = feasiblesequnce(son1)
    return son1


def oneplusonecrossover(x1, x2):
    z=[]
    a=2
    n=choice([6])
    for i in range(n):
        a = int(np.random.uniform(a, len(duration) / n*(i+1)))
        z.append(a)
        a=len(duration) / n*(i+1)
    #low=int(np.random.uniform(2,len(duration)/3))
    #mid=int(np.random.uniform(len(duration)/3,len(duration)/3*2))
    #high=int(np.random.uniform(len(duration)/3*2,len(duration)))
    #print("Z",z)
    randpos = choice(z)
    son1 = x1[:randpos] + x2[randpos:]
    son1 = correctomit(son1)
    son1 = feasiblesequnce(son1)
    son2 = x2[:randpos] + x1[randpos:]
    son2 = correctomit(son2)
    son2 = feasiblesequnce(son2)

    return son1,son2


def redundentmove(population):
    repop = copy.deepcopy(population)
    for i in repop:
        c = 0
        for j in population:
            if i == j:
                c = c + 1
                if c >= 2:
                    population.remove(j)
    repop = population
    #while len(repop) <= popm:
        # print("removelen", len(population))
    #    repop.append(genind())
    pop = repop
    return pop
def redundentmove_ga(population):
    repop = copy.deepcopy(population)
    for i in repop:
        c = 0
        for j in population:
            if i == j:
                c = c + 1
                if c >= 2:
                    population.remove(j)
    repop = population
    #while len(repop) <= popm:
        # print("removelen", len(population))
    #    repop.append(genind())
    pop = repop
    return pop

def redundentvaluemove(population):
    v = fitness(population, schedule)
    z = list(zip(v, population))
    # print("z",z)
    repop = copy.deepcopy(v)
    for i in repop:
        c = 0
        for j in z:
            if i == j[0]:
                c = c + 1
                if c >= 2:
                    z.remove(j)
    # print("z", z)
    repop = []
    for k in range(len(z)):
        repop.append(z[k][1])
    # print(repop)
    #while len(repop) <= 2:
        # print("removelen", len(population))
     #   repop.append(genind())
    pop = repop
    return pop

def redundentvaluemove_ga(population):
    v = fitness(population, schedule)
    z = list(zip(v, population))
    # print("z",z)
    repop = copy.deepcopy(v)
    for i in repop:
        c = 0
        for j in z:
            if i == j[0]:
                c = c + 1
                if c >= 2:
                    z.remove(j)
    # print("z", z)
    repop = []
    for k in range(len(z)):
        repop.append(z[k][1])
    # print(repop)
    #while len(repop) <= popm:
        # print("removelen", len(population))
    #    repop.append(genind())
    pop = repop
    return pop

def gamutation(x):
    k0 = copy.deepcopy(x[0])
    gamunewpopulation = []
    for i in range(len(x)):
        k = copy.deepcopy(x[i])
        if np.random.uniform() < 1:
            posi1 = sample(cities, 2)
            # print(posi1)
            posi1 = list(np.array(posi1) - 1)
            # print(posi1)
            k4 = copy.deepcopy(k)
            k4[posi1[0]] = k[posi1[1]]
            k4[posi1[1]] = k[posi1[0]]
            k4 = hunpai(k4)
        else:
            k4 = hunpai(k)
        k4 = feasiblesequnce(k4)
        gamunewpopulation.append(k4)
    #gamunewpopulation.insert(0,k0)
    return gamunewpopulation




def date_transfer_schedule(ind):
    cind=copy.deepcopy(ind)
    for i in range(len(ind)):
        cind[i]=ind[i]+np.random.uniform(0,1)
    b4 = cind
    b41 = convertdayplantoactschedule(b4)
    b42 = feasiblesequnce(b41)
    return b42

def groupedate_to_groupschedule(population):
    schedulegroup = []
    for i in range(len(population)):
        schedulegroup.append(date_transfer_schedule(population[i]))

    return schedulegroup


def schedule_make_kid(parentpop):
    kid = gamutation(parentpop)
    return kid


def killbad(y1, y2):
    y = compare(y1, y2)
    return y


def isos(population):
    xbest = population[0]
    for j in range(len(population)):
        tempx = list(range(len(population)))
        tempx2 = choice(tempx)
        x1 = copy.deepcopy(population[j])
        while tempx2 == j or tempx2 == 0:
            tempx2 = choice(tempx)
            # print("yun")
        x2 = copy.deepcopy(population[tempx2])
        # one king rule
        rand = genrand()
        x1new1 = list(np.array(x1) + rand * (np.array(xbest) - x2))
        x2new1 = list(np.array(x2) + rand * (np.array(xbest) - x1))
        x1new1 = correctind(x1new1)
        x2new1 = correctind(x2new1)
        x1 = compare(x1, x1new1)
        x2 = compare(x2, x2new1)
        # xmin1=minus1day(x1)
        # x1 = compare(x1, xmin1)
        # x1min2=minvaluesubstitute(x1,x2)
        # x1=compare(x1,x1min2)
        # xmin2=minus1day(x2)
        # x2 = compare(x2, xmin2)

        # mutualism
        # print("use",use)
        muturalvector = (np.array(x1) + np.array(x2)) / 2
        bf = choice([1, 2])
        # bf=max([schedule(x1) / schedule(xbest), schedule(x2) / schedule(xbest)])
        # bf = choice([schedule(x1)/schedule(xbest), schedule(x2)/schedule(xbest)]) # adjust search step according to the weight
        rand = 1 - 0.5 * (1 + np.array(genrand()))
        # rand = genrand()
        x1new2 = list(np.array(x1) + rand * (np.array(xbest) - muturalvector * bf))
        x2new2 = list(np.array(x2) + rand * (np.array(xbest) - muturalvector * bf))
        x1new2 = correctind(x1new2)
        x2new2 = correctind(x2new2)
        x1 = compare(x1, x1new2)
        x2 = compare(x2, x2new2)

        # xmin1=minus1day(x1)
        # x1 = compare(x1, xmin1)
        # xmin2=minus1day(x2)
        # x2 = compare(x2, xmin2)
        population[tempx2] = x2
        # commensalism-

        tempx3 = choice(tempx)
        while tempx3 == j or tempx3 == 0 or tempx3 == tempx2:
            tempx3 = choice(tempx)
            # print("yun1")
        x3 = np.array(population[tempx3])
        rand = 1 - 0.5 * (1 + np.array(genrand()))
        # rand=genrand()
        x1newcom = list(np.array(x1) + np.array(choice([-1, 1])) * rand * (np.array(xbest) - x3))
        x1newcom = correctind(x1newcom)
        x1 = compare(x1, x1newcom)
        # xmin1=minus1day(x1)
        # x1 = compare(x1, xmin1)

        # population[j] = x1
        # mutation
        tempx4 = choice(tempx)
        while tempx4 == j:
            tempx4 = choice(tempx)
            # print("yun2")
        x4 = copy.deepcopy(population[tempx4])
        x4para = mutation()
        x4 = compare(x4, x4para)
        # xmin4=minus1day(x4)
        # x4 = compare(x4, xmin4)
        population[tempx4] = x4
        # population[tempx4]=transfer(population[tempx4])
        # rand=genrand()
        population[j] = x1
    return population




def forgacrossover(populationsort):
    newpopulation = []
    p0= copy.deepcopy(populationsort[0])
    populationsort=redundentmove_ga(populationsort)
    if len(populationsort)==1:
        print("alarm")
        for j in range(5):
            populationsort.insert(1,hunpai(p0))
    for i in range(len(populationsort)):
        p1 = populationsort[i]
        p2 = sample(populationsort, 1)[0]
        son1, son2 = pmxcrossover(p1, p2)
        newpopulation.append(p1)
        newpopulation.append(p2)
        newpopulation.append(son1)
        newpopulation.append(son2)
    return newpopulation

def forgacrossover_realvalue(populationsort):
    newpopulation = []
    p0= copy.deepcopy(populationsort[0])
    populationsort=redundentmove_ga(populationsort)
    if len(populationsort)==1:
        print("alarm")
        for j in range(1):
            populationsort.insert(1,aco2_instance.search_path(date_transfer_schedule(genind())))
    for i in range(len(populationsort)):
        p1 = populationsort[i]
        p2 = sample(populationsort, 1)[0]
        newpopulation +=crossover_mutation_forrealvalue(p1,p2)
    return newpopulation

def bestcount(t3):
    n = 0
    for i in t3:
        if i == min(t3):
            n = n + 1
    return n


def forgaselection(x):
    # print("selectpopu",population)
    value1 = fitness(x, schedule)
    a = list(zip(x, value1))
    a.sort(key=sortsecond)
    temppopulation = []
    for i in range(len(a)):
        temppopulation.append(a[i][0])
    temppopulation=redundentmove(temppopulation)
    if len(temppopulation)>5:
        populationsort = temppopulation[:5]#+temppopulation[-2:]
        #populationsort.insert(2,aco2_instance.search_path(date_transfer_schedule(genind())))
    else:
        z=len(temppopulation)
        populationsort = temppopulation
        for j in range(5-z):
            populationsort.append(aco2_instance.search_path(date_transfer_schedule(genind())))
    # print("selectpopusort",populationsort)
    return populationsort

def crossover_mutation_forrealvalue(s, s1):
    mutationgroupopt = []
    chang1 = choice(range((len(s) - 1)))
    chang2 = int(np.random.uniform(chang1, len(s)))
    mutationgroupopt.append(s)
    mutationgroupopt.append(s1)
    son2 = s1[:chang1] + s[chang1:chang2]+s1[chang2:]
    s2 = aco2_instance.search_path(date_transfer_schedule(son2))
    mutationgroupopt.append(s2)

    #mutation buyao kankan

    #chang3 = max(1,choice(range(len(s2) - 1)))
    #b=int(np.random.uniform(0,s2[chang3]))
    #s3=copy.deepcopy(s2)
    #if np.random.uniform()<=1:
    #    s3[chang3]=s3[chang3]-b
    #s3=aco2_instance.search_path(date_transfer_schedule(s3))
    #mutationgroupopt.append(s3)
    return  mutationgroupopt

def purega_realvalue(winner,y):
    y=forgaselection(y)
    extragroup =y    #print("pgay",len(y))
    gatime=time.time()
    t1=[]
    t2=[]
    for i in range(1000):
        x1=forgacrossover_realvalue(extragroup)
        #print("pgax11", len(x1))
        extragroup = forgaselection(x1)
        v = fitness(extragroup, schedule)
        t1.append(extragroup[0])
        t2.append(min(t1))
        countbest = bestcount(t2)
        print("purega_realvalue",v)
        if v[0]<=opm or countbest>30:
            #print("finish")
            break
    return extragroup[0]
def purega(y):
    #y=forgaselection(y)
    extragroup = []
    for p0 in range(len(y)):
        extragroup.append(date_transfer_schedule(y[p0]))
    #print("pgay",len(y))
    #gatime=time.time()
    t1=[]
    t2=[]
    for i in range(1):
        x1=forgacrossover(extragroup)
        #print("pgax1",len(x1))
        x0=gamutation(x1)
        x1=x1+x0
        #print("pgax11", len(x1))
        x1=redundentmove(x1)
        x3=antistandardgroup(x1)
        #x3=redundentmove(x3)
        x4 = forgaselection(x3)
        #v = fitness(x4, schedule)
        #t1.append(x4[0])
        #t2.append(min(t1))
        #countbest = bestcount(t2)
        #print("purega",v)
        #x5=[]
        #for j in range(len(x4)):
        #    x5.append(date_transfer_schedule(x4[j]))
        #extragroup=x5

        #if v[0]<=opm or countbest>30:
            #print("finish")
        #    break
    return x4


def cgamutation(s):
    q1 = random.randint(1, nd_activity_num - 1)
    q2 = random.randint(q1, nd_activity_num)
    son2 = s[:q1] + s[q2:]+s[q1:q2]
    q1 = random.randint(1, nd_activity_num - 1)
    q2 = random.randint(q1, nd_activity_num)
    son3 = son2[:q1] + s[q1:q2] + son2[q2:]
    pc(son2)
    son2 = aco2_instance.search_path(date_transfer_schedule(son2))
    pc(son3)
    son3 = aco2_instance.search_path(date_transfer_schedule(son3))
    lt=[]
    lt.append(son2)
    lt.append(son3)
    return lt



def schedule_transger_date(mutationunit):
    mutationunit = feasiblesequnce(mutationunit)
    b4date = settingdate(mutationunit)
    # print(b4date)
    ind11 = converttodayplan(b4date, mutationunit)

    return ind11


def twopont_realnumbcross(x):
    xiao = int(np.random.uniform(2, len(duration) - 1))
    da = int(np.random.uniform(xiao, len(duration) - 1))
    son1 = x[:xiao] + x[da:] + x[xiao:da]
    pc(son1)
    # print("shuzhi",xiao,da)
    return son1

def threepoint_realnumbcross(x):
    xiao = int(np.random.uniform(2, len(duration) - 3))
    mid=int(np.random.uniform(xiao, len(duration) - 2))
    da = int(np.random.uniform(mid, len(duration) - 1))
    son1 = x[:xiao] + x[mid:da] + x[xiao:mid]+ x[da:]
    pc(son1)
    # print("shuzhi",xiao,da)
    return son1

def multitimestwopoint_realnumbcross(x,n):
    for i in range(n):
        x=twopont_realnumbcross(x)
    return x


def oneplusone(y):
    t1 = []
    t2 = []
    t3 = []
    t4 = []
    for i in range(1000):
        print("y",y)
        print("scheduley",schedule(y))
        print("date_transfer_schedule",date_transfer_schedule(y))
        t1.append(y)
        t2.append(schedule(y))
        y1 = date_transfer_schedule(y)
        t4.append(y1)
        fd = bestcount(t3)
        y2 = mutationalternative(y1)
        y3 = schedule_transger_date(y2)
        print(schedule(y3))
        t1.append(y3)
        t2.append(schedule(y3))
        index1 = np.argmin(t2)
        z = t1[index1]
        y4 = twopont_realnumbcross(z)
        y4, _ = transfer(y4)
        t1.append(y4)
        t2.append(schedule(y4))
        print(schedule(y4))
        t3.append(min(t2))
        index = np.argmin(t2)
        y = t1[index]
        print(i, schedule(y), y)
        if fd > 5:
            break
    return y


def minvaluesubstitute(x1, x2):
    for i in range(len(x1)):
        x1[i] = min(x1[i], x2[i])
    pc(x1)
    return x1
def gagenind():
    c = sample(cities,len(cities))
    # print("c",c)
    c=manytimeshuffle(c)
    return c
def hunpai(x):
    xiao = int(np.random.uniform(2, len(duration) - 3))
    mid=int(np.random.uniform(xiao, len(duration) - 2))
    da = int(np.random.uniform(mid, len(duration) - 1))
    z0=choice([x[:xiao],x[xiao:mid],x[mid:da],x[da:]])
    #z0 =x[xiao:mid]
    z=copy.deepcopy(z0)
    random.shuffle(z)
    if z0==x[:xiao]:
        son1 = z + x[xiao:mid]+ x[mid:da] + x[da:]
    if z0==x[xiao:mid]:
        son1 = x[:xiao] + z + x[mid:da] + x[da:]
    if z0==x[mid:da]:
        son1 = x[:xiao] + x[xiao:mid] + z + x[da:]
    if z0==x[da:]:
        son1 = x[:xiao] + x[xiao:mid] +x[mid:da] + z
    son1=feasiblesequnce(son1)
    return son1
def hunpai_realnumber(x):
    xiao = int(np.random.uniform(2, len(duration) - 3))
    mid=int(np.random.uniform(xiao, len(duration) - 2))
    da = int(np.random.uniform(mid, len(duration) - 1))
    z0=choice([x[:xiao],x[xiao:mid],x[mid:da],x[da:]])
    z=copy.deepcopy(z0)
    random.shuffle(z)
    if z0==x[:xiao]:
        son1 = z + x[xiao:mid]+ x[mid:da] + x[da:]
    if z0==x[xiao:mid]:
        son1 = x[:xiao] + z + x[mid:da] + x[da:]
    if z0==x[mid:da]:
        son1 = x[:xiao] + x[xiao:mid] + z + x[da:]
    if z0==x[da:]:
        son1 = x[:xiao] + x[xiao:mid] +x[mid:da] + z
    pc(son1)
    return son1


def manytimeshuffle(x):
    for i in range(10):
        random.shuffle(x)
    return x

def loda_data(file_name):

    global csvFile,  c, c1, rsl, rc, activity, pa, d, cities
    i=0
    csvFile= open(file_name)
    f = csv.reader(csvFile)

    for item in f:
        i = i + 1
        b = []
        b1 = []
        # if i == 15:
        #     opm = int(item[0].split()[-1])
        if i > 18 and i < 140:
            string = item[0]
            a = string.split()
            for j in range(len(a)):
                if j != 0 and j != 1 and j != 2:
                    b.append(int(a[j]))
            c.append(b)
        if i > 144 and i < 267:
            string1 = item[0]
            a1 = string1.split()
            for j in range(len(a1)):
                if j != 0 and j != 1 and j != 2:
                    b1.append(int(a1[j]))
                if j == 2:
                    duration.append(int(a1[j]))
            c1.append(b1)
        if i == 270:
            string2 = item[0]
            a2 = string2.split()
    for j2 in range(len(a2)):
        a2[j2] = int(a2[j2])
    rsl = a2
    rc = c1
    activity = list(np.array(list(range(122))) + 1)  ######## attention
    d = list(zip(activity, c))
    for k in range(len(activity)):
        pa.append([])
    for k1 in range(len(c)):
        for k2 in range(len(c[k1])):
            pa[c[k1][k2] - 1].append(activity[k1])

    for k3 in range(len(pa)):
        if pa[k3] == []:
            pa[k3] = [0]

    cities = list(np.array(list(range(len(duration)))) + 1)


def takeSecondd(elem):
    return elem[-1]
def cgapmxcrossoverforrealvalue(s, s1):
    chang1 = choice(range((len(s) - 1)))
    chang2 = int(np.random.uniform(chang1, len(s)))
    winner=copy.deepcopy(s)
    mutationgroup=[]
    son2 = s1[:chang1] + s[chang1:chang2]+s1[chang2:]
    mutationgroup.append(son2)
    mutationgroupopt=[]
    for i in range(len(mutationgroup)):
        print('cgapmxcrossoverforrealvalue',i)
        chang3 = max(1,choice(range(len(s) - 1)))
        b=int(np.random.uniform(0,mutationgroup[i][chang3]))
        mutationgroup[i] = aco2_instance.search_path(date_transfer_schedule(mutationgroup[i]))
        lss = copy.deepcopy(mutationgroup[i])
        mutationgroupopt.append(mutationgroup[i])
        lss[chang3]=mutationgroup[i][chang3]-b
        lss=aco2_instance.search_path(date_transfer_schedule(lss))
        mutationgroupopt.append(lss)

    return winner, mutationgroupopt

def schedule_to_answer(plan):
    solution=[]
    solutionendday=[]
    #controlv=0
    def constrainted_resource_test(s):
        v=0
        for i in s:
            #print(i)
            if i>0:
                #print(i)
                v=10000
                return v
            else:
                v=0
        return v
    for i in range(len(plan)):
        if i ==0:
            solution.append(0)
            solutionendday.append(solution[i]+duration[plan[i]-1])
        else:
            #print(i,plan[i])  ####### print
            #print(plan[:i])
            #print(pa[plan[i]-1])
            #print("jinqianji",set(pa[plan[i]-1]) & set(plan[:i]))  ####### print
            daystartoption=[]
            if len(set(pa[plan[i]-1]) & set(plan[:i])) !=0:
                for predecedent_act in (set(pa[plan[i]-1]) & set(plan[:i])):
                    daystartoption.append(solutionendday[plan.index(predecedent_act)])
            daystartoption1=max(daystartoption)
            #print("daystartoption1",daystartoption1)   ####### print
            newpoint = max(solution[i - 1],daystartoption1)
            #print("i", i, "newpoint", newpoint)  ####### print
            while newpoint !=1000:
                tempact_considered = []
                #print("i",i,"newpoint",newpoint) ####### print
                for j in range(len(plan[:i])):
                    if solutionendday[j]>newpoint:
                        tempact_considered.append(plan[j])
                #print("i",i,"linact",tempact_considered)  ####### print
                if len(tempact_considered )==0:
                    #solution.append(solution[i - 1])
                    #print("0 set")
                    #print("a",plan[i])  ####### print
                    solution.append(newpoint)
                    solutionendday.append(solution[i] + duration[plan[i] - 1])
                    #print("so", solution)   ####### print
                    #print("solend", solutionendday)  ####### print
                    newpoint = 1000
                else:
                    next_day_selection=[]
                    zyxh=np.zeros_like(rsl)
                    for k in range(len(tempact_considered)):
                        zyxh=zyxh+np.array(rc[tempact_considered[k]-1])
                        #print("zs", tempact_considered[k])  ####### print
                        se_poxition=plan.index(tempact_considered[k])
                        next_day_selection.append(solutionendday[se_poxition])
                    #print("i",i,"plan[i]",plan[i])   ####### print
                    zyxh=zyxh+np.array(rc[plan[i]-1])
                    zyxh=list(zyxh-np.array(rsl))
                    #print("zyxh",zyxh)   ####### print
                    controlv=constrainted_resource_test(zyxh)
                    #print("dddd",i,controlv)  ####### print
                    if controlv>0:
                        newpoint = min(next_day_selection)
                        #print(newpoint)
                    else:
                        #print ("ssss")
                        solution.append(newpoint)
                        solutionendday.append(solution[i] + duration[plan[i]-1])
                        #print("so",solution) ####### print
                        #print("solend",solutionendday)  ####### print
                        newpoint=1000
    #print("plan  ",plan)
    #print("so    ", solution)  ####### print
    #print("solend",solutionendday)  ####### print
    planwithso=list(zip(solution,plan))
    #print("planwithso",planwithso)
    def myf(a):
        return a[1]
    superzip=sorted(planwithso,key=myf)
    #print("superzip",superzip)
    answer=[]
    for i in range(len(superzip)):
        answer.append(superzip[i][0])
    #print("answer",answer)
    return answer#solution#,solutionendday


def genson_0(parent, start_idx, end_idx):
    parent_schedule = date_transfer_schedule(parent)

    # Select random activity to move
    activity_idx = np.random.randint(start_idx, end_idx)
    activity = parent_schedule[activity_idx]

    # Get predecessor and successor indices
    pred_indices = [parent_schedule.index(pred) for pred in pa[activity - 1]]
    succ_indices = [parent_schedule.index(succ) for succ in c[activity - 1]]

    max_pred_idx = max(pred_indices) if pred_indices else -1
    min_succ_idx = min(succ_indices) if succ_indices else len(parent_schedule)

    # Validate position constraints
    if max_pred_idx >= min_succ_idx - 1:
        return parent_schedule  # Return original if no valid positions

    # Select new position maintaining precedence constraints
    new_position = np.random.randint(max_pred_idx + 1, min_succ_idx)

    # Create new schedule by moving activity
    offspring = parent_schedule.copy()
    current_idx = offspring.index(activity)

    # Remove from current position and insert at new position
    del offspring[current_idx]
    if new_position > current_idx:
        new_position -= 1  # Adjust for removal

    offspring.insert(new_position, activity)

    return offspring


def swap_random_activities(sequence):
    if len(sequence) < 3:  # Need at least 2 activities to swap
        return sequence.copy()

    # Select two distinct random indices (excluding first and last if needed)
    idx1, idx2 = np.random.choice(range(1, len(sequence) - 1), size=2, replace=False)

    # Create new sequence with swapped activities
    new_sequence = sequence.copy()
    new_sequence[idx1], new_sequence[idx2] = new_sequence[idx2], new_sequence[idx1]

    return new_sequence

def genson(papa,q1,q2):
    papa=date_transfer_schedule(papa)
    papac=copy.deepcopy(papa)
     #poselect =  np.random.randint(q1,q2)

    frozen = get_frozen_with_unwanted_exclusion()
    non_frozen=non_fronze_acts(frozen)
    if np.random.uniform()>0.2:
        b =sample(non_frozen,1)[0]
        while b==1:
            b = sample(non_frozen, 1)[0]
    else:
        b = np.random.randint(2, len(duration))
    #print(b)
    jinqianindex=[]
    for i in pa[b - 1]:
        jinqianindex.append(papa.index(i))
    #print("gen",b,b_po,sh)
    maxsh=max(jinqianindex)
    #print("maxsh",maxsh)
    jinhouindex=[]
    for i in c[b - 1]:
        jinhouindex.append(papa.index(i))
    #print("gen",b,b_po,sh)
    minsh=min(jinhouindex)
    #print("minsh",maxsh,posi,minsh)
    posi = np.random.randint(maxsh + 1, minsh+1)
    while maxsh==posi-1 and minsh==posi+1:
        jinqianindex = []
        for i in pa[b - 1]:
            jinqianindex.append(papa.index(i))
        # print("gen",b,b_po,sh)
        maxsh = max(jinqianindex)
        # print("maxsh",maxsh)
        jinhouindex = []
        #print(c[b - 1])
        for i0 in c[b - 1]:
            jinhouindex.append(papa.index(i0))
        # print("gen",b,b_po,sh)
        minsh = min(jinhouindex)
        #print("minsh",maxsh,posi,minsh)
        posi = np.random.randint(maxsh + 1, minsh + 1)
        #print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
    actindex = papa.index(b)
    papac.insert(posi, b)
    #print("b", a)
    if posi < actindex:
        del papac[actindex + 1]
    else:
        del papac[actindex]
    return papac

def genson1(papa):
    papa=date_transfer_schedule(papa)
    papac=copy.deepcopy(papa)
    #poselect =  np.random.randint(q1,q2)
    poselect=np.random.randint(2,len(papa)-2)
    poselect=poselect
    #print(papa)
    b=papa[poselect]
    #print(b)
    jinqianindex=[]
    for i in pa[b - 1]:
        jinqianindex.append(papa.index(i))
    #print("gen",b,b_po,sh)
    maxsh=max(jinqianindex)
    #print("maxsh",maxsh)
    jinhouindex=[]
    for i in c[b - 1]:
        jinhouindex.append(papa.index(i))
    #print("gen",b,b_po,sh)
    minsh=min(jinhouindex)
    #print("minsh",maxsh,posi,minsh)
    posi = np.random.randint(maxsh + 1, minsh+1)
    while maxsh==posi-1 and minsh==posi+1:
        #poselect = np.random.randint(2, 121)
        #poselect = poselect+1
        #poselect = np.random.randint(q1, q2)
        poselect = np.random.randint(2, len(papa) - 2)
        b = papa[poselect]
        jinqianindex = []
        for i in pa[b - 1]:
            jinqianindex.append(papa.index(i))
        # print("gen",b,b_po,sh)
        maxsh = max(jinqianindex)
        # print("maxsh",maxsh)
        jinhouindex = []
        #print(c[b - 1])
        for i0 in c[b - 1]:
            jinhouindex.append(papa.index(i0))
        # print("gen",b,b_po,sh)
        minsh = min(jinhouindex)
        #print("minsh",maxsh,posi,minsh)
        posi = np.random.randint(maxsh + 1, minsh + 1)
        #print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
    actindex = papa.index(b)
    papac.insert(posi, b)
    #print("b", a)
    if posi < actindex:
        del papac[actindex + 1]
    else:
        del papac[actindex]
    return papac


def load_train_data( data_pairs):
    inputs = np.array([x for x, _ in data_pairs])  # This will create a 2D array of inputs
    outputs = np.array([y for _, y in data_pairs])
    return inputs, outputs


def make_a_date_plan(new_list):
    n = len(duration)
    in_degree = [0] * n
    for i in range(len(c)):
        for s in c[i]:
            #if s <= n:
            in_degree[s - 1] += 1

    start_times = [0] * n
    queue = [i for i in range(n) if in_degree[i] == 0]

    while queue:
        i = queue.pop(0)
        finish_time = start_times[i] + duration[i]

        if i >= len(c) or i >= len(new_list):
            continue  # skip dummy or out-of-bound activity

        for succ_idx, succ in enumerate(c[i]):
            #print(i,succ_idx, succ )
            lag = new_list[i][succ_idx]
            start_times[succ - 1] = max(start_times[succ - 1], finish_time + lag)
            in_degree[succ - 1] -= 1
            if in_degree[succ - 1] == 0:
                queue.append(succ - 1)

    return start_times



def correct_aon_lag(new_data): ## using right start date to produce right lag
   # print("c", len(c),c)
   # print("duration",duration)
   # print("pa",pa)
    new_lag=[]
    for i in range(len(c)):
        length=len(c[i])
        new_sublist=[]
        for j in range(length):
            lag=new_data[c[i][j]-1]-new_data[i]-duration[i]
            new_sublist.append(lag)
        new_lag.append(new_sublist)
   #print("w",new_lag)
    return new_lag

def flatten_gene(new_lag):
    flat = [item for sublist in new_lag for item in sublist]
    #print(flat)
    #print(new_lag)
    return flat

def build_full_predecessor_net(start_act):
    net = [start_act]
    seen = set([start_act])
    frontier = [start_act]

    while frontier:
        nxt = []
        for act in frontier:
            for pred in pa[act - 1]:  # pa is 1-based
                if pred > 0 and pred not in seen:
                    seen.add(pred)
                    net.append(pred)
                    nxt.append(pred)
        frontier = nxt

    net.remove(start_act)  # Optional: exclude the start node itself
    return net


def get_subgraph_parts(target_act):
    # Get all predecessors (the necessary computation chain)
    subgraph = set(build_full_predecessor_net(target_act))
    subgraph.add(target_act)  # Include the target itself
    return sorted(subgraph)

def get_subgraph_parts1(target_act):   ##build front frozen part macro level
    part1 = build_full_predecessor_net(target_act)  # excludes target_act

    part2 = set()
    for act in part1:
        for succ in c[act - 1]:
            if succ != target_act:  # exclude target_act
                part2.add(succ)

    core = set(part1) | part2 | {target_act}

    part3 = set()
    for act in core:
        preds = build_full_predecessor_net(act)
        part3.update(preds)  # Add all predecessors to part3

    subgraph = core | part3

    subgraph_complete = set(subgraph)
    for act in subgraph:
        for succ in c[act - 1]:
            if succ in subgraph:  # If any successor is inside subgraph
                subgraph_complete.update(c[act - 1])  # Freeze all edges from act
    frozen_graph=sorted(subgraph_complete)
    return frozen_graph


def get_frozen_with_unwanted_exclusion():
    n = len(c)
    num_subgraphs = random.choice([1, 3])
    frozen_sets = []

    for _ in range(num_subgraphs):
        valid_activities = [i for i in range(2, n + 1)]
        if valid_activities:
            target_act = random.choice(valid_activities)
            frozen_acts = get_subgraph_parts(target_act)
            frozen_sets.append(set(frozen_acts))

    # Combine all frozen activities
    all_frozen = set()
    for frozen_set in frozen_sets:
        all_frozen.update(frozen_set)

    # STRATEGICALLY SELECT UNWANTED ACTS TO EXCLUDE FROM FREEZING
    if np.random.uniform()<0.9:
        unwanted_acts = select_unwanted_activities(all_frozen, n)
        final_frozen = all_frozen - unwanted_acts
    else:
        final_frozen = all_frozen
    return final_frozen


def select_unwanted_activities(frozen_set, n, exclusion_rate=0.2):
    """Select activities to exclude from freezing"""
    unwanted = set()
    frozen_list = list(frozen_set)

    if not frozen_list:
        return unwanted

    # Calculate how many to exclude (30% of frozen set)
    num_to_exclude = max(1, int(len(frozen_list) * exclusion_rate))

    # Strategy 1: Exclude activities with many connections (high flexibility)
    highly_connected = find_highly_connected_activities(frozen_list)
    unwanted.update(random.sample(highly_connected, min(num_to_exclude, len(highly_connected))))

    # Strategy 2: Exclude activities with long duration (more room for optimization)
    if len(unwanted) < num_to_exclude:
        long_duration_acts = find_long_duration_activities(frozen_list)
        additional = min(num_to_exclude - len(unwanted), len(long_duration_acts))
        unwanted.update(random.sample(long_duration_acts, additional))

    # Strategy 3: Random exclusion if still needed
    if len(unwanted) < num_to_exclude:
        remaining_frozen = [act for act in frozen_list if act not in unwanted]
        additional = min(num_to_exclude - len(unwanted), len(remaining_frozen))
        unwanted.update(random.sample(remaining_frozen, additional))

    return unwanted


def find_highly_connected_activities(activity_list):
    """Find activities with many predecessors/successors"""
    connected_scores = []
    for act in activity_list:
        act_idx = act - 1
        num_connections = len(pa[act_idx]) + len([s for s in c[act_idx] if s > 0])
        connected_scores.append((act, num_connections))

    # Return top 40% most connected activities
    connected_scores.sort(key=lambda x: x[1], reverse=True)
    return [act for act, score in connected_scores[:max(1, len(connected_scores) // 3)]]


def find_long_duration_activities(activity_list):
    """Find activities with long durations"""
    duration_scores = []
    for act in activity_list:
        act_idx = act - 1
        duration_scores.append((act, duration[act_idx]))

    # Return top 40% longest activities
    duration_scores.sort(key=lambda x: x[1], reverse=True)
    return [act for act, d in duration_scores[:max(1, len(duration_scores) // 3)]]
def get_frozen():
    n=len(c)
    num_subgraphs = random.choice([1,2])#2#min(3, max(1, n // 10))  # Protect 1-3 subgraphs
    frozen_sets = []

    for _ in range(num_subgraphs):
        # Choose random activities that are not dummy activities
        valid_activities = [i for i in range(2, n+1)]  # Skip dummy start activity
        if valid_activities:
            target_act = random.choice(valid_activities)
            frozen_acts = get_subgraph_parts(target_act)
            frozen_sets.append(set(frozen_acts))

    # Combine all frozen activities
    all_frozen = set()
    for frozen_set in frozen_sets:
        all_frozen.update(frozen_set)



    return all_frozen
def lag_uniform_crossover(p1_flat, p2_flat, frozen,swap_prob=0.3):  # Lower probability favors elite
    """
    Uniform crossover with frozen subgraph protection.
    Better exploration while preserving elite's critical parts.
    """
    p1 = reverse_flatten(p1_flat)  # elite
    p2 = reverse_flatten(p2_flat)
    n = len(p1)

    # Get frozen subgraph
    target_act = int(np.random.uniform(2, n + 1))
    frozen_acts = get_subgraph_parts(target_act)
    frozen_set = set(frozen_acts)

    child1 = [row.copy() for row in p1]  # Start with elite as base
    child2 = [row.copy() for row in p2]  # Start with non-elite as base

    # Uniform crossover for non-frozen parts
    for i in range(n):
        if (i + 1) not in frozen_set and random.random() < swap_prob:
            # Swap entire activity rows between children
            child1[i], child2[i] = child2[i], child1[i]

    # Additional protection: ensure incoming lags to frozen acts come from elite
    for j in frozen_set:
        j0 = j - 1
        for pred in pa[j0]:
            if pred == 0: continue
            try:
                k = c[pred - 1].index(j)
                child1[pred - 1][k] = p1[pred - 1][k]  # From elite
                child2[pred - 1][k] = p1[pred - 1][k]  # From elite
            except ValueError:
                continue

    return flatten_gene(child1), flatten_gene(child2)

def lag_three_point_crossover1(p1_flat, p2_flat):
    """
    Table-based 3-point crossover with frozen subgraph protection.
    Only incoming lags to frozen activities are preserved from parent 1 (elite).
    """

    # Get lag table representations
    p1 = reverse_flatten(p1_flat)  # elite
    p2 = reverse_flatten(p2_flat)
    n = len(p1)  # number of activities (rows)

    # Select frozen subgraph from elite parent
    target_act = int(np.random.uniform(2, n + 1))  # avoid dummy
    frozen_acts = get_subgraph_parts(target_act)   # returns list of 1-based indices
    frozen_set = set(frozen_acts)

    # Prepare 3-point crossover indices for rows (activities)
    if n < 4:
        cuts = [0, n]  # fallback: use full crossover
    else:
        cuts = sorted(random.sample(range(1, n), 2))  # ensure 3 cuts within valid range

    #p0, p1_cut, p2_cut = cuts
    p0, p1_cut = cuts

    # Build initial children by alternating chunks
    #child1 = (
    #    p1[:p0] +
    #    p2[p0:p1_cut] +
    #    p1[p1_cut:p2_cut] +
    #    p2[p2_cut:]
    #)

    #child2 = (
    #    p2[:p0] +
    #    p1[p0:p1_cut] +
    #    p2[p1_cut:p2_cut] +
    #    p1[p2_cut:]
    #)

    child1 = (
        p1[:p0] +
        p2[p0:p1_cut] +
        p1[p1_cut:]
    )

    child2 = (
        p2[:p0] +
        p1[p0:p1_cut] +
        p1[p1_cut:]
    )

    # === Step 2: Recover incoming lags to frozen acts from elite parent (p1) ===
    for j in frozen_set:
        j0 = j - 1  # convert to 0-based
        for pred in pa[j0]:
            if pred == 0:
                continue
            try:
                k = c[pred - 1].index(j)
                # Recover lag from p1 (elite)
                child1[pred - 1][k] = p1[pred - 1][k]
                child2[pred - 1][k] = p2[pred - 1][k]
            except ValueError:
                continue  # Edge does not exist

    return flatten_gene(child1), flatten_gene(child2)

def reverse_flatten(flat):
    lengths = [len(s) for s in c]
    result = []
    i = 0
    for L in lengths:
        result.append(flat[i:i + L])
        i += L
    return result

def find_preceding_act(acts):   # find its direct preceding acts to selected net
    precedings=[]
    for act in acts:
        precede_list=pa[act-1]
        precedings=precedings+precede_list
    precedings=list(set(precedings))
    return precedings
def build_full_impact_net(start_act): ### all successor
    n = len(c)
    if n == 0 or not (1 <= start_act <= n): return []
    sink = max(max(row) for row in c if row) if c else n
    sink = max(sink, n)

    net, seen, frontier = [start_act], {start_act}, [start_act]
    while frontier:
        nxt = []
        for u in frontier:
            if 1 <= u <= n:
                for v in c[u-1]:
                    #if 1 <= v <= n and v != sink and v not in seen: ### it exclude the dummy finish
                    if 1 <= v <= n and v not in seen:
                        seen.add(v); net.append(v); nxt.append(v)
        frontier = nxt
    return net  # includes start_act
def get_back_part_frozen(act):  ### build an backward net based on selected act
    full_acts = build_full_impact_net(act)
    full_acts.remove(act)
    presa = find_preceding_act(full_acts)
    presa = presa + full_acts
    presa = list(set(presa))
    return presa
def lag_two_point_crossover1(p1_flat, p2_flat,frozen):
    """
    Table-based 3-point crossover with frozen subgraph protection.
    Only incoming lags to frozen activities are preserved from parent 1 (elite).
    """

    # Get lag table representations
    p1 = reverse_flatten(p1_flat)  # elite
    p2 = reverse_flatten(p2_flat)
    n = len(p1)  # number of activities (rows)

    # Select frozen subgraph from elite parent
    length=len(c)
    # Prepare 3-point crossover indices for rows (activities)
    if n < 4:
        cuts = [0, n]  # fallback: use full crossover
    else:
        cuts = sorted(random.sample(range(1, n), 2))  # ensure 3 cuts within valid range

    #p0, p1_cut, p2_cut = cuts
    p0, p1_cut = cuts


    child1 = (
        p1[:p0] +
        p2[p0:]
    )

    child2 = (
        p2[:p0] +
        p1[p0:]
    )

    # === Step 2: Recover incoming lags to frozen acts from elite parent (p1) ===
    for j in frozen:
        j0 = j - 1  # convert to 0-based
        for pred in pa[j0]:
            if pred == 0:
                continue
            try:
                k = c[pred - 1].index(j)
                # Recover lag from p1 (elite)
                child1[pred - 1][k] = p1[pred - 1][k]
                child2[pred - 1][k] = p2[pred - 1][k]
            except ValueError:
                continue  # Edge does not exist

    return flatten_gene(child1), flatten_gene(child2)

def lag_three_point_crossover1(p1_flat, p2_flat):
    """
    Table-based 3-point crossover with frozen subgraph protection.
    Only incoming lags to frozen activities are preserved from parent 1 (elite).
    """

    # Get lag table representations
    p1 = reverse_flatten(p1_flat)  # elite
    p2 = reverse_flatten(p2_flat)
    n = len(p1)  # number of activities (rows)

    # Select frozen subgraph from elite parent
    length=len(c)
    target_act=int(np.random.uniform(2,length+1))
    frozen_acts= get_subgraph_parts(target_act)
    if np.random.uniform()>0.5:
        target_backact = int(np.random.uniform(2, length + 1))
        frozen_back_ward_acts=get_back_part_frozen(target_backact)

        while set(frozen_acts) & set(frozen_back_ward_acts):
            target_act = int(np.random.uniform(2, length + 1))
            frozen_acts = get_subgraph_parts(target_act)
            target_backact = int(np.random.uniform(2, length + 1))
            frozen_back_ward_acts = get_back_part_frozen(target_backact)
        #total_frozen_act=set(frozen_acts+frozen_back_ward_acts)
        frozen_front = frozen_acts
        frozen_back = frozen_back_ward_acts
    else:

        #non_frozen = non_fronze_acts(total_frozen_act)
        frozen_front=frozen_acts
        frozen_back=None#frozen_back_ward_acts

    # Prepare 3-point crossover indices for rows (activities)
    if n < 4:
        cuts = [0, n]  # fallback: use full crossover
    else:
        cuts = sorted(random.sample(range(1, n), 2))  # ensure 3 cuts within valid range

    #p0, p1_cut, p2_cut = cuts
    p0, p1_cut = cuts

    # Build initial children by alternating chunks
    #child1 = (
    #    p1[:p0] +
    #    p2[p0:p1_cut] +
    #    p1[p1_cut:p2_cut] +
    #    p2[p2_cut:]
    #)

    #child2 = (
    #    p2[:p0] +
    #    p1[p0:p1_cut] +
    #    p2[p1_cut:p2_cut] +
    #    p1[p2_cut:]
    #)

    child1 = (
        p1[:p0] +
        p2[p0:p1_cut] +
        p1[p1_cut:]
    )

    child2 = (
        p2[:p0] +
        p1[p0:p1_cut] +
        p1[p1_cut:]
    )

    # === Step 2: Recover incoming lags to frozen acts from elite parent (p1) ===
    for j in frozen_front:
        j0 = j - 1  # convert to 0-based
        for pred in pa[j0]:
            if pred == 0:
                continue
            try:
                k = c[pred - 1].index(j)
                # Recover lag from p1 (elite)
                child1[pred - 1][k] = p1[pred - 1][k]
                child2[pred - 1][k] = p2[pred - 1][k]
            except ValueError:
                continue  # Edge does not exist
    if frozen_back:
        for j in frozen_back:
            j0 = j - 1  # convert to 0-based
            for k in c[j0]:
                k1=c[j0].index(k)
                child1[j0][k1] = p1[j0][k1]
                child2[j0][k1] = p2[j0][k1]

    return flatten_gene(child1), flatten_gene(child2)
def get_a_whole_frozn_subgraph_for_act_list():
    length=len(c)
    if 0<np.random.uniform() <=0.33:
        target_act=int(np.random.uniform(2,length+1))
        frozen_acts_front= get_subgraph_parts(target_act)
        front = frozen_acts_front
        back=[]

    elif 0.33<np.random.uniform()<=0.67:
        target_backact = int(np.random.uniform(2, length + 1))
        frozen_back_ward_acts=get_back_part_frozen(target_backact)
        #total_frozen_act = frozen_back_ward_acts
        front=[1]
        back=frozen_back_ward_acts
    else:
        target_act = int(np.random.uniform(2, length + 1))
        frozen_acts_front = get_subgraph_parts(target_act)
        target_backact = int(np.random.uniform(2, length + 1))
        frozen_back_ward_acts = get_back_part_frozen(target_backact)
        while set(frozen_acts_front) & set(frozen_back_ward_acts):
            target_act = int(np.random.uniform(2, length + 1))
            frozen_acts_front = get_subgraph_parts(target_act)
            target_backact = int(np.random.uniform(2, length + 1))
            frozen_back_ward_acts = get_back_part_frozen(target_backact)
        #total_frozen_act=set(frozen_acts_front+frozen_back_ward_acts)
        front=frozen_acts_front
        back= frozen_back_ward_acts
    total_frozen_act = front+back
    non_frozen = non_fronze_acts(total_frozen_act)
    return non_frozen,front,back#total_frozen_act

def frozen_order_from_starts(start_times, non_frozen,front,back):

    plan=date_transfer_schedule(start_times)
    front1=[]
    middle=[]
    for i in plan:
        if i not in non_frozen:
            front1.append(i)
        else:
            middle.append(i)
    return front1,middle
def non_fronze_acts(frozen):
    eligible_nodes = list(range(1, len(duration) + 1))
    non_frozen=set(eligible_nodes)-set(frozen)-set([len(duration)])
    return list(non_frozen)
def get_subgraph_act_order2(date):
    non_frozen, front,back = get_a_whole_frozn_subgraph_for_act_list()
    front, middle = frozen_order_from_starts(date, non_frozen, front,back)
    partial = front
    unschedule = copy.deepcopy(middle)
    schedule = []
    while len(schedule) < len(middle):
        for i in unschedule:
            if i ==1:
                partial.insert(0, i)
            else:
                preds = [p for p in pa[i - 1] if p != 0]
                if not set(preds).issubset(partial):  # placed = set(partial)
                    continue
                else:
                    f_index_set = []
                    for j in preds:
                        f_index_set.append(partial.index(j))
                    min_index = max(f_index_set)
                    suc_index_set=[]
                    full=build_full_impact_net(i)
                    if len(duration) not in full:
                        full.append(len(duration))
                    #print(i)
                    full.remove(i)
                    if set(full) & set(partial):
                        for k in list(set(full) & set(partial)):
                            suc_index_set.append(partial.index(k))
                    if len(suc_index_set)!=0:
                        up=min(suc_index_set)
                    else:
                        up=len(partial)
                    pos = random.randint(min_index + 1, up)
                    partial.insert(pos, i)
                    schedule.append(i)
    act_list = partial
    # act_list=correctomit(act_list)
    #act_list = feasiblesequnce(act_list)
    return act_list

def get_subgraph_act_order1(date):
    non_frozen, front, back = get_a_whole_frozn_subgraph_for_act_list()
    front, middle = frozen_order_from_starts(date, non_frozen, front, back)
    partial = front
    unschedule = copy.deepcopy(middle)
    schedule = []
    while len(schedule) < len(middle):
        for i in unschedule:
            preds = [p for p in pa[i - 1] if p != 0]
            if not set(preds).issubset(partial):  # placed = set(partial)
                continue
            else:
                f_index_set = []
                for j in preds:
                    f_index_set.append(partial.index(j))
                min_index = max(f_index_set)
                pos = random.randint(min_index + 1, len(partial))
                partial.insert(pos, i)
                schedule.append(i)
    act_list = partial
    # act_list=correctomit(act_list)
    act_list = feasiblesequnce(act_list)
    return act_list


def hybrid_mutation(flat, prob_struct=0.25, prob_block=0.25, prob_random=0.25):
    r = np.random.uniform()

    if r < prob_struct:
        return lag_mutate_single_entry(flat)  # Your structural, ripple-safe mutation#

    elif r < prob_struct + prob_block:
        return block_shift_mutation(flat)     # Coarser move: shift block of activities
    elif  r < prob_struct + prob_block+prob_random:
        return lag_mutate_random_entry(flat)
    else:
        return lag_mutate_random_entry_old(flat)


def hybrid_mutation1(flat, prob_struct=0.25, prob_block=0.25, prob_random=0.25):
    r = np.random.uniform()
    if  r<0.3:
        return block_shift_mutation(flat)
    elif r < 0.6:  # prob_struct:
        return lag_node_mutation(flat) # Your structural, ripple-safe mutation
    else:
        return lag_mutate_random_entry_old(flat)



def find_lag_boundary(flat,act):
    lag = reverse_flatten(flat)
    start_times = make_a_date_plan(lag)

    num_acts = len(start_times)
    #act = random.randint(1, num_acts - 1)  # skip dummy activity 0

    # Step 1: Find latest finish of predecessors
    latest_pre_finish = 0
    for pred in pa[act - 1]:
        if pred == 0:
            continue
        pred_start = start_times[pred - 1]
        pred_finish = pred_start + duration[pred - 1]
        try:
            lag_val = lag[pred - 1][c[pred - 1].index(act)]
        except ValueError:
            lag_val = 0
        latest_pre_finish = max(latest_pre_finish, pred_finish + lag_val)

    # Step 2: Find earliest start of successors
    earliest_succ_start = sum(duration)  # large number
    for succ in c[act - 1]:
        succ_start = start_times[succ - 1]
        try:
            lag_val = lag[act - 1][c[act - 1].index(succ)]
        except ValueError:
            lag_val = 0
        succ_bound = succ_start - lag_val - duration[act - 1]
        earliest_succ_start = min(earliest_succ_start, succ_bound)

    # Step 3: Pick a new start time within this window
    earliest = latest_pre_finish
    latest = max(earliest, earliest_succ_start)
    lag_boundary=latest-earliest
    return  lag_boundary

def lag_mutate_random_entry(flat): ### with limited lag boundary

    def lag_index(i, j):
        idx = 0
        for row in range(i):
            idx += len(c[row])
        return idx + j


    # --- Start mutation ---
    mutated = flat.copy()
    lag = reverse_flatten(mutated)
    start_times = make_a_date_plan(lag)

    num_acts = len(start_times)
    act = random.randint(1, num_acts - 1)  # skip dummy activity 0

    lag_boundary = find_lag_boundary(flat, act)
    if lag_boundary <= 0:
        return mutated  # no slack, no mutation

    # Collect related lag entries (incoming/outgoing)
    lag_targets = []
    for pred in pa[act - 1]:
        if pred == 0:
            continue
        try:
            pred_idx = pred - 1
            succ_pos = c[pred_idx].index(act)
            flat_idx = lag_index(pred_idx, succ_pos)
            lag_targets.append(flat_idx)
        except ValueError:
            continue

    for succ in c[act - 1]:
        try:
            act_idx = act - 1
            succ_pos = c[act_idx].index(succ)
            flat_idx = lag_index(act_idx, succ_pos)
            lag_targets.append(flat_idx)
        except ValueError:
            continue

    if not lag_targets:
        return mutated

    # Mutate one lag entry with bounded delta
    idx = random.choice(lag_targets)
    max_delta =lag_boundary
    delta = random.randint(1, max_delta)
    direction = random.choice([-1, 1])
    change = direction * delta

    mutated[idx] = max(0, mutated[idx] + change)

    return mutated

def lag_node_mutation(flat):
    mutated = flat.copy()
    mutated=reverse_flatten(mutated)
    act = random.randint(1, len(duration))  # skip dummy activity 0
    delta = int(np.random.uniform(0, opm))
    direction = np.random.choice([-1, 1])
    if act==1:

        l_bound=min(mutated[act-1])
        u_bound=max(mutated[act-1])
        if direction==1:
            mutated[act - 1]=list(np.array(mutated[act-1])+delta)
        else:
            delta=min(l_bound,delta)
            mutated[act - 1] = list(np.array(mutated[act - 1]) - delta)

    elif act==len(duration):
        if direction==1:
            preset=pa[act-1]
            for preact in preset:
                lag_index=c[preact-1].index(act)
                mutated[preact-1][lag_index] +=delta
        else:
            preset=pa[act-1]
            bound=[]
            for preact in preset:
                lag_index=c[preact-1].index(act)
                bound.append(mutated[preact-1][lag_index])
            low_b=min(min(bound),delta)
            for preact in preset:
                lag_index=c[preact-1].index(act)
                mutated[preact-1][lag_index] -=low_b
    else:

        l_b_s=min(mutated[act-1])
        preset=pa[act-1]
        bound = []
        for preact in preset:
            lag_index = c[preact - 1].index(act)
            bound.append(mutated[preact - 1][lag_index])
        l_b_p=min(bound)
        delta=min(l_b_s,l_b_p)
        step=direction*delta
        for preact in preset:
            lag_index = c[preact - 1].index(act)
            mutated[preact - 1][lag_index] -= step
        mutated[act - 1] = list(np.array(mutated[act - 1]) + step)
    date=make_a_date_plan(mutated)
    mutated=flatten_gene(correct_aon_lag(date))
    return mutated


def  lag_mutate_node_centric(flat, frozen):
    """Mutate by moving entire nodes rather than individual lags"""
    lag_table = reverse_flatten(flat)
    n = len(lag_table)

    # Choose a random non-dummy node to move
    if frozen is None:
        node_to_move = random.randint(1, n)  # 1-based activity index
    else:
        non_frozen = non_fronze_acts(frozen)
        if len(duration) in non_frozen:  # Assuming 'duration' is defined elsewhere
            non_frozen.remove(len(duration))
        node_to_move = random.choice(non_frozen)

    # Get all incoming edges to this node
    node_idx = node_to_move - 1
    incoming_edges = []
    for pred in pa[node_idx]:  # Assuming 'pa' is defined elsewhere
        if pred == 0:
            continue
        try:
            k = c[pred - 1].index(node_to_move)  # Assuming 'c' is defined elsewhere
            incoming_edges.append((pred - 1, k))  # (predecessor_idx, lag_position)
        except ValueError:
            continue

    if not incoming_edges:
        # Node has no incoming edges, can't mutate via lags
        return flat

    # Find the minimum current lag to determine maximum possible decrease
    current_lags = [lag_table[pred_idx][lag_pos] for pred_idx, lag_pos in incoming_edges]
    min_current_lag = min(current_lags)

    # Calculate safe delta range that won't make any lag negative
    max_decrease = min_current_lag  # Can't decrease more than the smallest lag
    max_increase = opm  # Assuming 'opm' is defined elsewhere

    # Generate delta within safe bounds
    if np.random.uniform()<0.9:
        delta = random.randint(-max_decrease, 0)
    else:
        delta=random.randint(0, int(opm/2))

    # Apply consistent delta to all incoming lags
    mutated_table = [row.copy() for row in lag_table]
    for pred_idx, lag_pos in incoming_edges:
        new_lag = mutated_table[pred_idx][lag_pos] + delta
        mutated_table[pred_idx][lag_pos] = new_lag

    # Flatten and return the mutated table
    return flatten_gene(mutated_table)


def checking_slack(flat,i):
    #print("www",i)
    lag_matrix = reverse_flatten(flat)
    mutated = copy.deepcopy(lag_matrix)
    preceding_lags=[]
    successor_lags=[]

    for act in pa[i - 1]:
        if act == 0:
            continue
        succs_of_pred = c[act - 1]
        if i in succs_of_pred:
            k = succs_of_pred.index(i)
            preceding_lags.append(mutated[act - 1][k] )#= max(0, mutated[act - 1][k] + change)

    # Mutate all lags from i → successors (tighten)
    for s_idx in range(len(c[i - 1])):
        successor_lags.append(mutated[i - 1][s_idx])# = max(0, mutated[i - 1][s_idx] - change)
    if len(preceding_lags)<=0:
        pre_low_bound=0
    else:
        pre_low_bound=min(preceding_lags)
    suc_low_bound=min(successor_lags)
    return pre_low_bound,suc_low_bound

def block_shift_mutation(flat):
    lag_matrix = reverse_flatten(flat)
    mutated = copy.deepcopy(lag_matrix)
    valid_acts = [i for i in range(1, len(c) + 1) if c[i - 1]]  # i has successors
    i = random.choice(valid_acts)

    frozen_subgraph=get_back_part_frozen(i)
    front_border_acts = [
        act for act in frozen_subgraph
        if any(pred not in frozen_subgraph for pred in pa[act - 1])
    ]
    move_boundary=[]
    for act in front_border_acts:
        prebound,_=checking_slack(flat,act)
        move_boundary.append(prebound)
    direction =-1#np.random.choice([-1, 1], p=[0.8, 0.2])
    if len(move_boundary)==0:
        move=0
    else:
        move=min(move_boundary)
    unit=move*direction
    for act in front_border_acts:
        for preact in pa[act - 1]:
            if preact == 0:
                continue
            succs_of_pred = c[preact - 1]
            if act in succs_of_pred:
                k = succs_of_pred.index(act)
                mutated[preact - 1][k] = max(0, mutated[preact - 1][k] + unit)

    return flatten_gene(mutated)

def lag_mutate_single_entry(flat):#### need to check it again  to make sure it correct
    lag_matrix = reverse_flatten(flat)
    mutated = copy.deepcopy(lag_matrix)
    visited = set()

    # Step 1: Select valid activity i (must have predecessors)
    valid_acts = [i for i in range(1, len(pa) + 1) if pa[i - 1]]
    if not valid_acts:
        return flat  # No valid activities to mutate

    i2 = random.choice(valid_acts)
    i =i2# np.random.choice([i1, i2])

    # Step 2: Determine mutation amount
    delta = np.random.randint(1, opm - duration[i - 1])
    direction = np.random.choice([-1, 1], p=[0.99, 0.01])  # prefer reducing lag
    change = direction * delta

    # Step 3: Mutate outgoing lags from pa[i] → i
    for k in pa[i - 1]:
        if k == 0:
            continue
        k_idx = k - 1

        for s_idx, succ in enumerate(c[k_idx]):
            if succ == i and (k_idx, s_idx) not in visited:
                if direction == -1 and mutated[k_idx][s_idx] < abs(change):
                    return flat  # Not enough slack, cancel mutation
                mutated[k_idx][s_idx] = max(0, mutated[k_idx][s_idx] + change)
                visited.add((k_idx, s_idx))

        # Step 4: Ripple to other successors of k (ī ≠ i)
        for i_bar in c[k_idx]:
            if i_bar == i:
                continue
            i_bar_idx = i_bar - 1

            # Step 4A: Adjust lags from hs → ī, keeping shared successor lags aligned
            for hs_act in pa[i_bar_idx]:
                if hs_act == 0:
                    continue
                hs_idx = hs_act - 1
                successors_hs = set(c[hs_idx])
                successors_ibar = set(c[i_bar_idx])
                shared_succs = successors_hs & successors_ibar

                for s_idx, succ in enumerate(c[hs_idx]):
                    if (hs_idx, s_idx) in visited:
                        continue
                    if succ in shared_succs:
                        # Check if all incoming lags to this shared successor are equal
                        pred_indices = [p - 1 for p in pa[succ - 1] if p != 0]
                        if not pred_indices:
                            continue
                        lag_values = []
                        try:
                            for pred_idx in pred_indices:
                                lag_idx = c[pred_idx].index(succ)
                                lag_values.append(mutated[pred_idx][lag_idx])
                        except ValueError:
                            continue

                        if len(set(lag_values)) == 1:
                            # Apply same change to all
                            new_lag = max(0, lag_values[0] + change)
                            for pred_idx in pred_indices:
                                lag_idx = c[pred_idx].index(succ)
                                mutated[pred_idx][lag_idx] = new_lag
                                visited.add((pred_idx, lag_idx))
                        # Else skip mutation for this shared successor

            # Step 4B: Structural alignment for predecessors of i_bar
            gs = pa[i_bar_idx]
            succs_ibar = set(c[i_bar_idx])
            for g in gs:
                if g == 0:
                    continue
                g_idx = g - 1
                succs_g = set(c[g_idx])
                shared = succs_g & succs_ibar
                if shared:
                    for s_idx, succ in enumerate(c[i_bar_idx]):
                        if succ in shared and (i_bar_idx, s_idx) not in visited:
                            mutated[i_bar_idx][s_idx] = max(0, mutated[i_bar_idx][s_idx] + change)
                            visited.add((i_bar_idx, s_idx))

    # Step 5: Return mutated lag gene
    return flatten_gene(mutated)

def data_mutation11(ind):
    lss = copy.deepcopy(ind)
    chang3 = random.randint(1, len(duration)-1)
    b = int(np.random.uniform(0, ind[chang3]))
    #if np.random.uniform() < 0.99:
    lss[chang3] = ind[chang3] - b
    #else:
    #    lss[chang3] = ind[chang3] + b
    lss = aco2_instance.search_path(date_transfer_schedule(lss))
    return lss


def data_mutation1(ind):
    lss = copy.deepcopy(ind)
    chang3 = random.randint(1, len(duration)-1)
    b = int(np.random.uniform(0, ind[chang3]))
    preday=[]
    sucday=[]
    pre_act=pa[chang3]
    for i in pre_act:
        preday.append(ind[i-1])
    suc_act=c[chang3-1]
    for i in suc_act:
        sucday.append(ind[i-1])
    b_min=ind[chang3]- max(preday)
    b_max=min(sucday)-ind[chang3]
    if np.random.uniform() < 0.9:
        if np.random.uniform()<0.2:
            lss[chang3] = ind[chang3] +b
        else:
            lss[chang3] = ind[chang3] -b
    else:
        #if 0.9 <= np.random.uniform() < 0.95:
        if np.random.uniform()<0.5:
            unit=int(np.random.uniform(0, b_max))
            lss[chang3] = ind[chang3] +unit
        else:
            lss[chang3] = ind[chang3] -b_min


    lss = aco2_instance.search_path(date_transfer_schedule(lss))
    return lss
def valley_directed_exploitation(ind, daily_gaps, max_shift=5):
    """
    Move activities from high-gap areas toward valleys - FIXED VERSION
    """
    # Find valleys in the gap profile
    valleys = find_valleys_simple(daily_gaps)

    if not valleys:
        return ind  # Return original if no valleys found

    # Find activities in high-gap areas near valleys
    high_gap_acts = find_activities_in_high_gap_areas(ind, daily_gaps, valleys)

    if not high_gap_acts:
        return ind  # Return original if no suitable activities found

    # Select one random activity from high-gap areas
    act_idx = random.choice(high_gap_acts)
    current_day = ind[act_idx]

    # Find nearest valley
    nearest_valley = find_nearest_valley(current_day, valleys)

    if not nearest_valley:
        return ind

    # Calculate move toward valley with PROPER RANGE CHECKING
    if current_day < nearest_valley:
        # Move forward - ensure we have a valid range
        max_possible_shift = min(max_shift, nearest_valley - current_day)
        if max_possible_shift > 0:  # Only move if range is valid
            shift = random.randint(1, max_possible_shift)
            new_day = current_day + shift
        else:
            return ind  # Cannot move forward
    else:
        # Move backward - ensure we have a valid range
        max_possible_shift = min(max_shift, current_day - nearest_valley)
        if max_possible_shift > 0:  # Only move if range is valid
            shift = random.randint(1, max_possible_shift)
            new_day = current_day - shift
        else:
            return ind  # Cannot move backward

    # Apply feasibility check
    if is_move_feasible(act_idx, new_day, ind):
        ind[act_idx] = new_day
        #print(f"  Valley-directed: Act {act_idx} {current_day} → {new_day} (toward valley {nearest_valley})")

    return ind


def find_valleys_simple(daily_gaps, min_gap_diff=5):
    """Find local minima in gap profile - FIXED VERSION"""
    valleys = []
    days = sorted(daily_gaps.keys())

    if len(days) < 3:
        return valleys

    for i in range(1, len(days) - 1):
        prev_gap = daily_gaps[days[i - 1]]
        curr_gap = daily_gaps[days[i]]
        next_gap = daily_gaps[days[i + 1]]

        # Valley: current gap lower than both neighbors
        if (curr_gap < prev_gap and curr_gap < next_gap and
                (prev_gap - curr_gap) > min_gap_diff):
            valleys.append(days[i])

    return valleys


def find_activities_in_high_gap_areas(ind, daily_gaps, valleys, high_gap_threshold=20):
    """Find activities located in high-gap areas near valleys - FIXED VERSION"""
    high_gap_acts = []

    for act_idx, day in enumerate(ind):
        # Skip if activity doesn't exist in current schedule
        if act_idx >= len(ind):
            continue

        # Skip dummy activities
        if duration[act_idx] == 0:
            continue

        if day in daily_gaps and daily_gaps[day] > high_gap_threshold:
            # Check if this high-gap area is near a valley
            for valley in valleys:
                if abs(day - valley) <= 15:  # Within 15 days of a valley
                    high_gap_acts.append(act_idx)
                    break

    return high_gap_acts


def find_nearest_valley(current_day, valleys):
    """Find the valley closest to current day - FIXED VERSION"""
    if not valleys:
        return None

    # Filter out valleys that are too close (would cause range errors)
    valid_valleys = [v for v in valleys if abs(v - current_day) > 0]
    if not valid_valleys:
        return None

    return min(valid_valleys, key=lambda v: abs(v - current_day))


def is_move_feasible(act_idx, new_day, ind):
    """Feasibility check using global pa (predecessors) - FIXED VERSION"""
    # Basic sanity checks
    if new_day < 0:
        return False

    if act_idx >= len(pa) or act_idx >= len(ind):
        return False

    # Check predecessor constraints
    if pa[act_idx]:
        for pred in pa[act_idx]:
            if hasattr(pred, '__iter__'):
                # Handle numpy array or list
                for p in pred:
                    if p < len(ind) and new_day < ind[p] + duration[p]:
                        return False
            else:
                # Single predecessor
                if pred < len(ind) and new_day < ind[pred] + duration[pred]:
                    return False

    return True
def data_mutation(ind):
    lss = copy.deepcopy(ind)
    if np.random.uniform() > 0.1:
        # Your original mutation (50% chance)
        chang3 = random.randint(1, len(duration)-1)
        b = int(np.random.uniform(0, ind[chang3]))
        lss[chang3] = ind[chang3] - b
        lss = aco2_instance.search_path(date_transfer_schedule(lss))
        return lss
    else:
        # Valley-directed mutation (50% chance)
        daily_gaps = calculate_daily_resource_gap(lss, 0, lss[-1])
        mutated_ind = valley_directed_exploitation(lss, daily_gaps, max_shift=5)
        lss = aco2_instance.search_path(date_transfer_schedule(mutated_ind))
        return lss

def local_exploit(winner):
    begin=True
    ite=0
    while begin:
        ite +=1
        if np.random.uniform()<0:
            dg=get_subgraph_act_order2(winner)  ### same logic with get_subgraph_act_order2(best_date_plan), but here is writen by computer, more quick due to the index operation in my code 2
        else:
            dg = get_subgraph_act_order1(winner)
        dg=aco2_instance.search_path(dg)
        #print(dg[-1])
        if dg[-1]<winner[-1]:
            winner=dg
            print("success")
            break
        #else:
        #    print("not success")
        if ite>30:
            break
    return winner


def lag_uniform_crossover_improved(p1_flat, p2_flat, frozen, swap_prob=0.3):
    """
    Focused version - ONLY incoming lags based on dependency type
    """
    p1 = reverse_flatten(p1_flat)
    p2 = reverse_flatten(p2_flat)

    child1 = [row.copy() for row in p1]
    child2 = [row.copy() for row in p2]

    for act_id in range(1, len(p1) + 1):
        act_idx = act_id - 1

        if act_idx >= len(pa):
            continue

        # Only process activities that have incoming lags
        incoming_predecessors = [p for p in pa[act_idx] if p != 0]
        if not incoming_predecessors:
            continue  # Skip activities with no incoming lags (like start)

        incoming_count = len(incoming_predecessors)

        if act_id in frozen:
            # Frozen: protect all incoming lags
            for pred in incoming_predecessors:
                if act_id in c[pred - 1]:
                    pos = c[pred - 1].index(act_id)
                    child1[pred - 1][pos] = p1[pred - 1][pos]
                    child2[pred - 1][pos] = p1[pred - 1][pos]

        elif incoming_count == 1:
            # Independent: exchange individually with probability
            pred = incoming_predecessors[0]  # Only one predecessor
            if act_id in c[pred - 1] and random.random() < swap_prob:
                pos = c[pred - 1].index(act_id)
                child1[pred - 1][pos], child2[pred - 1][pos] = p2[pred - 1][pos], p1[pred - 1][pos]

        else:  # incoming_count > 1
            # Sibling: exchange as group with probability
            if random.random() < swap_prob:
                for pred in incoming_predecessors:
                    if act_id in c[pred - 1]:
                        pos = c[pred - 1].index(act_id)
                        child1[pred - 1][pos] = p2[pred - 1][pos]
                        child2[pred - 1][pos] = p1[pred - 1][pos]

    return flatten_gene(child1), flatten_gene(child2)

def lag_uniform_crossover_improved_1(p1_flat, p2_flat, frozen,swap_prob=0.3):
    """
    Improved uniform crossover with multiple frozen subgraphs
    """
    p1 = reverse_flatten(p1_flat)  # elite
    p2 = reverse_flatten(p2_flat)
    n = len(p1)

    # Simple strategy: protect multiple random subgraphs (no undefined functions needed)


    child1 = [row.copy() for row in p1]
    child2 = [row.copy() for row in p2]

    # Uniform crossover for non-frozen parts
    for i in range(n):
        if (i + 1) not in frozen and random.random() < swap_prob:
            child1[i], child2[i] = child2[i], child1[i]

    # Protect ALL frozen activities' incoming lags
    for j in frozen:
        j0 = j - 1
        for pred in pa[j0]:
            if pred == 0: continue
            try:
                k = c[pred - 1].index(j)
                child1[pred - 1][k] = p1[pred - 1][k]  # From elite
                child2[pred - 1][k] = p1[pred - 1][k]  # From elite
            except ValueError:
                continue

    return flatten_gene(child1), flatten_gene(child2)


def ga_one_by_one(winner,total_schedule):
    starttime=time.time()
    q1 = random.randint(1, nd_activity_num - 1)
    q2 = random.randint(q1, nd_activity_num)
    son2 = winner[:q1] + winner[q2:] + winner[q1:q2]
    son2 = schedule_to_answer(date_transfer_schedule(son2))
    #son2 = schedule_transger_date(date_transfer_schedule(son2))
    winnerset=[]
    tk1 = []
    tk2= []
    countbest=0
    insupwinner = []
    while total_schedule <=50000 and winner[-1]>opm:
        q1 = random.randint(1, nd_activity_num - 1)
        q2 = random.randint(q1, nd_activity_num)
        son21 = son2[:q1] + winner[q1:q2] + son2[q2:]
        son22 = winner[:q1] + son2[q1:q2] + winner[q2:]
        son23 = son2[:q1] + winner[q1:]
        son24=winner[:q2]+son2[q2:]
        son21=choice([son21,son22,son23,son24])
        son3 = aco2_instance.search_path(date_transfer_schedule(son21))
        #son3 = schedule_to_answer(date_transfer_schedule(son21))
        mutationgroup= []
        #son4=schedule_single_crossover(winner,son21)
     #  dg2=shiyan(winner)
        tk1.append(winner[-1])
        tk2.append(min(tk1))
        countbest = bestcount(tk2)

                    #break
            #mutationgroup.append(bca)
        #print("a",a[-1])
        #dg2 = aco2_instance.search_path(dg2)
        dg = gagenind()
        dg = feasiblesequnce(dg)
        #z=copy.deepcopy(dg)
        dg0 = date_transfer_schedule(winner)
        dg, dg1 = oneplusonecrossover(dg, dg0)
        #dg = schedule_to_answer(dg)
        dg = aco2_instance.search_path(dg)
        #dg1 = schedule_to_answer(dg1)
        dg1 = aco2_instance.search_path(dg1)
      # mutationgroup.append(dg2)
        #z = swap_activity(dg0)
        #dg2 = aco2_instance.search_path(z)
        mutationgroup.append(dg)
        mutationgroup.append(dg1)
        mutationgroup.append(son3)
        mutationgroupopt= []
        for i in range(len(mutationgroup)):
            lss0 = copy.deepcopy(mutationgroup[i])
            lss = data_mutation1(lss0)
            mutationgroupopt.append(lss)
        y=mutationgroupopt
        total_schedule += len(y)
        y=paixu(y)
        if winner[-1] < y[0][-1]:#+rsconstraint(y[0]):
            winner = winner
        else:
            winner = y[0]
            #print(winner[-1],winner)
        son2 = y[1]
        print(total_schedule,starttime-time.time(),winner[-1],(winner[-1]-opm)/opm*100,rsconstraint(winner),countbest)
        if countbest>500:
            mode=False
            break
            return winner,winner[-1],total_schedule,mode


    return winner,winner[-1],total_schedule,mode

def find_cpm(s):
    flat_s=flatten_gene(correct_aon_lag(s))
    flat_cpm=[]
    for i in flat_s:
        flat_cpm.append(0)
    cpm_date=make_a_date_plan(reverse_flatten(flat_cpm))
    return cpm_date[-1]

def ga(winner,ft):

    print(duration)
    print(rsl)
    print(pa)
    print(rc)
    starttime = time.time()



    if winner != None:
        winner=winner
    else:
        winner = aco2_instance.search_path_ini(1)[0]
    #winner=[0, 0, 0, 0, 6, 6, 7, 17, 7, 7, 9, 3, 9, 30, 9, 17, 39, 39, 17, 17, 23, 18, 22, 38, 27, 37, 51, 27, 55, 31, 24, 47, 24, 45, 24, 38, 38, 17, 50, 48, 45, 46, 39, 51, 18, 62, 67, 40, 49, 47, 36, 56, 83, 61, 46, 88, 53, 62, 72, 76, 82, 83, 49, 51, 48, 53, 69, 87, 57, 90, 59, 74, 102, 75, 76, 96, 67, 60, 94, 84, 100, 69, 57, 67, 83, 76, 102, 85, 60, 106, 95, 94, 102, 84, 106, 84, 90, 107, 94, 88, 96, 98, 107, 110, 112, 102, 98, 115, 105, 126, 113, 119, 109, 107, 113, 123, 122, 116, 129, 127, 135, 137]


    cpm_date=find_cpm(winner)
    print("cpm",cpm_date)
    # winner=[0, 0, 0, 31, 32, 9, 33, 18, 37, 9, 21, 68, 43, 34, 53, 44, 68, 23, 37, 74, 18, 23, 87, 44, 51, 33, 43, 49, 60, 76, 59, 54, 96, 80, 105, 96, 105, 94, 76, 68, 122, 86, 94, 81, 86, 113, 123, 104, 114, 76, 123, 125, 133, 106, 137, 104, 126, 123, 140, 141, 127, 148]
    total_schedule = 0

    q1 = random.randint(1, nd_activity_num - 1)
    q2 = random.randint(q1, nd_activity_num)
    son2 = winner[:q1] + winner[q2:] + winner[q1:q2]
    son2 = schedule_to_answer(date_transfer_schedule(son2))
    # son2 = schedule_transger_date(date_transfer_schedule(son2))
    winerset = []
    tk1 = []
    tk2 = []
    countbest = 0
    winerset = [winner]
    temp=son2
    s_num=0
    mode=True
    population=[]
    opp=0
    for i in range(10):
        population.append(aco2_instance.search_path_ini(1)[0])
    starttime = time.time()
    while total_schedule <= 50000 and winner[-1] > opm:
        #print("EEEEE",len(population))
        mutationgroup = []

        for i in range(len(population)):

            son2=population[i]
            temp=population[i]

            q1 = random.randint(1, nd_activity_num - 1)
            q2 = random.randint(q1, nd_activity_num)

            bca = aco2_instance.search_path(genson(winner, q1, q2))
            if bca[-1] < winner[-1]:
                #print("yes", bca[-1])
                winner = bca
                mutationgroup.append(bca)
            #if bca[-1]<son2[-1]:
            #    son2=bca


            son21 = son2[:q1] + winner[q1:q2] + son2[q2:]
            son22 = winner[:q1] + son2[q1:q2] + winner[q2:]
            son23 = son2[:q1] + winner[q1:]
            son24 = winner[:q2] + son2[q2:]
            son21 = choice([son21, son22, son23, son24])





            son3 = aco2_instance.search_path(date_transfer_schedule(son21))
            mutationgroup.append(son3)
            if  np.random.uniform()<0.1 :
                flat_temp = flatten_gene(correct_aon_lag(temp))
                flat_winner = flatten_gene(correct_aon_lag(winner))
                #frozen=get_frozen()
                frozen = get_frozen_with_unwanted_exclusion()
                if np.random.uniform() < 0.1:
                #ind3, ind4 = lag_uniform_crossover(flat_temp, flat_winner)
                    if np.random.uniform() < 10.5:

                        lag_mute = lag_mutate_node_centric(flat_temp,frozen)
                        #date = make_a_date_plan(reverse_flatten(lag_mute))
                        #flat_temp=flatten_gene(correct_aon_lag(date))
                        flat_temp=lag_mute
                    #else:
                    #    lag_mute = block_shift_mutation(flat_temp)
                    #    flat_temp = lag_mute

                ind3, ind4 = lag_uniform_crossover_improved(flat_temp, flat_winner,frozen)
                #ind3, ind4 = lag_two_point_crossover1(flat_temp, flat_winner, frozen)





                ind3 = make_a_date_plan(reverse_flatten(ind3))
                ind3 = aco2_instance.search_path(date_transfer_schedule(ind3))

                ind4 = make_a_date_plan(reverse_flatten(ind4))
                ind4 = aco2_instance.search_path(date_transfer_schedule(ind4))

                mutationgroup.append(ind3)
                mutationgroup.append(ind4)

        # son3 = schedule_to_answer(date_transfer_schedule(son21))

        # son4=schedule_single_crossover(winner,son21)
        #  dg2=shiyan(winner)
        tk1.append(winner[-1])
        tk2.append(min(tk1))
        countbest = bestcount(tk2)
        # knownwinner = [0, 9, 0, 0, 7, 13, 22, 18, 9, 30, 10, 37, 30, 54, 37, 46, 24, 55, 45, 39, 56, 65, 67, 30, 62, 65, 47,70, 71, 72, 72, 80]
        # mutationgroup.append(knownwinner)

                    # break
            # mutationgroup.append(bca)
        # print("a",a[-1])
        # dg2 = aco2_instance.search_path(dg2)
        dg = gagenind()
        dg = feasiblesequnce(dg)
        # z=copy.deepcopy(dg)
        dg0 = date_transfer_schedule(winner)
        dg, dg1 = oneplusonecrossover(dg, dg0)
        # dg = schedule_to_answer(dg)
        dg = aco2_instance.search_path(dg)
        # dg1 = schedule_to_answer(dg1)
        dg1 = aco2_instance.search_path(dg1)
        # mutationgroup.append(dg2)
        # z = swap_activity(dg0)
        # dg2 = aco2_instance.search_path(z)
        mutationgroup.append(dg)
        mutationgroup.append(dg1)





       # mutationgroup.append(winner)
        #utationgroup.append(son4)
        mutationgroupopt= []
        for i in range(len(mutationgroup)):

            mutationgroupopt.append(mutationgroup[i])
            lss0 = copy.deepcopy(mutationgroup[i])
            #if np.random.uniform() < 0.5:
            lss = data_mutation1(lss0)
            mutationgroupopt.append(lss)
            if  np.random.uniform()<0.1:
                flat_lss = flatten_gene(correct_aon_lag(lss0))
                if np.random.uniform()<0.50:
                    lag_mute = lag_mutate_node_centric(flat_lss,frozen=None)
                else:
                    lag_mute = block_shift_mutation(flat_lss)

                date = make_a_date_plan(reverse_flatten(lag_mute))
                date[-1] +=rsconstraint(date)
                #lss1 = aco2_instance.search_path(date_transfer_schedule(date))
                mutationgroupopt.append(date)
                lss1 = aco2_instance.search_path(date_transfer_schedule(date))
                mutationgroupopt.append(lss1)

        y=mutationgroupopt+population
        y=redundentmove(y)
        total_schedule += len(y)
        y=paixu(y)
        if len(y)<5:
            for i in range(5-len(y)):
                #print("YES")
                new=aco2_instance.search_path_ini(1)[0]
                y.append(new)
        y=y[:5]
        tempvalue=copy.deepcopy(winner[-1])
        if winner[-1] < y[0][-1]:  # +rsconstraint(y[0]):
            winner = winner
        elif winner[-1] == y[0][-1]:
            winner = y[0]
        elif winner[-1] > y[0][-1]:
            if rsconstraint(y[0])==0:
                print("find new solution")
                print(y[0])
            winner=y[0]

        if winner not in winerset and rsconstraint(winner) ==0:
            winerset.append(winner)
        #winner=winerset[-1]
        if mode==True and opp<0:
            winner,winner[-1],total_schedule,mode=ga_one_by_one(winerset[-1],total_schedule)
            tk1 = []
            tk2 = []
            opp +=1
            mode=False
        if countbest>500:
            mode=True

        son2=y[1]
        #temp = sample(y[1:5], 1)[0]
        population=y
        print(ft,"wwwwwwww",len(population),winerset[-1][-1],rsconstraint(winerset[-1]))






        #print(c)
        #print(file_name, opm)
        #print("ssssssssssssssss",winner)
        print(total_schedule,starttime-time.time(),winner[-1],(winner[-1]-opm)/opm*100,rsconstraint(winner),countbest)
        if countbest>1200:
            tk1 = []
            tk2 = []
            countbest = 0
            population=[]
            for i in range(10):
                ind=genind()
                #ind= schedule_to_answer(date_transfer_schedule(ind))
                population.append(ind)


         #print(date_transfer_schedule(winner))

        #3print(countbest)
        #if time.time()-starttime>300:
        #    break

    return winerset[-1],winerset[-1][-1]
nd_activity_num = 120

import re
problem_type="j120.sm/"

#filelist=os.listdir(problem_type)


filelist=['j12031_8.sm']
winner=None
#winner=[0, 0, 0, 0, 1, 19, 6, 2, 14, 6, 39, 33, 7, 23, 6, 23, 29, 9, 13, 29, 16, 7, 28, 33, 5, 23, 28, 38, 2, 23, 16, 28, 63, 31, 36, 33, 42, 36, 56, 54, 68, 15, 32, 39, 29, 71, 48, 42, 58, 49, 49, 24, 24, 52, 15, 67, 61, 54, 38, 67, 62, 3, 56, 62, 66, 82, 19, 23, 38, 33, 71, 19, 62, 73, 86, 39, 75, 29, 48, 39, 80, 15, 46, 48, 55, 73, 49, 54, 63, 75, 66, 80, 78, 52, 75, 49, 91, 92, 85, 69, 83, 97, 81, 81, 83, 78, 64, 83, 75, 71, 94, 88, 82, 91, 86, 93, 92, 102, 101, 105, 102, 110]











#winner= [0, 0, 0, 4, 5, 10, 5, 18, 5, 23, 23, 10, 10, 17, 4, 10, 34, 44, 11, 16, 58, 28, 11, 17, 26, 17, 20, 51, 26, 37, 38, 26, 20, 48, 18, 35, 10, 10, 80, 70, 14, 50, 28, 28, 45, 59, 62, 37, 61, 59, 46, 87, 51, 44, 62, 71, 17, 59, 95, 95, 71, 105, 27, 59, 109, 50, 52, 37, 102, 46, 27, 75, 61, 76, 86, 52, 64, 105, 64, 117, 71, 95, 72, 79, 112, 90, 79, 73, 102, 64, 109, 118, 75, 95, 75, 76, 79, 125, 85, 96, 76, 85, 122, 87, 96, 123, 116, 105, 109, 102, 114, 109, 118, 103, 122, 118, 126, 129, 127, 127, 133, 141]

#filelist=['j12047_2.sm','j12047_3.sm','j12047_4.sm','j12047_5.sm','j12047_6.sm','j12047_7.sm','j12047_8.sm','j12047_9.sm']

fopt = open('120cpm.txt', 'r')
line_counter = 0
raw_lines = fopt.read().splitlines()
fopt.close()
# opt = [[0 for col in range(11)] for raw in range(int(len(raw_lines)/10)+1)]
# ans = [[0 for col in range(11)] for raw in range(int(len(raw_lines)/10)+1)]
opt = [[0 for col in range(11)] for raw in range(61)]
ans = [[0 for col in range(11)] for raw in range(61)]
for line in raw_lines:
    ints = list(map(int, re.findall(r'\d+', line)))
    opt[ints[0]][ints[1]] = ints[2]

count=0
diff=0.0
better = 0
cout=0
import csv
totzero=0

tot_time=0.0
tot_deviation=0.0
f = open(problem_type[:-4] + 'detail1212_5000.txt', 'a+')
ff = open(problem_type[:-4] + 'detail1212_5000.txt', 'a+')
for item in filelist:
    file_name = item
    ids=file_name.split('_')
    opm=(opt[int(ids[0][4:])][int(ids[1][:-3])])
    clean()
    print(file_name,opm)
    loda_data(problem_type+file_name)
    #aco_instance = aco.RCPSP(problem_type+file_name)
    aco2_instance = aco2.RCPSP(problem_type+file_name)
    aco2_instance.new()
    loop_limit = 4
    loop_tot = 0
    final_search_set = []
    best_date = []
    best_duration = 1000
    tt1= time.time()
    schedulenumber=0
    ga_result_date, ga_result_duration = ga(winner,filelist)
    #while schedulenumber<5000:
        #ga_result_date, ga_result_duration,schedulenumber = ga()
    #   ga_result_date, ga_result_duration,schedulenumber= gabreak(ga_result_date,schedulenumber)
    sorted_nums = sorted(enumerate(ga_result_date), key=lambda x: x[1])
    ga_path = [i[0] for i in sorted_nums]
    #print("GA date", ga_result_date)
    # print("GA path", ga_path)
    # print("GA 工期", ga_result_duration)

    if ga_result_duration < best_duration:
        # aco_instance.ga_update_pheromone_gragh(ga_result_date, ga_result_duration)
        best_duration = ga_result_duration
        best_date = ga_result_date
    t2= time.time()
    deviation = round((best_duration-opm)*100/opm, 3)
    total_time = round(t2-tt1,2)
    tot_time+=total_time
    tot_deviation+=deviation
    print("date：", best_date)
    print("date：", best_duration, " opm", opm, 'deviation', deviation, "% use time", total_time, "s")
    if deviation == 0:
        totzero+=1
    f.write(item[:-3] + " " + str(best_date) + " " + str(best_duration)+ " " + str(deviation)+" "+ str(total_time) + '\n')
    ff.write(item[:-3] + " " + str(best_duration) + " " + str(deviation) + '\n')
f.write(str(round(tot_deviation/len(filelist),3) )+ '\n')
f.write( str(round(tot_time/len(filelist),3)))
print(str(round(tot_deviation/len(filelist),3) )+ '\n')
print( str(round(tot_time/len(filelist),3)))
f.close()
ff.close()
print(totzero)
