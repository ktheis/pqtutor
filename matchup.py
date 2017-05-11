__author__ = 'Karsten2'

# check symbols that get overwritten
# check on-the-fly-expressions for valid syntax
#

from collections import defaultdict, OrderedDict
from itertools import permutations

from calculator import scan, calc, calc2, State, make_paired_tokens, create_Python_expression, classify_input
from quantities import Units, Q

import io

feedback = '''
 * * * * * * * *
*  1: PERFECT!  *
*  2: AWESOME!  *
*  3: SUBLIME!  *
 * * * * * * * *
'''

feedback = '''
 * * * * * * * *
*  1: %s!  *
*  2: %s!  *
*  3: %s!  *
 * * * * * * * *
'''

model = '''T_gas = 243 K
m[N2] = 1.3452 g
V[N2] = 25.9 mL
P_gas = ?
R_gas = 8.314 J / (K mol)
M[N2] = 28 g/mol
n[N2] = m[N2] / M[N2]
P_gas = n[N2] R_gas T_gas / V[N2]'''

stud1 = '''T = 243 K
m_ = 1.3452 g
V_ = 25.9 mL
V2 = 394.0 mL
P = ?
R = 8.314 J / (K mol)
M_ = 28 g/mol
n = m_ / M_
P = n R T / V_'''

stud2 = '''T = 24.3 K
m2 = 15412.5 g
m_ = 1.3452 kg
V_ = 25.9 mm
P = ?
R = 8.314 J / (K mol)
M_ = 28 g/mol
n = m_ / M_
P = n R T / V_'''

stud3 = '''T = 243.00 K
m_ = 1.3452 g
V_ = 25.9 mL
P = ?
'''

stud4 = '''T = 243 K
m_ = 1.3452 g
V_ = 25.9 g
M_ = 28 g/mol
P = m_ 8.314 J / (K mol) T / V_'''

stud5 = '''T = 313 K
R = 8.314 J /(K mol)
K_ = 3.4E-27
DelG = R T ln(K_)'''

def levenshtein(s1, s2):
    '''edit distance between two strings'''
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

Empty, Calculation, ConversionIn, ConversionUsing, Comment, Flags, Unknown = range(7)

def classified_expressions(input, state):
    '''
    :param input: PQcalc input
    :yields: type of input and additional information for every value/calculation in the input
    '''
    input_section = None
    unk = 0
    for line in input.splitlines():
        type, name, expression = classify_input(line, state)
        if type in (Empty, Comment, Flags):
            continue
        if type == Unknown:
            yield('Unknown', name)
            continue
        parsed = scan(expression)
        paired, comment = make_paired_tokens(parsed)
        expression2 = create_Python_expression(paired, state)
        print(expression2)
        if parsed[-2][1] == '':
            parsed = parsed[:-2]
        if any(p[0] == 'I' for p in parsed) or sum(1 for p in parsed if p[0] == 'N') > 1:
           snucks = set()
           for i, p in enumerate(parsed):
                if p[0] == 'N' and i + 2 < len(parsed) and parsed[i+2][0] == 'U':
                    j = i + 1
                    while j < len(parsed) and parsed[j][0] in 'OU':
                        j += 1
                    exp2 = ' '.join(p2[1] for p2 in parsed[i:j])
                    name2 = 'Snuck' + str(unk)
                    unk += 1
                    snucks.add(name2)
                    yield ('Snuck', name2 + ' = ' + exp2, name2, exp2, input_section)
                if i >= 2 and p[0] == 'U' and parsed[i-2][0] not in 'UN':
                    print('#################Panic, unit without number:', line)
                if p[0] == 'I' and p[1] not in state and p[1].startswith('M[') and p[1].endswith(']'):
                    yield ('Assign', p[1]+' = '+ p[1], p[1], p[1], input_section)
                    snucks.add(p[1])
           if name not in state:
               yield ('Calc', name, expression, input_section,
                   {p[1] for p in parsed if p[0] == 'I'}|snucks,
                   {p[1] for p in parsed if p[0] == 'F'},
                   {p[1] for p in parsed if p[0] == 'O'})
        else:
            yield ('Assign', line, name, expression, input_section)

inputq = '''Q(Fraction(1, 200), 'a', Units(kg=1), 0.0, {'g'})+Q(0.0043, '', Units(kg=1), 0.00010000000000000002, {'g'})'''


def collect_inputs(input, doubledip=False, snuck=True):
    '''
    Figures out which parts of input are assignments, and stores them ordered by dimension
    :param input: PQcalc input for analysis
    :param storage: names of variables stored in lists with common dimensions
    :param qstore: qstore[name] = quantity with that name
    :return:
    '''
    answers = []
    storage = defaultdict(list)
    qstore = dict()
    cstore = OrderedDict()
    state = State()
    for line in input.splitlines():
        type, name, q, expression = calc2(line, state)
        if type == 'Unknown':
            answers.append(name)
            continue
        if type not in ('Calc', 'Known'):
            continue
        q.calc = False
        if type == 'Calc':
            parsed = scan(expression)
            q.I = {p[1] for p in parsed if p[0] == 'I'}
            q.F = {p[1] for p in parsed if p[0] == 'F'}
            q.O = {p[1] for p in parsed if p[0] == 'O'}
            q.expression = expression
            q.calc = True
        state[name] = q

    snucks = set()
    for name in state:
        try:
            state[name].calc
        except:
            state[name].calc = False
        q = state[name]
        if name.startswith('Snuck'):
            snucks.add(name)
            state[name].calc = False
        '''
        For some reason, "a using kg" erases the provenance, so need to check differently
        '''
        if not q.calc or (q.name=='-%s' and not q.provenance[0].provenance):
            q.inquestion = False
            if snuck or not name.startswith('Snuck') or q.uncert or q.units != Units():
                storage[q.units].append(name)
        else:
            q.inquestion = False
            if doubledip and not name in answers:
                storage[q.units].append(name)
            q.I.update(snucks)
            snucks = set()
            cstore[name] = (q.I, q.F, q.O, q.expression) # I F O expression
        qstore[name] = q
    return storage, qstore, cstore, answers


from comments import typicalunits
from collections import namedtuple

Quant_score = namedtuple('Quant_score', 'numerical units number uncert name bonus')

def quant_score(units, number, uncert, name, bonus):
    score = 0
    score += [0, 35, 45, 50][number]
    score += [0, 10][uncert]
    score += [0, 7][name]
    score += [0, 40][units]
    score += bonus
    return Quant_score(min(100, score), units, number, uncert, name, bonus)

def similarity(n1, n2, q1, q2, bonus = 0):
    number = uncert = name = 0
    if q1.uncert and q2.uncert:
        if abs(q1.number - q2.number)*4 < q1.uncert + q2.uncert:
            number = 3
        elif abs(q1.number - q2.number)*2 < q1.uncert + q2.uncert:
            number = 2
        elif abs(q1.number - q2.number) < q1.uncert + q2.uncert:
            number = 1
        if q1.uncert < 1.5 * q2.uncert and q1.uncert * 1.5 > q2.uncert:
            uncert = 1
        elif q1.uncert == q2.uncert:
            uncert = 1
            print('************************************ wah ***************************************')
    elif q2.uncert:
        if abs(q1.number - q2.number) < 2 * q2.uncert:
            number = 3
    else:
        if q1.number == q2.number:
            number = 3
        uncert = 1
    s = n2[0] if n1 else '&'
    if not n2.startswith('Snuck'):
        if s == 'Δ' and len(n2 > 2):
            s = n2[1]
        if s in typicalunits and typicalunits[s][0] == q2.units:
            name = 1
        elif n1 and n2 and n1[0] == n2[0]:
            name = 1
    return quant_score(1, number, uncert, name, bonus)



def high_quality_matches(ddict_model, ddict_student, qstore1, qstore2):
    match1 = dict()
    match2 = dict()
    scores = dict()
    for dim in ddict_model:
        for q1 in ddict_model[dim]:
            for q2 in ddict_student[dim]:
                if q2 in match2:
                    continue
                score = similarity(q1, q2, qstore1[q1], qstore2[q2], bonus=0)
                # print(score, q1, q2, repr(q1), repr(q2))
                if score.numerical >= 90:
                    match1[q1] = q2
                    match2[q2] = q1
                    scores[q1] = score
                    break
    return match1, match2, scores


def shallow_matches(ddict_model, qstore1, ddict_student, qstore2, match1, match2, scores):
    for dim2 in ddict_student:
        for q2 in ddict_student[dim2]:
            if q2 in match2:
                continue
            bests = Quant_score(-100, 0,0,0,0,0)
            bestn = None
            for dim1 in ddict_model:
                for q1 in ddict_model[dim1]:
                    if q1 in match1:
                        continue
                    s1 = str(qstore1[q1])
                    s2 = str(qstore2[q2])
                    worst = max(len(s1), len(s2))
                    fallback = (worst - levenshtein(s1, s2)) * 40 / worst
                    if qstore1[q1].units == qstore2[q2].units:
                        score = similarity(q1, q2, qstore1[q1], qstore2[q2], bonus=fallback)
                    else:
                        score = Quant_score(fallback, 0,0,0,0, fallback)
                    if score.numerical > bests.numerical:
                        bests = score
                        bestn = q1
            if not bestn or bests.numerical < 19:
                continue
            score = bests
            #rint(bests, score, q2.name, bestn, qstore1[bestn], qstore2[q2.name])
            if score.numerical >= 19:
                match1[bestn] = q2
                match2[q2] = bestn
                scores[bestn] = score


def all_dependencies(name, cstore, qstore):
    '''
    Obtain all leaves of the dependency tree (not the nodes, though)
    :param name: name of calculated quantity
    :param cstore: all calculated quantities
    :param qstore: all quantities, calculated or not
    :return: {leaves}
    '''
    dep = set()
    for child in cstore[name][0]:
        if child in dep:
            continue
        elif child in cstore and not child == name:
            dep = dep | all_dependencies(child, cstore, qstore)
        else:
            dep.add(child)
    dep = [d for d in dep if (qstore[d].units != Units() or qstore[d].uncert)]
    return set(dep)

Calc_score = namedtuple('Quant_score', 'numerical dependency units number name')

def calc_score(dependency, units, number, name):
    score = 5
    score += dependency
    if units:
        score += 25
    if number:
        score += 20
    if name:
        score += 5
    return Calc_score(min(100, score), dependency, units, number, name)


def similarity_calc(n1, n2, q1, q2, dep1, dep2, match2, f1, o1, f2, o2):
    '''
    Score how similar two calculations are.
    50 pts for correct dependencies, 25 pts for units, 20 pts for value, 5 pts bonus for good name
    :param q1: quantity
    :param q2:
    :param dep1: dependencies
    :param dep2:
    :param match2: maps names
    :param f1: functions
    :param o1: operators
    :param f2:
    :param o2:
    :return: score 0..100
    '''
    units = number =  1
    dependency = name = 0
    dep2t = {(match2[d2] if d2 in match2 else 'unmatched_'+d2) for d2 in dep2}
    print('\nI am now matching', q1, '(+/-)', '%.2g' % q1.uncert, 'with', q2, '(+/-)', '%.2g' % q2.uncert)
    if q1.units != q2.units:
        print('\tunit mismatch', q1, q2)
        units = 0
    elif abs(q1.number - q2.number) > abs(q1.uncert + q2.uncert)/2:
        print('\tvalue mismatch', q1, q2)
        number = 0
    if n1[0] == n2[0]:
        print('\tname match', n1, n2)
        name = 1
    print('\toperators:', o1, o2, '\tfunctions:', f1, f2)
    matches = dep1 & dep2t
    leftovers = dep1 - dep2t
    if not leftovers:
        print('\t', ', '.join((str(d2)+'<=>'+str(match2[d2]) for d2 in dep2)))
        dependency = 50
    else:
        dependency = 50 * (1 - len(leftovers) / len(dep1))
        print ('\t', dependency, matches, leftovers)
        print('dependency', dep1, dep2t)
    return calc_score(dependency, units, number, name)

def calculation_matches(cstore1, qstore1, cstore2, qstore2, match1, match2, answers1, answers2, scores):
    if answers1:
        names1 = [n for n in cstore1 if n in answers1]
    else:
        names1 = [next(reversed(cstore1))]
    #rint (names1)
    names2 = [n for n in cstore2]
    #rint (names2)
    items = len(names1)
    success = 0
    matched = 0
    for name1 in reversed(names1):
        i1, f1, o1, ex1 = cstore1[name1]
        dep1 = all_dependencies(name1, cstore1, qstore1)
        bestscore = Calc_score(-100, 0, 0, 0, 0)
        bestname = None
        for name2 in reversed(names2):
            if name2 in match2:
                continue
            i2, f2, o2, ex2 = cstore2[name2]
            all_dep = all_dependencies(name2, cstore2, qstore2)
            score = similarity_calc(name1, name2, qstore1[name1], qstore2[name2],
                                    dep1, all_dep, match2,
                                    f1, o1, f2, o2)
            if score.numerical >= 95:
                match1[name1] = name2
                match2[name2] = name1
                scores[name1] = score
                success += score.numerical
                matched += 1
                print('\nLook no further: ', name1, name2, '%4.1f' % score.numerical, score)
                break
            if score.numerical > bestscore.numerical:
                bestscore = score
                bestname = name2
        else:
            if bestscore.numerical > 50:
                match1[name1] = bestname
                match2[bestname] = name1
                scores[name1] = score
                success += score.numerical
                matched += 1
                print('\nNot great, but best bet: ', name1, bestname,  '%4.1f' % score.numerical, score)
                names2.remove(bestname)
    return success/100, matched, items

def report_matches(ddict_model, qstore1, ddict_student, qstore2, match1, match2, scores):
    print('\nmatch report:')
    for m1 in match1:
        m2 = match1[m1]
        print('\t', scores[m1].numerical, m1, 'with', m2, qstore1[m1], qstore2[m2], scores[m1])
    if any(q not in match1 for dim in ddict_model for q in ddict_model[dim]):
        print('unmatched model quantities:')
    for dim in ddict_model:
        for q in ddict_model[dim]:
            if q not in match1:
                print(' + ', q, qstore1[q])
    if any(q not in match2 for dim in ddict_student for q in ddict_student[dim]):
        print('unmatched student quantities:')
    for dim in ddict_student:
        for q in ddict_student[dim]:
            if q not in match2:
                print(' + ', q, qstore2[q])
    print('end of match report\n')

def collection_done(student_answer, model_answer):
    print('******************* Checking collection *******************************')
    print('\n'.join(s for s in student_answer.splitlines() if s))
    print('_____________________________________________')
    print(model_answer)
    f = io.StringIO('')
    model_commands = model_answer.splitlines()[1:]
    if '=' not in model_commands[0]:
        model_commands.pop(0)
    ddict_model, qstore1, cstore1, answers1 = collect_inputs('\n'.join(model_commands), snuck=False)
    print('model: \n', '\n'.join(q for q in qstore1), '\n', '\n'.join(str(d) for d in ddict_model))
    ddict_student, qstore2, cstore2, answers2 = collect_inputs(student_answer, doubledip=True)
    match1, match2, scores = high_quality_matches(ddict_model, ddict_student, qstore1, qstore2)
    print(sum(1 for q in qstore1 if not qstore1[q].calc), len(match1))
    #rint(ddict_model, match1)
    shallow_matches(ddict_model, qstore1, ddict_student, qstore2, match1, match2, scores)
    for name in match2:
        if name in cstore2:
            del(cstore2[name])
    report_matches(ddict_model, qstore1, ddict_student, qstore2, match1, match2, scores)
    nr_assignments = sum(len(ddict_model[d]) for d in ddict_model for q in ddict_model[d] if not qstore1[q].name.startswith('M['))
    print(scores)
    perfect = sum(scores[s].numerical for s in scores)/(100 * nr_assignments)
    return len(scores) == nr_assignments


def checkanswer(student_answer, model_answer):
    print('******************* Grading *******************************')
    print('\n'.join(s for s in student_answer.splitlines() if s))
    print('_____________________________________________')
    print(model_answer)
    f = io.StringIO('')
    model_commands = model_answer.splitlines()[1:]
    if '=' not in model_commands[0]:
        model_commands.pop(0)
    ddict_model, qstore1, cstore1, answers1 = collect_inputs('\n'.join(model_commands), snuck=False)
    print('model: \n', '\n'.join(q for q in qstore1), '\n', '\n'.join(str(d) for d in ddict_model))
    ddict_student, qstore2, cstore2, answers2 = collect_inputs(student_answer, doubledip=True)
    match1, match2, scores = high_quality_matches(ddict_model, ddict_student, qstore1, qstore2)
    print(sum(1 for q in qstore1 if not qstore1[q].calc), len(match1))
    #rint(ddict_model, match1)
    shallow_matches(ddict_model, qstore1, ddict_student, qstore2, match1, match2, scores)
    for name in match2:
        if name in cstore2:
            del(cstore2[name])
    report_matches(ddict_model, qstore1, ddict_student, qstore2, match1, match2, scores)
    nr_assignments = sum(len(ddict_model[d]) for d in ddict_model)
    print(scores)
    perfect = sum(scores[s].numerical for s in scores)/(100 * nr_assignments)
    missing = sum(1 for d in ddict_model for q in ddict_model[d] if not(q in match1 or q.name.startswith('M['))) / nr_assignments
    mismatched = 1 - perfect - missing
    if nr_assignments:
        pounds = round(7 * mismatched)
        if not pounds and any(scores[s].numerical != 100 for s in scores):
            pounds = 1
        letters = round(7 * perfect)
        if perfect and not letters:
            letters = 1
        undersc = 7 - pounds - letters
        #rint(f'knowns ... nr:{nr_assignments}, +:{perfect:.0%}, huh:{mismatched:.0%}, missing:{missing:.0%}')
        #rint("knowns ... nr:{}, +:{:.0%}, huh:{:.0%}, missing:{:.0%}".format(nr_assignments, perfect, mismatched, missing))
        part1score = 'PERFECT'[:letters] + '#' * pounds + '_' * undersc
    else:
        part1score = 'NOKnown'
    #rint(letters, pounds, undersc)
    print(feedback % (part1score, '_______', '_______'))


    recalc = False
    for q2 in qstore2:
        if q2 not in match2:
            continue
        q1 = match2[q2]
        if 19 < scores[q1].numerical < 100:
            #rint(f'fixing (?) {q2}:{repr(qstore2[q2])}')
            qstore2[q2] = qstore1[q1]
            #rint(f'fixed (?) {q2}:{repr(qstore2[q2])}, score was {scores[q1]}')
            recalc = True

    if recalc:
        newstate = State()
        for q2 in qstore2:
            newstate[q2] = qstore2[q2]
        for q2 in cstore2:
            _, _, _, exp = cstore2[q2]
            type_text, name, quantity, expression = calc2(exp, newstate)
            qstore2[q2] = quantity

    #rint('\n\ncheck formula\n\n')
    #rint(f'model answers: {answers1}\n student answers: {answers2}')
    #print(all_dependencies('P_gas', cstore1, qstore1))
    cscore, cmatched, citems = calculation_matches(cstore1, qstore1, cstore2, qstore2, match1, match2, answers1, answers2, scores)
    if citems:
        succ = int(7 * cscore / citems)
        noty = int(7 * (citems - cmatched) / citems)
        pounds = 7 - succ - noty
        #rint(f'{citems} steps, {cmatched} matches, {cscore}')
        part3score = 'SUBLIME'[:succ] + '#'*pounds + '_'* noty
    else:
        part3score = 'NO CALC'
    #rint(feedback % (part1score, '_______', part3score), file=f)
    s = f.getvalue()
    f.close()
    w = '<h3>Writing down what you know: {:.0%}</h3>'.format(perfect)
    if citems:
        r = '<h3>Credit for result: {:.0%}</h3>'.format(cscore / citems)
    else:
        r = '<h3>no results?</h3>'
    #rint(s)
    outp = []
    result, good_input, = calc(State(), '\n'.join(model_commands))
    _, brief_work, _, _, _ =  result
    return r+w+ brief_work



def print_dep(cstore, var, depth, qstore, trans=None):
    print('\t'*(depth-1), trans[var] if (trans and var in trans) else var, qstore.get(var))
    for dep in cstore[var][0]:
        if dep in cstore:
            print_dep(cstore, dep, depth + 1, qstore, trans)
        else:
            print('\t'*depth, trans[dep] if (trans and dep in trans) else dep, qstore.get(dep))

'''
for var in cstore1:
    break
    if any(var in dep for v in cstore1 for dep in cstore1[v][0]):
        continue
    print_dep(cstore1, var, 1, qstore1)


for var in cstore2:
    break
    if any(var in dep for v in cstore2 for dep in cstore2[v][0]):
        continue
    print_dep(cstore2, var, 1, qstore2, match2)
'''

question = '''One of the frequencies used to transmit and receive cellular telephone signals in the United States is 850 MHz. What is the wavelength in meters of these radio waves?
'''
answer = '''ν = 850. MHz
λ = ?
@ c0 = ν λ
c0 = 298792458 m / s
λ = c0 /ν
λ using cm
'''

queue = []
"""
def choicenator(options, question='Which option?'):
    #return options[0]
    print('\n'*8, '_'*40)
    print(question)
    options = options.split(', ')
    if queue:
        options.extend(queue)
    for i, op in enumerate(options):
        print('{}: {}'.format(i, op))
        if not i:
            print()
    answer = input('>>>>')
    if not answer:
        return options[0]
    try:
        nr = int(answer)
        return options[nr]
    except:
        queue.append(answer)
        if len(queue) > 3:
            queue.pop(0)
        return 'manually entered:' + answer

from collections import Counter
from can2 import signatures

def dimdep(q, counter):
    for child in q.provenance:
        if not child.provenance:
            counter[child.units] += 1
        else:
            dimdep(child, counter)

from can2 import pretty_dim

def guess_formula(q, chapter):
    dimcount = Counter()
    dimcount[q.units] += 1
    dimdep(q, dimcount)
    signature = frozenset((units, 1 if dimcount[units] == 1 else 2) for units in dimcount)
    if signature in signatures:
        guesses = []
        for formula, chap, discr in reversed(signatures[signature]):
            if chap == chapter:
                guesses.insert(0, (formula, chap, discr))
            elif chap < chapter:
                guesses.append((formula, chap, discr))
        if len(guesses) == 1:
            if '#' in guesses[0][0]:
                return guesses[0][0].split('#')[1]
            return 'Jonas...'
        else:
            for formula, chap, discr in guesses:
                pass #rint('maybe', chap, discr, formula)
            return ', '.join(g[0].split('#')[1] for g in guesses)

    if len(signature) == 1:
        if q.name == 'is %s':
            return 'Identity'
        if all(dimcount[d] == 3 for d in dimcount) and q.name in ('%s + %s', '%s - %s'):
            return 'change in quantity'
    for dim, multi in signature:
        print(pretty_dim(dim)*(2 if multi>1 else 1), end=', ')

    print(signature)
    return 'Whatchamacallit'

from nameit import pronounce, SuperSpecials

'''<h3>Example 3.4b: Deriving Grams from Moles for an Element</h3>
What is the mass of 2.561 mol of gold?
<h4>Answer:</h4>
n[Au] = 2.561 mol #@! known_explicit
m[Au] = ? #@! unknown
M[Au] = M[Au] #@! known_data periodic table
m[Au] = n[Au] M[Au] #@! calculation_answer
The mass of the gold sample is 504.4 gram. #@! interpretation
'''

def add_annotation(question, answer, chapter):
    answers = []
    phase1 = []
    phase2 = []
    phase3 = []
    phase4 = []
    lastcalc = None
    #rint(question)
    doctored_question = question.replace('<em>','').replace('</em>','').replace('-g',' g').replace('-M',' M')
    state = State()
    phase = 0
    for line in answer.splitlines():
        #rint('_' * 40)
        #rint(line)
        type, name, q, expression = calc2(line, state, keep_provenance = False)
        if '#' in line:
            previous_comment = line.split('#')[1] + ', '
        else:
            previous_comment = ''
        if type == 'Unknown':
            nome = choicenator(previous_comment + pronounce(name),
                                 'What is a good name for this quantity?{}'.format(line.split("=")[0]))
            #rint(f'{line}  # looking for {nome}')
            answers.append(f'{}  # looking for {}'.format(line, nome))
        elif type == 'Comment' and line:
            if line.startswith('Think about it'):
                phase = 4
            if phase == 4:
                phase4.append(line)
            elif phase == 3:
                phase3.append(line)
            elif phase == 2:
                phase2.append(line)
            else:
                phase1.append(line)
        if not expression:
            continue
        expression = expression.strip()
        if type == 'Known':
            numberstring = expression.split(' ')[0]
            if not phase:
                phase = 1
            doctored_expression = expression.replace('°aC', '°C').replace('°aC', '°ΔC').replace('. ',' ')
            if doctored_expression in doctored_question:
                #rint(f'{line}  # known quantity from question')
                phase1.append('{}  # known quantity from question'.format(line))
            else:
                if name in SuperSpecials:
                    bestchoice = 'Physical constant ({}), '.format(SuperSpecials[name])
                else:
                    bestchoice = ''
                source = choicenator(previous_comment + bestchoice + 'question, periodic table, question (implicit), physical constant, data table',
                                     f'How do you know {pronounce(name)}|{line}|{doctored_question}? From...')
                #rint(f'{line}  # known quantity from {source}')
                if source == 'question':
                    phase1.append(f'{line}  # known quantity from {source}')
                else:
                    phase2.append(f'{line}  # known quantity from {source}')
        elif type == 'Calc':
            if phase < 3:
                phase = 3
            formula_name = guess_formula(q, chapter)
            if formula_name == 'Whatchamacallit':
                print(q, chapter, '_'*10, expression)
            source = choicenator(previous_comment + formula_name + ', Stoich ratio, Change in quantity', f'What formula is that: |{line}|?')
            #rint(f'{line}  # formula {source}')
            phase3.append(f'{line}  # formula {source}')
            lastcalc = line
    if answers:
        phase1.extend(answers)
    elif lastcalc:
        unknown = lastcalc.split('=')[0].strip()
        nome = choicenator(pronounce(unknown),
                           f'What is a good name for this quantity?|{unknown}|')
        answers.append(f'{unknown} = ?  # looking for {nome}')
    with open('annotation.txt', 'a', encoding='utf-8') as logfile:
        print(question, file=logfile)
        print('<Read question>', file=logfile)
        for line in phase1:
            print(line, file=logfile)
        for line in answers:
            print(line, file=logfile)
        if phase2:
            print('<Plan and collect>', file=logfile)
        for line in phase2:
            print(line, file=logfile)
        print('<Calculation>', file=logfile)
        for line in phase3:
            print(line, file=logfile)
        for line in phase4:
            print(line, file=logfile)

import sqlite3

def get_examples():
    connection = sqlite3.connect(database='examples')
    cursor = connection.cursor()
    cursor.execute("SELECT * from homework")
    for result in cursor:
        yield result
    connection.close()


def get_expressions():
    for a in get_examples():
        if a[1].endswith('b') and a[1].startswith(''):
            try:
                chapter = int(a[1][:-1].split('.')[0])
            except ValueError:
                chapter = 0
            yield a[2], a[3], chapter

if __name__ == '__main__':
    print('hello')
    for question, answer, chapter in get_expressions():
        if chapter != 4:
            continue
        #rint(question)
        add_annotation(question, answer, chapter)
"""
