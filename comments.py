from mathparser import interpret, scan_it, make_paired_tokens, create_Python_expression, scan
import quantities
from quantities import Q, X, unitquant, Units, latex_name, latex_number, latex_writer
#import calculator # access to State
from fractions import Fraction
from collections import OrderedDict


class BareState(OrderedDict):
    def __init__(self, memory=None, mob=None):
        OrderedDict.__init__(self)
        self.flags = set()


'''
The concentration of CaCl2 in the solution is 1.5e-12 mol/L
                     !!!!!                    mmmmmmmmmmmmm

The reaction HOH -> H+ + OH- proceeds very quickly
             !!!!!!!!!!!!!!!

The relation is c = n/V, where n is the chemical amount of solute
                mm=mmmm

The bla (n0 refers to the ground state) occurs
         mm


Chemistry: enclose in mhchem tags and hope for the best
Math: interpret using X()

'''
def markup_comments(line):
    #rint('mark', line)
    try:
        return markup_chem(line)
    except:
        return(line)

def markup_comments2(line):
    """

    :param line: String containing the comment
    :return: String with variables and chemistry marked-up in LateX
    """
    #rint('markup', line)


    a = []
    for word in mysplit3(line):
        a.extend(autodetect(word))
    interpretation = []
    for item in a:
        if item[0] == "!":
            interpretation.append('\\(\\ce{%s}\\)' % item[1])
        elif item[0] == "{":
            interpretation.append(consume_image(item[1]))
        elif item[0] == "N":
            if 'E' in item[1] or 'e' in item[1]:
                numbertext = '\\(' + latex_number(item[1]) + '\\)'
            else:
                numbertext = item[1]
            interpretation.append('''<span onclick="insertAtCaret('commands','%s', '0')">%s</span>''' % (item[1], numbertext))
        elif item[0] == "_":
            try:
                interpretation.append('''<span onclick="insertAtCaret('commands','%s', '0')">\\(%s\\)</span>''' % (item[1], latex_name(item[1])))
            except:
                interpretation.append(item[1])
        else:
            interpretation.append(format_comment(item[1]))
    #rint('interpretation', interpretation)
    return ''.join(interpretation)



typicalunits = dict(
    c=(Units(m=-3, mol=1), "concentration"),
    E=(Units(kg=1,m=2,s=-2), "energy"),
    S=(Units(kg=1,m=2,s=-2,mol=-1,K=-1), "molar entropy"),
    H=(Units(kg=1,m=2,s=-2,mol=-1), "molar enthalpy"),
    G=(Units(kg=1,m=2,s=-2,mol=-1), "molar Gibbs energy"),
    V=(Units(m=3), "volume"),
    m=(Units(kg=1), "mass"),
    P=(Units(kg=1, m=-1, s=-2), "pressure"),
    T=(Units(K=1), "absolute temperature"),
    t=(Units(s=1), "time"),
    n=(Units(mol=1), "chemical amount"),
    M=(Units(kg=1, mol=-1), "molar mass"),
)

typicalunits["["] = (Units(), "activity")
typicalunits["ρ"] = (Units(kg=1,m=-3), "density")
typicalunits["ν"] = (Units(s=-1), "frequency")
typicalunits["λ"] = (Units(m=1), "wavelength")


def mysplit2(line):
    openers = '"{<'
    closers = {'{':'}', '"': '"', '<': '>', '[': ']'}
    curword = []
    closewith = None
    for c in line:
        if closewith == c:
            curword.append(c)
            yield ''.join(curword)
            curword = []
            closewith = None
        elif not closewith and c in openers and closers[c] in line:
            if curword:
                yield ''.join(curword)
            curword = [c]
            closewith = closers[c]
        elif not closewith and c == ' ' and curword:
            yield ''.join(curword) + ' '
            curword = []
        else:
            curword.append(c)
    if curword:
        yield ''.join(curword)

def mysplit3(line): # in the absence of equations
    openers = '"{<'
    closers = {'{':'}', '"': '"', '<': '>', '[': ']'}
    curword = []
    closewith = None
    for ci, c in enumerate(line):
        if closewith:
            curword.append(c)
            if closewith == c:
                yield ''.join(curword)
                curword = []
                closewith = None
            continue
        if c in openers and closers[c] in line:
            if curword:
                yield ''.join(curword)
            curword = [c]
            closewith = closers[c]
        elif c in ' ?).' and curword:
            if c == ')' and ci < len(line)-1 and not line[ci+1] in ' .?':
                curword.append(c)
            elif c == '.' and curword[-1].isdigit and ci < len(line)-1 and line[ci+1] != ' ':
                curword.append(c)
            else:
                yield ''.join(curword)
                curword = [c]
        elif curword and curword[0] in ' ?).' and c != ' ':
            yield ''.join(curword)
            curword = [c]
        else:
            curword.append(c)
    if curword:
        yield ''.join(curword)


tests = '''
Where is the <bold>NaCl<unbold> in the mixture (glucose plus alanine)?
Here the number is 3.452e-4 (tomorrow and (NH4)2SO4) and stuff'''.splitlines()

for line in tests:
    pass#rint('|'.join(a for a in mysplit3(line)))



def consume_image(charlist):
    cl2 = []
    charlist.pop(0)
    while charlist:
        c = charlist.pop(0)
        if c == "}":
            break
        cl2.append(c)
    return '<img src=%s>' % "".join(cl2)


def format_comment(word):
    charlist = list(word)
    cl2 = []
    while 1:
        c = charlist.pop(0)
        if c == " " and cl2 and cl2[-1] == ' ':
            cl2.append("&nbsp;")
        else:
            cl2.append(c)
        if not charlist or charlist[0] in "!_":
            break
    return "".join(cl2).replace('( ', '(')


def consume_identifier(charlist):
    cl2 = []
    charlist.pop(0)
    while charlist:
        if charlist[0] == " ":
            charlist.pop(0)
            break
        cl2.append(charlist.pop(0))
    space = '' if charlist and charlist[0] in '.,?)' else ' '
    return "\\(%s\\)" % latex_name("".join(cl2)) + space


def format_identifier(name):
    return consume_identifier(["_"] + list(name))


def consume_formula(charlist):
    #print(''.join(charlist))
    cl2 = []
    charlist.pop(0)
    while charlist:
        c = charlist.pop(0)
        if c == " ":
            break
        cl2.append(c)
    space = '' if charlist and charlist[0] in '.,?)' else ' '
    return '\\(\\ce{%s}\\)' % "".join(cl2) +  space


#rint(repr(molar_mass('NaCl')))
#rint(repr(molar_mass('(NH4)2SO4')))

element_regex = r'[BCFHIKNOPSUVWY]|[ISZ][nr]|[ACELP][ru]|A[cglmst]|B[aehikr]|C[adefl-os]|D[bsy]|Es|F[elmr]|G[ade]|H[efgos]|Kr|L[aiv]|M[cdgnot]|N[abdehiop]|O[gs]|P[abdmot]|R[abe-hnu]|S[bcegim]|T[abcehilms]|Xe|Yb'

elements = {'Tb', 'Na', 'Hs', 'Ir', 'Tl', 'Fl', 'Sm', 'Rn', 'As', 'Sb', 'Es', 'Hf', 'I',
            'La', 'Cm', 'Fm', 'Nb', 'P', 'Ga', 'Li', 'Os', 'Rg', 'In', 'No', 'Db', 'Ti',
            'Ta', 'Lv', 'S', 'Cl', 'Cd', 'Lr', 'Po', 'Cn', 'Si', 'Fr', 'Er', 'Cf', 'Br',
            'Pu', 'Xe', 'W', 'C', 'Sn', 'Pd', 'Re', 'Uup', 'Zn', 'Gd', 'K', 'Dy', 'Rf',
            'F', 'Ra', 'Rh', 'Kr', 'Cs', 'Sg', 'Ac', 'Bi', 'Y', 'Ru', 'Pm', 'Th', 'Sr',
            'Np', 'Mt', 'Mg', 'H', 'Hg', 'Se', 'Yb', 'Co', 'Ce', 'Cr', 'Zr', 'Ag', 'Uuo',
            'Ar', 'Al', 'B', 'Pr', 'Pa', 'Ho', 'Pb', 'Fe', 'Pt', 'Uut', 'Ba', 'Rb', 'Bh',
            'Ne', 'Ni', 'Ge', 'Mn', 'Tm', 'Au', 'Nd', 'Eu', 'At', 'Te', 'Ca', 'Md', 'Bk',
            'Tc', 'Sc', 'V', 'Cu', 'He', 'Am', 'Uus', 'N', 'O', 'Ds', 'Lu', 'Be', 'Mo', 'U'}

def elementor(t):
    candidate = []
    text = t.replace('(aq)', 'Uus').replace('(l)', 'Uus').replace('(s)', 'Uus').replace('(g)', 'Uus')
    if text.endswith('-') or text.endswith('+'):
        text = text[:-1] + 'Am'
    candidate = []
    textlist = list(text)
    while textlist:
        c = textlist.pop(0)
        if c.isdigit() or c in '+-()^':
            yield 0.5
        elif not c.isupper():
            candidate.append(c)
            if textlist:
                continue
        cc = ''.join(candidate)
        if cc in elements:
            yield 1
        elif cc:
            yield -len(candidate)/2
        candidate=[]
        if c.isupper():
            candidate = [c]
    cc = ''.join(candidate)
    if cc in elements:
        yield 1


def formula_score(text):
    if text == 'H+' or text == '->' or text == '<=>' or text in '(s) (l) (g) (aq)'.split():
        return 1
    nritems = score = 1
    elements = 0
    for u in elementor(text):
        nritems += abs(u)
        score += u
        if u == 1.0:
            elements += 1
    if not elements:
        return 0.0
    if elements == 1 and not any(c.isdigit() for c in text):
        return 0.0
    if score == nritems:
        return 1.0
    return score/nritems

def int_score(text):
    if 'e' in text or 'E' in text:
        return 0.0
    try:
        i = float(text)
        return 1.0
    except:
        return 0.0

def scinot_score(text):
    if text[0].isdigit and '.' in text:
        try:
            a = float(text)
            return 1
        except:
            pass
    return 0

def equal_score(text):
    if text.strip() == '=':
        return 1
    return 0

def wordscore(text):
    length = len(text)
    dings = 0
    vowel = 0
    for c in text:
        if c in "aeiouy":
            vowel += 1
        elif c.isdigit():
            dings = +1
    for c in text[1:]:
        if c.isupper():
            dings += 1
    if not vowel:
        dings += 1
    return max((length - dings)/length-0.1, 0.7)

def symbolscore(text):
    if '_' in text and not '/' in text:
        return 1.0
    if text.startswith('Δ'):
        return 1.0
    if '[' in text and ']' in text.split('[')[1]:
        return 1.0
    if len(text) == 2 and text[1].isdigit() and not text[0] in '+-0123456789':
        return 0.75
    return 0.0

def endparen(a):
    if a[-1] != ')':
        return False
    if a.count('(') - a.count(')') == -1:
        return True
    return False

def autodetect(b2):
    if b2.endswith(' '):
        trailing_blank = ' '
        a = b2.rstrip()
    else:
        trailing_blank = ''
        a = b2[:]
    #rint('pre autodetect:', b2)
    if b2 and b2[0] in '{[<"':
        return (b2[0], b2),
    delim = ''
    frontdelim = ''
    if not a:
        return [(' ', ' '),]
    if a[-1] in '.,?' or endparen(a):
        delim = a[-1]
        a = a[:-1]
        if a and endparen(a):
            delim = ')' + delim
            a = a[:-1]
    if not a:
        return (')', delim),
    if a[0] == '(' and ')' not in a:
        frontdelim = '( '
        a = a[1:]
    if not a:
        return ('(', frontdelim + delim),
    b = [(scinot_score(a), 'N'), (equal_score(a), '='), (int_score(a), 'i'),
         (formula_score(a), '!'), (wordscore(a), '.'), (symbolscore(a), '_')]
    if a == 'CO':
        pass #rint(b)
    b.sort(key=lambda x: -x[0])
    if delim:
        delim = delim + trailing_blank
        trailing_blank = ''
    result = []
    if frontdelim:
        result.append(('(', '('),)
    result.append((b[0][1], a+trailing_blank),)
    if delim:
        result.append((')', delim), )
    return result


a = '''The concentration of CaCl2 in the solution is 1.5e-12 mol/L
The reaction HOH -> H+ + OH- (aq) proceeds very quickly when NaCl and CuBr2 are heated
The relation is c = n/V, where n is the chemical amount of solute
The bla (n0 refers to the ground state) occurs'''.splitlines()

latex_subs = {"%s * %s": "%s \\cdot %s",
            "%s ^ %s": "{%s}^{%s}",
            "exp0(%s)": "e^{%s}",
            "exp(%s)": "\\mathrm{exp}(%s)",
            "log(%s)": "\\mathrm{log}(%s)",
            "ln(%s)": "\\mathrm{ln}(%s)",
            "sin(%s)": "\\mathrm{sin}(%s)",
            "cos(%s)": "\\mathrm{cos}(%s)",
            "tan(%s)": "\\mathrm{tan}(%s)",
            "sqrt(%s)": "\\sqrt{%s}",
            "quadn(%s": "\\mathrm{quadn}(%s",
            "quadp(%s": "\\mathrm{quadp}(%s",
            "avg(%s": "\\mathrm{avg}(%s",
            "min(%s": "\\mathrm{min}(%s",
            "sum(%s": "\sum (%s",
            "max(%s": "\\mathrm{max}(%s",
            "abs(%s)": "\\mathrm{abs}(%s)",
            "moredigits(%s)": "\\mathrm{moredigits}(%s)",
            "uncertainty(%s)": "\\mathrm{uncertainty}(%s)",
    }

def markup_math(item):
    item = item.replace('?', ' ?')
    out = []
    mathtext = []
    rightmath = ''
    #rint('math:' + item)
    formatted = ''
    listt = item.split('=')
    #rint(listt)
    for i, block in enumerate(listt):
        paired, comment = make_paired_tokens(scan(block, count_paren=False), comma_error=False)
        for j, p in enumerate(paired):
            if p[0] == 'I':
                if (wordscore(p[2]) > symbolscore(p[2]) and len(p[2]) != 1):
                    p[0] = 'W'
                if p[2] in '?!':
                    p[0] = 'W'
        if paired and i:
            #rint ('left:', paired)
            left = [paired.pop(0)]
            if left[0][0] == 'W':
                left[0] = ('I', left[0][1], left[0][2])
            while paired:
                if paired[0][0] != 'W' or paired[0][1] not in '*,':
                    if paired[0][0] == 'W':
                        p0, p1, p2 = paired.pop(0)
                        left.append(['I', p1, p2])
                    else:
                        left.append(paired.pop(0))
                else:
                    break
            if left[-1][0] != 'Z':
                left.append(['Z','*',''])
            try:
                exp0 = create_Python_expression(left[:], BareState(), free_expression=True, warning=False)
                x = eval(exp0)
                x.setdepth()
                mathtext.append(x.steps(-1, latex_writer, subs=latex_subs))
            except (AttributeError, SyntaxError):
                leftish = left[:-1]
                leftish.extend(paired)
                paired = leftish[:]
        if paired and len(listt) - i > 1:
            right = [paired.pop()]
            if paired:
                right.append(paired.pop())
            if right[-1][0] == 'W':
                right[-1] = ('I', right[-1][1], right[-1][2])

            while paired:
                if paired[-1][0] != 'W' or paired[-1][1] not in '*,':
                    if paired[0][0] == 'W':
                        p0, p1, p2 = paired.pop()
                        right.append(('I', p1, p2))
                    else:
                        right.append(paired.pop())
                else:
                    break
            try:
                if right[-1][1] == ',':
                    right[-1] = (right[-1][0], '*', right[-1][2])
                exp0 = create_Python_expression(list(reversed(right)), BareState(), free_expression=True, warning=False)
                #rint(list(reversed(right)), 'right of block:', exp0)
                x = eval(exp0)
                x.setdepth()
                rightmath = x.steps(-1, latex_writer, subs=latex_subs)
            except:
                rightmath = 'trouble with right of = in' + item
                print('failed right:', list(reversed(right)))
                print(item)
                raise
        if paired: # something remains that is not math
            if mathtext:
                out.append('''<span style="font-size: 12pt; color: navy;" onclick="insertAtCaret('commands','%s', '0')">\\(%s\\)</span>''' % (item, ''.join(mathtext)))
                mathtext = []
            if paired[-1][0] == 'Z':
                paired.pop()
            middle = paired[0][2] + block.split(paired[0][2], maxsplit=1)[1]
            if right and right[-1][2] == paired[-1][2]:
                middle = middle.rsplit(paired[-1][2], maxsplit=1)[0]
            else:
                middle = middle.rsplit(paired[-1][2], maxsplit=1)[0] + paired[-1][2]

            #rint(middle)
            out.append(markup_comments2(middle))
            mathtext = [rightmath]
            rightmath = ''
        elif rightmath and not i:
            mathtext = [rightmath]
            rightmath = ''

        mathtext.append(' = ')
    if mathtext and ''.join(mathtext[:-1]):
        out.append('''<span style="font-size: 12pt; color: navy" onclick="insertAtCaret('commands','%s', '0')">\\(%s\\)</span>''' % (item, ''.join(mathtext[:-1])))
    return ' '.join(out)


def markup_chem(b):
    #rint(b)
    listt = []
    for word in mysplit2(b):
        listt.extend(autodetect(word))
    #rint(''.join('%-*s' % (len(a[1]), a[0]) for a in listt))
    if any(item[0] == '!' for item in listt):
        newlist = []
        formula = ''
        while listt:
            current = listt.pop(0)
            if current[0] == '!':
                if not formula and newlist and newlist[-1][0] == 'i':
                    formula = newlist.pop()[1]
                formula = formula + current[1]
            elif formula and current[0] == 'N':
                formula = formula + current[1]
            elif formula and current[1] == '+ ' and listt and listt[0][0] in '!i':
                formula = formula + current[1] + listt.pop(0)[1]
            else:
                if formula:
                    newlist.append(('!', formula))
                    formula = ''
                newlist.append(current)
        if formula:
            newlist.append(('!', formula))
        listt = newlist[:]
    #rint(''.join('%-*s' % (len(a[1]), a[0]) for a in listt))


    newlist = []
    math = ''
    while listt:
        current = listt.pop(0)
        if current[0] in '!<{':
            if math:
                newlist.append(('.', math))
                math = ''
            newlist.append(current)
        else:
            math = math + current[1]
    if math:
        newlist.append(('.', math))
    listt = newlist[:]
    #rint(''.join('%-*s' % (len(a[1]), a[0]) for a in listt))

    result = []
    for i, item in enumerate(listt):
        if item[0] == '<':
            result.append(item[1])
        elif item[0] == '{':
            result.append(consume_image(list(item[1])))
        elif item[0] == '!':
            result.append('''<span style="font-size: 12pt;" onclick="insertAtCaret('commands','[%s]', 0)">\\(\ce{%s}\\)</span>''' % (item[1].rstrip(), item[1]))
        elif '=' in item[1]:
            result.append(markup_math(item[1]))
        else:
            result.append(markup_comments2(item[1]))
    return ' '.join(result)

b = 'The concentration of MgCl2 -> Mg^2+ + 2 Cl- is calculated as c[MgCl2] = b * 3.14 mg * n[MgCl2] / V_solution'
#rint(b)
#rint(markup_chem(b))


task = '''for i in range(100000): calc("","dd = exp(45.34) / log(6.9654) \\n yy = 87 mg/uL", False)'''

typical_units_reverse = {typicalunits[sym][0] :sym for sym in typicalunits}
typical_units_reverse[Units(mol=1, m=-3)] = '[]'

def extract_knowns(text):
    text = text.replace('<em>M</em>', 'M').\
        replace('×10', ' × 10').replace('−', '-').replace('<sup>', '^').\
        replace('10^', '10 ').replace('</sup>', '')
    #rint('\n'.join([text[i:i+80] for i in range(0, len(text), 80)]))
    while text:
        tokens, remainder = scan_it(text)
        if remainder and remainder.startswith('='):
            text = remainder[1:].strip()
        else:
            text = remainder
        ltokens = [[t[0], t[1]] for t in tokens]
        #rint(ltokens)
        for j, t in enumerate(ltokens): #first pass to find units
            if t[0] == 'I':
                punit = t[1]
                while punit and punit[-1] in '),.?':
                    punit = punit[:-1]
                if punit in unitquant:
                    ltokens[j][0] = 'U'
                    ltokens[j][1] = punit
                elif punit == '°C' or punit == '°aC':
                    ltokens[j][0] = 'U'
                    ltokens[j][1] = '°aC'
        shift = 0
        for j, t in enumerate(ltokens): #second pass to find number + unit
            if shift:
                shift -= 1
                continue
            if t[0] != 'N':
                continue
            known = t[1] + (' ' if '.' in t[1] else '. ')
            if len(ltokens) > j+7 and ltokens[j+1:j+5] == [['O', ''], ['I', '×'], ['O', ''], ['N', '10']]:
                known = known[:-1] + 'E' + ltokens[j+5][1]
                if ltokens[j+6][0] == 'N':
                    known += ltokens[j+6][1]
                shift = 6
            units = False
            for j2, t2 in enumerate(ltokens[j+1+shift:]):
                if t2[0] in 'OU' and t2[1] != ',':
                    known = known + t2[1]
                    units = True
                elif known.endswith('-') and t2[0] == 'N' and len(t2[1]) == 1 and t2[1] in '123':
                    known = known + t2[1]
                    shift += j2 + 1
                else:
                    break
            if units:
                while known and known[-1] in '),.?':
                    known = known[:-1]

                try:
                    q = interpret(known, BareState())
                    #rint(q)
                    if q.units in typical_units_reverse:
                        yield(typical_units_reverse[q.units] + ' = ' + known)
                    else:
                        yield('Q1 = ' + known)
                except:
                    yield('Q2 = ' + known)
            else:
                yield('N = ' + known)



'''
for k in extract_knowns('A flask containing 8.0e2 g of water is heated, and the temperature of the water increases from 21 °C to 85 °C. How much heat did the water absorb? T0 = 21 °aC T1 = 85 °aC ΔT = T1 - T0 m[H2O] = 8.0e2 g'):
    print(k)
'''
