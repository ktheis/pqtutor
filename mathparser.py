import quantities
from quantities import Q, X, Units, QuantError, latex_name, unitquant
from re import UNICODE, match
from fractions import Fraction

class CalcError(ArithmeticError): pass


def interpret(t, state, warning=True, keep_onthefly=False):
    '''
    Process input mathematical expression into a valid Python expression and return the result of evaluating it. This is
    a four step process. First, the string is broken into tokens by scan(), then grouped into pairs of operators and
    values by make_paired_tokens(), then turned into a valid Python expression by create_Python_expression, and finally
    evaluated with eval() to yield a quantity Q().

    :param t: the expression as string
    :param state: contains known quantities as ordered dict, along with flags and output
    :return: a quantity Q()

    >>> str(interpret('3 mol/L', State()))
    '3 mol/L'
    >>> str(interpret('30 s + 1 min', State()))
    '(3 / 2) min'

    There are implicit parentheses around a number and the units following it.
    >>> str(interpret('4 mol/L / 2 mol/L', State()))
    '2'

    Multiple fraction slashes in units are confusing, better to use parentheses to group explicitly
    >>> str(interpret('3.5 J/mol/K', State()))
    '3.5 J/(K mol)'
    >>> str(interpret('3.5 J/mol K', State()))
    '3.5 K J/mol'
    >>> str(interpret('3.5 J/(mol K)', State()))
    '3.5 J/(K mol)'

    Non base units are retained
    >>> str(interpret('5.6 mmol', State()))
    '5.6 mmol'

    Math with symbols is allowed as long symbols are defined
    >>> str(interpret('2a', State("Q(2.5, units=Units(), uncert=0.1, name='a')")))
    '5.0'

    ?>>> interpret('2a', State())
    calculator.CalcError: unknown symbol a encountered

    Here are the actual results:
    >>> interpret('3 mol/L', State())
    Q(3000.0, '', Units(m=-3,mol=1), 0.0, set([u'L', u'mol']))
    >>> interpret('30 s + 1 min', State())
    Q(90.0, '%s + %s', Units(s=1), 0.0, set([u's', u'min']), (Q(30.0, '', Units(s=1), 0.0, set([u's'])), Q(60.0, '', Units(s=1), 0.0, set([u'min']))))
    >>> interpret('4 mol/L / 2 mol/L', State())
    Q(2.0, '%s / %s', Units(), 0.0, set([u'L', u'mol']), (Q(4000.0, '', Units(m=-3,mol=1), 0.0, set([u'L', u'mol'])), Q(2000.0, '', Units(m=-3,mol=1), 0.0, set([u'L', u'mol']))))
    >>> interpret('3.5 J/mol/K', State())
    Q(3.5, '', Units(kg=1,m=2,s=-2,mol=-1,K=-1), 0.1, set([u'K', u'J', u'mol']))
    >>> interpret('3.5 J/mol K', State())
    Q(3.5, '', Units(kg=1,m=2,s=-2,mol=-1,K=1), 0.1, set([u'K', u'J', u'mol']))
    >>> interpret('3.5 J/(mol K)', State())
    Q(3.5, '', Units(kg=1,m=2,s=-2,mol=-1,K=-1), 0.1, set([u'K', u'J', u'mol']))
    >>> interpret('5.6 mmol', State())
    Q(0.0056, '', Units(mol=1), 0.00010000000000000002, set([u'mmol']))
    >>> interpret('2a', State("Q(2.5, units=Units(), uncert=0.1, name='a')"))
    Q(5.0, '%s * %s', Units(), 0.2, set([]), (Q(2.0, units=Units(), uncert=0.0), Q(2.5, 'a', Units(), 0.1)))
    '''

    paired, comment = make_paired_tokens(scan(t))
    try:
        expression = create_Python_expression(paired, state, warning=warning, keep_onthefly=keep_onthefly)
################ EVAL EVAl EVAL #######################
        #rint('***************', expression)
        q = eval(expression)
################ EVAL EVAl EVAL #######################
        q.comment = comment
        if type(q) != Q:
            raise CalcError('<div style="color: red;">misused comma? %s</div><br>' % expression)
        return q
    except OverflowError as duh:
        raise CalcError('<br>%s<br><br><div style="color: red;">Math overflow (thanks, Jonas): %s</div><br>' % (t, duh))



def scan(t, count_paren = True):
    '''
    Scan text for identifers('I'), operators('O'), numbers('N') and comments('C') using the regular expression scanner.

    :param t: string of the expression to be parsed
    :return: list of tuples containing tokens ('X', text)

    >>> scan('3 mol/L')
    [(u'N', u'3'), (u'O', u''), (u'U', u'mol'), (u'O', u'/'), (u'U', u'L'), (u'O', u''), (u'Z', u'')]

    >>> scan('30 s + 1 min')
    [(u'N', u'30'), (u'O', u''), (u'U', u's'), (u'O', u'+'), (u'N', u'1'), (u'O', u''), (u'U', u'min'), (u'O', u''), (u'Z', u'')]

    >>> scan('2a')
    [(u'N', u'2'), (u'I', u'a'), (u'O', u''), (u'Z', u'')]

    >>> scan('4 7 #comment')
    [(u'N', u'4'), (u'O', u''), (u'N', u'7'), (u'O', u''), (u'C', u'#comment'), (u'Z', u'')]
    '''

    tokens, remainder = scan_it(t + " ")
    if remainder:
        raise CalcError("got stuck on |%s|" % remainder)
    flatop = (c for ttyp, ttex in tokens if ttyp == 'O' for c in ttex)
    paren = 0
    for c in flatop:
        if c == '(':
            paren += 1
        elif c == ')':
            if not paren and count_paren:
                raise CalcError("Closing parenthesis ')' is missing a matching opening one '(' to the left of it")
            paren -= 1
    if paren and count_paren:
        raise CalcError("Parentheses don't match: need %d more ')'" % paren)
    tokens.append(("Z", ""))
    for i, (ttype, ttext) in enumerate(tokens):
        if ttype == "I":
            if ttext.endswith("Ohm"):
                ttext = ttext.replace("Ohm", "Ω")
            if ttext in quantities.unitquant:
                if ttext.startswith("u"):
                    ttext = "μ" + ttext[1:]
                tokens[i] = "U", ttext
                if ttext == 'min' and len(tokens) > i and '(' in tokens[i+1][1] and any(',' in t[1] for t in tokens[i+1:] ):
                    tokens[i] = 'F', ttext
            elif ttext in ('°aC', '°ΔC'):
                tokens[i] = "U", ttext
            elif ttext in quantities.functions:
                tokens[i] = "F", ttext
    infunc = []
    paren = 0
    for ttype, _ in tokens: #huh, doesnt do anything?
        if ttype == 'F':
            infunc.append(paren)
    return tokens


def extract_identifier(a):
    return match(re_identifier[1], a)


re_comment = ('C', r"[#!].*")
re_operator = ('O', r"[ ,()/*^+-]+")
re_float = ('N', r"((\d*\.\d+)|(\d+\.?))(\(\d\d?\))?([Ee][+-]?\d+)?")
re_identifier = ('I', r"[^\[ ,()/*\^+\-=]+(\[[^]]+\])?[^\[ ,()/*\^+\-=]*|\[[^]]+\][^\[ ,()/*\^+\-=]*")

def scan_it(text):
    answer = []
    while text:
        for pattern in [re_comment, re_operator, re_float, re_identifier]:
            m = match(pattern[1], text)
            if m:
                p = pattern[0]
                break
        else:
            break
        answer.append((p, text[m.start(): m.end()].strip()))
        text = text[m.end():]
    #rint(answer)
    return answer, text


"""
operator: one or more of the following: | ,()/*^+-|
float: any floating point representation with uncertainty, e.g. 3.5(1)E-34
identifier: has to start with non-operator non-digit, may have something in brackets, may have something added
identifier: anything in brackets followed by anything
"""


def make_paired_tokens(raw_tokens, comma_error = True):
    '''

    :param raw_tokens: A list of tokens (item ID, str) from scan()
    :return: a list of paired tokens (item ID, pre-operator, item text)

    Folds operator and identifier/number tokens into paired tokens containing item ID (N, U, I, Z), pre-operator and item text.

    This is the second step in turning the input text into a Python expression.
    It also adds implicit '*' operators and removes comments. There might be artifact '*' at the beginning and at the end.

    User input '3 mol/L' turns into '* 3 * mol / L *'
    >>> make_paired_tokens([('N', '3'), ('O', ''), ('U', 'mol'), ('O', '/'), ('U', 'L'), ('O', ''), ('Z', '')])
    [[u'N', u'*', u'3'], [u'U', u'*', u'mol'], [u'U', u'/', u'L'], [u'Z', u'*', u'']]

    User input '30 s + 1 min' turns into '* 30 * s + 1 * min *'
    >>> make_paired_tokens([('N', '30'), ('O', ''), ('U', 's'), ('O', '+'), ('N', '1'), ('O', ''), ('U', 'min'), ('O', ''), ('Z', '')])
    [[u'N', u'*', u'30'], [u'U', u'*', u's'], [u'N', u'+', u'1'], [u'U', u'*', u'min'], [u'Z', u'*', u'']]

    User input '2a' turns into '* 2 * a *'
    >>> make_paired_tokens([('N', '2'), ('I', 'a'), ('O', ''), ('Z', '')])
    [[u'N', u'*', u'2'], [u'I', u'*', u'a'], [u'Z', u'*', u'']]

    User input '4 7' turns into '* 4 * 7 *'
    >>> make_paired_tokens([('N', '4'), ('O', ''), ('N', '7'), ('O', ''), ('C', '#comment'), ('Z', '')])
    [[u'N', u'*', u'4'], [u'N', u'*', u'7'], [u'Z', u'*', u'']]

    '''
    #print ('make_paired_tokens', raw_tokens)
    tokens = []
    comment = ''
    tokenit = (x for x in raw_tokens)
    for ttype, ttext in tokenit:
        if ttype == "O":
            if ttext:
                operator = ttext
            else:
                operator = "*"
            for c in operator:
                if c in "+-*/^,":
                    break
            else:
                operator = fixoperator(operator, tokens)
            if ',' in operator and comma_error:
                if len(tokens) < 1 or not any(t[0] == 'F' for t in tokens):
                    raise CalcError("commas are only allowed to separate arguments of functions; didn't find any function preceeding the comma")
                pre = operator.split(',',1)
                paren = pre.count('(') - pre.count(')')
                for i,t in reversed(list(enumerate(tokens))):
                    if paren == 0 and t[1].startswith('(') and i > 0:
                        #print (tokens)
                        if tokens[i-1][0] == 'F':
                            break
                        raise CalcError("commas are allowed only to separate arguments of functions; %s is not function" % tokens[i-1][2])
                    if paren > 0:
                        raise CalcError("commas are allowed only to separate arguments of functions; parentheses count off")
                    paren += t[1].count('(') - t[1].count(')')
                else:
                    raise CalcError("commas are allowed only to separate arguments of functions")
            if hasattr(tokenit, "__next__"):  # python 2.7 vs 3.1
                ttype, ttext = tokenit.__next__()
            else:
                ttype, ttext = tokenit.next()
        else:
            operator = "*"
        if ttype == "C":
            tokens.append(["Z", operator, ""])
            comment = '<span style="color:black">&nbsp;&nbsp;&nbsp; ' + ttext[1:] + '</span>'
            break
        tokens.append([ttype, operator.replace("^", "**"), ttext])
    return fixfractions(tokens), comment

def fixfractions(tokens):
    newtokens = []
    while tokens:
        # ['N','...(','integer'],['N','/','integer'],['...',')','...]
        if (len(tokens) > 2 and tokens[0][0] == 'N' and tokens[1][0] == 'N' and tokens[0][1].endswith('(') and tokens[2][1].startswith(')') and tokens[1][1] == '/' and
            '.' not in tokens[0][2] and '.' not in tokens[1][2] and int(tokens[1][2]) != 0):
                fractoken = ['N', tokens[0][1], '%s / %s' % (tokens[0][2], tokens[1][2])]
                newtokens.append(fractoken)
                tokens.pop(0)
                tokens.pop(0)
        else:
            newtokens.append(tokens.pop(0))
    #print (newtokens)
    return newtokens


def fixoperator(operator, tokens):
    """
    Change implicit multiplication to explicit '*' in operator unless it follows a function call.

    >>> fixoperator(' ', ['I'])
    u' *'
    >>> fixoperator(' )  (   ', ['I'])
    u' )  *(   '
    >>> fixoperator(') ', ['I'])
    u') *'
    >>> fixoperator('(', ['I'])
    u'*('
    >>> fixoperator('(', ['F'])
    u'('

    no '*' inserted prior to function call
    """

    if tokens and tokens[-1][0] == "F":
        return operator
    if '(' in operator:
        return "*(".join(operator.split('(',1))
    return operator + '*'


def create_Python_expression(paired_tokens, state, free_expression = False, warning=True, keep_onthefly = False):
    '''

    :param paired_tokens: parsed and processed list of tokens from make_paired_tokens
    :param state: contains known quantities as ordered dict, along with flags and output
    :return: a string containing a valid python expression yielding a quantity Q() as result

    User input '3 mol/L'
    >>> create_Python_expression([['N', '*', '3'], ['U', '*', 'mol'], ['U', '/', 'L'], ['Z', '*', '']], {})
    u"Q(3000.0, '', Units(m=-3,mol=1), 0.0, set(['L', 'mol']))"

    User input '30 s + 1 min)
    >>> create_Python_expression([['N', '*', '30'], ['U', '*', 's'], ['N', '+', '1'], ['U', '*', 'min'], ['Z', '*', '']], {})
    u"Q(30.0, '', Units(s=1), 0.0, set(['s']))+Q(60.0, '', Units(s=1), 0.0, set(['min']))"

    User input '4 7'
    >>> create_Python_expression([['N', '*', '4'], ['N', '*', '7'], ['Z', '*', '']], {})
    u"Q('4')*Q('7')"

    User input '2a'
    >>> create_Python_expression([['N', '*', '2'], ['I', '*', 'a'], ['Z', '*', '']], {})
    calculator.CalcError: unknown symbol a encountered

    User input '2a'
    >>> create_Python_expression([['N', '*', '2'], ['I', '*', 'a'], ['Z', '*', '']], State("Q(number=5.0, name='a')"))
    u"Q('2')*Q(5.0, 'a', Units(), 0.0)"

    User input 'log(7)'
    >>> create_Python_expression([['F', '*', 'log'], ['N', '(', '7'], ['Z', ')*', '']], {})
    u"quantities.log(Q('7'))"

    '''

    result = []
    iscalculation = any(x[0]=='I' for x in paired_tokens)
    complaint = '__tutor__' in state.flags and iscalculation and any(x[0]=='U' for x in paired_tokens)
    while True:  # consume "Z", "I", "F", "U", "N" in paired_tokens
        ttype, operator, ttext = paired_tokens.pop(0)
        if ttype in "ZIF":
            result.append(operator)
            if ttype == "Z":
                #print ('at end:', ttype, operator, ttext, result)
                break
            if ttype == "F":
                result.append("quantities.qfunc('" + ttext + "',")
                if isinstance(paired_tokens[0][1], tuple):
                    gg = 5
                paired_tokens[0][1] = paired_tokens[0][1].replace('(', '', 1)
            else:  # ttype == "I"
                if ttext in state:
                    result.append(state[ttext].__repr__())
                elif free_expression:
                    result.append("X('%s')" % ttext)
                elif ttext.startswith('M[') and ttext.endswith(']'):
                    q = molar_mass(ttext[2:-1])
                    result.append(repr(q))
                    if keep_onthefly:
                        state[ttext] = q
                else:
                    raise CalcError("unknown symbol |%s| encountered" % ttext)
            continue
        # ttype in "UN", i.e. either unit or number
        quant = ["Q('%s')" % ttext]
        if ttype == "N" and "." in ttext:
            if magic(ttext if "(" not in ttext else ttext.split("(")[0]) and not "__showuncert__" in state.flags:
                raise CalcError(
                    "If you always use powerful tools, your basic skills might get rusty. Do this calculation using a method other than PQCalc, please")
        if ttype == "N" and paired_tokens[0][0] != "U" and operator != '**' and (
                    ttext != '1' or '/' not in paired_tokens[0][1]):
            result.append(operator)
            result.append(quant[0])
            if keep_onthefly and iscalculation:
                q = Q(ttext)
                #print (f'added {q} to state ({repr(q)}')
                #print(result)
                state.addsnuck(q)
            continue
        if ttype == "U":
            if warning:
               state.printit('<div style="color: green;">Warning: Unit without number %s</div><br>'% ttext)
            else:
                print('Unit without number: ' + ttext)
        quant_text, paired_tokens, operator = \
            interpret_N_U_cluster(quant, paired_tokens, complaint, operator, result, state, keep_onthefly = keep_onthefly)
        result.append('%s%s' % (operator, quant_text))
    expression = "".join(result)[:-1]
    if expression.endswith('*'):
        expression = expression[:-1]
    if free_expression:
        expression =  expression.replace('Q(', 'X(').replace('quantities.q', 'quantities.x')
    if expression.startswith("*"):
        return expression[1:]
    return expression

def interpret_N_U_cluster(quant, orig_paired, complaint, operator, result, state, keep_onthefly = False):
    '''
    Find quantity introduced on the fly and evaluate as Q(). This is done to avoid cluttering the output with
    trivial calculations such as 2 * mol / L = 2 mol/L. This step also has consequences for order of operation, as
    quantities with units are treated as a single entity (with implied parentheses around them).

    Has to figure out where quantity ends, e.g. 8.314 J/(K mol) * 273 K or 5 mol/L / 2 mol/L
                                                ***************   +++++    *******   +++++++

    Complications arise with exponents in the units, e.g. 5 m ** 2 / J
    or parentheses, e.g. 8.314 J/(K mol) vs 8.314 J /(K 2 kg)

    :param quant: a list containing the first quantity in the cluster, e.g. "Q('2')" or "Q('kg')
    :param orig_paired: the paired list containing items on the right of the first quantity in the cluster
    :return: repr() of the quantity, and the paired tokens that have not been used

    user input: '3 mol / L'
    >>>interpret_N_U_cluster(["Q('3')"],[['U', '*', 'mol'], ['U', '/', 'L'], ['Z', '*', '']])
    ("Q(3000.0, '', Units(m=-3,mol=1), 0.0, set(['L', 'mol']))", [['Z', '*', '']])

    user input: '30 s + 1 min'
    >>>interpret_N_U_cluster(["Q('30')"],[['U', '*', 's'], ['N', '+', '1'], ['U', '*', 'min'], ['Z', '*', '']])
    ("Q(30.0, '', Units(s=1), 0.0, set(['s']))", [['N', '+', '1'], ['U', '*', 'min'], ['Z', '*', '']])
    '''

    paired = orig_paired[:]
    complaint = complaint and any('U' in x for x in orig_paired)
    notyetclosed = None
    openp = 0
    for i, (ttype, op, ttext) in enumerate(paired):
        o = op.count("(")
        c = op.count(")")
        if o:
            openp += o
            if not notyetclosed:
                notyetclosed = i  # start of new parentheses that might not close
        if c:
            openp -= c
            if openp < 0:
                break
            notyetclosed = None
        if not (ttype == "U" or (ttype == "N" and "**" in op)):
            break  # we're done if we encounter anything but a unit (with the exception of an exponent on a unit)
    end = notyetclosed if notyetclosed else i  # take up to open parenthesis that wasn't closed, or to end of N-U cluster
    special = ''
    if end == 1 and paired[0][2] == '°aC':
        special = '°aC'
        paired[0][2] = 'K'
    for j in range(end):
        if paired[j][2] == '°ΔC':
            paired[j][2] = 'K'
            special = '°ΔC'
            print('paired', paired, end)
        quant.append(paired[j][1] + "Q('%s')" % paired[j][2])
    #rint(quant)
    quantstr = "".join(quant)
    #print('before paren', quantstr, paired[end][1])
    openparentheses = quantstr.count("(") - quantstr.count(")")
    if openparentheses > 0:
        for ii, c in enumerate(paired[end][1]):
            if c == ")":
                openparentheses -= 1
            if not openparentheses:
                break
        else:
            raise CalcError("parentheses count off %s %s" % (quant, paired[end][1]))
        quantstr = quantstr + paired[end][1][:ii + 1]
        paired[end][1] = paired[end][1][ii + 1:]
    try:
        #rint ('before eval cluster', quantstr, paired[end][1])
################ EVAL EVAl EVAL #######################
        q = eval(quantstr)
        if special:
            q.prefu.add(special)
            #rint(quantstr)
            #rint('before cluster', q.number, q.prefu, q.units, q.provenance, q.name, '|%s|' % operator, result)
            if '°aC' in q.prefu and q.units == unitquant['K'].units:
                if (operator == '-' and not result) or (len(operator)>1 and operator.endswith('-')):
                    q.number = 273.15 - q.number
                    operator = operator[:-1]
                else:
                    q.number += 273.15
            #rint('after cluster', q.number, q.prefu, q.units, q.provenance, q.name)
################ EVAL EVAl EVAL #######################
    except SyntaxError:
        raise CalcError('<br>%s<br><br><div style="color: red;">Mangled math</div><br>' % quantstr)
    except OverflowError as duh:
        raise CalcError('<br>%s<br><br><div style="color: red;">Math overflow: %s</div><br>' % (quantstr, duh))
    except AttributeError as duh:
        raise CalcError('<br>%s<br><br><div style="color: red;">Bad comma?: %s</div><br>' % (quantstr, duh))
    if complaint:
        raise CalcError('<br>%s<br><br><div style="color: red;">Please give all quantities a name before using them in a calculation</div><br>' % q)

    q.name = ""
    q.provenance = []
    if keep_onthefly:
        state.addsnuck(q)
    return repr(q), paired[end:], operator

def crashtest():
    print('crashtest')
    try:
        t = '1.2E-7'
        print('trying scanner')
        tokens, remainder = scan_it(t + " ")
        print('scanner did it!')
        '''
        s = scan(t)
        print('scanned fine')
        paired = make_paired_tokens(s)
        print('got tokens')
        expression = create_Python_expression(paired, State())
        print('got expression', expression)
        interpret('1.2E-7', State())
        '''
    except:
        return 'threw exception'
    return 'survived test'

def check_name(sym, state):
    '''
    Check whether the name chosen for a quantity conforms to the rules and doesn't clash with a name already used

    :param sym: a name for a new quantity
    :param state: contains known quantities as ordered dict, along with flags and output
    :return: no return value (sym and output get changed in place)
    '''
    tokens, remainder = scan_it(sym)
    if len(tokens) != 1 or tokens[0][0] != "I":
        raise CalcError(("Please don't use %s as a name for a quantity<br><pre>%s</pre>" %
                         (sym, rules_for_symbol_name)))
    if sym in quantities.unitquant or sym in quantities.functions:
        conf = "function" if sym in quantities.functions else "unit"
        raise CalcError(("You can't use %s as a name for a quantity because it is already the name of a %s<br>"
                         "You can use %s_ though, and the underscore will not show in the formatted output." %
                         (sym, conf, sym)))
    return sym


rules_for_symbol_name = """Rules for names: Start with a letter, then letters or numbers or underscores.
  Examples: m0, y, s_15
Special rule #1: You can add anything in brackets, [...], or just have something in brackets
  Examples: [NaCl], [Na+], c[Na+], M[Na+]
Special rule #2: You can't use names already used for units or functions. If you do, the program will add an underscore.
  Examples: mm, s, V, and log are not allowed, and will be used as mm_, s_, V_, and log_"""



endings = {"9351", "1736", "2271", "0261", "3589", "4259", "5257", "8637", "6264", "7126"}


def magic(numberstring):
    if "e" in numberstring:
        numberstring = numberstring.split("e")[0]
    if "E" in numberstring:
        numberstring = numberstring.split("E")[0]
    if len(numberstring) < 5:
        return False
    dig = [int(i) for i in numberstring.replace(".", "")]
    quer = sum(int(n) for n in dig[:-4])
    four = "%04d" % int("".join(str((d + quer) % 10) for d in dig[-4:]))
    return four in endings

atomic_weights = {'H': '1.008', 'He': '4.002602(2)', 'Li': '6.94', 'Be': '9.0121831(5)', 'B': '10.81', 'C': '12.011',
                  'N': '14.007', 'O': '15.999', 'F': '18.998403163(6)', 'Ne': '20.1797(6)', 'Na': '22.98976928(2)',
                  'Mg': '24.305', 'Al': '26.9815385(7)', 'Si': '28.085', 'P': '30.973761998(5)', 'S': '32.06',
                  'Cl': '35.45', 'Ar': '39.948(1)', 'K': '39.0983(1)', 'Ca': '40.078(4)', 'Sc': '44.955908(5)',
                  'Ti': '47.867(1)', 'V': '50.9415(1)', 'Cr': '51.9961(6)', 'Mn': '54.938044(3)', 'Fe': '55.845(2)',
                  'Co': '58.933194(4)', 'Ni': '58.6934(4)', 'Cu': '63.546(3)', 'Zn': '65.38(2)', 'Ga': '69.723(1)',
                  'Ge': '72.630(8)', 'As': '74.921595(6)', 'Se': '78.971(8)', 'Br': '79.904', 'Kr': '83.798(2)',
                  'Rb': '85.4678(3)', 'Sr': '87.62(1)', 'Y': '88.90584(2)', 'Zr': '91.224(2)', 'Nb': '92.90637(2)',
                  'Mo': '95.95(1)', 'Tc': '97.', 'Ru': '101.07(2)', 'Rh': '102.90550(2)', 'Pd': '106.42(1)',
                  'Ag': '107.8682(2)', 'Cd': '112.414(4)', 'In': '114.818(1)', 'Sn': '118.710(7)', 'Sb': '121.760(1)',
                  'Te': '127.60(3)', 'I': '126.90447(3)', 'Xe': '131.293(6)', 'Cs': '132.90545196(6)',
                  'Ba': '137.327(7)', 'La': '138.90547(7)', 'Ce': '140.116(1)', 'Pr': '140.90766(2)',
                  'Nd': '144.242(3)', 'Pm': '145.', 'Sm': '150.36(2)', 'Eu': '151.964(1)', 'Gd': '157.25(3)',
                  'Tb': '158.92535(2)', 'Dy': '162.500(1)', 'Ho': '164.93033(2)', 'Er': '167.259(3)',
                  'Tm': '168.93422(2)', 'Yb': '173.045(10)', 'Lu': '174.9668(1)', 'Hf': '178.49(2)',
                  'Ta': '180.94788(2)', 'W': '183.84(1)', 'Re': '186.207(1)', 'Os': '190.23(3)', 'Ir': '192.217(3)',
                  'Pt': '195.084(9)', 'Au': '196.966569(5)', 'Hg': '200.592(3)', 'Tl': '204.38', 'Pb': '207.2(1)',
                  'Bi': '208.98040(1)', 'Po': '209.', 'At': '210.', 'Rn': '222.', 'Fr': '223.', 'Ra': '226.',
                  'Ac': '227.', 'Th': '232.0377(4)', 'Pa': '231.03588(2)', 'U': '238.02891(3)', 'Np': '237.',
                  'Pu': '244.', 'Am': '243.', 'Cm': '247.', 'Bk': '247.', 'Cf': '251.', 'Es': '252.', 'Fm': '257.',
                  'Md': '258.', 'No': '259.', 'Lr': '262.', 'Rf': '267.', 'Db': '270.', 'Sg': '269.', 'Bh': '270.',
                  'Hs': '270.', 'Mt': '278.', 'Ds': '281.', 'Rg': '281.', 'Cn': '285.', 'Nh': '286.', 'Fl': '289.',
                  'Mc': '289.', 'Lv': '293.', 'Ts': '293.', 'Og': '294.'}

def matching_closing(text):
    p = 1
    for i, c in enumerate(text):
        if c == '(':
             p += 1
        if c == ')':
            p -= 1
            if not p:
                return i
    return None

def chunks(text):
    tx = text[:]
    while tx:
        if tx[:2] in atomic_weights:
            e = tx[:2]
            tx = tx[2:]
        elif tx[0] in atomic_weights:
            e = tx[0]
            tx = tx[1:]
        elif tx[0] == '(':
            p = matching_closing(tx[1:])
            e = tx[:p+1]
            tx = tx[p+2:]
        else:
            raise CalcError('molar mass gone wrong', tx)
        if not tx or not tx[0].isdigit():
            nr = 1
        else:
            digs = ''
            while tx and tx[0].isdigit():
                digs += tx[0]
                tx = tx[1:]
            nr = int(digs)
        yield e, nr

def molar_mass(text):
    M = Q()
    tx = text[:]
    for element, nr in chunks(tx):
        if element.startswith('('):
            #rint (nr, '* (', end='')
            M += Q(nr) * molar_mass(element[1:])
            #rint (')', end='+')
        else:
            M += Q(nr) * Q(atomic_weights[element]) * unitquant['g'] / unitquant['mol']
            #rint(nr, '*', element, end='+')
    M.provenance = set()
    M.name = 'M[%s]' % text
    return M
