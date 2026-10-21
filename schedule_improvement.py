import re, copy, random, os, time
global ant_num
ant_num =1
delta_t, p, a, pga =  0.00001, 0.1, 0.9, 0.99
activity_num = 0
R = []
d = []
r = []
suc_act = []
pre_act = []
LS = []
LF = []
ES = []
EF = []
T = 0
pheromone_graph = []
init_resource_left = []
resource_usage=[]


def load_data(path_to_file):
    f = open(path_to_file, 'r')
    raw_lines = f.read().splitlines()
    f.close()
    data = {'E': {}, 'd': [], 'r': []}
    line_counter = 0
    for line in raw_lines:
        ints = list(map(int, re.findall(r'\d+', line)))
        if len(ints) == 0:
            line_counter += 1
            continue
        else:
            if line_counter < 18:
                if 'jobs' in line:
                    data['n'] = int(ints[0])
                elif 'horizon' in line:
                    data['T'] = int(ints[0])
                elif '- renewable' in line:
                    data['n_res'] = int(ints[0])
            elif 18 <= line_counter < 18 + data['n']:
                jobnr = int(ints[0]) - 1
                data['E'][jobnr] = [int(succ) - 1 for succ in ints[3:]]
            elif 18 + data['n'] + 4 <= line_counter < 18 + 2 * data['n'] + 4:
                data['d'].append(int(ints[2]))
                data['r'].append([int(x) for x in ints[3:]])
            elif line_counter == 18 + 2 * data['n'] + 4 + 3:
                data['R'] = [int(x) for x in ints]
            line_counter += 1
    activities = {}
    for j in range(data['n']):
        pred = [i for i in range(j) if j in data['E'][i]]
        act = Activity(j, pred, data['E'][j], data['d'][j], data['r'][j])
        activities[j] = act
    project_name = os.path.basename(os.path.normpath(os.path.splitext(path_to_file)[0]))
    project = Project(project_name, activities, data['R'], data['T'])

    return project


class Activity():
    def __init__(self, id, pred, succ, d, r):
        self.id = id
        self.pred = pred
        self.succ = succ
        self.d = d
        self.r = r

class Project():
    def __init__(self, name, act, R, T):
        self.name = name
        self.act = act
        self.V = [i for i in act]  # activities
        self.E = [(i, j) for i in self.V for j in act[i].succ]
        self.n = len(act) - 2
        self.R = R
        self.K = range(len(R))
        self.T = T
        self.forward_pass()
        self.backward_pass()

    def forward_pass(self):
        n = self.n
        self.act[0].ES = 0
        self.act[0].EF = 0
        for j in range(1, n + 2):
            self.act[j].ES = max(self.act[i].EF for i in self.act[j].pred)
            self.act[j].EF = self.act[j].ES + self.act[j].d

    def backward_pass(self):
        n = self.n
        self.act[n + 1].LF = self.T
        self.act[n + 1].LS = self.T
        for j in range(n, -1, -1):
            self.act[j].LF = min(self.act[i].LS for i in self.act[j].succ)
            self.act[j].LS = self.act[j].LF - self.act[j].d


class Ant(object):

    def __init__(self, ID):

        self.ID = ID
        self.__clean_data()

    def __clean_data(self):
        self.path = []
        self.date = []
        self.total_duration = 0
        self.move_count = 0
        self.candidate_activity = [True for i in range(activity_num)]
        self.resource_left = copy.deepcopy(init_resource_left)
        self.current_activity = 0
        self.next_activity = -1
        self.path.append(0)
        self.date.append(0)
        self.candidate_activity[0] = False
        self.move_count = 1
        self.SB = [T for i in range(activity_num)]
        self.SF = [T for i in range(activity_num)]
        self.SFTB = [T for i in range(activity_num)]
        self.TB = []
        self.TF = []
        self.TFB = []
        self.rs_left_TF=[]
        self.rs_left_SB=[]
        self.rs_left_SFTB=[]

    def __choose_next_activity_ini(self):

        self.next_activity = -1
        select_activities_prob = [0.0 for i in range(activity_num)]
        total_prob = 0.0
        maxlft=0
        dg=[]
        for i in range(activity_num):
            if self.candidate_activity[i]:
                temp_flag = 1
                for j in pre_act[i]:
                    if self.candidate_activity[j]:
                        temp_flag = 0
                        break
                if temp_flag == 0:
                    select_activities_prob[i] = 0
                else:
                    maxlft=max(maxlft,LF[i])
                    dg.append(i)

        for j in dg:
            select_activities_prob[j]=(maxlft-LF[j]+1)
            total_prob+=select_activities_prob[j]
        if total_prob > 0.0:
            temp_prob = random.uniform(0.0, total_prob)
            for i in dg:
                temp_prob -= select_activities_prob[i]
                if temp_prob < 0.0:
                    self.next_activity = i
                    break
        return self.next_activity

    def __move(self, start_time_for_next, cost_day):

        self.path.append(self.next_activity)
        self.date.append(start_time_for_next)
        self.candidate_activity[self.next_activity] = False
        self.total_duration = max(start_time_for_next + cost_day, self.total_duration)
        self.current_activity = self.next_activity
        self.move_count += 1
    def __choose_next_activity_mid(self):

        self.next_activity = -1
        select_activities_prob = [1.0/activity_num for i in range(activity_num)]
        total_prob = 0.0
        for i in range(activity_num):
            if self.candidate_activity[i]:
                temp_flag = 1
                for j in pre_act[i]:
                    if self.candidate_activity[j]:
                        temp_flag = 0
                        break
                if temp_flag == 0:
                    select_activities_prob[i] = 0
                else:
                    select_activities_prob[i] = 0.1
                    total_prob += select_activities_prob[i]


        if total_prob > 0.0:
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(activity_num):
                if self.candidate_activity[i]:
                    temp_prob -= select_activities_prob[i]
                    if temp_prob < 0.0:
                        self.next_activity = i
                        break

        return self.next_activity

    def __choose_next_activity_mid2(self):

        self.next_activity = -1
        select_activities_prob = [0.0 for i in range(activity_num)]
        total_prob = 0.0
        LSmax = 0.0

        for i in range(activity_num):
            if self.candidate_activity[i]:
                temp_flag = 1
                for j in pre_act[i]:
                    if self.candidate_activity[j]:
                        temp_flag = 0
                        break
                if temp_flag == 0:
                    select_activities_prob[i] = 0
                else:
                    LSmax = max(LSmax, LS[i])

        for i in range(activity_num):
            if self.candidate_activity[i]:
                temp_flag = 1
                for j in pre_act[i]:
                    if self.candidate_activity[j]:
                        temp_flag = 0
                        break
                if temp_flag == 0:
                    select_activities_prob[i] = 0
                else:
                    select_activities_prob[i] = pheromone_graph[i][self.move_count] * ((LSmax - LS[i] + 1) / LSmax)
                    total_prob += select_activities_prob[i]
                    # print('select_activities_prob[i]',select_activities_prob[i],i)

        if total_prob > 0.0:
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(activity_num):
                if self.candidate_activity[i]:
                    temp_prob -= select_activities_prob[i]
                    if temp_prob < 0.0:
                        self.next_activity = i
                        break

        return self.next_activity


    def search_path_mid(self, path, sep1,sep2):
        global prob, prob_backup
        global resource_usage
        self.__clean_data()
        resource_usage=[0 for i in range(T+1)]
        for i in range(sep1):
            self.candidate_activity[path[i]]=False
        for i in range(sep2,activity_num):
            self.candidate_activity[path[i]]=False


        while self.move_count < activity_num:
            if self.move_count<sep1 or self.move_count>=sep2:
               self.next_activity = path[self.move_count]
            else:
                self.next_activity =self.__choose_next_activity_mid()
                # print('mmid',self.next_activity)
            cost_day = d[self.next_activity]
            scheduled = 0
            start_time_for_next = 0
            for i in pre_act[self.next_activity]:
                index_i = self.path.index(i)
                start_time_for_next = max(start_time_for_next, self.date[index_i] + d[i])
            while scheduled == 0:
                r_enough = 1
                for i in range(cost_day):
                    for j in range(len(R)):
                        if self.resource_left[start_time_for_next + i][j] - r[self.next_activity][j] < 0:
                            r_enough = 0
                            break
                if r_enough:
                    for cost_dayi in range(cost_day):
                        self.resource_left[start_time_for_next + cost_dayi] = list(map(lambda x: x[0] - x[1], zip(
                            self.resource_left[start_time_for_next + cost_dayi], r[self.next_activity])))
                    scheduled = 1
                else:
                    start_time_for_next += 1
            self.__move(start_time_for_next, cost_day)

        resource_usage = self.resource_left
        I = self.path
        sorted_nums = sorted(enumerate(self.path), key=lambda x: x[1])
        SFI = [self.date[i[0]] for i in sorted_nums]
        sorted_nums = sorted(enumerate(self.date), key=lambda x: (x[1], self.path[x[0]]))
        TFI = [self.path[i[0]] for i in sorted_nums]
        self.SF = SFI
        self.TF = TFI
        self.rs_left_TF = resource_usage
        I_reversed = list(reversed(I))
        SBI, sb_usage = self.toSB(I_reversed)
        sorted_nums = sorted(enumerate(SBI), key=lambda x: (x[1], x[0]))
        TBI = [i[0] for i in sorted_nums]
        self.SB = SBI
        self.TB = TBI
        self.rs_left_SB = sb_usage
        SFTBI, sf_usage= self.toSF(self.TB)
        sorted_nums = sorted(enumerate(SFTBI), key=lambda x: (x[1], x[0]))
        TFI = [i[0] for i in sorted_nums]
        self.SFTB = SFTBI
        self.rs_left_SFTB = sf_usage
        self.TFB = TFI

    def search_path_mid2(self, path, sep1,sep2):
        global resource_usage
        self.__clean_data()
        resource_usage=[0 for i in range(T+1)]
        for i in range(sep1):
            self.candidate_activity[path[i]]=False
        for i in range(sep2,activity_num):
            self.candidate_activity[path[i]]=False


        while self.move_count < activity_num:
            if self.move_count<sep1 or self.move_count>=sep2:
               self.next_activity = path[self.move_count]
            else:
                self.next_activity =self.__choose_next_activity_mid2()
                # print('mmid',self.next_activity)

            cost_day = d[self.next_activity]
            scheduled = 0
            start_time_for_next = 0
            for i in pre_act[self.next_activity]:
                index_i = self.path.index(i)
                start_time_for_next = max(start_time_for_next, self.date[index_i] + d[i])
            while scheduled == 0:
                r_enough = 1
                for i in range(cost_day):
                    for j in range(len(R)):
                        if self.resource_left[start_time_for_next + i][j] - r[self.next_activity][j] < 0:
                            r_enough = 0
                            break
                if r_enough:
                    for cost_dayi in range(cost_day):
                        self.resource_left[start_time_for_next + cost_dayi] = list(map(lambda x: x[0] - x[1], zip(
                            self.resource_left[start_time_for_next + cost_dayi], r[self.next_activity])))
                    scheduled = 1
                else:
                    start_time_for_next += 1
            self.__move(start_time_for_next, cost_day)

        resource_usage = self.resource_left
        I = self.path
        sorted_nums = sorted(enumerate(self.path), key=lambda x: x[1])
        SFI = [self.date[i[0]] for i in sorted_nums]
        sorted_nums = sorted(enumerate(self.date), key=lambda x: (x[1], self.path[x[0]]))
        TFI = [self.path[i[0]] for i in sorted_nums]
        self.SF = SFI
        self.TF = TFI
        self.rs_left_TF = resource_usage
        I_reversed = list(reversed(I))
        SBI, sb_usage = self.toSB(I_reversed)
        sorted_nums = sorted(enumerate(SBI), key=lambda x: (x[1], x[0]))
        TBI = [i[0] for i in sorted_nums]
        self.SB = SBI
        self.TB = TBI
        self.rs_left_SB = sb_usage
        SFTBI, sf_usage= self.toSF(self.TB)
        sorted_nums = sorted(enumerate(SFTBI), key=lambda x: (x[1], x[0]))
        TFI = [i[0] for i in sorted_nums]
        self.SFTB = SFTBI
        self.rs_left_SFTB = sf_usage
        self.TFB = TFI


    def search_path(self, path):

        global resource_usage
        self.__clean_data()
        resource_usage=[0 for i in range(T+1)]

        while self.move_count < activity_num:
            # print('self.move_count')
            self.next_activity = path[self.move_count]
            cost_day = d[self.next_activity]
            scheduled = 0
            start_time_for_next = 0

            for i in pre_act[self.next_activity]:
                index_i = self.path.index(i)
                start_time_for_next = max(start_time_for_next, self.date[index_i] + d[i])
            while scheduled == 0:
                r_enough = 1
                for i in range(cost_day):
                    for j in range(len(R)):
                        if self.resource_left[start_time_for_next + i][j] - r[self.next_activity][j] < 0:
                            r_enough = 0
                            break
                if r_enough:
                    for cost_dayi in range(cost_day):
                        self.resource_left[start_time_for_next + cost_dayi] = list(map(lambda x: x[0] - x[1], zip(
                            self.resource_left[start_time_for_next + cost_dayi], r[self.next_activity])))
                    scheduled = 1
                else:
                    start_time_for_next += 1
            self.__move(start_time_for_next, cost_day)

        resource_usage = self.resource_left
        I = self.path
        sorted_nums = sorted(enumerate(self.path), key=lambda x: x[1])
        SFI = [self.date[i[0]] for i in sorted_nums]
        sorted_nums = sorted(enumerate(self.date), key=lambda x: (x[1], self.path[x[0]]))
        TFI = [self.path[i[0]] for i in sorted_nums]
        self.SF = SFI
        self.TF = TFI
        self.rs_left_TF = resource_usage
        I_reversed = list(reversed(I))
        SBI, sb_usage = self.toSB(I_reversed)
        sorted_nums = sorted(enumerate(SBI), key=lambda x: (x[1], x[0]))
        TBI = [i[0] for i in sorted_nums]
        self.SB = SBI
        self.TB = TBI
        self.rs_left_SB = sb_usage
        SFTBI, sf_usage= self.toSF(self.TB)
        sorted_nums = sorted(enumerate(SFTBI), key=lambda x: (x[1], x[0]))
        TFI = [i[0] for i in sorted_nums]
        self.SFTB = SFTBI
        self.rs_left_SFTB = sf_usage
        self.TFB = TFI


    def search_path_ini(self):

        self.path = [0]
        self.move_count = 0
        self.date = [0]
        self.total_duration = 0
        self.resource_left = copy.deepcopy(init_resource_left)
        self.candidate_activity = [True for i in range(activity_num)]
        self.next_activity = -1
        self.candidate_activity[0] = False
        self.move_count = 1
        self.SB = [T for i in range(activity_num)]
        self.SF = [T for i in range(activity_num)]
        self.SFTB = [T for i in range(activity_num)]
        self.TB = []
        self.TF = []
        self.TFB = []
        self.rs_left_TF = []
        self.rs_left_SB = []
        self.rs_left_SFTB = []

        while self.move_count < activity_num:

            # self.next_activity = self.__choose_next_activity_ini()
            self.next_activity = -1
            select_activities_prob = [0.0 for i in range(activity_num)]
            total_prob = 0.0
            maxlft = 0
            dg = []
            for i in range(activity_num):
                if self.candidate_activity[i]:
                    temp_flag = 1
                    for j in pre_act[i]:
                        if self.candidate_activity[j]:
                            temp_flag = 0
                            break
                    if temp_flag == 0:
                        select_activities_prob[i] = 0
                    else:
                        maxlft = max(maxlft, LF[i])
                        dg.append(i)

            for j in dg:
                select_activities_prob[j] = (maxlft - LF[j] + 1)
                total_prob += select_activities_prob[j]
            if total_prob > 0.0:
                temp_prob = random.uniform(0.0, total_prob)
                for i in dg:
                    temp_prob -= select_activities_prob[i]
                    if temp_prob < 0.0:
                        self.next_activity = i
                        break
            cost_day = d[self.next_activity]
            scheduled = 0
            start_time_for_next = 0

            for i in pre_act[self.next_activity]:
                index_i = self.path.index(i)
                start_time_for_next = max(start_time_for_next, self.date[index_i] + d[i])
            while scheduled == 0:
                r_enough = 1
                for i in range(cost_day):
                    for j in range(len(R)):
                        if self.resource_left[start_time_for_next + i][j] - r[self.next_activity][j] < 0:
                            r_enough = 0
                            break
                if r_enough:
                    for cost_dayi in range(cost_day):
                        self.resource_left[start_time_for_next + cost_dayi] = list(map(lambda x: x[0] - x[1], zip(
                            self.resource_left[start_time_for_next + cost_dayi], r[self.next_activity])))
                    scheduled = 1
                else:
                    start_time_for_next += 1
            self.__move(start_time_for_next, cost_day)
        resource_usage = self.resource_left
        I = self.path
        sorted_nums = sorted(enumerate(self.path), key=lambda x: x[1])
        SFI = [self.date[i[0]] for i in sorted_nums]
        sorted_nums = sorted(enumerate(self.date), key=lambda x: (x[1], self.path[x[0]]))
        TFI = [self.path[i[0]] for i in sorted_nums]
        self.SF = SFI
        self.TF = TFI
        self.rs_left_TF = resource_usage
        I_reversed = list(reversed(I))
        SBI, sb_usage = self.toSB(I_reversed)
        sorted_nums = sorted(enumerate(SBI), key=lambda x: (x[1], x[0]))
        TBI = [i[0] for i in sorted_nums]
        self.SB = SBI
        self.TB = TBI
        self.rs_left_SB = sb_usage
        SFTBI, sf_usage = self.toSF(self.TB)
        sorted_nums = sorted(enumerate(SFTBI), key=lambda x: (x[1], x[0]))
        TFI = [i[0] for i in sorted_nums]
        self.SFTB = SFTBI
        self.rs_left_SFTB = sf_usage
        self.TFB = TFI

    def search_path_ini_1(self):

        self.path = [0]
        self.move_count = 0
        self.date = [0]
        self.total_duration = 0
        self.resource_left = copy.deepcopy(init_resource_left)
        self.candidate_activity = [True for i in range(activity_num)]
        self.next_activity = -1
        self.candidate_activity[0] = False
        self.move_count = 1
        self.SB = [T for i in range(activity_num)]
        self.SF = [T for i in range(activity_num)]
        self.SFTB = [T for i in range(activity_num)]
        self.TB = []
        self.TF = []
        self.TFB = []
        self.rs_left_TF = []
        self.rs_left_SB = []
        self.rs_left_SFTB = []

        while self.move_count < activity_num:

            # self.next_activity = self.__choose_next_activity_ini()
            self.next_activity = -1
            select_activities_prob = [0.0 for i in range(activity_num)]
            total_prob = 0.0
            maxlft = 0
            dg = []
            for i in range(activity_num):
                if self.candidate_activity[i]:
                    temp_flag = 1
                    for j in pre_act[i]:
                        if self.candidate_activity[j]:
                            temp_flag = 0
                            break
                    if temp_flag == 0:
                        select_activities_prob[i] = 0
                    else:
                        dg.append(i)

            self.next_activity=dg[random.randint(0,len(dg)-1)]
            cost_day = d[self.next_activity]
            scheduled = 0
            start_time_for_next = 0

            for i in pre_act[self.next_activity]:
                index_i = self.path.index(i)
                start_time_for_next = max(start_time_for_next, self.date[index_i] + d[i])
            while scheduled == 0:
                r_enough = 1
                for i in range(cost_day):
                    for j in range(len(R)):
                        if self.resource_left[start_time_for_next + i][j] - r[self.next_activity][j] < 0:
                            r_enough = 0
                            break
                if r_enough:
                    for cost_dayi in range(cost_day):
                        self.resource_left[start_time_for_next + cost_dayi] = list(map(lambda x: x[0] - x[1], zip(
                            self.resource_left[start_time_for_next + cost_dayi], r[self.next_activity])))
                    scheduled = 1
                else:
                    start_time_for_next += 1
            self.__move(start_time_for_next, cost_day)
        resource_usage = self.resource_left
        I = self.path
        sorted_nums = sorted(enumerate(self.path), key=lambda x: x[1])
        SFI = [self.date[i[0]] for i in sorted_nums]
        sorted_nums = sorted(enumerate(self.date), key=lambda x: (x[1], self.path[x[0]]))
        TFI = [self.path[i[0]] for i in sorted_nums]
        self.SF = SFI
        self.TF = TFI
        self.rs_left_TF = resource_usage
        I_reversed = list(reversed(I))
        SBI, sb_usage = self.toSB(I_reversed)
        sorted_nums = sorted(enumerate(SBI), key=lambda x: (x[1], x[0]))
        TBI = [i[0] for i in sorted_nums]
        self.SB = SBI
        self.TB = TBI
        self.rs_left_SB = sb_usage
        SFTBI, sf_usage = self.toSF(self.TB)
        sorted_nums = sorted(enumerate(SFTBI), key=lambda x: (x[1], x[0]))
        TFI = [i[0] for i in sorted_nums]
        self.SFTB = SFTBI
        self.rs_left_SFTB = sf_usage
        self.TFB = TFI

    def toSB(self, I_reversed):
        rs_left = copy.deepcopy(init_resource_left)
        SB = [T for i in range(activity_num)]
        sb_move_count = 1

        while sb_move_count < activity_num:

            SB_next_activity = I_reversed[sb_move_count]
            cost_day = d[SB_next_activity]
            scheduled = 0
            finish_time_for_next = T
            for i in suc_act[SB_next_activity]:
                finish_time_for_next = min(finish_time_for_next, SB[i])
            while scheduled == 0:
                r_enough = 1
                for i in range(cost_day):
                    for j in range(len(R)):
                        if rs_left[finish_time_for_next - i][j] - r[SB_next_activity][j] < 0:
                            r_enough = 0
                            break
                if r_enough:
                    for cost_dayi in range(cost_day):
                        rs_left[finish_time_for_next - cost_dayi] = list(map(lambda x: x[0] - x[1], zip(
                            rs_left[finish_time_for_next - cost_dayi], r[SB_next_activity])))
                    scheduled = 1
                else:
                    finish_time_for_next -= 1
            SB[SB_next_activity] = finish_time_for_next - cost_day
            sb_move_count += 1

        bias = SB[0]
        for i in range(activity_num):
            SB[i] -= bias
        return SB, rs_left

    def toSF(self, I):
        rs_left = copy.deepcopy(init_resource_left)
        SF = [0 for i in range(activity_num)]
        sf_move_count = 1

        while sf_move_count < activity_num:

            SF_next_activity = I[sf_move_count]
            cost_day = d[SF_next_activity]
            scheduled = 0
            start_time_for_next = 0
            for i in pre_act[SF_next_activity]:
                start_time_for_next = max(start_time_for_next, SF[i] + d[i])
            while scheduled == 0:
                r_enough = 1
                for i in range(cost_day):
                    for j in range(len(R)):
                        if rs_left[start_time_for_next + i][j] - r[SF_next_activity][j] < 0:
                            r_enough = 0
                            break
                if r_enough:
                    for cost_dayi in range(cost_day):
                        rs_left[start_time_for_next + cost_dayi] = list(map(lambda x: x[0] - x[1], zip(
                            rs_left[start_time_for_next + cost_dayi], r[SF_next_activity])))
                    scheduled = 1
                else:
                    start_time_for_next += 1
            SF[SF_next_activity] = start_time_for_next
            sf_move_count += 1

        return SF, rs_left




class RCPSP(object):

    def __init__(self, file_name):
        global activity_num, R, d, r, suc_act, pre_act, LS, LF, T, init_resource_left, pheromone_graph
        project = load_data(file_name)
        V = project.V
        E = project.E
        activity_num = project.n + 2
        R = project.R
        d = [project.act[i].d for i in V]
        r = [project.act[i].r for i in V]
        suc_act = [project.act[i].succ for i in V]
        pre_act = [project.act[i].pred for i in V]
        self.suc_act=suc_act
        self.pre_act=pre_act
        self.d=d
        self.r=r
        self.R=R

        LS = [project.act[i].LS for i in V]
        LF = [project.act[i].LF for i in V]
        ES = [project.act[i].ES for i in V]
        EF = [project.act[i].EF for i in V]
        T = project.T
        self.ES = ES
        self.LS = LS
        self.LF = LF
        self.EF = EF

        init_resource_left = [[Ri for Ri in R] for timestep in range(T + 1)]
        pheromone_graph = [[delta_t for col in range(activity_num)] for raw in range(activity_num)]

        self.new()

    def new(self):
        self.ant =Ant(0)
        self.ants = [Ant(ID) for ID in range(ant_num)]
        self.iter = 1
        self.best_ant = Ant(-1)
        self.best_ant.total_duration = T
        self.n = activity_num

    def search_path(self, path):
        for i in range(len(path)):
            path[i] -= 1
        self.ant.search_path(path)

        if self.ant.SF[-1] <= self.ant.total_duration:
            self.ant.path = self.ant.TF
            self.ant.date = self.ant.SF
            self.ant.total_duration = self.ant.SF[-1]
            resource_usage = self.ant.rs_left_TF

        if self.ant.SB[-1] < self.ant.total_duration:
            self.ant.path = self.ant.TB
            self.ant.date = self.ant.SB
            self.ant.total_duration = self.ant.SB[-1]
            resource_usage = self.ant.rs_left_SB


        if self.ant.SFTB[-1] < self.ant.total_duration:
            self.ant.path = self.ant.TFB
            self.ant.date = self.ant.SFTB
            resource_usage = self.ant.rs_left_SFTB
            self.ant.total_duration = self.ant.SFTB[-1]
        # for i in range(self.ant.total_duration):

            # r1_usage = (R[0]-resource_usage[i][0]) / R[0]
            # r2_usage = (R[1]-resource_usage[i][1]) / R[1]
            # r3_usage = (R[2]-resource_usage[i][2]) / R[2]
            # r4_usage = (R[3]-resource_usage[i][3]) / R[3]
            # print(r1_usage, r2_usage, r3_usage, r4_usage)


        return self.ant.date

    def search_path_mid(self, path,sep1,sep2):
        for i in range(len(path)):
            path[i]-=1
        # print(path)
        self.ant.search_path_mid(path,sep1,sep2)

        if self.ant.SF[-1] <= self.ant.total_duration:
            self.ant.path = self.ant.TF
            self.ant.date = self.ant.SF
            self.ant.total_duration = self.ant.SF[-1]
            resource_usage = self.ant.rs_left_TF

        if self.ant.SB[-1] < self.ant.total_duration:
            self.ant.path = self.ant.TB
            self.ant.date = self.ant.SB
            self.ant.total_duration = self.ant.SB[-1]
            resource_usage = self.ant.rs_left_SB


        if self.ant.SFTB[-1] < self.ant.total_duration:
            self.ant.path = self.ant.TFB
            self.ant.date = self.ant.SFTB
            resource_usage = self.ant.rs_left_SFTB
            self.ant.total_duration = self.ant.SFTB[-1]

        return self.ant.date

    def search_path_mid2(self,path,sep1,sep2,iter):
        for i in range(len(path)):
            path[i]-=1
        global prob, prob_backup,pheromone_graph
        pheromone_graph = [[delta_t for col in range(activity_num)] for raw in range(activity_num)]

        self.iter = 1
        while self.iter <= iter:
            for ant in self.ants:
                ant.search_path_mid2(path,sep1,sep2)
                # print('ant.path',ant.path)

                if ant.SF[-1] <= ant.total_duration:
                    ant.path = ant.TF
                    ant.date = ant.SF
                    ant.total_duration = ant.SF[-1]

                if ant.SB[-1] < ant.total_duration:
                    ant.path = ant.TB
                    ant.date = ant.SB
                    ant.total_duration = ant.SB[-1]

                if ant.SFTB[-1] < ant.total_duration:
                    ant.path = ant.TFB
                    ant.date = ant.SFTB
                    ant.total_duration = ant.SFTB[-1]

                if ant.total_duration < self.best_ant.total_duration:
                    self.best_ant = copy.deepcopy(ant)

            # print('iteration',self.iter)
            # print('best date solution until now:',self.best_ant.date)
            # print('best date solution until now:',self.best_ant.path)
            self.__update_pheromone_gragh()
            self.iter += 1
        return self.best_ant.date

    def __update_pheromone_gragh(self):
        # local update
        self.ants.sort(key=lambda ant: ant.total_duration)
        for ant in self.ants:
            for i in range(activity_num):
                pheromone_graph[ant.path[i]][i] += delta_t

        # evaporation
        for i in range(activity_num):
            for j in range(activity_num):
                pheromone_graph[i][j] = pheromone_graph[i][j] * (1 - p)
        # global update
        for i in range(activity_num):
            pheromone_graph[self.best_ant.path[i]][i] = (1-p) / self.best_ant.total_duration + p * \
                                                   pheromone_graph[self.best_ant.path[i]][i]


    def search_path_0(self, path):

        self.ant.search_path(path)

        if self.ant.SF[-1] <= self.ant.total_duration:
            self.ant.path = self.ant.TF
            self.ant.date = self.ant.SF
            self.ant.total_duration = self.ant.SF[-1]
            resource_usage = self.ant.rs_left_TF

        if self.ant.SB[-1] < self.ant.total_duration:
            self.ant.path = self.ant.TB
            self.ant.date = self.ant.SB
            self.ant.total_duration = self.ant.SB[-1]
            resource_usage = self.ant.rs_left_SB


        if self.ant.SFTB[-1] < self.ant.total_duration:
            self.ant.path = self.ant.TFB
            self.ant.date = self.ant.SFTB
            resource_usage = self.ant.rs_left_SFTB
            self.ant.total_duration = self.ant.SFTB[-1]
        # for i in range(self.ant.total_duration):

            # r1_usage = (R[0]-resource_usage[i][0]) / R[0]
            # r2_usage = (R[1]-resource_usage[i][1]) / R[1]
            # r3_usage = (R[2]-resource_usage[i][2]) / R[2]
            # r4_usage = (R[3]-resource_usage[i][3]) / R[3]
            # print(r1_usage, r2_usage, r3_usage, r4_usage)


        return self.ant.date








    def search_path_ini(self,popm):

        group=[]
        for i in range(popm):
            self.ant.search_path_ini()
            if self.ant.SF[-1] <= self.ant.total_duration:
                self.ant.path = self.ant.TF
                self.ant.date = self.ant.SF
                self.ant.total_duration = self.ant.SF[-1]

            if self.ant.SB[-1] < self.ant.total_duration:
                self.ant.path = self.ant.TB
                self.ant.date = self.ant.SB
                self.ant.total_duration = self.ant.SB[-1]

            if self.ant.SFTB[-1] < self.ant.total_duration:
                self.ant.path = self.ant.TFB
                self.ant.date = self.ant.SFTB
                self.ant.total_duration = self.ant.SFTB[-1]
            group.append(self.ant.date)

        return group

    def search_path_ini_1(self,popm):

        group=[]
        for i in range(popm):
            self.ant.search_path_ini_1()
            if self.ant.SF[-1] <= self.ant.total_duration:
                self.ant.path = self.ant.TF
                self.ant.date = self.ant.SF
                self.ant.total_duration = self.ant.SF[-1]

            if self.ant.SB[-1] < self.ant.total_duration:
                self.ant.path = self.ant.TB
                self.ant.date = self.ant.SB
                self.ant.total_duration = self.ant.SB[-1]

            if self.ant.SFTB[-1] < self.ant.total_duration:
                self.ant.path = self.ant.TFB
                self.ant.date = self.ant.SFTB
                self.ant.total_duration = self.ant.SFTB[-1]
            group.append(self.ant.date)

        return group



