# coding=utf-8
"""
Functions to run an interpreter for expressions containing physical quantities.

Based on the Q class in the quantities module, this provides functions to input and interpret expressions,
calculating their values and showing the steps, and finally storing the quantities so that they can be
used for further calculations.

This is an arithmetic calculator rather than an algebra system (i.e. unknowns are not allowed and will lead to
error messages). Output is either in plain text or in HTML/MathML via LaTeX.

Call hierarchy:

    calc(memory, commands, mob):
        class State(OrderedDict):
        classify_input(a, state):
            extract_identifier()
        check_name(sym, state):
        interpret(t, state): -> mathparser.py
        register_result(result0, sym, state):
        show_work(result, sym, flags, error=False, addon="", skipsteps=False):

        comments(line):
        convert_units(input_type, command, quant, units, state):
        create_comment(a, state):
            markup_comment(): -> comments.py
        create_unknown()
        change_flag(flags, name, expression):
        deal_with_errors(err, a, state):
    calc2:
        see calc


"""

from form import exdict
from mathparser import CalcError, interpret, scan_it
from mathparser import check_name, extract_identifier
import quantities
from quantities import QuantError, Q, X, latex_name, unitquant, Units
from comments import create_comment, markup_comment
from chemistry import typicalunits, pronounce, naming_conventions
# from mpmath import mpf
from fractions import Fraction

# X, Units, Fraction are all for an eval statement

Empty, Calculation, ConversionIn, ConversionUsing, Comment, Flags, Unknown, CalcUsing = range(8)


def calc(memory, commands):
    '''

    :param memory: quantities already defined, given as repr()s line by line in a string
    :param commands: string of user input specifying math operations to define new quantities
    :return: everything needed to show the result in a browser and keep state for the next calculation
    '''
    state = State(memory)
    try:
        for command in commands.replace('\r', '').split("\n"):
            input_type, name, expression = classify_input(command, state)
            if input_type in [Calculation, CalcUsing]:
                name = check_name(name, state)
                if input_type == Calculation:
                    quantity = interpret(expression, state)
                else:
                    expression, preferred_units = expression.split(' using', maxsplit=1)
                    quantity = interpret(expression, state)
                    if quantity.provenance:
                        raise CalcError("Please don't calculate and convert in a single statement")
                state.printwork(show_work(quantity, name, state.flags))
                register_result(quantity, name, state)
            elif input_type == Comment:
                create_comment(name, state)
            elif input_type == Unknown:
                create_unknown(name, state)
            elif input_type in [ConversionUsing, ConversionIn]:
                convert_units(input_type, name, expression, state)
            elif input_type == Flags:
                change_flag(state.flags, name, expression)
            state.log_input(command)
    except (CalcError, OverflowError, QuantError) as err:
        deal_with_errors(err, command, state)
    return state.export()


from collections import OrderedDict


class State(OrderedDict):
    def __init__(self, memory=''):
        """
        Loads quantities from previous calculations by evaluating their repr()s

        :param memory: String of repr()s
        :stores OrderedDict of symbols, output, logput
        """
        OrderedDict.__init__(self)
        self.flags = set()
        self.output, self.logput, self.good_input = [], [], []
        self.snuck = 0
        if memory:
            for a in memory.replace('\r', '').split('\n'):
                if a.startswith('__'):
                    self.flags.add(a)
                else:
                    q = eval(a)
                    self[q.name] = q

    def addsnuck(self, q):
        name = 'Snuck%s' % self.snuck
        self.snuck += 1
        for qn in self:
            if str(self[qn]) == str(q):
                q.twin = qn
                break
        self[name] = q

    def popsnuck(self):
        if self.snuck > 0:
            self.snuck -= 1
            name = 'Snuck%s' % self.snuck
            del (self[name])

    def printit(self, str):
        self.output.append(str)

    def logit(self, str):
        self.logput.append(str)

    def printnlog(self, str):
        self.printit(str)
        self.logit(str)

    def printwork(self, outlog):
        cond1 = len(self.output) >= 2
        cond2 = cond1 and not self.output[-2].endswith('>')
        if cond1 and cond2:
            self.printnlog('<br>')
        self.output.extend(outlog[0])
        self.logput.extend(outlog[1])

    def log_input(self, inp):
        self.good_input.append(inp)

    def export(self):
        if self.output and not self.output[-1].endswith("<hr>"):
            self.output = ["<hr>"] + self.output
        verbose_work = '\n'.join(self.output)
        if "__latex__" in self.flags:
            verbose_work = "<pre>" + verbose_work.replace(r'\)', '$').replace(r'\(', '$') + "</pre>"
        brief_work = '\n'.join(self.logput)
        memory = [q.__repr__() for q in self.values()] + list(self.flags)
        m = '\n'.join(memory)
        known = [s + " = " + self[s].__str__() for s in self]
        linespace = '60%' if '__scrunch__' in self.flags else '120%'
        input_log = '\n'.join(self.good_input)
        if not input_log.endswith('\n'):
            input_log = input_log + '\n'
        return (verbose_work, brief_work, m, known, linespace), input_log


naming_rules = '''Rules for names: Start with a letter, then letters or numbers or underscores (no blanks).
  Examples: m0, y, s_15
Special rule #1: You can't use symbols that are used in math, such as "+ - = * / ( )" or have special meanings for comments such as "! @ # %".
Special rule #2: You can add anything in brackets, [...], or just have something in brackets
  Examples: [NaCl], [Na+], c[Na+], M[Na+]
Special rule #3: You can't use names already used for units or functions. If you do, the program will add an underscore.
  Examples: mm, s, V, and log are not allowed, and will be used as mm_, s_, V_, and log_'''


def classify_input(a, state):
    '''
    :param a: the user input string containing a calculation, unit conversion or comment
    :param state: contains known quantities as ordered dict, along with flags and output
    :return: a tuple (type of input, symbol name, expression/units)


    >>> classify_input(' ', State())
    (0, None, None)
    >>> classify_input('K[A<=>B] = 13', State())
    (1, u'K[A<=>B]', u' 13')
    >>> classify_input('R using J', State())
    (3, u'R', u'J')
    >>> classify_input('K[A<=>B] in mM', State())
    (2, u'K[A<=>B]', u'mM')
    >>> classify_input('5 + 6', State())
    (1, u'result', u'5 + 6')
    >>> classify_input('#comment', State())
    (4, None, None)
    >>> classify_input('!H2O', State())
    (4, None, None)

    '''
    if not a or not a.strip():
        return Empty, None, None
    if '__newby__' in state.flags and not a.startswith('__'):
        state.printit('<pre style="color:maroon"><b>>>>> %s</b></pre>' % a.replace('<', '&lt;').replace('>', '&gt;'))
    elif not a.startswith('__'):
        state.printit("<br>" if not '/h' in ''.join(state.output[-1:]) else '')
    state.logit("<br>" if not '</h' in ''.join(state.logput[-1:]) else '')

    if a[0] in "!#@":
        return Comment, a, None
    a = a.strip()
    if a.startswith('__'):
        if not '=' in a:
            return Comment, a, None
        name, onoff = a.split('=', 1)
        return Flags, name.strip(), onoff
    match = extract_identifier(a)
    start = match.end() if match else 0
    rest = a[start:].strip()
    if match and rest.startswith('='):
        r2 = rest[1:].strip()
        if not r2:
            return Empty, None, None
        if r2[0] == '?':
            return Unknown, a[:start], None
        scanned, remainder = scan_it(rest[1:])
        if remainder and remainder.startswith('='):
            return Comment, '@' + a, None
        if ' using' in rest[2:]:
            return CalcUsing, a[:start], rest[1:]
        return Calculation, a[:start], rest[1:]  # Calculation #
    elif match and a[start:].startswith(' using') and a[:start].strip() in state:
        return ConversionUsing, a[:start], rest[len('using'):].strip()
    elif match and a[start:].startswith(' in ') and a[:start].strip() in state:
        return ConversionIn, a[:start], rest[len('in'):].strip()
    if ' =' in a:
        name = a.split(' =')[0]
        if ' ' not in name:  # e.g. '<img src="https://opentextbc.ca//hematite.jpg", width = "20%">
            raise CalcError("%s is not a valid name for a quantity<br><pre>%s</pre>" % (name, naming_rules))
    try:  # check for calculation on the fly, e.g. '5 + 6' instead of 't = 5 + 6'
        interpret(a, state, warning=False)
    except (CalcError, OverflowError, QuantError):
        return Comment, a, None
    if '__names__' not in state.flags and '__newby__' not in state.flags:
        return Calculation, "result", a
    else:
        raise CalcError("Please assign calculations to a value ... or switch to advanced mode")


def register_result(result0, sym, state, keep_provenance=False):
    """
    Enters the quantity that was just calculated into the database

    :param result0: quantity Q()
    :param sym: name of the quantity
    :param state: contains known quantities as ordered dict, along with flags and output
    """
    if not keep_provenance:
        result0.provenance = []
        result0.name = sym[:]
    if hasattr(result0, 'depth'):
        del result0.depth
    if sym in state and '__allowupdate__' not in state.flags:
        state.printit('<div style="color: green;">Warning: Updated value of \\(%s\\)</div><br>' % (latex_name(sym)))
    state[sym] = result0
    if '__fracunits__' not in state.flags:
        for u in result0.units:
            if u.denominator != 1:  # oddly, ints have and floats don't
                state.printit('<div style="color: green;">Warning: Units have non-integer exponents %s</div><br>' % u)
    if "__checkunits__" in state.flags:
        if len(sym) == 1 or sym[1] in "_0123456789[" or sym[0] == "[":
            if sym[0] in naming_conventions and result0.units != naming_conventions[sym[0]][0][0]:
                state.printit(
                    '<div style="color: green;">Warning: \\(%s\\) looks like a %s, but units are strange</div><br>' % (
                        latex_name(sym), naming_conventions[sym[0]][0][1]))


latex_subs = {"%s / %s": "\\dfrac{%s}{%s}",
              "%s * %s": "%s \\cdot %s",
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
              "sum(%s": "\\sum (%s",
              "max(%s": "\\mathrm{max}(%s",
              "abs(%s)": "\\mathrm{abs}(%s)",
              "moredigits(%s)": "\\mathrm{moredigits}(%s)",
              "uncertainty(%s)": "\\mathrm{uncertainty}(%s)",
              }


def show_work(result, sym, flags, error=False, addon="", skipsteps=False):
    """
    Shows the steps in getting from formula to calculated value. This function is called not only by calc(),
    but also by convert_units() and deal_with_errors() to show steps in calculations.

    :param result: value and provenance of the quantity Q()
    :param sym: name of the quantity
    :param flags: Switches that determine how much detail is shown
    :param error: True if used to show an error in a step of a calculation
    :param addon: Used when called from convert_units(ConversionIn)
    :param skipsteps: True when intermediate steps are to be skipped
    :return: tuple containing detailed output, brief output
    """
    output = []
    logput = []
    math = 'plain math' not in flags
    if math:
        writer = quantities.latex_writer
        if "__latex__" not in flags:
            logput.append(
                '''<span style="color:navy; cursor:pointer; font-size:12pt;" onclick="insertAtCaret('commands','%s ', 0)">''' % sym)
            output.append(
                '''<span style="color:navy; cursor:pointer; font-size:12pt;" onclick="insertAtCaret('commands','%s ', 0)">''' % sym)
    else:
        writer = quantities.ascii_writer
    subs = latex_subs if math else None
    d = result.setdepth()
    if math:
        template1 = "%s \(= %s%s\)%s<br>"
        template2 = r"<br><span title='%s'>\(\ \ \ =%s%s\)</span><br>"
    else:
        template1 = "%s = %s%s%s" if d <= 0 else "%s = %s\n   = %s%s"
        template2 = "%s   = %s%s (%s)"
    task = result.steps(-1, writer, subs, ())  # task
    if '__hidenumbers__' in flags:
        task = result.steps(-1, quantities.latex_writer, subs)
    name = r"<span title='%s'>\(%s\)</span>" % (pronounce(sym, result.units), latex_name(sym)) if math else sym
    output.append(template1 % (name, task, addon, markup_comment(result.comment)))
    logput.append(template1 % (name, task, addon, markup_comment(result.comment)))
    if not skipsteps:
        for dd in range(1, d + 1):
            if dd == 1:

                first = result.steps(dd, writer, subs, flags)
                if '__hidenumbers__' in flags:
                    first = result.steps(dd, quantities.latex_writer, subs, {'__hidenumbers__'})
                if first != task:
                    output.append(template2 % ("", first, addon))
            else:
                output.append(template2 % ("", result.steps(dd, writer, subs, flags), addon))  # intermediate steps
    result_str = result.steps(0, writer, subs, flags)  # result
    if '__hideunits__' in flags:
        task = result.steps(-1, writer, subs, flags)
    if result_str != task and not error and not ('__hidenumbers__' in flags and d == 0):
        logput.append(template2 % (pronounce(sym, result.units), result_str, addon))
        output.append(template2 % (pronounce(sym, result.units), result_str, addon))
    if math and not '__latex__' in flags:
        logput.append('<br></span>')
        output.append('<br></span>')
    return output, logput


def convert_units(input_type, quant, units, state):
    """
    Shows the quantity in different units, either once only ('in') or from now on ('using')

    :param input_type: Whether conversion is with "using" or "in"
    :param quant: Q() to be converted
    :param units: requested units
    :param state: contains known quantities as ordered dict, along with flags and output
    :raise CalcError: if requested units are unknown
    """
    flags2 = state.flags - {'__hideunits__'}
    if input_type == ConversionUsing:
        print(repr(state[quant.strip()]))
        if units in ['°ΔC', '°aC']:
            prefu = [units]
            q = state[quant.strip()] + Q(0.0)
            if units == '°aC' and unitquant['K'].units != q.units:
                raise CalcError("Only quantities in kelvin may be converted to celsius")
        else:
            prefu = units.split()
            for p in prefu:
                if p not in unitquant:
                    raise CalcError(
                        "PQCalc does not recognize the unit '%s', so 'using' does not work. Try 'in' instead." % p)
            try:
                q = state[quant.strip()] + Q(0.0)
            except KeyError:
                raise CalcError("The quantity '%s' is not defined yet. Check for typos." % quant.strip())
        q.name = ''
        q.provenance = None
        q.comment = ''
        outp, _ = show_work(q, quant, flags2)
        output = (outp[:-1])
        state[quant.strip()].prefu = set(prefu)
        q_old = state[quant.strip()]
        if q_old.provenance:  # when called by calc2
            q_old.name = ''
            q_old.provenance = None
        q = q_old + Q(0.0)
        q.comment = ''
        outp, _ = show_work(q, quant, flags2)
        output.extend(outp[-2 if not 'plain math' in state.flags else -1:])
        q = state[quant.strip()] + Q(0.0)
        q.name = ""
        q.provenance = None
        _, logp = show_work(q, quant, flags2)
        state.printit('\n'.join(output))
        state.logit('\n'.join(logp))
        print(repr(state[quant.strip()]))
    else:
        tmp = interpret(units, state, warning=False)
        try:
            qq = state[quant.strip()] / tmp
        except KeyError:
            raise CalcError("The quantity '%s' is not defined yet. Check for typos." % quant.strip())
        addon = ("\mathrm{\ %s}" % quantities.latex_name(units))
        work = show_work(qq, quant, flags2, addon=addon)
        state.printwork(work)


def create_unknown(sym, state):
    state.printnlog(
        '''<span title="%s" style="color:navy; font-size:12pt; cursor:pointer" onclick="insertAtCaret('commands','%s = ', 0)">''' % (
        pronounce(sym), sym))
    state.printnlog("\(%s\) = ?<br>" % latex_name(sym))
    state.printnlog('<br></span>')


def change_flag(flags, name, expression):
    if expression.strip() != '0':
        flags.add(name)
    else:
        flags.discard(name)


def deal_with_errors(err, a, state):
    """

    :param err: the exception that was raised
    :param a: the imput that led to the exception
    :param state: contains known quantities as ordered dict, along with flags and output
    :raise err: For exceptions not raised explicitly "unexpected errors"
    """
    if type(err) is QuantError:
        # QuantError((complaint, Q(0, name, provenance=provenance)))
        problem = err.args[0]
        state.printit('<div style="color: red;"><pre>' + a + "</pre>")
        state.printit('Calculation failed: %s<br><br></div>' % problem[0])
        if problem[1]:
            output, _ = show_work(problem[1], "problem", state.flags, error=True)
            state.printit('\n'.join(output))
        state.printit("</div>")
    elif type(err) is ZeroDivisionError or type(err) is OverflowError:
        state.printit("Overflow error, sorry: %s" % a)
    elif type(err) is CalcError:
        if "__newby__" not in state.flags:
            state.printit('<div style="color: red;"><pre>' + a + "</pre></div>")
        state.printit(err.args[0])
    else:
        raise err


def calc2(command, state=State(), keep_provenance=True):
    '''

    :param command:
    :param state:
    :return: type, name, q, expression = calc2(line, state)
    '''
    quantity = None
    name = None
    type_text = 'Calc'
    try:
        input_type, name, expression = classify_input(command, state)
        if input_type == Calculation:
            name = check_name(name, state)
            quantity = interpret(expression, state, keep_onthefly=True)
            if quantity.provenance and any(name == q.name for q in quantity.provenance):
                print('uhoh')
            if not quantity.provenance:
                if quantity.name and not name.startswith('M['):
                    quantity = Q(number=quantity.number, name='is %s', units=quantity.units, uncert=quantity.uncert,
                                 provenance=(quantity,))
                else:
                    if quantity.units != Units():
                        state.popsnuck()
                    type_text = 'Known'
            if quantity.name == '-%s' and not quantity.provenance[0].provenance:
                type_text = 'Known'
            register_result(quantity.copy(), name, state, keep_provenance=keep_provenance)
        elif input_type == CalcUsing:
            name = check_name(name, state)
            expression, preferred_units = expression.split(' using', maxsplit=1)
            quantity = interpret(expression, state)
            if quantity.provenance:
                raise CalcError("Please don't calculate and convert in a single statement")
            register_result(quantity.copy(), name, state)
            type_text = 'Known'
            convert_units(ConversionUsing, name, preferred_units, state)
        elif input_type in [ConversionUsing, ConversionIn]:
            convert_units(input_type, name, expression, state)
            return 'Conversion', None, None, None
        elif input_type == Unknown:
            return 'Unknown', name, None, None
        else:
            return 'Comment', None, None, None
    except (CalcError, OverflowError, QuantError) as err:
        raise
        return 'Error', None, None, None
    return type_text, name, quantity, expression


def test_examples(math, minex, maxex):
    a = 0
    for ex, commands in exdict.items():
        a += 1
        if False and a in [2, 3, 12, 14, 19, 20, 21, 22, 24, 25, 26, 27, 42]:
            # print(a, ex)
            continue
        if a < minex:
            continue
        if a > maxex:
            break
        print(a)
        # print('########################################################################')
        print(a, '#          %-60s#' % ex)
        # print('########################################################################')
        # print (commands)
        try:
            if a == 45:
                gg = 5
            results, input_log = calc("", commands, math)
        except:
            raise
        verbose_work, brief_work, m, known, linespace = results
        for line in verbose_work[1:]:
            pass  # print(line)


def profile_program():
    import cProfile

    memory = ""
    cProfile.run(task)


if __name__ == "__main__":
    print('hello')
    # profile_program()

    test_examples('ipud', 0, 400)
    print('did the examples')
    test_examples('iphone', 0, 400)
    print('did the examples again')
    '''commands = input(">>> ")
    memory = ""
    while True:
        output, _, memory, _, _, _, _ = calc(memory, commands, 'ipud')
        for line in output[1:]:
            print(line)
        memory = '\n'.join(memory)
        commands = input(">>> ")
    '''

"""
Test input that should fail gracefully:

sadf = 56 * (67 )()

asdf = 5 + t + &#@

gg = sin(45)

vv = 10^10^10

omg = 1 / 10^-1000
"""
