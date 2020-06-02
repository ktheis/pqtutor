# coding=utf-8

from bottle import get, post, run, request, response, static_file, default_app
from http import cookies
import re

"""
Module to tie the quantities, calculator, and form modules together into an online calculator.

The calculator is hosted on ktheis.pythonanywhere.com, but you could have a local server or run it
on other platforms. In the calculator, you define values of named physical quantities,
and then do arithmetic with them. The web server is implemented using web.py.

"""
from calculator import calc, State
from comments import extract_knowns, create_comment, markup_comment
from form import newform, printableLog, helpform, exdict, submitform
from database import get_example, get_answer, example_list
from database import metacognitive_followup
from exampletracer import grade_answer, generate_hints, generate_tutor_comments
from chemistry import show_formulae, formula_details, show_quantities
import datetime
import urllib.parse
import json
from html import escape, unescape
from phenotype import newpheno, workpheno


@get('/')
def index_get():
    known = [' -- nothing yet -- ']
    query = request.query
    if 'switch' in query:
        commands = "\n".join(["__%s__ = 1" % switch for switch in query['switch'].split("*")])
        result, inputlog = calc('', commands)
        return newform(result, '', inputlog)
    if 'prefill' in query:
        prefill = urllib.parse.unquote(query.prefill)
    else:
        prefill = ''
    datestamp = datetime.datetime.now()
    metadata = '\n'.join(["0","0", datestamp.isoformat()])
    print('The get time is', datestamp)
    return newform(('', '', '', known, ''), '', '', metadata=metadata, prefill=prefill)


@post('/')
def index_post():
    # response.set_header('Content-Type', 'text/html; charset=utf-8')
    response.set_header('X-XSS-Protection', '0')
    datestamp = datetime.datetime.now()
    if request.forms.get('sub') == "reset":
        return newform(('', '', '', '', ''), '', '')
    if request.forms.get('sub') == "resubmit":
        prefill = request.forms.inputlog
        return newform(('', '', '', [], ''), '', '', actualpref=prefill)
    if request.forms.get('sub') == "help":
        return helpform()

    oldmemory = request.forms.get('memory')
    oldinputlog = request.forms.get('inputlog')
    oldlogbook = request.forms.get('logbook')
    md = unescape(request.forms.get('metadata'))
    print(md)
    try:
        level, sessionid, lasttime = md.splitlines()
        level = int(level)
        sessionid = int(sessionid)
    except:
        level, sessionid, lasttime = 0, 0, "no time"
    commands = request.forms.get('commands')
    level += 1
    if request.forms.get('sub') == "export":
        return printableLog(State(oldmemory), oldlogbook, oldinputlog)
    metadata = '\n'.join([str(level), str(sessionid), datestamp.isoformat()])
    print(metadata)

    result, newinputlog = calc(oldmemory, commands)
    # verboselog, brieflog, memory, known, linespace = result
    inputlog = oldinputlog + newinputlog
    print(inputlog)
    return newform(result, oldlogbook, inputlog, metadata=metadata)

newtext = '''
This form is to add a new question (and answer). Just enter the material in the input box and press go to check it.
Then, press Save to upload it to the question database and note the url that will access the question. Below are shortcuts to start with a heading
and to insert the answer header. Everything after the answer header is the model answer and will not be shown when working
 on the new problem (it will be used to generate prompts from the study group, though, and for checking the answer once it is submitted. The answer should
 conclude with a multiple choice question (again, use the short cut).<br><br>
<span style="color:navy; cursor:pointer; font-size:12pt;"
onclick="insertAtCaret('commands','<h3></h3>', 5)">add heading<br></span>
<span style="color:navy; cursor:pointer; font-size:12pt;"
onclick="insertAtCaret('commands','\\n<h4>Answer:</h4>\\n', 0)">add answer<br></span>
<span style="color:navy; cursor:pointer; font-size:12pt;"
onclick="insertAtCaret('commands','{&quot;http:\\example.com&quot;}', 0)">add image<br></span>
<span style="color:navy; cursor:pointer; font-size:12pt;"
onclick="insertAtCaret('commands','<a href=./hw1.1>worked example</a>', 0)">add link to worked example<br></span>
<span style="color:navy; cursor:pointer; font-size:12pt;"
onclick="insertAtCaret('commands','\\nThink about it: ...?\\n a) ...\\nb) ...\\nc) ...\\nd) ...', 0)">add multiple choice<br></span>
'''

@get('/lab12')
def pheno_get():
    return newpheno()

@post('/lab12')
def pheno_post():
    start = request.forms.get('start')
    clones = request.forms.get('clones')
    what = request.forms.get('what')
    parameters = request.forms.get('parameters')
    return workpheno(start, clones, what, parameters)


@get('/author')
def new_get():
    known = [' -- nothing yet -- ']
    return newform((newtext, '', '', known, ''), '', '', action='author',
                   button2=' Save ', otherbuttons=('export',))

@get('/ico/:file')
def send_ico(file):
    return static_file(file, root='static/')


@get('/<nr:re:example.*>')
def example(nr):
    """
    Shows the PQCalc form pre-filled with example calculation commands.
    """
    # web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
    known = ["nothing yet"]
    prefill = nr.split('example')[1]
    return newform(('', '', '', known, ''), '', '', prefill=prefill)


@get('/<nr:re:workedexample.*>')
def workedexample(nr):
    """
    Presents a worked example.
    """
    response.set_header('X-XSS-Protection', '0')
    prefill = nr.split('example')[1]
    text = exdict[prefill][:-2]
    if '<h4>Answer:</h4>' in text:
        text = text.split('<h4>Answer:</h4>')[0]
    result, good_input = calc('', text)
    logbook = ''
    pref = '' #''\n'.join(extract_knowns('='.join(text.split('\n')[1:])))+'\n'
    #print(pref)
    #print(text)
    show_top = not prefill.endswith('problem')
    return newform(result, logbook, good_input, actualpref=pref, show_top=show_top)

@get('/cookie')
def cookie():
    mem = request.get_cookie("visited")
    if mem:
        mem = eval(mem)
        pref = mem.decode('utf-8')
    else:
        response.set_cookie("visited", "nothing yet")
        pref = "Hello there. Nice to meet you"
    return newform(('', '', '', '', ''), '', '', actualpref=pref, action='./cookie')

@post('/cookie')
def cookie_post():
    oldsymbols = request.forms.get('memory')
    logbook = request.forms.get('logbook')
    inputlog = request.forms.get('inputlog')
    if request.forms.get('sub') == "export":
        allsymbols = State(oldsymbols, False)
        return printableLog(allsymbols, logbook, inputlog)
    if request.forms.get('sub') == "help":
        return helpform(False)
    commands = request.forms.get('commands')
    result, good_input = calc(oldsymbols, commands, False)

    inputlog = inputlog + good_input
    enc = inputlog.encode('utf-8')
    enc = repr(enc[-3000:])
    response.set_cookie("visited", enc)
    return newform(result, logbook, inputlog, action='./cookie')


@get('/<hwid:re:hw.*>')
def hw(hwid):
    datestamp = datetime.datetime.now()
    try:
        course = request.url.split('.com')[1]
    except:
        course = 'none'
    metadata = '\n'.join(["0","0", course, datestamp.isoformat()])
    if 'ConfChem' in hwid:
        hwid = hwid.replace('ConfChem', '')
    WESP = False
    if hwid.endswith('a'):
        hwid = hwid[:-1]
        WESP = True
    question = get_example(hwid[2:])
    if not question:
        return example_list()
    if '@@' in question:
        question, pref = question.split('@@', 1)
    else:
        pref = ''
    answer, followup = get_answer(hwid[2:])
    #rint('question', question)
    result, good_input = calc('', question + '\n__names__ = 1')

    inputlog = good_input
    logbook = ''
    if hwid[-1].isalpha():
        outp, logp, memory, known, linespace = result
        outp = '<span style="font-size: 12pt; color: maroon;">' + outp + '</span><br>'
        logp = '<span style="font-size: 12pt; color: maroon;">' + logp + '</span><br>'
        outp = outp.replace('color: navy', 'color: indigo')
        logp = logp.replace('color: navy', 'color: indigo')
        if followup:
            outp = outp + '<hr>' + '<span title="%s">Think about it...</span>' % followup.splitlines()[0]
        result = outp, logp, memory, known, linespace
        return newform(result, logbook, inputlog,
                       action=hwid, button2='help', otherbuttons=('export',), actualpref=pref, metadata=metadata)
    if WESP:
        outp, logp, memory, known, linespace = result
        outp = outp + '<br><hr><br>Now try this <a href="./%sb">related problem<a><br><br><hr>' % hwid
        result = outp, logp, memory, known, linespace
        return newform(result, logbook, inputlog, action=hwid, button2='help', otherbuttons=('export',), show_top=True, metadata=metadata)
    return newform(result, logbook, inputlog, action=hwid, button2='help', otherbuttons=('export',), show_top=True, metadata=metadata)


def tablefy(nestedlist):
    outp = ['<table>']
    for row in nestedlist:
        outp.append('<tr>')
        for item in row:
            outp.append('<td>' + item + '</td>')
        outp.append('</tr>')
    outp.append('</table>')
    return '\n'.join(outp)


def sanitize(text):
    if 'onclick' in text:
        text =  re.sub('onclick="[^"]*"', '', text)
        ''''onclick="insertAtCaret('commands','Sorry, click-to-paste not supported on this browser', '0')"'''
        return text
    return text

@post('/<hwid:re:hw.*>')
def hw_post(hwid):
    datestamp = datetime.datetime.now()
    oldsymbols = request.forms.get('memory')
    logbook = request.forms.get('logbook')
    inputlog = request.forms.get('inputlog')
    oldstuff = len(inputlog.splitlines())
    browser = request.environ.get('HTTP_USER_AGENT').lower()
    md = unescape(request.forms.get('metadata'))
    try:
        level, sessionid, course, lasttime, help_sought = md.splitlines()
        level = int(level)
        sessionid = int(sessionid)
        help_sought = int(help_sought)
    except:
        level, sessionid, course, lasttime, help_sought = 0, 0, "none", "no time", 0
    commands = request.forms.get('commands')
    level += 1
    hints = request.forms.get('hints')
    if hints:
        hints = json.loads(unescape(hints))
    #rint(oldstuff, inputlog)
    if request.forms.get('sub') == "export":
        allsymbols = State(oldsymbols)
        return printableLog(allsymbols, logbook, inputlog)
    ####################################
    result, good_input, = calc(oldsymbols, commands)
    ####################################
    metadata = '\n'.join([str(level), str(sessionid), course, datestamp.isoformat(), str(help_sought)])

    if commands:
        inputlog = inputlog + "\n" + good_input
    outp, logp, memory, known, linespace = result
    if 'chrome' in browser:
        outp = sanitize(outp)
        logp = sanitize(logp)
        result = outp, logp, memory, known, linespace
    answer, followup = get_answer(hwid[2:])
    question = get_example(hwid[2:])
    if '@@' in question:
        question, pref = question.split('@@', 1)
    student_answer = inputlog[:]
    for q in question.splitlines():
        if not q:
            continue
        student_answer = student_answer.replace(q+'\r\n', '')
        if q.startswith('@@'):
            break
    if request.forms.get('sub') == "done":
        if not followup:
            followup = metacognitive_followup()
        if help_sought:
            outp = outp + '<hr><br>You talked to the study group %d times. I hope they were helpful.<br>' % help_sought
        else:
            outp = outp + '<hr><br>The study group had a lot to say (maybe ask them next time)<br>'
        fu = followup.splitlines()
        fu[0] = fu[0] + '<br>'
        rform = '<input type="radio" id="%s" name="multchoice" value="%s"><label for="%s">%s</label><br>'
        for i, letter in enumerate(['a', 'b', 'c', 'd'], start = 1):
            fu[i] = rform % (letter, letter, letter, markup_comment(fu[i].split(maxsplit=1)[1]))
        outp += '<h4>One last question...</h4>'
        outp +=  ''.join(fu) + '<br>Please choose an answer above and enter your pin below before you submit your work.<br>'
        try:
            memory = grade_answer(student_answer, answer, question, hwid, verbose=True)
        except ZeroDivisionError:
            memory = hwid + ": The grading TA is out for the day. We'll check your work later"
        return submitform((outp, logp, memory, '', ''), logbook, inputlog,
                       actualpref='PIN',
                       button2='send', action='yippee', metadata=metadata)
    if not commands:
        if '__tutor__' in inputlog:
            outp = 'Tutor says: Please input commands. I will comment but give no hints'
        else:
            if not hints:
                #rint("Hints for:", hwid)
                #rint("Student answer:", student_answer)
                hints, debug_info = generate_hints (hwid, student_answer, answer, question)
                for h in hints:
                    pass #rint(h)
                #rint('done with hints')
            else:
                debug_info = None
            if '__debug__' in inputlog:
                outp = '\n'.join(hints)
                hints = None
            else:
                outp = hints.pop(0)
                if not hints:
                    hints = [outp]
            if '__debug__' in inputlog and debug_info:
                outp = outp + tablefy(debug_info)
            hints = json.dumps(hints)
        metadata = '\n'.join([str(level), str(sessionid), course, datestamp.isoformat(), str(help_sought + 1)])
        return newform((outp, '', memory, known, linespace), logbook, inputlog, action=hwid, button2='done', otherbuttons=('export',), hints=hints, metadata=metadata)
    else:
        if '__tutor__' in inputlog and '__tutor__' not in commands:
            feedback = generate_tutor_comments (hwid, inputlog, oldstuff, answer, question)
            outp, logp, memory, known, linespace = result
            return newform((outp + feedback, logp, memory, known, linespace), logbook, inputlog,
                           action=hwid, button2='done', otherbuttons=('export',), metadata=metadata)

    return newform(result, logbook, inputlog,
                   action=hwid, button2='done', otherbuttons=('export',), metadata=metadata)

@post('/yippee')
def hw_post():
    md = unescape(request.forms.get('metadata'))
    try:
        level, sessionid, course, lasttime, help_sought = md.splitlines()
        level = int(level)
        sessionid = int(sessionid)
        help_sought = int(help_sought)
    except:
        level, sessionid, course, lasttime = 0, 0, "none", "no time", 0
    grade = request.forms.get('memory')
    logbook = request.forms.get('logbook')
    inputlog = request.forms.get('inputlog')
    oldstuff = len(inputlog.splitlines())
    if '__names__ = 1' in inputlog:
        inputlog = inputlog.split('__names__ = 1')[1]
    for line in inputlog.splitlines():
        if line:
            print(line)
    commands = request.forms.get('commands')
    print(grade)
    for line in commands.splitlines():
        print(line)
    hwid = grade.split(':')[0].split('hw')[1]
    try:
        author = commands.split("email):")[1][:4]
    except:
        author = ''
    return grade + '\n<br><hr>Thanks for submitting!'

@get('/<nr:re:formulae.*>')
def formula(nr):
    response.set_header('X-XSS-Protection', '0')
    try:
        if '.' in nr:
            text = formula_details(*nr.split('formulae')[1].split('.'))
            result, good_input = calc('', text)
            outp, logp, memory, known, linespace = result
            result = outp, logp, memory, known, linespace
            return newform(result, '', '', action=None, button2='', otherbuttons='',
                           actualpref="\n\nClick on formulas to make commands appear here (and then copy into calculator)\n")
        else:
            text = show_formulae(int(nr.split('formulae')[1]))
    except ZeroDivisionError:
        text = 'No data'
    result, good_input = calc('', text)
    return newform(result, '', '', action=None, button2='', otherbuttons='', show_top=True,
                   actualpref="\n\nClick on formulas to make commands appear here (and then copy into calculator)\n")

@get('/<nr:re:units.*>')
def unit_table(nr):
    response.set_header('X-XSS-Protection', '0')
    try:
        text = show_quantities(int(nr.split('units')[1]), flashcard=False)
        s = State()
        for line in text.splitlines():
            if line.startswith('@'):
                create_comment(line, s)
            else:
                s.printnlog(line)
    except ValueError:
        result = ('No data',)
    result = '\n'.join(line.replace('<br>','') for line in s.output), '', '', '', ''
    return newform(result, '', '', action=None, button2='', otherbuttons='', show_top=True,
                   actualpref="Click on formulas to make commands appear here\n")




if __name__ == '__majin__':
    hwid = 'hw3.19b'
    answer, followup = get_answer(hwid[2:])
    question = get_example(hwid[2:])
    student_answer = '''
      V_1 = 0.0250 L
      c_1 = 2.04 M
      V_2 = 0.5000 L
      c_2 = ?
      c_2 = (V_1 * c_1)/V_2
'''.strip().splitlines()

    for i, line in enumerate(student_answer):
        print(line.strip())
        hints, debug_info = generate_hints(hwid, '\n'.join(student_answer[:i+1]), answer, question)
        for h in hints[:-1]:
            print('    ', h.split('<br>')[-1])

run(host='localhost', port=8080, debug=True)
#application = default_app()
