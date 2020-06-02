from chemistry import pronounce, Species, interpret_equation, compare_reactions
from chemistry import physconst, typical_units_reverse, typicalunits, good_units, dimension_name, naming_conventions
from calculator import calc, calc2, State
from quantities import Units
from mathparser import scan

from collections import defaultdict, OrderedDict, namedtuple

import random
from fractions import Fraction
from collections import defaultdict as ddict

__author__ = 'Karsten Theis'

"""
Functions to generate hints by comparing student answer to model answer

Call-tree:

generate_hints
    check_so_far
        check_knowns
            collect_inputs
                ->calc2, scan
            high_quality_matches
                similarity
                    quant_score
            shallow_matches
                levenshtein (recursive)
            preliminaries
            solution_structure
                all_dependencies (recursive)
            collect_and_organize_hints
                context
            ->pronounce
        check_calculations
            calculation_matches
                all_dependencies
                similarity_calc
                    calc_score
            fix_knowns
            good_units
            collect_and_organize_hints
        next_steps
            interpret_equation
                element_counter
                    chunk_species
                        matching_closing
            ->pronounce
            compare_reactions
                balancing_issues
                    interpret_equation
                prettyeq
            solution_structure
    flatten
    hint_it
        chapterize
        ->calc

generate_tutor_comments
    check_so_far

check_answer
    high_quality_matches
    report_known_matches
    calculation_hint
        all_dependencies
        ->pronounce
        hint_it
    calculation_matches
    preliminaries
    shallow_matches
    report_calculation_matches
        report_matches
    -> calc
    fix_knowns
        -> calc2
    collect_inputs

"""
# check symbols that get overwritten
# check on-the-fly-expressions for valid syntax
#


def generate_hints (hwid, student_answer, model_answer, question):
    #rint('generating hints')
    try:
        chapter = int(hwid[2].split('.')[0])
    except:
        chapter = 0
    hints, debug_info = evaluate_progress(student_answer, model_answer, question, hwid)
    if not hints or (len(hints) == 1 and ('CO' in hints or 'In' in hints or 'Kn' in hints or 'Sn' in hints or 'A1n' in hints)):
        hints['A1'] = 'all done'
    output = []
    #rint('*'*60)
    for h in hints:
        pass #rint(h, hints[h])
    if 'CO' in hints:
        output.append(hint_it(hwid, chapter, 'CO', '', category=hints['CO']))
    for h in hints:
        if h != 'CO' and h != 'Z':
            output.append(hint_it(hwid, chapter, h, '', category=hints[h]))
    output = [f for f in flatten(output)]
    if any(b in hints for b in 'Kw Ii Ipm !b !f A2 B2'.split()):
        output.extend(hint_it(hwid, chapter, 'err', '', category=''))
    if 'Z' in hints:
        output.extend(hint_it(hwid, chapter, 'Z', '', category=hints['Z']))
    output.extend(hint_it(hwid, chapter, 'z', '', category='arrgh'))
    return output, debug_info


def evaluate_progress(student_answer, model_answer, question, hwid, ignore=None):
    hints = OrderedDict()
    model, student, scores, debug_info = check_knowns(model_answer, question, student_answer, hints, hwid, ignore)
    if hints and any(h not in {'Snu', 'Ksp', 'Kcap', 'Is', 'Ks', 'Is2', 'Ks2', 'Ip', 'CO', 'In', 'Kn', 'Sn', 'Sk'} for h in hints):
        hints['Z'] = 'Reread the question and look for known quantities'
        return hints, debug_info
    debug_info2 = check_calculations(model, question, student, scores, hints, ignore)
    if debug_info2:
        debug_info.append(('model', 'student', 'problems with calculations'))
        debug_info.extend(debug_info2)
    if False and hints and any(h not in {'Snu', 'Ksp', 'Kcap', 'Is', 'Ks', 'Is2', 'Ks2', 'I', 'Ip', 'CO', 'In', 'Kn', 'Sn', 'Sk'} for h in hints):
        return hints, debug_info
    if 'A6b' in hints:
        return hints, debug_info
    if ignore:
        return hints, debug_info
    hints2 = OrderedDict()
    debug_info2 = next_steps(model, student, question, hints2)
    if debug_info2:
        debug_info.append(('model', 'student', 'pumps'))
        debug_info.extend(debug_info2)
    for h in hints:
        hints2[h] = hints[h]
    return hints2, debug_info


def check_knowns(model_answer, question, student_answer, hints, hwid, ignore=None):
    outp = []
    #model_commands = preliminaries(model_answer, student_answer)
    model = collect_inputs(model_answer, question, snuck=False)
    #pprint.print(model)
    ddict_model, qstore1, cstore1, answers1, match1, context1 = model
    solution_structure(qstore1, cstore1, answers1, context1)
    if not answers1 and cstore1:
        answers1.append([cstore1[-1]])
    student = collect_inputs(student_answer, question, is_student=True, doubledip=False, snuck=True)
    _, qstore2, cstore2, answers2, match2, _ = student

    try:
        chapter = int(hwid[2].split('.')[0])
    except:
        chapter = 0
    scores = high_quality_matches(model, student, chapter=chapter)
    shallow_matches(model, student, scores, chapter=chapter)
    data = False
    missing = []
    for qm in qstore1:
        if qstore1[qm].type.startswith('Known_explicit'):
            data = True
            if qm in match1:
                if scores[qm].numerical < 96:
                    if match1[qm].startswith('Snuck'):
                        hints['Sk'] = str(qstore2[match1[qm]])
                    elif scores[qm].number == 3 and scores[qm].units and scores[qm].uncert:
                        hints['Is' if scores[qm].uncert == 2 else 'Is2'] = match1[qm]
                    elif qstore1[qm].number * qstore2[match1[qm]].number < 0.0:
                        hints['Ipm'] = match1[qm]
                    else:
                        hints['Ii'] = match1[qm]
                elif scores[qm].name != 2:
                    s = match1[qm][0]
                    if good_units(s.lower() if s.isupper() else s.upper(), qstore1[qm].units):
                        hints['Kcap'] = match1[qm]
                    else:
                        hints['In'] = match1[qm]

                outp.append((qm, match1[qm], str(scores[qm].numerical)))
            else:
                missing.append(pronounce(qm))
                outp.append((qm, 'missing: ' + pronounce(qm), ' '))
        elif qm not in cstore1:
            outp.append((qm, match1[qm] if qm in match1 else 'not matched yet', ' '))
    for qm in qstore1:
        if qm not in match1 and qstore1[qm].type == 'Known_from_picture':
            hints['Ip'] = pronounce(qm)
    spurious = []
    for qs in qstore2:
        if qs in cstore2:
            continue
        if qs.startswith('Snuck'):
            qn = str(qstore2[qs])
            hints['Snu'] = qn
            continue
        qn = qs if not qs.startswith('Snuck') else str(qstore2[qs])
        if qs not in match2:
            if qs in answers2:
                hints['Work'] = qs
                continue
            q = qstore2[qs]
            if q.units != Units() or q.uncert or q.number not in {1, -1, 2, -2, 3, -3, Fraction(1, 2), Fraction(-1, 2)}:
                s = qn[0]
                n2 = qn
                if s == 'Δ' and len(n2) > 2:
                    s = n2[1]
                hint_spurious = False
                if s in typicalunits and (len(n2) < 2 or n2[1] in '[_' or n2[1].isdigit()):
                    if not good_units(s, q.units):
                        hint_spurious = True
                        if good_units(s.lower() if s.isupper() else s.upper(), q.units):
                            hints['Kcap'] = qn
                        elif q.units == Units():
                            hints['Kspnu'] = qn + ' (' + dimension_name(typicalunits[s]) + '?)'
                        else:
                            hints['Kspn'] = dimension_name(q.units)
                if not hint_spurious:
                    spurious.append(qn)
                outp.append((' ', qs, 'spurious?'))
            else:
                outp.append((' ', qs, 'it makes sense?'))
                continue
        elif qstore1[match2[qs]].type.startswith('Known_explicit'):
            continue
        elif scores[match2[qs]].number != 3:
            hints['Kw'] = qn
        elif scores[match2[qs]].uncert != 0:
            hints['Ks' if scores[match2[qs]].uncert == 2 else 'Ks2'] = qn
        elif scores[match2[qs]].name != 2:
            q = qstore2[qs]
            s = qs[0]
            n2 = qs
            if s == 'Δ' and len(n2) > 2:
                s = n2[1]
            if s in typicalunits and (len(n2) < 2 or n2[1] in '[_' or n2[1].isdigit()):
                if not good_units(s, q.units):
                    if good_units(s.lower() if s.isupper() else s.upper(), q.units):
                        hints['Kcap'] = qn
                    elif q.units == Units():
                        hints['Kspnu'] = qn + ' (' + dimension_name(typicalunits[s]) + '?)'
                    else:
                        hints['Kspn'] = dimension_name(q.units)
            else:
                hints['Kn'] = qn
        elif ignore and qstore2[qs].linenr > ignore:
            hints['Kok'] = qn
    if missing:
        hints['I'] = ' and '.join(missing)
    if spurious:
        hints['Ksp'] = ' and '.join(spurious)

    if not student[1] and data:
        hints.clear()
        hints['K'] ='Get started'

    if not hints:
        for qs in qstore2:
            if len(qs) == 1 and not qs in {'T', 'P', 'R'}:
                hints['Sn'] = qs
    if len(set(qstore1) | set(answers1)) >= 4:
        collect_and_organize_hints(model, student, hints)
    return model, student, scores, outp


def check_calculations(model, question, student, scores, hints, ignore=None):
    outp = []
    recalc = '' #fix_knowns(model, student, scores)
    calculation_matches(model, student, scores)
    ddict_model, qstore1, cstore1, answers1, match1, context1 = model
    ddict_student, qstore2, cstore2, answers2, match2, context2 = student
    for name in qstore2:
        if not name.startswith('Snuck'):
            continue
        value = str(qstore2[name])
        for qn in qstore2:
            if str(qstore2[qn]) == value and not qn.startswith('Snuck'):
                hints['Num'] = qn + ' a.k.a ' + value
    if len(set(qstore1) | set(answers1)) >= 4:
        collect_and_organize_hints(model, student, hints)
    response = None
    for a in cstore1:
        if a not in match1 or a not in scores:
            continue
        student_answer = match1[a]
        if a not in scores:
            pass#rint('waaaaah')
        if scores[a].dependency == 40:
            if scores[a].units == 1:
                if scores[a].number:
                    if recalc:
                        response = 'A0'
                    elif scores[a].name or student_answer in answers2:
                        response = 'A1'
                    else:
                        response = 'A1n'
                else:
                    if len(qstore1[a].N) != len(qstore2[student_answer].N):
                        response = 'A2b'
                    else:
                        response = 'A2'
            else:
                response = 'A3'
                if qstore2[student_answer].units not in typical_units_reverse:
                    response = 'A3a'
            #rint(response)
        else:
            s_dep = all_dependencies(student_answer, cstore2, qstore2)
            m_dep = all_dependencies(a, cstore1, qstore1)
            #rint (s_dep)
            #rint (m_dep)
            m_dep = {match1.get(m, pronounce(m)) for m in m_dep}
            spurious = ' and '.join(c for c in (s_dep - m_dep))
            missing = ' and '.join(m_dep - s_dep)
            if missing:
                moddep = set()
                for child in cstore1[a][0]:
                    if child in match1 and match1[child] not in cstore2[student_answer][0]:
                        moddep |= {child}
                    else:
                        moddep |= all_dependencies(child, cstore1, qstore1)
                moddep = {match1.get(m, pronounce(m)) for m in moddep}
                missing = ' and '.join(c for c in (moddep - s_dep))

            if spurious and missing:
                response = 'A7:' + missing + ' instead of ' + spurious
            elif spurious:
                #rint('student', cstore2[student_answer][0])
                #rint('model', cstore1[a][0])

                #rint('spurious', spurious)
                response = 'A6:' + spurious
            elif missing:
                #rint('missing', missing)
                response = 'A4:' + missing
            else:
                response /= 0
        outp.append((a, student_answer, response))
        if response in ('A1', 'A0') and not ignore:
            continue
        #outp.append((a, student_answer, response))
        if not ignore or qstore2[match1[a]].linenr > ignore:
            hints[response] = pronounce(a)
    for student_answer in cstore2:
        if student_answer in match2:
            if not scores[match2[student_answer]].name:
                hints['A1n'] = student_answer
                s = student_answer[0]
                if good_units(s.lower() if s.isupper() else s.upper(), qstore2[student_answer].units):
                    hints['B3cap'] = student_answer

            continue
        if student_answer in answers2:
            hints['A6b'] = student_answer
        if qstore2[student_answer].units not in typical_units_reverse:
            hints['A3a'] = student_answer #units not used in GenChem
        else:
            n2 = student_answer
            s = n2[0]
            if s == 'Δ' and len(n2) > 2:
                s = n2[1]
            if s in typicalunits and (len(n2)<2 or n2[1] in '[_' or n2[1].isdigit()):
                if good_units(s, qstore2[student_answer].units):
                    if student_answer in answers2:
                        hints['A6a'] = student_answer # listed as answer, good units, wrong value
                    else:
                        hints['B4'] = student_answer # good units, not sure where we are going with this
                else:
                    if good_units(s.lower() if s.isupper() else s.upper(), qstore2[student_answer].units):
                        hints['B3cap'] = student_answer
                    else:
                        hints['B3'] = student_answer # units don't match name
            else: # no knowledge about what units should be
                hints['B6'] = student_answer
        outp.append(('dunno...', student_answer, ''))
    return outp



def next_steps(model, student, question, hints):
    """
    Figures out what moves (calculations, chemistry, algebra) could be next
    :param model: data describing model answer
    :param student: data describing student answer
    :param hints: dictionary of hints
    :return: N/A
    """
    ddict_student, qstore2, cstore2, answers2, match2, context2 = student
    ddict_model, qstore1, cstore1, answers1, match1, context1 = model
    outp = []
    if not answers2 and answers1:
        if not any(a in match1 for a in answers1):
            hints['U'] = ' and '.join(pronounce(a) for a in answers1)
            outp.append((repr(answers1), 'no goals set', ''))
        if not cstore2 and not all(a.startswith('!') for a in answers1):
            hints['U'] = ' and '.join(pronounce(a) for a in answers1 if not a.startswith('#'))
            return # expecting calculations, but none yet
    elif sum(1 for a in answers2 if a[0] not in '!#') < sum(1 for a in answers1 if a not in match1 and a[0] not in '#!'):
        hints['Us'] = 'more unknowns'
    elif len(answers2) > 1 and not cstore2 and 'Plan' not in context2:
        hints['P'] = 'multiple unknowns, what is the plan (write Plan and order of calculation)?'
    elif sum(1 for a in answers2 if a[0] not in '!#') == sum(1 for a in answers1 if a[0] not in '#!'):
        outp.append((repr(answers1), repr(answers2), 'matching # of quantitative goals'))
        #rint('unknowns checked out')
    ddict_model, qstore1, cstore1, answers1, match1, context1 = model
    assignm, calcs = solution_structure(qstore1, cstore1, answers1, context1)
    matches = set(match1.keys())
    best = 1000
    bestcalc = None
    bestnow = 1000
    bestnowcalc = None
    for item in calcs:
        if item in matches:
            continue
        needed_for = "Nothing depends of this subgoal"
        if item not in answers1:# intermediate calculation
            n = still_needed(item, cstore1, matches, answers1)
            if n:
                needed_for = n
            else:
                outp.append((item, 'not calculated', needed_for))
                continue #no reason to calculate this (already calculated things that depend on it)
        m = len(calcs[item] - matches) #number of knowns missing for this step
        if m: #missing knowns: choose the one missing the least
            if item in answers1:
                outp.append((item, 'not yet', 'problem goal, calculation requires ' + ' and '.join(calcs[item] - matches)))
            else:
                outp.append((item, 'not yet', 'need for ' + needed_for + ', calculation requires ' + ' and '.join(calcs[item] - matches)))
            if m < best:
                best = m
                bestcalc = item
        else: #ready to go: choose the least complex calculation
            if item in answers1:
                outp.append((item, 'not yet', 'problem goal; ready to go'))
            else:
                outp.append((item, 'not yet', 'need for ' + needed_for + '; ready to go'))
            if len(calcs) < bestnow:
                bestnow = len(calcs[item])
                bestnowcalc = item
    if bestnowcalc:
        if bestnowcalc in answers1:
            #rint('...pump for calculating answer', item)
            hints['S2a:' + ' and '.join(match1.get(c, c) for c in cstore1[bestnowcalc][0])] = pronounce(bestnowcalc)
            hints['S3a'] = pronounce(bestnowcalc)
        else:
            #rint('...pump for calculating', item)
            hints['S2:' + ' and '.join(match1.get(c, c) for c in cstore1[bestnowcalc][0])] = pronounce(bestnowcalc)
            hints['S3'] = pronounce(bestnowcalc)

    elif bestcalc:
        #rint('...pump for lowest-hanging fruit: "How would you calculate', bestcalc + '?"')
        nitem = pronounce(match1.get(bestcalc, bestcalc))
        hints['S'] = nitem
        #rint('   ...pump for missing knowns', calcs[bestcalc] - matches)
        for item in calcs[bestcalc] - matches:
            nitem = pronounce(match1.get(item, item))
            if qstore1[item].type.endswith('stoich'):
                if '\n!' not in question and 'chemical equation' not in context2:
                    hints['E'] = nitem
                else:
                    hints['Eu'] = nitem
            elif qstore1[item].type.endswith('constant'):
                hints['Dc'] = nitem
            elif qstore1[item].type.endswith('chemformula'):
                hints['F'] = nitem
            elif not qstore1[item].type.endswith('picture') and not qstore1[item].type.endswith('explicit'):
                hints['D'] = nitem
    if 'Conversion' in context1:
        for item, _ in context1['Conversion']:
            if ' in ' in item:
                funits = item.split(' in ')[1]
                if funits not in qstore2:
                    hints['Conv'] = funits
        if 'Conversion' not in context2:
            hints['Conv2'] = ''

    if 'algebra' in context1 and 'algebra' not in context2:
        first_occurence = min(linenr for formula, linenr in context1['algebra'])
        if not any(qstore1[qn1].linenr > first_occurence for qn1 in match1 if qn1 in cstore1):
            hints['@'] = 'algebra'
    if 'chemical equation' in context1:
        if all(a.startswith('!chemical equation') for a in answers1):
            hints.clear()
        if 'chemical equation' not in context2:
            if any(a.startswith('!chemical equation') for a in answers1):
                hints['!2'] = 'chemical equation'
            else:
                hints['!'] = 'chemical equation'
        else:
            #hoping that the final chemical equations match - fails when model has multiple
            r1 = context1['chemical equation'][-1][0]
            r2 = context2['chemical equation'][-1][0]
            _, spur, miss, bal, coeff = compare_reactions(interpret_equation(r1[1:]),
                                                       interpret_equation(r2[1:]))
            if spur and not miss:
                hints['!s'] = spur
            elif miss and not spur:
                hints['!m'] = miss
            elif miss and spur:
                hints['!ms'] = miss+'; '+spur
            elif bal:
                hints['!b'] = bal
            elif coeff:
                hints['!c'] = coeff
    if 'chemical formula' in context1:
        if all(a.startswith('!chemical formula') for a in answers1):
            hints.clear()
        if 'chemical formula' not in context2:
            if any(a.startswith('!chemical formula') for a in answers1):
                hints['!3'] = 'chemical formula'
            else:
                hints['!4'] = 'chemical formula'
        else:
            s1 = Species(context1['chemical formula'][-1][0])
            s2 = Species(context2['chemical formula'][-1][0])
            if s1 ^ s2:
                missing = s1 - s2
                spurious = s2 - s1
                problems = missing | spurious
                if all(s[0] == 'charge' for s in problems):
                    hints['!q'] = s2.text
                else:
                    hints['!f'] = s2.text
                #rint(missing, spurious)
            elif s1.phase and s1.phase != s2.phase:
                hints['!p'] = 'phase'
    if 'chemical formula' in context2 or 'chemical equation' in context2:
        if 'chemical formula' not in context1 and 'chemical equation' not in context1:
            hints['!un'] = 'line starting with !'
    return outp


def still_needed(item, cstore1, matches, answers1):
    for item2 in cstore1: # possible reasons to calculate this
        if item in cstore1[item2][0] and item2 not in matches: #actual reason to calculate this
            if item2 in answers1 or still_needed(item2, cstore1, matches, answers1):
                return item2
    return None

def rubric(model):
    rub = dict()
    _, qstore, cstore, answers, _, context = model
    an = answers[:]
    qu = [q for q in qstore if qstore[q].type.startswith('Known_explicit')]
    im = [q for q in qstore if qstore[q].type.startswith('Known') and q not in qu]

    qu.extend(['?' + a for a in answers if a[0] != '#'])
    im.extend(c+':' + q[0] for c in context if c.startswith('!') for q in context[c])
    chemans = len([a for a in answers if a[0] == '!'])
    if chemans:
        im = im[:-chemans]
    st = [c+':' + q[0] for c in context if not (c[0] in '#!' or c == 'unknown') for q in context[c]]
    st.extend([q for q in cstore if q not in answers])
    for cat in qu, im, st, an:
        break
        print(cat)
    s = len(an + qu + im + st)
    #rint('Here is how the grading will work')
    rub['question'] = int(100 * len(qu) / s)    # qu stands for question
    rub['data'] = int(100 * len(im) / s)    # im stands for implicit knowns
    rub['work'] = int(100 * len(st) / s)   # st stands for steps
    rub['answer'] = 100 - sum(rub[r] for r in rub)
    #rint('  %d%% for collecting information from the question' % int(100 * nr_ex / s))
    #rint('  %d%% for finding the other necessary quantities' % int(100 * nr_im / s))
    #rint('  %d%% for documenting your work (chemistry, math, comments)' % int(100 * nr_st / s))
    #rint('  %d%% for the answers and the path to them' % int(100 * nr_an / s))
    return rub, qu, im, st, an


def grade_answer(student_answer, model_answer, question, hwid, verbose = False):
    """
    compare answer to model answer for grading
    :param student_answer: submitted student work
    :param model_answer:
    :param question: the question the student is working on
    :param hwid: the ID of the question (containing the chapter number)
    :return: formatted score, ready for display
    """
    doctored_question = question.replace('<em>', '').replace('</em>', '').replace('-g', ' g').replace('-M', ' M').replace('molar','M')
    try:
        model = collect_inputs(model_answer, doctored_question, snuck=False)
    except:
        return '<hr>' + hwid + ': <br>' + 'Not your fault, pqcalc has a problem with grading this problem. You get a 100...<br>'
    student = collect_inputs(student_answer, doctored_question, doubledip=True)
    grading_rubric, qu, im, st, an = rubric(model)

    scores = high_quality_matches(model, student)
    shallow_matches(model, student, scores)
    recalc = '' #fix_knowns(model, student, scores)
    calculation_matches(model, student, scores)
    an_sc, quant_sc, an_feedback = score_answers(an, scores, model, student)
    st_sc, work_feedback = score_work(st, quant_sc, scores, model, student)
    ex_sc, im_sc, inputs_feedback = report_known_matches(model, student, scores, qu, im)
    sco = dict()
    sco['question'] = ex_sc
    sco['data'] = im_sc
    sco['work'] = st_sc
    sco['answer'] = an_sc
    total = 0
    grade = ['<hr>' + hwid + ': ']
    for r in grading_rubric:
        if not grading_rubric[r]:
            continue
        p = int(sco[r] * grading_rubric[r] / 100)
        total += p
        #grade.append('<br>%s: %d out of %d points' % (r, p, grading_rubric[r]))
    if inputs_feedback:
        grade.append('<h3>Input</h3>' + '<br>'.join(inputs_feedback))
    if recalc:
        grade.append('<br>To check answer, inputs were changed as follows:<br>' + '<br>'.join(recalc))
    if work_feedback:
        grade.append('<h3>Work</h3>' + '<br>'.join(work_feedback))
    if an_feedback:
        grade.append('<h3>Answer</h3>' + '<br>'.join(an_feedback))
    #grade.append('<h3>Model answer</h3>' + '<br>'.join(model_answer.splitlines()))
    if not verbose:
        grade = [hwid + ': ']
    comment = 'Good answer! Now try a similar question just with pencil and paper.'
    if total < 90:
        if total < 80:
            if total < 70:
                comment = 'Maybe go to office hours to work on this problem now that you are familiar with it?'
            else:
                comment = 'Maybe do some more end-of-chapter problems with your study group?'
        else:
            comment = 'Look at the feedback and take some notes. What you want to focus on next time?'
    grade.append('<hr>PQtutor says: %s' % comment)

    ''' ''.join(hint[:-1]) + '''
    if recalc:
        recalc = 'Changed '+' and '.join(recalc)
    else:
        recalc = ''
    return '<br>\n'.join(grade)
    #return collect_and_organize_score + recalc + ''.join(hint) + solve_score + brief_work


def stuff_score(model, student):
    _, qstore2, _, _, _, context2 = student
    _, qstore1, _, _, _, context1 = model
    if sum(len(context1[c]) for c in context1):
        return min(100, 100 * sum(len(context2[c]) for c in context1) / sum(len(context1[c]) for c in context1))
    return 0


def collect_inputs(input, question, doubledip=False, snuck=True, is_student=False):
    '''
    Figures out which parts of input are assignments, and stores them ordered by dimension
    :param input: PQcalc input for analysis
    :return:
    '''
    commands = [line for line in input.splitlines() if line and line != '\n']
    answers, context, state = classify_commands(commands, question, is_student)
    qstore, cstore, storage = classify_calcs(answers, doubledip, snuck, state)
    if not is_student and not answers and cstore:
        q = next(reversed(cstore))
        answers.append(q)
        qstore[q].type = 'CalcAnswerAssumed'
    return storage, qstore, cstore, answers, dict(), context


def classify_commands(commands, question, is_student):
    answers = []
    types = []
    context = ddict(list)
    #result, _ = calc('', question)
    state = State()
    #for s in state:
    #    state[s].type = 'Question'
    for linenr, line in enumerate(question.splitlines() + commands):
        if not line.strip():
            continue
        type, name, q, expression = calc2(line, state)
        types.append(type + ' ' + line)
        if type == 'Unknown':
            answers.append(name)
            context['unknown'].append((line, linenr))
            continue
        if type in ('Calc', 'Known'):
            q.linenr = linenr
        elif type == 'Comment':
            if line.startswith('!'):
                if '->' in line or '<=>' in line:
                    comtype = 'chemical equation'
                else:
                    comtype = 'chemical formula'
            elif line.startswith('@'):
                comtype = 'algebra'
            elif line.startswith('Plan'):
                comtype = 'Plan'
            elif line.endswith('?'):
                if 'chemical equation' in line:
                    comtype = '!chemical equation'
                if 'chemical formula' in line:
                    comtype = '!chemical formula'
            elif not is_student and linenr == len(commands) - 1: #comment after the answer has been given
                comtype = '#AnswerText'
            else:
                comtype = 'Generic'
            if comtype[0] in '!#':
                answers.append(comtype)
            context[comtype].append((line, linenr))
            types[-1] = comtype + ' ' + line
            continue
        else:
            if type == 'Conversion':
                context['Conversion'].append((line, linenr))
            continue
        q.type = 'Mistery'
        if type == 'Calc':
            parsed = scan(expression)
            q.I = {p[1] for p in parsed if p[0] == 'I'}
            q.F = {p[1] for p in parsed if p[0] == 'F'}
            q.O = {p[1] for p in parsed if p[0] == 'O'}
            q.N = {p[1] for p in parsed if p[0] == 'N'}
            q.expression = expression
            if name in answers:
                q.type = 'CalcAnswer'
            else:
                q.type = 'CalcStep'
        elif type == 'Known':
            if '#@!#@!' in line:
                q.type = line.split('#@!#@!')[1]
            elif name.startswith('M['):
                q.type = 'Known_chemformula'
            elif name.startswith('ν['):
                q.type = 'Known_stoich'
            else:
                doctored_expression = expression.replace('°aC', '°C').replace('°aC', '°ΔC').replace('. ', ' ').strip()
                doctored_question = question.replace('<em>', '').replace('</em>', '').replace('-g', ' g').replace('-M',' M').replace('molar', 'M')
                if doctored_expression in doctored_question:
                    q.type = 'Known_explicit'
                elif doctored_expression[1:] in doctored_question:
                    q.type = 'Known_explicit_minus'
                elif doctored_expression.split()[0] in question:
                    q.type = 'Known_explicit_I_think'
                elif '[' in name and ']' in name.split('[')[1]:
                    q.type = 'Known_lookup_data'
                elif name in physconst and q.units == physconst[name]:
                    q.type = 'Known_physical_constant'
                else:
                    q.type = 'Known_from_somewhere_else'
        state[name] = q
        types[-1] = q.type + ' ' + line
    for i, t in enumerate(types):
        pass #rint(i, t)
    return answers, context, state


def classify_calcs(answers, doubledip, snuck, state):
    qstore = dict()
    cstore = OrderedDict()
    storage = defaultdict(list)
    snucks = set()
    linenr = None
    #rint(state.keys())
    for name in state:
        q = state[name]
        if name.startswith('Snuck'):
            snucks.add(name)
            q.type = 'Snuck'
            q.linenr = linenr
            #rint('snuck', name, repr(state[name]), 'model' if not doubledip else 'student')
        elif name.startswith('M['):
            q.type = 'Known_chemformula'
            if linenr:
                q.linenr = linenr
        else:
            try:
                linenr = q.linenr
            except AttributeError:
                linenr = None
        if not q.type.startswith('Calc') or (q.name == '-%s' and not q.provenance[0].provenance):
            if snuck or not name.startswith('Snuck') or q.uncert or q.units != Units():
                storage[q.units].append(name)
        else:
            if doubledip and not name in answers:
                storage[q.units].append(name)
            q.I.update(snucks)
            if snucks:
                print(name, ' snuck in ', snucks, q.I)
            snucks = set()
            cstore[name] = (q.I, q.F, q.O, q.expression)
        qstore[name] = q
    return qstore, cstore, storage


def high_quality_matches(model, student, chapter=None):
    ddict_model, qstore1, cstore1, answers1, match1, context1 = model
    ddict_student, qstore2, cstore2, answers2, match2, context2 = student

    scores = dict()
    for dim in ddict_model:
        for q1 in ddict_model[dim]:
            for q2 in ddict_student[dim]:
                if q2 in match2:
                    continue
                score = similarity(q1, q2, qstore1[q1], qstore2[q2], bonus=0, chapter=chapter)
                # #rint(score, q1, q2, repr(q1), repr(q2))
                if score.numerical >= 100:
                    match1[q1] = q2
                    match2[q2] = q1
                    scores[q1] = score
                    break
    #rint(sum(1 for q in qstore1 if not qstore1[q].type.startswith('Calc')), len(match1))
    return scores


Calc_score = namedtuple('Calc_score', 'numerical dependency units number name')
Quant_score = namedtuple('Quant_score', 'numerical units number uncert name bonus')


def quant_score(units, number, uncert, name, bonus):
    score = 0
    score += [0, 25, 35, 45][number]
    score += [10, 2, 0][uncert]
    score += [0, 3, 7][name]
    score += [0, 40][units]
    score += bonus
    return Quant_score(min(100, score), units, number, uncert, name, bonus)


def shallow_matches(model, student, scores, chapter=None):
    ddict_model, qstore1, cstore1, answers1, match1, context1 = model
    ddict_student, qstore2, cstore2, answers2, match2, context2 = student
    for q2 in qstore2:
        if q2 in match2 or q2 not in ddict_student[qstore2[q2].units]:
            continue
        bests = Quant_score(-100, 0,0,0,0,0)
        bestn = None
        for q1 in qstore1:
            if q1 in match1 or q1 in cstore1:
                continue
            if qstore1[q1].units != qstore2[q2].units:
                score = Quant_score(0, 0, 0, 0, 0, 0)
            else:
                score = similarity(q1, q2, qstore1[q1], qstore2[q2], bonus=1, chapter=chapter)
            if score.numerical > bests.numerical:
                bests = score
                bestn = q1
        if bestn and bests.numerical > 35:
            #rint(s2, 'matched with', str(qstore1[bestn]), bests)
            match1[bestn] = q2
            match2[q2] = bestn
            scores[bestn] = bests
    for name in match2:
        if name in cstore2:
            del(cstore2[name])


def similarity(n1, n2, q1, q2, bonus = 0, chapter=None):
    number = uncert = name = 0
    if q1.uncert and q2.uncert:
        if abs(q1.number - q2.number) < q1.uncert:
            number = 3
        elif abs(q1.number - q2.number) < q1.uncert * 3:
            number = 2
        elif abs(q1.number - q2.number) < q1.uncert * 10:
            number = 1
        if q1.uncert > 9 * q2.uncert:
            uncert = 1 # student value looks more certain than it should
        elif q1.uncert * 9 < q2.uncert:
            uncert = 2 # student value too uncertain
            #rint('************************************ wah ***************************************')
    elif q2.uncert:
        if abs(q1.number - q2.number) < q2.uncert:
            number = 3
        elif abs(q1.number - q2.number) < 2 * q2.uncert:
            number = 2
        elif abs(q1.number - q2.number) < 4 * q2.uncert:
            number = 1
    elif q1.uncert:
        if abs(q1.number - q2.number) < q1.uncert:
            number = 3
        elif abs(q1.number - q2.number) < 2 * q1.uncert:
            number = 2
        elif abs(q1.number - q2.number) < 4 * q1.uncert:
            number = 1
    else:
        if q1.number == q2.number:
            number = 3
        uncert = 0
    if bonus and not number:
        s1 = str(q1)
        s2 = str(q2)
        worst = max(len(s1), len(s2))
        bonus += 25 * (worst - levenshtein(s1, s2)) / worst
    s = n2[0] if n1 else '&'
    if not n2.startswith('Snuck'):
        if s == 'Δ' and len(n2) > 2:
            s = n2[1]
        if s in typicalunits and (len(n2)<2 or n2[1] in '[_' or n2[1].isdigit()) and not (chapter==6 and s=='n'):
            if typicalunits[s] == q2.units:
                name = 1
        if n1 and n2 and n1[0] == n2[0]:
            name = 2
        if len(n2)>1 and n2[1] in 'abcdefghijklmnopqrstuvwxyz':
            name = 2
    if not name and bonus:
        worst = max(len(n1), len(n2))
        bonus += 7 * (worst - levenshtein(n1, n2)) / worst
    if not q2.type.startswith('Known'):
        bonus -= 5
    return quant_score(1, number, uncert, name, bonus)


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


def solution_structure(qstore, cstore, answers, context):
    assignments = set()
    calculations = dict()
    byunit = ddict(list)
    for q in qstore:
        quant = qstore[q]
        byunit[quant.units].append(q)
        if quant.type.startswith('Known'):
            assignments.add(q)
        elif quant.type.startswith('Calc'):
            dependencies = all_dependencies(q, cstore, qstore)
            calculations[q] = dependencies
    twostate = 0
    for unit in byunit:
        if len(byunit[unit])> 1:
            #rint('Same units: ', ' + '.join(byunit[unit]) )
            twostate += 1
    if twostate >= 1:
        pass#rint('extra credit (hahaha) for organizing names')
    return assignments, calculations


def all_dependencies(name, cstore, qstore):
    '''
    Obtain all leaves of the dependency tree (not the nodes, though)
    :param name: name of calculated quantity
    :param cstore: all calculated quantities
    :param qstore: all quantities, calculated or not
    :return: {leaves}
    '''
    dep = set()
    if name not in cstore:
        return {name}
    for child in cstore[name][0]:
        if child in dep:
            continue
        elif child in cstore and not child == name:
            dep = dep | all_dependencies(child, cstore, qstore)
        else:
            if child.startswith('Snuck') and hasattr(qstore[child], 'twin'):
                dep.add(qstore[child].twin)
            else:
                dep.add(child)
    dep = [d for d in dep if (qstore[d].units != Units() or qstore[d].uncert) or d.startswith('ν[') or d.startswith('N')]
    dep = [d if not d.startswith('Snuck') else str(qstore[d]) for d in dep]
    newstate = State()
    return set(dep)


def calc_score(dependency, units, number, name):
    score = 5
    score += dependency
    if units:
        score += 35
        if number:
            score += 15
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
    if q1.units != q2.units:
        units = 0
    elif abs(q1.number - q2.number) > abs(q1.uncert + q2.uncert)/2:
        number = 0
    if n1[0] == n2[0]:
        name = 1
    if len(n2) > 1 and n2[1] in 'abcdefghijklmnopqrstuvwxyz':
        name = 1
    leftovers = dep1 ^ dep2t
    if not leftovers:
        dependency = 40
    else:
        dependency = 20 - 5 * len(leftovers)
    return calc_score(dependency, units, number, name)


def calculation_matches(model, student, scores):
    ddict_model, qstore1, cstore1, answers1, match1, context1 = model
    ddict_student, qstore2, cstore2, answers2, match2, context2 = student
    if not cstore1 or not answers1:
        return 0.0
    names1 = [n for n in cstore1]
    #rint (names1)
    names2 = [n for n in cstore2]
    #rint (names2)
    items = len(names1)
    success = 0
    matched = 0
    for name2 in reversed(names2):
        i2, f2, o2, ex2 = cstore2[name2]
        dep2 = all_dependencies(name2, cstore2, qstore2)
        #check_cancelation(dep2, name2 + ' = ' + ex2, qstore2)
        bestscore = Calc_score(-100, 0, 0, 0, 0)
        bestname = None
        distinction = 0
        for name1 in names1:
            if name1 in match1:
                continue
            i1, f1, o1, ex1 = cstore1[name1]
            dep1 = all_dependencies(name1, cstore1, qstore1)
            score = similarity_calc(name1, name2, qstore1[name1], qstore2[name2],
                                    dep1, dep2, match2,
                                    f1, o1, f2, o2)
            #rint(score.numerical, name1, dep1, name2, dep2)
            if score.numerical >= 95:
                match1[name1] = name2
                match2[name2] = name1
                scores[name1] = score
                success += score.numerical
                matched += 1
                #rint('\nLook no further: ', name1, name2, '%4.1f' % score.numerical, score)
                break
            if score.numerical >= bestscore.numerical:
                distinction = score.numerical - bestscore.numerical
                bestscore = score
                bestname = name1
            elif distinction > bestscore.numerical - score.numerical:
                distinction = bestscore.numerical - score.numerical
        else:
            if bestscore.numerical > 50 and distinction > 5:
                match1[bestname] = name2
                match2[name2] = bestname
                if bestname in answers1 and name2 in answers2:
                    pass #score.numerical += 20
                scores[bestname] = bestscore
                success += bestscore.numerical
                matched += 1
                #rint('\nNot great, but best bet: ', bestname, name2,  '%4.1f' % bestscore.numerical, bestscore)
                names1.remove(bestname)

def check_cancelation(dep, ex, qstore):
    newstate = State()
    for d in dep:
        newstate[d] = qstore[d]
    _, _, qold, _ = calc2(ex, newstate)
    for d in dep:
        num = newstate[d].number
        newstate[d].number *= 2
        _, _, qnew, _ = calc2(ex, newstate)
        newstate[d].number = num
        ratio = qold.number / qnew.number
        if abs(ratio - 1.0) < 0.00001:
            print('who cares about', d)



def score_answers(an, scores, model, student):
    if not len(an):
        return 0.0, 0.0, []
    ddict_model, qstore1, cstore1, answers1, match1, context1 = model
    ddict_student, qstore2, cstore2, answers2, match2, context2 = student
    calc_sum = 0
    calc_score = 0
    other_score = 0
    feedback = []
    for a in an:
        if a[0] == '!':
            if a[1:] in context2:
                for eq in context2[a[1:]]:
                    print(eq)
                print('model:')
                other_score += 100
                for eq in context1[a[1:]]:
                    print(eq)
                print('model:')
            else:
                feedback.append('Expected ' + a[1:])
        elif a[0] == '#':
            if a in context2:
                other_score += 100
            else:
                feedback.append('Expected a sentence summarizing your conclusions')
        else:
            calc_sum += 1
            if a in scores:
                calc_score += scores[a].numerical
                if scores[a].numerical != 100:
                    feedback.append('Your answer for ' + match1[a] + ' is ' + str(qstore2[match1[a]]) +
                                    '. The model answer is ' + str(qstore1[a]))
            else:
                feedback.append('You did not calculate the ' + pronounce(a, qstore1[a].units))

    an_sc = (calc_score + other_score) / len(an)
    if calc_sum:
        return an_sc, calc_score / calc_sum, feedback
    return an_sc, 0.0, feedback


def score_work(st, quantsc, scores, model, student):
    if not st:
        return 0.0, []
    if quantsc > 97:
        return 100, ['The calculation documented your path to the solution sufficiently']
    feedback = []
    ddict_model, qstore1, cstore1, answers1, match1, context1 = model
    ddict_student, qstore2, cstore2, answers2, match2, context2 = student
    work_score = 0
    for a in st:
        if a in cstore1: # a calculation
            if a in scores:
                work_score += scores[a].numerical
            else:
                for ans1 in (ans1 for ans1 in answers1 if ans1 in cstore1):
                    if not ans1 in match1 and a in all_dependencies(ans1, cstore1, qstore1):
                        feedback.append('It might have helped to calculate the ' + pronounce(a) + ' to figure out the ', ans1)
                        break
                else:
                    work_score += 100
                    feedback.append('You got the ' + pronounce(ans1) + ' without calculating the ' + pronounce(a) + ' explicitly, which is fine.')
        else:
            if a.split(':')[0] in context2:
                type, eq2 = a.split(':', maxsplit=1)
                bestscore = 0
                for b in context2[type]:
                    score, *_ = compare_reactions(interpret_equation(b[0][1:]), interpret_equation(eq2[1:]))
                    bestscore = max(bestscore, score)
                work_score += bestscore
            else:
                feedback.append('How about some' + a)
    return work_score / len(st), feedback


def fix_knowns(model, student, scores):
    ddict_model, qstore1, cstore1, answers1, match1, context1 = model
    ddict_student, qstore2, cstore2, answers2, match2, context2 = student
    recalc = []
    for q2 in qstore2:
        if q2 not in match2:
            continue
        q1 = match2[q2]
        if 19 < scores[q1].numerical < 100 and (scores[q1].number < 3 or scores[q1].uncert < 1):
            #rint('fixing (?) {}:{}'.format(q2, repr(qstore2[q2])))
            #rint('fixed (?) {}:{}, score was {}'.format(q2, repr(qstore2[q2]), scores[q1]))
            recalc.append(q2+' from '+ str(qstore2[q2]) + ' to ' + str(qstore1[q1]))
            qstore2[q2] = qstore1[q1]
    if recalc:
        newstate = State()
        for q2 in qstore2:
            newstate[q2] = qstore2[q2]
        for q2 in cstore2:
            _, _, _, exp = cstore2[q2]
            type_text, name, quantity, expression = calc2(exp, newstate)
            qstore2[q2] = quantity

    return recalc


def collect_and_organize_hints(model, student, hints):
    ddict_model, qstore1, cstore1, answers1, match1, context1 = model
    ddict_student, qstore2, cstore2, answers2, match2, context2 = student
    mdict = ddict(list)
    pdict = ddict(set)
    for q in qstore1:
        mdict[qstore1[q].units].append(q)
    for u in mdict:
        if len(mdict[u]) < 2:
            continue
        for q in mdict[u]:
            for a in quantity_name_context(q):
                pdict[a].add(q)
    for a in pdict:
        if len(pdict[a]) < 2:
            continue
        #rint(a, ' '.join(pdict[a]))
        cont = [set(quantity_name_context(match1[q1])) for q1 in pdict[a] if q1 in match1 and not match1[q1].startswith('Snuck')]
        if len(cont) < 2:
            continue
        common = cont[0]
        for c in cont[1:]:
            common &= c
        if not common:
            #rint('trouble with', ' and '.join([match1[q1] for q1 in pdict[a] if q1 in match1]))
            hints['CO'] = ' and '.join([match1[q1] for q1 in pdict[a] if q1 in match1])


def quantity_name_context(q):
    if '[' in q:
        before, rest = q.split('[',1)
        middle, end = rest.split(']', 1)
        q = before + '_' + middle + '_' + end
    if len(q) > 1 and q[1].isdigit():
        q = q[0] + '_' + q[1:]
    for a in q.split('_')[1:]:
        if a:
            yield a


def flatten(list_of_lists):
    while 1:
        empty = True
        for list in list_of_lists:
            if list:
                yield list.pop(0)
                empty = False
        if empty:
            break


hints_english = {
    'K': ['T: Need to start writing down quantities given in the question',
          'Q: The first thing I like to do is to write down all the quantitative information in the question. Press go for more suggestions from the virtual study group.',
          'B: The units usually give a great clue what kind of quantities the question talks about.',
          'L: What was the unknown in the worked example?',
          'C: chapter specific wisdom*'],
    'Work': ['T: You need to show your work, not just write down the answer',
            "B: I think we are supposed to calculate quantity's name with PQcalc, not copy the value from somewhere else",
            "Q: We need to show how quantity's name relates to the known quantities",
            "L: What calculations did they do in the worked example?"],
    'Ksp': ['T: Unintelligible or unexpected quantity',
            "L: Did they use quantity's name in the worked example or is it just extra information?",
            "Q: Is there some typo in quantity's name?",
            "B: Can we take another look at quantity's name in the question?"],
    'Kcap': ['T: Check capitalization',
             "Q: We have to be careful with the capitalization, e.g. t is time and T is temperature",
             "C: What about the capitalization of quantity's name (unit table)?",
             "L: M is molar mass and m is mass",
             "B: V is volume and v is velocity (unit table)"],
    'Kspn': ['T: Unintelligible or unexpected quantity with unit mismatch',
             "Q: Maybe we should take another look at the exact text of the question",
             "C: Is there a quantity's name mentioned in the question (unit table)?",
             "L: Was there a quantity's name in the worked example? Check for typos and units",
             "B: Let's check whether the name and units we chose is appropriate for a quantity's name (unit table)"],
    'Kspnu': ['T: No units, name suggests it should have units',
             "Q: Most quantities have units, or at least should have...",
             "C: What is a good unit for quantity's name (unit table)?",
             "L: Was there a quantity's name in the worked example? Check for typos and units",
             "B: Let's check whether the name and units we chose is appropriate for a quantity's name (unit table)"],
    'Kw': ['T: Implicit known has incorrect value',
           "Q: Where did we look up quantity's name? Was it a source we can trust?",
           "B: Is quantity's name correct (value, sig figs, exponent)?",
           'L: Where did they find additional data in the worked example?'],
    'Ks': ['T: Implicit known has too few sigfig',
           "Q: I like to pay attention to significant figures of data I gather. If we write down too few, our result will be approximate only",
           'B: Remember how you do sigfigs in this calculator? <a href="ico/manual.html">manual</a>',
           "L: Where did they get quantity's name in the worked example ?"],
    'Num': ['T: Use of numerical value instead of quantity name',
           "Q: If we gave it a name, we should use the name in calculations.",
           "B: We should not be entering numbers anymore (quantity's name).",
           "L: How did they use quantity's name in the worked example ?"],
    'Conv': ["T: Need to define a new unit",
           "B: What kind of unit is quantity's name?",
           "Q: I don't think PQcalc knows about the unit quantity's name mentioned in the question",
           "L: How did they use quantity's name in the worked example ?"],
    'Conv2': ["T: Question asks for unit conversion",
           "Q: Did we convert units like it says in the question?",
           "B: Big unit small number, small unit big number... sometimes a different unit helps to understand the answer",
           "L: Was there a unit conversion in the worked example ?"],
    'Ks2': ['T: Implicit known has too many sigfig',
           "Q: I like to pay attention to significant figures of data I gather.",
           'B: Remember how you do sigfigs in this calculator? <a href="ico/manual.html">manual</a>',
           "L: Where did they get quantity's name in the worked example ?"],
    'Is': ['T: Explicit known has to few sigfig',
           "Q: I like to pay attention to significant figures given in the question. If we write down too few, our result will be approximate only",
           'B: Remember how you do sigfigs in this calculator? <a href="ico/manual.html">manual</a>',
           'L: How did they interpret the sigfigs in the worked example?'],
    'Is2': ['T: Explicit known has too many sigfig',
           "Q: I like to pay attention to significant figures given in the question",
           'B: Remember how you do sigfigs in this calculator? <a href="ico/manual.html">manual</a>',
           'L: How did they interpret the sigfigs in the worked example?'],
    'I': ['T: You are missing some explicit knowns',
          "Q: I like to reread the question to make sure I'm not missing any given quantities",
          'B: If it has units, write it down',
          "C: What happened to quantity's name?",
          'L: What other data did they use in the worked example?'],
    'Ii': ['T: You have mistakes in some explicit knowns',
           "L: So we are collecting information from the question. Let's make sure we get that first step right.",
           "Q: I like to reread the question to check for typos (upper/lower case, sig figs, exponent, units?)",
           'B: Did we correctly copy units and values from the question?'],
    'Ipm': ['T: You have incorrect sign in explicit known',
           "Q: My dad used to say (+) or (-) is a matter of luck)",
           'B: What does it mean when this quantity type is negative or positive?'],
    'CO': ['T: You chose a strange name or swapped two quantities',
           "Q: If there are multiple quantities with the same units, it is easy to mix them up",
           "C: Don't quantity's name belong together and should have the same label?",
           'B: I like to organize my quantities in before/after or by chemical species, and name them accordingly'],
    'In': ['T: You chose a strange name',
           "B: The unit table might suggest a name more conventional than quantity's name.",
           "Q: If there is no conventional one-letter symbol for a quantity, we could use a word as a name so nobody gets confused",
           'L: How did they name quantities they looked up in the worked example?'],
    'Snu': ["T: You did not give quantity's name a name",
           "Q: The advantage of naming quantities is to learn about their meaning and where they are coming from",
           "C: In the calculation, where is quantity's name coming from?",
           "L: What name did they choose for something like quantity's name in the worked example?"],
    'Kn': ['T: You chose a strange name',
           "Q: I like to check whether the name matches the units",
           "C: Where did we look up quantity's name? Did they have a better name for it?",
           'B: How about we check the unit table to see if the name we chose makes sense?'],
    'Sn': ['T: You chose a short name',
           "Q: Do you know more about quantity's name that you could add to the name",
           "L: Did they have more descriptive names for quantities in the worked example?",
           'B: We could add a subscript to the name, and then an adjective like initial/final, the physical state, the substance it refers to'],
    'Sk': ['T: You should name it',
           "Q: Can we give quantity's name a name?",
           "L: Did they have descriptive names for quantities in the worked example?",
           "B: We could use the common symbol for quantity's name, and add a descriptive subscript or - in brackets - the substance it refers to"],
    'Z': ['T: We are not discussing calculations yet',
           "Q: We better collect all the knowns and unknowns before we start calculating"],
    'Us': ['T: There are multiple unknowns; what are they?',
           'B: What are we trying to figure out? What <em>are</em> the unknowns?',
           'Q: Sometimes there is more than one unknown',
           'L: What were the unknowns in the worked example?'],
    'U': ['T: What is the unknown?',
          'B: What are we trying to figure out? What is the unknown? (write something like "q = ?" or "chemical equation?"',
          'Q: If we look at the problem above, is there a question mark somewhere, or a keyword like "calculate" or "determine"?',
          'L: What was the unknown in the worked example?'],
    'E': ['T: We need a chemical equation to calculate next goal',
          'B: I like writing down the chemical equation of the reaction we are talking about.',
          'L: Was there a chemical equation in the worked example?',
          'C: What type of reaction is this? Can we write it down?'],
    'Eu': ['T: We need to interpret a chemical equation to calculate next goal',
           'B: What do we do with a balanced chemical equation?',
           'Q: I like clicking on stuff I''m not familiar with (like chemical equations)',
           'L: How did they use the chemical equation in the worked example?'],
    'F': ['T: We need a chemical formula to calculate next goal',
          'B: Is there some information we can get from the periodic table?',
          'L: Was there a chemical formula in the worked example?',
          'C: Do we know its chemical formula?'],
    'D': ['T: Known from external source',
          'C: We got all the information given explicitly in the question. Great! What is next?',
          'L: What other quantities were used in the worked example?',
          'Q: Maybe they are not giving us all the information directly. Maybe we can look something up.',
          'B: The appendices of the textbook contain a lot of data on different chemical species'],
    'Ip': ['T: Known from image in question',
          'Q: Did you see the picture shown in the question?',
          'B: Can we extract some data from the picture?'],
    'Dc': ['T: Known constant',
           'Q: Some constants (like π) are so common, you would be expected to know them',
           'B: The appendices of the textbook contain a lot of physical constants',
           'L: Which physical constants did they use in the worked example?'],
    '!2': ['T: non-quantitative question',
           'C: This chapter has questions that are quantitative and others that are not',
           'B: The answer might just be a formula'
           'L: What form did the answer have in the worked example'],
    '!un': ['T: unexpected chemical equation',
            'C: Do we really need a chemical equation here?',
            'B: Chemical equations are necessary if the stoichiometry is relevant, but is it in this case?',
            'Q: Anything that helps me to understand the chemistry - you know chemical equations are not my strength... '],
    '!': ['T: non-quantitative question',
          "Q: Didn't we say we are looking for a chemical formula or equation? Not my strength...",
          'B: Are we ready to summarize the chemical insight?'],
    '!s': ['T: spurious chemical species',
           "Q: Great, we are writing a chemical equation! I'm more at home with numbers, so can you walk me through it?",
           "B: Is there solvent or some other species that doesn't belong in the equation?",
           'C: Are we writing a molecular or a net ionic reaction?'],
    '!m': ['T: missing chemical species',
           "Q: Fascinating, all those symbols! Which formula corresponds to which substance?",
           "B: Did we account for all the reactants and products?",
           'C: Are we writing a molecular or a net ionic reaction?'],
    '!ms': ['T: incorrect chemical species',
            "B: Let's check that all reactants and products fit to the information we have?",
            'C: For complicated ionic or molecular formulas, I like to check the subscripts and the charges'],
    '!b': ['T: not balanced',
           "B: If we want to use the coefficients later, better make sure the reaction is balanced",
           'L: How did they balance the equation in the worked example?'],
    '!c': ['T: coefficients wrong or different',
           "B: We can always multiply all coefficient by the same number",
           'C: Did they ask for integer coefficients? Does one of the coefficients have to be one?'],
    '!f': ['T: chemical formula different',
           "B: Does the periodic table help to check this chemical formula?",
           'L: What kind of chemical formula did they use in the worked example?'],
    '!p': ['T: phase missing or incorrect',
           "B: Did we write down the physical state of the species?",
           'C: Sometimes the physical state helps to understand what is going on'],
    '!q': ['T: incorrect charge',
           "B: Can we learn about the charge of this ion by looking at the periodic table?",
           'C: Is there a table of common anions and cations somewhere?'],
    'P': ['T: Decide on order of figuring out unknowns',
          'Q: There are multiple unknowns here. Which one should we start with?',
          'L: In what order did they proceed in the worked example?'],
    'S': ['T: Time for some calculation, but lacking data',
          "Q: Are we still missing some data to calculate quantity's name?",
          "C: If the question mentions concepts I don't understand, I like to go to the chapter summary",
          'L: How did they approach the calculation in the worked example?',
          "B: How could we calculate the quantity's name (mathematical formulae)?",
          ],
    'S2': ['T: You have sufficient data (set of knowns) to do the next step',
           "Q: Hey, we are making progress! What is the next step?",
           "C: Cool, now we can apply the new stuff we learned in this chapter",
           'B: Can we use set of knowns to calculate something useful (mathematical formulae)?',
           'L: What did they do with set of knowns (or similar quantities) in the worked example?',
           ],
    'S3': ["T: You have sufficient data to determine the quantity's name",
           'Q: So what can we calculate at this point?',
           "B: Are we ready to answer the question in one step, or do we need multiple steps?",
           "C: How would we calculate the quantity's name (mathematical formulae)",
          ],
    'S2a': ['T: You have sufficient data to start calculating the answer',
           'B: Can we use set of knowns to answer the question (mathematical formulae)?',
          ],
    'S3a': ["T: You have sufficient data to determine the answer, quantity's name",
            'Q: I get the feeling we are getting close to the answer. What was the unknown again?',
            "C: How would we calculate the quantity's name (mathematical formulae)?",
            "L: How did they determine this quantity type in the worked example?",
            ],
    '@': ['T: You will use a complicated mathematical equation, better write it down',
          'Q: I love solving mathematical equations for the unknown... is it time for starting a line with "@"?',
          'B: Could we just write down the mathematical equation that relates all the quantities (starting with an "@" so it is a comment)?',
          'C: What kind of mathematical formulae were introduced in this chapter?',
          'L: What mathematical formula did they use in the worked example, and did they have to solve for a variable first?'],
    'z': ['{"ico/B.jpg" height ="100" style="display: inline"}{"ico/Q.jpg" height ="100" style="display: inline"}{"ico/L.jpg" height ="100" style="display: inline"}{"ico/C.jpg" height ="100" style="display: inline"}<br>Our little software minds are blown. Try office hours or a tutor, maybe? Goodbye for now...',
          '{"ico/L.jpg" height ="100" style="display: inline"}{"ico/C.jpg" height ="100" style="display: inline"}{"ico/B.jpg" height ="100" style="display: inline"}{"ico/Q.jpg" height ="100" style="display: inline"}<br>How about a little water break? We seem to be stuck anyway. See you in a bit...',
          '{"ico/C.jpg" height ="100" style="display: inline"}{"ico/B.jpg" height ="100" style="display: inline"}{"ico/Q.jpg" height ="100" style="display: inline"}{"ico/L.jpg" height ="100" style="display: inline"}<br>What time is it? We need to go recharge our positronic brains. See you later!',
          '{"ico/L.jpg" height ="100" style="display: inline"}{"ico/C.jpg" height ="100" style="display: inline"}{"ico/B.jpg" height ="100" style="display: inline"}{"ico/Q.jpg" height ="100" style="display: inline"}<br>Maybe we can ask about this problem right before next class. Looking forward to it!',
          ],
    'err': ['C: Stoichiometry, signs, ln/log'],
    'A0': ['T: Calculation correct, inputs need fixing',
           "Q: Let's go over the entire thing again before we submit it",
           'B: To avoid typos when entering numbers from the question, just click on the numbers. Try it!',
           'L: Check what the textbook answer is before you submit'],
    'A1n': ['T: This is correct with a funky name',
           "Q: Is that a good name for our answer?",
           'B: Do the name and the units match?',
           'L: How did they name the result in the worked example?'],
    'A1': ['T: This is correct',
           "Q: We made some progress! Let's figure out a way to check our work",
           'B: Does the answer have the correct units? Maybe we are done.',
           'C: Is the result comparable to what we saw previously in the chapter?',
           'L: One more look at the worked example, and then we are ready to submit?'],
    'A2': ['T: correct units but wrong value. Input confusion or wrong formula (+/- maybe)',
           "B: Does this value for quantity's name make sense?",
           "C: Is the formula we are using correct? The units seem to make sense...",
           "Q: Can we try the formula with simpler numbers where we know the answer?",
           "L: Let's compare this to the worked example."],
    'A2b': ['T: correct units but wrong value. Input confusion or wrong formula (+/- maybe)',
           'B: Can we compare our calculation to the mathematical formulae at the end of the chapter?',
           'C: Are we multiplying by the wrong unitless number?',
           "L: Let's compare this to the worked example."],
    'A3': ['T: Wrong dimensions, check formula and inputs',
           "Q: I love it, we are in the middle of calculating things. Now we can take a look at the units we got.",
           "B: Let's check whether the units we got make sense for the quantity's name (unit table)",
           "C: Let's take another close look at the mathematical formulae at the end of the chapter",
           'L: What mathematical formula did they use in the worked example?<br>'],
    'B3cap': ['T: Units inconsistent with variable name, maybe capitalization problem',
             "Q: We have to be careful with the capitalization, e.g. t is time and T is temperature",
             "C: What about the capitalization of quantity's name (unit table)?",
             "L: M is molar mass and m is mass...",
             "B: V is volume and v is velocity ... (unit table)"],
    'B3': ['T: Wrong dimensions, check formula and inputs and name',
           "B: Let's check whether the units we got are appropriate for quantity's name (unit table)",
           'L: What steps did they do in the worked example, and how did they name those quantities?',
           "C: Let's take another close look at the mathematical formulae at the end of the chapter"],
    'A3a': ['T: Funky dimensions, check formula and inputs',
            "C: And we have a result! I don't remember anything in this chapter with those units...",
            "B: The units of quantity's name are crazy looking (unit table)",
            'Q: Did we divide instead of multiply, or forgot parentheses, or something like that?',
            'L: What happened to the units in the worked example?'],
    'A4': ['T: this might be a step in the calculation, but not the answer. Checking step.',
           'Q: Is this already the answer or is there a step missing?',
           "C: Doesn't quantity's name depend on missing quantity?"],
    'A6': ['T: Spurious quantity should not be in this calculation',
           'C: Lets check if we find the formula among the end-of-chapter mathematical formulae?',
           "Q: Does it really matter for quantity's name what spurious quantity is?",
           "B: Just because the question mentions a quantity does not mean it is relevant for the calculation.",
           'L: Did they use spurious quantity in the worked example?'],
    'A7': ['T: Use missing quantity in this calculation',
           'C: Lets check if we find the formula among the end-of-chapter mathematical formulae?',
           "Q: To calculate quantity's name, don't we need missing quantity?",
           'L: In the worked example, didn''t they use missing quantity?'],
    'A6a': ['T: Answer does not match model answer',
            'C: Let''s check if we find the formula among the end-of-chapter mathematical formulae?',
            'Q: The units of the answer look good. Is there some other mixup?',
            'L: How did they get the answer in the worked example? What is the result given in the textbook?'],
    'A6b': ['T: Answer does not match model answer',
            "C: Is the formula we used for quantity's name new in this chapter?",
            "Q: Looks like we have an answer, but something is fishy",
            "L: How did they calculate the answer in the worked example?"],
    'B0': ['Q: Cool, what do we do next?',
           'L: That was so original - now what?'],
    'B1': ['T: This is a correct step from the model answer',
           'Q: Cool, what do we do next?',
           'B: What did we want to figure out again?'
           'L: Are we done? How did they finish up the worked example?'],
    'B2': ['T: correct units but wrong value. Input confusion or wrong formula (+/- maybe) or wrong name',
           'B: Does this value make sense?',
           'Q: Did we confuse two quantities with the same units (c1 vs. c2, for example)?',
           "L: Let's compare this to the worked example?"],
    'B4': ['T: Calculation is not following path shown in example, although it might be valid',
           'B: Did we plug in the right quantities, or did we get confused?',
           'Q: Sometimes, even if the unit make sense, there is a problem with the calculation.'
           "L: Does calculating quantity's name help us to get the answer? How did they proceed in the worked example?"],
    'B5': ["T: Unknown step, dimensionally incorrect",
           "B: Let's check whether the units we got are appropriate for the quantity's name (unit table)",
           'C: Do we have the wrong formula for the right quantity (check mathematical formulae)',
           "L: Did they even calculate the quantity's name in the worked example?"],
    'B6': ["T: Unknown step, unsure about dimensions",
           "Q: Does this step help us reach our goal?",
           "B: We should try to use conventional names for quantities so that others understand our calculation",
           "L: Did they even calculate quantity's name in the worked example?"],
}


book_of_chapter_specific_errors = {
    0: 'Did we confuse perimeter and area? Did we get the formula right? Use an simple example (e.g. rectangle of 2 by 3) on graph paper to figure it out',
    1: 'If you need the answer in different units, the "using" command will help. To truncate significant figures, multiply by one with different significant fiugres, i.e. 1.0 or 1.00 or 1.000',
    3: 'Is the chemical formula correct? Did we correctly calculate how many atoms of each type are in the compound? Did we confuse compound names?',
    4: 'Is the equation balanced? Did we consider the stoichiometric coefficients? Do we have to first figure out which reactant is limiting?',
    5: 'This is a chapter where you have to watch positive and negative signs like a hawk. The difference in temperature ΔT should be negative if the temperature is dropping. '
       'For heat transfer between A and B, the sign depends on whether you are talking about A or B, i.e. q_A = - q_B. '
       'For calculations with heat of formation and bond dissociation energies, the sign is different for reactants and products.',
    6: 'I got nothing',
    7: 'There is a lot of counting electrons here. Remember electrons have a negative charge, so if an ion has more electrons than the neutral atom, it will be negative.'
       'On the flip side, if there are too few electrons, the ion will be positively charged. Make sure you know whether you are counting the total number of electrons,'
       'or the number of valence electrons. Again, negatively charged ions have more valence electrons than the uncharged atom',
    8: 'Still counting electrons. See chapter 7',
    9: 'You do know the temperature has to be on the Kelvin scale to plug it into pV = nRT? Otherwise, for gas mixtures, use the partial pressure, not the overall pressure.',
    10: 'How do you solve for the argument of a function (i.e. what is in the parentheses)? You apply the inverse function on both sides. '
        'For the natural logarithm, it goes like this: If q_known = ln(q_unknown), to get q_unknown you apply the exponential function exp() to both sides and get exp(q_known) = q_unknown.'
        'Before you take a logarithm or an exponential, make sure your all the units have cancelled out, otherwise you will get an error message.',
    11: 'ΔT_b and ΔT_f are defined in a way that they are always positive. You have to add ΔT_b to the boiling point of the pure solvent (boiling point elevation) but'
        'have to subtract ΔT_f from the freezing point of the pure solvent to get the actual boiling/freezing points. Who came up with that?',
    12: 'Kinetics has weird units. The reaction rate (M/s) and the half life (1/s) always have the same units, but the rate constants are either M/s, 1/s or 1/(M s), '
        'depending on the reaction order. Keep in mind the stoichiometry when you are talking about different species, and switch signs when'
        'switching from reactants (which are used up, concentration decreases) to products (which are made, concentration increases)',
    13: 'In this chapter, we leave units behind. Concentrations are given as [] without units. Q and K are unitless quantities'
        ' (this means we can take their logarithm without getting into trouble)',
    14: 'One of the most important concepts for other chemistry courses: pH. All the logarithms here are base-10 and are called log(). '
        'The inverse of the log() is power of 10, 10^x. Make sure you use thermodynamic concentrations [] if you want to take their logarithm. '
        'If you use ln() instead of log(), everything will be off by a factor of 2.3, so make sure you use log().',
    15: 'Pretty colors in this chapter',
    16: 'Thermodynamics... where doth equilibrium lie? You have to remember your skills from chapter 5, watching positive and negative signs like a hawk. '
        'There is some confusion about dimensions - mostly, ΔG, ΔH, and ΔS are intensive quantities, i.e. per amount of substance. '
        'Sometimes, like in ΔS = q_rev / T or S = k ln(W), they are not.',
    17: 'In electrochemistry, check that your half reactions are correct and add up so you know how many electrons are transferred. '
        'They are not counted twice, so if the oxidation half reaction produces 3 electrons and the reduction half reaction consumes 3 electrons '
        '(balanced, as it should be), z=3 and not six. Again, signs matter and you need to know which half reaction is oxidation adn which one is reduction.',
    18: 'Shiny metalls',
    19: 'Even more pretty colors than in chapter 15',
    20: 'Take the course',
    21: 'Square of the distance, pal... walk away'

}


book_of_wisdom = {
    0: 'Try to make your own question with numbers that are easy to calculate with (maybe 2, 3, and 6).',
    1: 'Learn some greek letters like μ(mu), ρ(rho) and ν(nu). Become familiar with dimensions and units of quantities you encounter.',
    2: "Use the periodic table, and make sure you don't mix up element such as copper (Cu) and cobalt (Co).",
    3: 'This chapter is all about chemical amounts of substances.\n '
         'Check whether the problem is about a pure substance (where you can use the molar mass M) '
         'or a solution (where you can use the definition of concentration or the dilution law) '
         'or about composition of a compound (where you can use the chemical formula).',
    4: 'This chapter is about stoichiometry, i.e. how the amounts of substances in a reaction are related'
       ' to one another.\n We should make sure we have a balanced equation so we can apply\n'
       '@n_1 / ν_1 = n_2 / ν_2\n Stoichiometry problems are either about stoichiometric ratio (equation above) or about limiting reactant (if I have this much of one '
       'and this much of another reactant, how much can react before we run out of one reactant), where we can use'
         '\n@ n[->] = min(n_react1 / ν_1, n_react2 / ν_2, ...)',
    5: 'Two types of calculation, either involving calorimetry or tabular data. For the tabular data, you need a balanced equation.',
    6: 'Look at the periodic table to make sense of this material',
    7: 'Before you do anything, look at the periodic table (metal/non-metal, valence electrons, electronegativity)',
    8: 'See chapter 7',
    9: "It's a gas...",
    10: 'It is all about charge distribution, so check the electronegativity and add partial charges to your Lewis structures',
    11: 'Salt melts ice, i.e. the freezing point of salt water is lower than that of pure water',
    12: 'Rates change with concentration because those determine how likely molecules bump into one another. Rates change with temperature'
        ' because at higher temperature there is more thermal (kinetic) energy to overcome the activation barrier',
    13: 'Equilibrium: forward and reverse rates are equal (concentrations are constant but usually not equal to one another). '
        'Know the three ways of determining what happens after disturbing an equilibrium: Q vs K, kinetic argument, Le Chatelier',
    14: 'Low pH (< 7), high proton concentration, [H3O+] > [OH-], acidic. Neutral when pH = 7 and [H3O+] = [OH-]. High pH (> 7), low proton concentration, [H3O+] < [OH-].'
        'Protonation is more likely at low pH than at high pH',
    15: 'Pretty colors in this chapter',
    16: 'If ΔG of a reaction is negative, equilibrium lies in the forward direction.',
    17: 'Electrochemistry is the easiest way to drive reactions with a positive ΔG, i.e. away from equilibrium. '
        'We use electrochemistry to charge our cell phone batteries',
    18: 'Shiny metals',
    19: 'Even more pretty colors than in chapter 15',
    20: 'Take the course (Orgo I and II, that is)',
    21: 'Square of the distance, pal... walk away'
}


def chapterize(text, chapter, hwid, extra, name='dunno'):
    text = '{"ico/%s.jpg" height ="100" style="display: inline" title="Your turn"}' % text[0] + '<br>' + text[2:]
    if 'worked example' in text:
        link = '<a href="./%s" target="_blank">worked example</a>' % hwid[:-1]
        text = text.replace('worked example', link)
    if "this quantity type" in text:
        text = text.replace("this quantity type", 'the ' + name.split('of')[0])
    if "set of knowns" in text:
        text = text.replace("set of knowns", extra)
    if "its chemical formula" in text:
        text = text.replace("its chemical formula", 'the chemical formula of ' + name.split('of ')[1])
    if 'missing quantity' in text:
        text = text.replace('missing quantity', extra)
    if 'appendices of the textbook' in text:
        link = '<a href="https://chem.libretexts.org/Textbook_Maps/General_Chemistry_Textbook_Maps/Map%3A_Chemistry_(OpenSTAX)/Appendices" target="_blank">appendices of the textbook</a>'
        text = text.replace('appendices of the textbook', link)
    if 'unit table' in text:
        table = '<a href="./units%s" target="_blank">unit table</a>' % chapter
        text = text.replace('unit table', table)
    if 'spurious quantity' in text:
        text = text.replace('spurious quantity', extra)
    if 'mathematical formulae' in text:
        link = '<a href="./formulae%s" target="_blank">mathematical formulae</a>' % chapter
        text = text.replace('mathematical formulae', link)
    if 'chapter summary' in text:
        link = '<a href="./ico/summary.html#%s" target="_blank">chapter summary</a> ' % chapter
        text = text.replace('chapter summary', link)
    if 'chapter specific wisdom*' in text:
        chap = int(chapter)
        if chapter in book_of_wisdom:
            wisdom = book_of_wisdom[chap]
        else:
            wisdom = 'I got nothin'
        text = text.replace('chapter specific wisdom*', wisdom)
        #text = 'C spent hours in the library researching the types of questions in this chapter, and here is - in her own words - what she learned<br>' + text
    if 'Stoichiometry, signs, ln/log' in text:
        chapter = 1 if chapter == 'J' else int(chapter)
        if chapter in book_of_chapter_specific_errors:
            wisdom = 'Here are some mistakes I have seen for problems in this chapter.' + book_of_chapter_specific_errors[chapter]
        else:
            wisdom = 'I got nothin'
        text = text.replace('Stoichiometry, signs, ln/log', wisdom)
    if "quantity's name" in text:
        text = text.replace("quantity's name", name)
    elif "next goal" in text:
        text = text.replace("next goal", name)
    else:
        text = text.replace("Your turn", name)

    return text


def hint_it (hwid, chapter, hint_type, name, category=None):
    if ':' in hint_type:
        hint_type, extra = hint_type.split(':', maxsplit=1)
    else:
        extra = ''
    hintlist = hints_english[hint_type]
    if hint_type == 'z':
        hintlist = [random.choice(hints_english['z'])]
    output = []
    for h in hintlist:
        if h[1] == ':' and h[0] in 'BLCQ':
            command = chapterize(h, chapter, hwid, extra=extra, name=category)
            if hint_type in '!m !ms !s !c !b'.split():
                command = command + ' (clicking on the reaction arrow will copy and paste)'
        elif h[0:2] == 'T:':
            continue
        else:
            command = h
        result, _ = calc('', command) #hint_type.replace('!', '⚗') +
        outp, *_ = result
        output.append(outp)
    return output


def yup(cutoff=6):
    last = ''
    words = {   'Yup': 20,
                'OK': 20,
                'uh-huh': 20,
                'mm-hmm': 18,
                'check': 18,
                'cool': 18,
                '😀': 5,
                '😁': 5,
                '😄': 5,
                '😃': 5,
                'darn tootin''': 1,
                'for reals': 1,
                'fo shizzle': 1,
                'good call': 5,
                'hot diggety': 1,
                'right': 16,
                'sho''nuff': 1,
                'way': 2,
                'yea': 16,
                'yessum': 1,
                }
    mylist = [k for k in words for dummy in range(words[k])]
    while 1:
        w = random.choice(mylist)
        if w != last and words[w] > cutoff:
            yield w
            last = w


def kapow():
    last = ''
    words = {   'Yee-haw': 4,
                'Olé': 2,
                'Hurrah': 5,
                'Ha': 2,
                'Boo-ya': 4,
                'Kapow!': 4,
                'Aha': 3,
                'Eureka': 1,
                }
    mylist = [k for k in words for dummy in range(words[k])]
    while 1:
        w = random.choice(mylist)
        if w != last:
            yield w
            last = w


def uhoh():
    last = ''
    words = {   'ahem': 6,
                'er': 6,
                'hm': 6,
                'hmph': 4,
                'huh?': 4,
                'oops': 4,
                'uh-oh': 2,
                'whoa': 1,
                'yikes': 1,
                '😕': 1,
                }
    mylist = [k for k in words for dummy in range(words[k])]
    while 1:
        w = random.choice(mylist)
        if w != last:
            yield w
            last = w

my_yup = yup(0)
my_yup6 = yup()
my_kapow = kapow()
my_uhoh = uhoh()

def generate_tutor_comments (hwid, student_answer, oldstuff, model_answer, question):
    try:
        chapter = int(hwid[2].split('.')[0])
    except:
        chapter = 1
    hints = evaluate_progress(student_answer, model_answer, question, hwid, ignore=oldstuff)
    hints.pop('I', None)
    hints.pop('Kok', None)
    response = my_uhoh
    if 'A0' in hints or  'A1' in hints:
        response = my_kapow
    if not hints:
        response = my_yup
    if response != my_kapow and any(b in hints for b in 'B3 B4'.split()):
        return 'Tutor says: Whoa, these ideas match nothing on my cheat sheet. Talk to a real tutor if you want to continue on this path'
    return 'Tutor says: ' + next(response)



#rint('************ 13 **************')
#show_formulae(13)
#rint('************ 4 **************')
#rint(show_formulae(4))

import pprint


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
duration = 5.1 s
m[N2] = 1.3452 g
V[N2] = 25.9 mL
P_gas = ?
R_gas = 8.314 J / (K mol)
M[N2] = 28 g/mol
n[N2] = m[N2] / M[N2]
P_gas = n[N2] R_gas T_gas / V[N2]'''

model_question = 'ahe 1.3452 g of nitrogen is stored in a 25.9 mL cylinder at 243 K. What is the pressure after 5.1 s (approximately)?'


model_question = 'How many grams of CaCl2 (110.98 g/mol) are contained in 250.0 mL of a 0.200-<em>M</em> solution of calcium chloride?'

model_question = 'Which is the limiting reactant when 5.00 g of H2 and 10.0 g of O2 react and form water?'

model='''V_solution = 250.0 mL
c[CaCl2] = 0.200 M
m[CaCl2] = ?
n[CaCl2] = c[CaCl2] V_solution
m[CaCl2] = n[CaCl2]  M[CaCl2]'''

model = '''m[H2] = 5.00 g
m[O2] = 10.0 g
! 2 H2 + O2 -> 2 H2O
ν[H2] = 2
ν[O2] = 1
n[H2] = m[H2] / M[H2]
n[O2] = m[O2] / M[O2]
n[->] = min(n[H2] / ν[H2], n[O2] / ν[O2])
O2 is limiting
'''

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


def report_matches(ddict_model, qstore1, ddict_student, qstore2, match1, match2, scores):
    return
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


def preliminaries(model_answer, student_answer):
    #rint('******************* Grading *******************************')
    #rint('\n'.join(s for s in student_answer.splitlines() if s))
    #rint('_____________________________________________')
    #rint(model_answer)
    model_commands = model_answer.splitlines()[1:]
    '''
    if '=' not in model_commands[0]:
        model_commands.pop(0)
    '''
    return model_commands


def report_calculation_matches(citems, cmatched, cscore):
    if citems:
        succ = int(7 * cscore / citems)
        noty = int(7 * (citems - cmatched) / citems)
        pounds = 7 - succ - noty
        part3score = 'SUBLIME'[:succ] + '#' * pounds + '_' * noty
    else:
        part3score = 'NO CALC'
    if citems:
        r = '<h3>Credit for result: {:.0%}</h3>'.format(cscore / citems)
    else:
        r = '<h3>no quantitative results...</h3>'
    return r


def calculation_hint3452(model, student, hwid, recalc, scores):
    ddict_model, qstore1, cstore1, answers1, match1, context1 = model
    ddict_student, qstore2, cstore2, answers2, match2, context2 = student
    chapter = hwid[2:].split('.')[0]
    hint = 'need unknown'
    for a in answers1:
        spurious = missing = ''
        if a not in match1:
            #rint('bad match')
            hint = 'Where is your calculation? Looking for the %s' % pronounce(a)
            continue
        student_answer = match1[a]
        if scores[a].dependency == 50:
            if scores[a].units == 1:
                if scores[a].number in {1, 2, 3}:
                    if recalc:
                        response = 'A0'
                    elif scores[a].name or student_answer in answers2:
                        response = 'A1'
                    else:
                        response = 'A1n'
                else:
                    if False: #len(qstore1[a].N) != len(qstore2[student_answer].N):
                        response = 'A2b'
                    else:
                        response = 'A2'
            else:
                response = 'A3'
                if qstore2[a].units not in typical_units_reverse:
                    response = 'A3a'
            #rint(response)
        else:
            s_dep = all_dependencies(student_answer, cstore2, qstore2)
            m_dep = all_dependencies(a, cstore1, qstore1)
            m_dep = {match1.get(m, m) for m in m_dep}
            spurious = ', '.join(c for c in s_dep - m_dep)
            missing = ', '.join(c for c in m_dep - s_dep)
            if spurious:
                #rint('student', cstore2[student_answer][0])
                #rint('model', cstore1[a][0])

                #rint('spurious', spurious)
                response = 'A6:' + spurious
            elif missing:
                #rint('missing', missing)
                response = 'A4:' + missing
        if response == 'A1':
            return ''
        hint = hint_it(hwid, chapter, response, student_answer)
        if response[:2] in ('A4', 'A6') and not scores[a].units:
            response = 'A3' if qstore2[a].units in typical_units_reverse else 'A3a'
            hint = hint + '<br>' + hint_it(hwid, chapter, response, student_answer)
    return hint

def report_known_matches(model, student, scores, qu, im):
    ddict_model, qstore1, cstore1, answers1, match1, context1 = model
    ddict_student, qstore2, cstore2, answers2, match2, context2 = student
    report_matches(ddict_model, qstore1, ddict_student, qstore2, match1, match2, scores)
    score_qu = 0
    feedback = []
    for a in qu:
        if a.startswith('?'):
            if a[1:] in scores and scores[a[1:]].numerical > 95:
                score_qu += 100
            else:
                if a[1:] in match1 and (match1[a[1:]] in answers2 or match1[a[1:]] in cstore2):
                    score_qu += 100
                    if not match1[a[1:]] in answers2:
                        feedback.append('It would have been nice to announce your goal of calculating the ' + pronounce(a[1:]) + ', but no need to take off points.')
                elif '!chemical equation' in a:
                    if 'chemical equation' in context2:
                        score_qu += 100
                    else:
                        feedback.append('Tell us that you need to write a chemical reaction')
                elif '!chemical formula' in a:
                    if 'chemical formula' in context2:
                        score_qu += 100
                    else:
                        feedback.append('Tell us that you need to write a chemical formula')
                else:
                    feedback.append('Tell us that you need to calculate the ' + pronounce(a[1:]))
        elif a in scores:
            score_qu += scores[a].numerical
            if scores[a].numerical < 100:
                name = match1[a]
                if name.startswith('Snuck'):
                    name = str(qstore2[name])
                    feedback.append('Should have defined "' + name + '" before using it.')
                else:
                    feedback.append(pronounce(name) + ' is (partially) incorrect ' + str(qstore2[name]) + ' vs. ' + str(qstore1[a]))
        else:
            feedback.append(pronounce(a) + ' is missing from the knowns')
    if score_qu:
        score_qu = score_qu / len(qu)
    score_im = 0
    for a in im:
        if a.startswith('!'):
            if a in context1:
                score_im += 100
            else:
                feedback.append('You need a ', a[1:])
        elif a in scores:
            score_im += scores[a].numerical
            if scores[a].numerical < 100:
                feedback.append(match1[a] + ' does not match ' + pronounce(a) + repr(scores[a]))
        else:
            feedback.append('You somehow need to obtain the '+ pronounce(a))
    if score_im:
        score_im = score_im / len(im)
    return score_qu, score_im, feedback


Empty, Calculation, ConversionIn, ConversionUsing, Comment, Flags, Unknown = range(7)

#rint('\n'.join(repr(a[2:4]) for a in chemeq_harvest('!MgCl2 -> Mg2+(aq) + 2 Cl-(aq)')))
#rint('\n'.join(repr(a[2:4]) for a in chemeq_harvest('!C6H12O6(s) -> C6H12O6(aq)')))



inputq = '''Q(Fraction(1, 200), 'a', Units(kg=1), 0.0, {'g'})+Q(0.0043, '', Units(kg=1), 0.00010000000000000002, {'g'})'''

if __name__ == '__main__':
    for item in sorted(hints_english.keys()):
        print(item, hints_english[item][0][3:])