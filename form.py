# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from quantities import functions, known_units
from html import escape

selector = '''
<select %s onchange="insertAtCaret('commands',this.options[this.selectedIndex].value, %s);">
  %s
</select>'''

selectoroption = '''
  <option value="%s">%s</option>'''

def fill_selector(header, choices, backup=0):
    html = ['<option value="" selected="selected" disable="disabled">%s</option>' % header]
    for term in choices:
        html.append(selectoroption % (term, term))
    return selector % ("", backup, "".join(html))

# unit selectors, pre-baked
unit_list = list(known_units.keys())
unit_list.sort(key=lambda x: x.lower())
unit_selector = fill_selector("units", unit_list)

# function selectors, pre-baked
function_list = [f + "()" for f in functions]
function_list.extend(["using  ", "in  "])
function_selector = fill_selector("functions", function_list, backup=1)

# special symbol selector, pre-baked
symbol_list = ["⌗ve","μ", "π","ℎν ％ℳ","ΔᵣG°′","αβγδεζησχ","∞∡ℏ","äöüßø", "ΓΘΛΦΨ"]
symbol_selector = fill_selector("symbols", symbol_list)

def quant_selectors(known):
    """ Make the selector for known quantities
    """
    choices = known.split("\n")
    return fill_selector("quantities", [term.rsplit("=",1)[0] for term in choices])

example_template = '''
<h3>How to use PQcalc</h3>
<p>PQcalc is an online calculator for students learning science in college.
To learn how to use it by example, click on any of the examples below, look at the
input, then press go and study the output. A more comprehensive documentation of
the program is  <a href="http://www.bioinformatics.org/pqcalc/manual">here</a>.
<h3>Example calculations</h3><pre>%s</pre>
'''


def helpform(mob):
    return example_template % exhtml

def newform(outp, logp, mem, known, log, mob, oneline, inputlog, prefill="", linespace="100%", logo=""):
    mem = "\n".join(mem)
    known = "\n".join(known)
    if not outp:
        logo = PQlogo
    mem = mem.replace('"', '&quot;')
    inputlog = inputlog.replace('"', '&quot;')
    logbook = log.replace('"', '&quot;') + "\n" + ("\n".join(logp)).replace('"', '&quot;')
    out = log.replace('&quot;', '"') + "\n".join(outp)
    keyb = "" if mob else 'class="keyboardInput"'
    selectors = quant_selectors(known)
    selectors = selectors + unit_selector + function_selector + symbol_selector
    rows = 3
    if prefill:
        prefill = exdict[prefill][:-2]
        rows =len(prefill.split("\n"))
    data = dict(output=out, memory=mem, rows=rows, selectors=selectors, logbook=logbook, keyboard=keyb,
                prefill=prefill, head=head, buttons=buttons, linespacing=linespace, logo=logo, inputlog=inputlog)
    if oneline and not prefill:
        return template_oneline % data
    return template % data


def printableLog(symbols, logbook, inputlog):
    known = "\n".join([s + "=" + si.__str__() for s, si in symbols.items()])
    return printable_view % (known, escape(inputlog), logbook)




head = '''<head>
<meta name="format-detection" content="telephone=no">
<meta name="viewport" content="width=device-width; initial-scale=0.8;">

<link rel="shortcut icon" href="/ico/favicon.ico">

<script type="text/javascript"
  src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>

<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    TeX: { extensions: ["mhchem.js"] },
    "HTML-CSS": {scale: 85}
    });
</script>


<script type="text/javascript">

function goToAnchor() {
  location.href = "#commands";
}

</script>


<script type="text/javascript">
<!--

function insertAtCaret(areaId,text,backup) {
    var txtarea = document.getElementById(areaId);
    var scrollPos = txtarea.scrollTop;
    var strPos = 0;
    var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ?
        "ff" : (document.selection ? "ie" : false ) );
    if (br == "ie") {
        txtarea.focus();
        var range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        strPos = range.text.length;
    }
    else if (br == "ff") strPos = txtarea.selectionStart;

    var front = (txtarea.value).substring(0,strPos);
    var back = (txtarea.value).substring(strPos,txtarea.value.length);
    txtarea.value=front+text+back;
    strPos = strPos + text.length - backup;
    if (br == "ie") {
        txtarea.focus();
        var range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        range.moveStart ('character', strPos);
        range.moveEnd ('character', 0);
        range.select();
    }
    else if (br == "ff") {
        txtarea.selectionStart = strPos;
        txtarea.selectionEnd = strPos;
        txtarea.focus();
    }
    txtarea.scrollTop = scrollPos;
}
</script>
<style>
@media all {
	.page-break	{ display: none; }
}

@media print {
	.page-break	{ display: block; page-break-before: always; }
}
</style>

</head>
'''

buttons = '''
<input type="button" value="+" onclick="insertAtCaret('commands','+',0);" />
<input type="button" value="-" onclick="insertAtCaret('commands','-',0);" />
<input type="button" value="*" onclick="insertAtCaret('commands',' * ',0);" />
<input type="button" value="/" onclick="insertAtCaret('commands',' / ',0);" />
<input type="button" value="^" onclick="insertAtCaret('commands','^',0);" />
<input type="button" value="()" onclick="insertAtCaret('commands','()', 1);" />
<input type="button" value="=" onclick="insertAtCaret('commands',' = ', 0);" />
<input type="button" value="[]" onclick="insertAtCaret('commands','[]', 1);" />
'''

rest ='''
'''

PQlogo = '''<table><tr><td>

   <img  src="data:image/gif;base64,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"
width="115" height="76">



    </td><td>
    <h3> <br> 1. Set up a problem <br> 2. Solve it and press "go" <br> 3. See the work and the results </h3>
    </td></tr></table><br>
'''

template = '''<html>
%(head)s
<body>

    %(logo)s
    <div style="line-height:%(linespacing)s">

            %(output)s</div>
            <div class="page-break"></div>
            <form enctype="multipart/form-data" action="." method="post">
            <textarea autofocus rows="%(rows)d" cols="42" id="commands" name="commands" %(keyboard)s  type="number" autocapitalize="off"
              autocomplete="on" spellcheck="false" style="font-weight: bold; font-size: 12pt;"
              >%(prefill)s</textarea> <p>
            <input type="submit" name="sub" style="font-weight: bold; font-size: 18pt;" value="  go  ">

            %(selectors)s </p>
            %(buttons)s
            <input type="submit" name = "sub" value="export" />
            <input type="submit" name = "sub" value="reset" />
            <input type="submit" name = "sub" value="help" />

            <input type="hidden" name="memory" value = "%(memory)s"/>
            <input type="hidden" name="inputlog" value = "%(inputlog)s"/>
            <input type="hidden" name="logbook" value = "%(logbook)s"/>
</body>
</html>
'''

template_oneline = '''<html>
%(head)s
<body onload="goToAnchor();">
<table>
    <tr><td><h1> PQCalc</h1></td><td>
    <h3> : a scientific calculator that keeps track of units and uncertainties of physical quantities</h3>
    </td></tr></table>
<table width=100%% cellspacing="2" cellpadding="10">

    <tr>
        <td width=100%% valign="top" style="border-width:6;border-color:#1132FF;border-style:ridge">
            %(output)s
            <form enctype="multipart/form-data" action="." method="post">
            <input type="text" autofocus size="50" id="commands" name="commands" %(keyboard)s  autocapitalize="off"
              autocomplete="off" spellcheck="false" style="font-weight: bold; font-size: 12pt;">
            <input type="submit" name="sub" value="  go  ">
            <p>
            <a name="myAnchor" ></a>
            %(buttons)s
            <input type="submit" name = "sub" value="print" />
            <input type="submit" name = "sub" value="reset" />
            <input type="submit" name = "sub" value="help" />
            </p>
            %(selectors)s
            <input type="hidden" name="memory" value = "%(memory)s"/>
            <input type="hidden" name="inputlog" value = "%(inputlog)s"/>
            <input type="hidden" name="logbook" value = "%(logbook)s"/>

</body>
</html>
'''



printable_view = '''<html>
<head>
<meta name="format-detection" content="telephone=no">

<script type="text/javascript"
  src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({ TeX: { extensions: ["mhchem.js"] }});
</script>
</head>
<body>Calculation done with PQCalc, the physical quantity calculator<br>
that knows about quantities, units and uncertainties.<br><br>
by Karsten Theis, Chemical and Physical Sciences, Westfield State University<br>
inquiries and bug reports to ktheis@westfield.ma.edu<br><br>
Program currently hosted at
<a href="http://www.bioinformatics.org/pqcalc">
bioinformatics.org/PQCalc </a> and
<a href="http://ktheis.pythonanywhere.com/">
http://ktheis.pythonanywhere.com/ </a>
<h2> Known quantities </h2>
<PRE>%s</PRE>
<h2> Input </h2>
<PRE>%s</PRE>

<h2> Log of the calculation </h2>
%s
</div>
</body>
</html>
'''

example = '''problem = 1.71
# This has no units, no names like n[CH4], no sigfigs
0.6274*1.00e3/(2.205*2.54^3)
a_textbook = 17.4

problem = Units
t1 = 180 s
t2 = 4 min #notice the different unit
t_sum = t1 + t2
t_sum using s
days = min * 60 * 24
t_sum in days

problem = SigFigs Multiply
a_3sigfig = 2.63
a_5sigfig = 2.6300
b_4sigfig = 0.3128
c_less = a_3sigfig * b_4sigfig
c_more = a_5sigfig * b_4sigfig

problem = SigFigs Add
a_3sigfig = 2.63
a_5sigfig = 2.6300
b_4sigfig = 0.3128
c_less = a_3sigfig + b_4sigfig
c_more = a_5sigfig + b_4sigfig

problem = Addition
a = 5.1 s
b = 3.4 s
c = a + b

problem = Order of operations
a = -3 kJ / 5 mM * (4 atm + 5.4 Pa)

problem = Different numbers
a = (1/2) 1/s^2
__showuncert__ = 1
b = 2.341(4)
c = sqrt(a)
d = a^(1/3)

problem = Functions
a = 0.34
b = minimum(log(a), ln(a), exp(a), sin(a), cos(a), tan(a)) - maximum(absolute(-45.6(4)), quadp(1,2,-3))

problem = division
# 12.05 mol of dry ice have a mass of 530.4 g.
# What is the molar mass of [CO2]?
m[CO2] = 530.4 g
n[CO2]=12.05 mol
M[CO2] = m[CO2] /  n[CO2]

problem = crash1
m = 0.0
b = .6 / m_

problem = 4.111
V_Analyte = 100.0 mL
V_Titrant = 3.19 mL
c_Titrant = 0.0250 M
# 1:1 stochiometry...
c_Analyte = c_Titrant * V_Titrant / V_Analyte
#answer: c_Analyte =7.98e-4 M

problem = GenChem constants
R = 8.314 J/(mol K)
T_room = 293.15 K
P_atm = 1 atm
q_e = 1.602176E-19 C
c0 = 299792458 m/s
F = 96485.33 C/mol
M_H = 1.08 g/mol
M_C = 12.011 g/mol
M_O = 15.999 g/mol
M_Na = 22.9897 g/mol
M_Cl = 35.45g/mol
M_N = 14.007 g/mol
N_A = 6.02214E23 /mol

problem = languages
# Chemical equation
# 化学方程式
# Химическое уравнение
# 化学反応式
# Reaktionsgleichung
# 화학반응식
# Ecuación química
# إنشاء حسابد خول
# Równanie reakcji
# Phương trình hóa học
! O2(g) + 2H2(g) -> 2H2O(g)


problem = 1.87
percent = 1/100
year = 365 * 24 h
input_Fertilizer = 1500. kg / year
input_N = 10 percent * input_Fertilizer
wash_N = 15 percent * input_N
flow_stream = 1.4 m^3/min
[N]added = wash_N / flow_stream
[N]added using mg L
a_textbook = 0.031 mg/L

problem = 1.96
pi = 3.14159265
d_gasoline = 0.73 g/mL
d_water = 1.00 g/mL
diameter = 3.2 cm
radius = diameter / 2
m_water = 34.0 g
m_gasoline = 34.0 g
V_water = m_water / d_water
V_gasoline = m_gasoline / d_gasoline
V_total = V_water + V_gasoline
h_total = V_total / (radius^2 * pi)

#######
problem = 3.91

#given
m[CxHy] = 135.0 mg
m[CO2] = 440.0 mg
m[H2O] = 135.0 mg
M[CxHy] = 270.0 g/mol

#calculated from chemical formula
M[C] = 12.0107 g/mol
M[O] = 15.9994 g/mol
M[H] = 1.00794 g/mol
M[CO2] = M[C] + 2 * M[O]
M[H2O] = 2 * M[H] + M[O]
#<div class="page-break"></div>
#calculation
n[CO2] = m[CO2] / M[CO2]
n[C] = n[CO2]
n[H2O] = m[H2O] / M[H2O]
n[H] = n[H2O]*2
n[CxHy] = m[CxHy] / M[CxHy]
ratio[nuC:nuH] = n[C] / n[H]

# _M[CxHy] = _M[C] * _nuC + _M[H] * _nuH = _M[C] * _ratio[nuC:nuH] _nuH + _M[H] * _nuH
# _M[CxHy] = _nuH * (_M[C] * _ratio[nuC:nuH] + _M[H] )
nuH = M[CxHy] / (M[C] * ratio[nuC:nuH] + M[H])
nuC = ratio[nuC:nuH] * nuH
#texbook answer: [C20H30]

######
problem = 3.103

# If 2.50 g of [KO2] react with
# 4.50 g of [CO2], how much dioxygen
# will form (together with [K2CO3])?
m[KO2] = 2.50 g
m[CO2] = 4.50 g
! 4KO2 + 2CO2 -> 3O2 + 2K2CO3
ν[KO2] = 4
ν[CO2] = 2
ν[O2] = 3

#calculate M from chemical formula
__skip__=1
M[C] = 12.0107 g/mol
M[O] = 15.9994 g/mol
M[K] = 39.0983 g/mol

M[KO2] = M[K] + 2 * M[O]
M[CO2] = M[C] + 2 * M[O]

#calculation
__skip__=0
n[KO2] = m[KO2] / M[KO2]
n[CO2] = m[CO2] / M[CO2]

n[KO2 -> lim] = n[KO2] / ν[KO2]
n[CO2 -> lim] = n[CO2] / ν[CO2]

n[lim] = minimum(n[KO2 -> lim], n[CO2 -> lim])
V[O2] = n[lim] ν[O2] 8.314 J/(K mol) 298 K / 1 atm
V[O2] using L
m[O2] = n[lim] ν[O2] * 2 * M[O]
# textbook : _m[O2] = 0.844 g



problem = 6.87
# What is the density of radon at 298 K and 1 atm?
T = 298 K
P = 1.00 atm
R = 8.314 J / (mol K)
R using atm L
M_Rn = 222. g / mol
# Consider _n_Rn  = 1 mol
# Any other value would give the same result...
n_Rn = 1 mol
V0 = n_Rn * R T / P
m0 = n_Rn M_Rn
ρ = m0 / V0


problem = 17.27
[H+] = 3.45e-8 M
pH = -log([H+]/1 M)
#answer =
######

problem = 17.49
K_a = 1.80e-4
c = 0.0600 M
# K_a = x^2/(0.06-x) <=> x^2 + x K_a - 0.06 K_a c/M = 0
# solve quadratic: either quadp or quadn gives physically sensible answer
A_ = 1
B_ = K_a
C_ = - K_a c / 1 M
xp = quadp(A_, B_, C_)
xn = quadn(A_, B_, C_)

pH = -log(xn)
# using the approximation that c[AH] = c[total]
pH = -1/2 log(c / M K_a)
######

problem = 16.115

K1 = 4.10e-4
T1 = CtoKscale(2000.)
T2 = CtoKscale(25.)
ΔH  = 180.6 kJ/mol
R = 8.314 J/(mol K)
# ln(_K2 / _K1) = -ΔH/R (1/_T2 - 1/_T1)
K2 = K1 exp(-ΔH/R (1/T2 - 1/T1))
######
problem = made.up
T = 298.0 K
R = 8.314 J/(mol K)
K_eq = 2.54e6
ΔG° = - R T ln(K_eq)

problem = first semester
5 + 3
__tutor__ = 1
6 + 8
R_gas = 0.08205746(14) L atm K^-1 mol^-1
R_ryd = 1.0973731568539(55)e7 m^-1

problem = practice units
__hideunits__ = 1
R = 8.3144621(75) J/(K mol)
T = 298.0 K
K_eq = 2.54e6
ΔG° = - R T ln(K_eq)


problem = second semester
R = 8.3144621(75) J/(K mol)
T = 298.0 K
K_eq = 2.54e6
ΔG° = - R T ln(K_eq)

problem = physical chemistry
__showuncert__= 1

# gas constant
R =  8.3144621(75) J/(K mol)
# Boltzmann constant
k_B = 1.3806488(13)e-23 J/K
# Plank constant
h = 6.62606957(29)e-34 J s
# Speed of light (nowadays not a measurement, but a definition)
c0 = 299792458 m/s
# Mathematical constant Pi to 17 digits
π = 3.1415926535897932
# Permeability in vacuum
μ0 = 4 N A^-2 π / 10000000
# Permittivity in vacuum
ε0 = 1 / (c0^2 μ0)
# mass of electron
m_elec= 9.10938215(45)e-31kg
# Elementary charge
e = 1.60217657e-19 C
# Rydberg constant from first principles
R_H = m_elec e^4 / (8 h_^3 ε0^2 c0)
#Bohr radius to check
ħ = h_ / (2π)
a0 = 4 π ε0 ħ^2 /(m_elec e^2)

problem = R_units
R = 8.314 Pa m^3/(mol K)
R2 = R / (101325 Pa * 1 m^3) * 1 atm * 1000 L
R3 = R * 1 atm * 1000 L / (101325 Pa * 1 m^3)
R4 = R * (1 atm / 101325 Pa) * (1000 L / 1 m^3)
P = 1 atm
P using Pa

problem = concentration
# Titration of KOH with [H2SO4] to equivalence point
# Given:
V[KOH] = 5.00 mL
[H2SO4] = 0.100 M
V[H2SO4] = 34.5 mL
# Plan: 1) _n[H2SO4] via c=n/V,
#       2) _n[KOH] via coefficients,
#       3) _[KOH] via c=n/V
n[H2SO4] = [H2SO4] * V[H2SO4]
!H2SO4 + 2 KOH -> 2 H2O + 2 K+ + 2 SO4^2-
n[KOH] = n[H2SO4] / 1 * 2
[KOH]original = n[KOH] / V[KOH]


problem = showcase chemistry markup
# Limiting reagent problem
# The balanced reaction is:
! H2SO4 + 2 KOH -> 2 H2O + 2 K+ + 2 SO4^2-
# Given:
n[H2SO4]start = 3.4 mmol
n[KOH]start = 7.4 mmol
n[->] = minimum(n[H2SO4]start/1, n[KOH]start/2)
n[H2SO4]end = n[H2SO4]start - 1 * n[->]
n[KOH]end = n[KOH]start - 2 * n[->]

problem = J Chem Ed 2012, 89, 326−334
#   0.564 grams of [AgNO3] is dissolved in 25.00 mL of 0.250 molar [BaCl2].
#   A precipitate forms and is isolated and weighed.
#   Its mass is 0.392 grams.
#   What is the percent yield of the reaction?
m[AgNO3]= 0.564 g
V[BaCl2 sol] = 25.00 mL
c[BaCl2] = 0.250 M
m_prec= 0.392 g
#   Plan:
#      1) Nature of precipitate
#      2) Find limiting reagent
#      3) Calculate yield!
#
#   1) Nature of precipitate
! BaCl2(s) -> Ba^2+(aq) + 2 Cl- (aq)
! AgNO3(s) -> Ag+(aq) + NO3- (aq)
#   [AgNO3], [BaCl2], and [Ba(NO3)2] are soluble, [AgCl] isn't
#
#   2) Find limiting reagent
#      First, need a balanced chemical equation
! 2AgNO3 + BaCl2 -> 2AgCl(s) + Ba^2+ + 2 NO3-
#      Try either reagent in excess and see which gives least product
#        Case A: [AgNO3] limiting and [BaCl2] in excess
M[AgNO3] = 169.87 g/mol
n[AgNO3] = m[AgNO3] / M[AgNO3]
#            [AgNO3] and [AgCl] at equimolar ratio
n[AgCl]A = n[AgNO3]
#        Case B: [AgNO3] in excess and [BaCl2] limiting
n[BaCl2] = c[BaCl2] V[BaCl2 sol]
#          [BaCl2] and [AgCl] at 1:2 molar ratio
n[AgCl]B = n[BaCl2] * 2
#     _n[AgCl]A is smaller than _n[AgCl]A , so [AgNO3] is limiting
#
#   3) Calculate yield
M[AgCl] = 143.32 g/mol
m[AgCl]theoretical = n[AgCl]A * M[AgCl]
m[AgCl]actual = m_prec
yield = m[AgCl]actual / m[AgCl]theoretical

problem = units with non-integer powers
# Inspired by http://www.chem.ox.ac.uk/vrchemistry/rates/newhtml/order3.htm
#The reaction of chlorine with chloroform to yield carbon tetrachloride and hydrogen chloride is
! Cl2 + CHCl3 -> CCl4 + HCl
# The observed rate expression for production of HCl is first order in chloroform and half order in chlorine. If the rate is 0.183 M/s and the concentrations of chloroform and chlorine are 0.400 M and 1.52 mM, respectively, what is the rate constant of the reaction?
rate = 0.183 M/s
[Cl2] = 1.52 mM
[CHCl3] = 0.400 M
k[->] = rate / ( [Cl2]^(1/2) * [CHCl3] )



problem = error in adding
a = 5.6 km + 25.1 mol

problem = error in power
a = 5.6 ^ (25 mol)

problem = error in division
a = 5.6 / 0.0

problem = error with parentheses
a = (5 + 6))

problem = error in minimum function
a = minimum(7 M, 34 mol)

problem = limitations: numeric overflow
a = 10^10^10

problem = warning in square root
#This works
a = sqrt(2.3 mm * 4.9 km)
#This works too, but results in a warning
a = sqrt(2.3 mm * 4.13 g)

problem = limitations: imaginary numbers
#PQcalc works with real numbers, only
a = sqrt(-1)

problem = error in log function
a = log(0.34 mol/L)

problem = error in log function
a = log(-23.8)

problem = tutorial
# You are asked to make about 80 mL of a 0.150 mol/L aqueous solution of magnesium chloride by mixing the pure solid with water.
V_requested = 80 mL

[MgCl2] = 0.150 mol/L

# First, calculate how much [MgCl2] you need.
n[MgCl2] = [MgCl2] V_requested

# Because we want to use a balance to measure the pure solid, we need to calculate the mass from the chemical amount.

M[MgCl2] = 95.211 g/mol

m[MgCl2]exact = n[MgCl2] M[MgCl2]

# You took a bit more than the required mass and placed 1.213 g of [MgCl2] into a 100 mL graduated cylinder.
#
# To which volume do you have to add water to obtain a 0.150 M solution?

V_exact = m[MgCl2]exact / (M[MgCl2] [MgCl2] )

m[MgCl2]actual = 1.213g

V_actual = m[MgCl2]actual / (M[MgCl2] [MgCl2])


# Another, simpler way of calculating: Instead of 1.143 g, you have 1.213 g, so you have to add more  water to obtain a proportionally larger volume

V_made_2 = V_exact * m[MgCl2]actual / m[MgCl2]exact

problem = integrate images

#How does water form from the elements, and what is the chemical equation?
#{"http://bit.ly/1PvpnpD" width ="160"}
!H2 + O2 -> 2H2O

problem = 1.1* Calculation of Density
<h3>Example 1.1: Calculation of Density</h3>
#Gold — in bricks, bars, and coins — has been a form of currency for centuries. In order to swindle people into paying for a brick of gold without actually investing in a brick of gold, people have considered filling the centers of hollow gold bricks with lead to fool buyers into thinking that the entire brick is gold. It does not work: Lead is a dense substance, but its density is not as great as that of gold, 19.3 g/cm3. What is the density of lead if a cube of lead has an edge length of 2.00 cm and a mass of 90.7 g?
m_cube = 90.7 g
l_cube = 2.00 cm
d_gold = 19.3 g/cm^3
#<h4>Plan</h4>The density of an object can be calculated by dividing its mass by its volume. The volume of a cube is calculated by cubing the edge length. First, we will calculate the volume of the cube. Then, we will calculate the density of the lead cube.
V_cube = l_cube ^ 3
d_lead = m_cube / V_cube
#(We will discuss the reason for rounding to the first decimal place in the next section.)
#<h4>Check Your Learning</h4>
(a) To three decimal places, what is the volume of a cube (cm3) with an edge length of 0.843 cm?
(b) If the cube in part (a) is copper and has a mass of 5.34 g, what is the density of copper to two decimal places?
#Answer:
#(a) 0.599 cm^3; (b) 8.91 g/cm^3

problem = 1.2 Using Displacement of Water to Determine Density
<h3>Example 1.2: Using Displacement of Water to Determine Density</h3>
Using Displacement of Water to Determine Density
#This  (http://openstaxcollege.org/l/16phetmasvolden)PhET simulation illustrates another way to determine density, using displacement of water. Determine the density of the red and yellow blocks.
#<h4>Plan</h4>When you open the density simulation and select Same Mass, you can choose from several 5.00-kg colored blocks that you can drop into a tank containing 100.00 L water. The yellow block floats (it is less dense than water), and the water level rises to 105.00 L. While floating, the yellow block displaces 5.00 L water, an amount equal to the weight of the block. The red block sinks (it is more dense than water, which has density = 1.00 kg/L), and the water level rises to 101.25 L.
#The red block therefore displaces 1.25 L water, an amount equal to the volume of the block. The density of the red block is:
#density=massvolume=5.00 kg1.25 L=4.00 kg/L
#Note that since the yellow block is not completely submerged, you cannot determine its density from this information. But if you hold the yellow block on the bottom of the tank, the water level rises to 110.00 L, which means that it now displaces 10.00 L water, and its density can be found:
#density=massvolume=5.00 kg10.00 L=0.500 kg/L<h4>Check Your Learning</h4>Remove all of the blocks from the water and add the green block to the tank of water, placing it approximately in the middle of the tank. Determine the density of the green block.
#Answer:
#2.00 kg/L
#<hr>
problem = 1.3 Rounding Numbers
<h3>Example 1.3: Rounding Numbers</h3>
Rounding Numbers
#Round the following to the indicated number of significant figures:
#(a) 31.57 (to two significant figures)
#(b) 8.1649 (to three significant figures)
#(c) 0.051065 (to four significant figures)
#(d) 0.90275 (to four significant figures)
#<h4>Plan</h4>(a) 31.57 rounds “up” to 32 (the dropped digit is 5, and the retained digit is even)
#(b) 8.1649 rounds “down” to 8.16 (the dropped digit, 4, is less than 5)(c) 0.051065 rounds “down” to 0.05106 (the dropped digit is 5, and the retained digit is even)
#(d) 0.90275 rounds “up” to 0.9028 (the dropped digit is 5, and the retained digit is even)
#<h4>Check Your Learning</h4>Round the following to the indicated number of significant figures:
#(a) 0.424 (to two significant figures)
#(b) 0.0038661 (to three significant figures)
#(c) 421.25 (to four significant figures)
#(d) 28,683.5 (to five significant figures)
#
#Answer:
#(a) 0.42; (b) 0.00387; (c) 421.2; (d) 28,684
#<hr>
problem = 1.4 Addition and Subtraction with Significant Figures
<h3>Example 1.4: Addition and Subtraction with Significant Figures</h3>
Addition and Subtraction with Significant Figures
#Rule: When we add or subtract numbers, we should round the result to the same number of decimal places as the number with the least number of decimal places (i.e., the least precise value in terms of addition and subtraction).
#(a) Add 1.0023 g and 4.383 g.
#(b) Subtract 421.23 g from 486 g.
#<h4>Plan</h4>
#(a) 1.0023 g+ 4.383 g5.3853 g
#Answer is 5.385 g (round to the thousandths place; three decimal places)
#(b)    486 g−421.23 g64.77 g
#Answer is 65 g (round to the ones place; no decimal places)
#
#
#
#<h4>Check Your Learning</h4>(a) Add 2.334 mL and 0.31 mL.
#(b) Subtract 55.8752 m from 56.533 m.
#
#Answer:
#(a) 2.64 mL; (b) 0.658 m
#<hr>
problem = 1.5 Multiplication and Division with Significant Figures
<h3>Example 1.5: Multiplication and Division with Significant Figures</h3>
Multiplication and Division with Significant Figures
#Rule: When we multiply or divide numbers, we should round the result to the same number of digits as the number with the least number of significant figures (the least precise value in terms of multiplication and division).
#(a) Multiply 0.6238 cm by 6.6 cm.
#(b) Divide 421.23 g by 486 mL.
#<h4>Plan</h4>
#(a) 0.6238 cm×6.6cm=4.11708cm2⟶result is4.1cm2(round to two significant figures)four significant figures×two significant figures⟶two significant figures answer
#(b) 421.23 g486 mL=0.86728... g/mL⟶result is 0.867 g/mL(round to three significant figures)five significant figuresthree significant figures⟶three significant figures answer
#<h4>Check Your Learning</h4>(a) Multiply 2.334 cm and 0.320 cm.
#(b) Divide 55.8752 m by 56.53 s.
#
#Answer:
#(a) 0.747 cm2 (b) 0.9884 m/s
#<hr>
problem = 1.6 Calculation with Significant Figures
<h3>Example 1.6: Calculation with Significant Figures</h3>
Calculation with Significant Figures
#One common bathtub is 13.44 dm long, 5.920 dm wide, and 2.54 dm deep. Assume that the tub is rectangular and calculate its approximate volume in liters.
#<h4>Plan</h4>
#V=l×w×d=13.44 dm×5.920 dm×2.54 dm=202.09459...dm3(value from calculator)=202 dm3, or 202 L(answer rounded to three significant figures)<h4>Check Your Learning</h4>What is the density of a liquid with a mass of 31.1415 g and a volume of 30.13 cm3?
#
#Answer:
#1.034 g/mL
#<hr>
problem = 1.7 Experimental Determination of Density Using Water Displacement
<h3>Example 1.7: Experimental Determination of Density Using Water Displacement</h3>
Experimental Determination of Density Using Water Displacement
#A piece of rebar is weighed and then submerged in a graduated cylinder partially filled with water, with results as shown.
#
#
#
#(a) Use these values to determine the density of this piece of rebar.
#(b) Rebar is mostly iron. Does your result in (a) support this statement? How?
#
#SolutionThe volume of the piece of rebar is equal to the volume of the water displaced:
#volume=22.4 mL−13.5 mL=8.9 mL=8.9 cm3(rounded to the nearest 0.1 mL, per the rule for addition and subtraction)
#The density is the mass-to-volume ratio:
#density=massvolume=69.658 g8.9 cm3=7.8 g/cm3
#(rounded to two significant figures, per the rule for multiplication and division)
#From Table 1.4, the density of iron is 7.9 g/cm3, very close to that of rebar, which lends some support to the fact that rebar is mostly iron.
#<h4>Check Your Learning</h4>An irregularly shaped piece of a shiny yellowish material is weighed and then submerged in a graduated cylinder, with results as shown.
#
#
#
#(a) Use these values to determine the density of this material.
#(b) Do you have any reasonable guesses as to the identity of this material? Explain your reasoning.
#
#Answer:
#(a) 19 g/cm3; (b) It is likely gold; the right appearance for gold and very close to the density given for gold in Table 1.4.
#<hr>
problem = 1.8 Using a Unit Conversion Factor
<h3>Example 1.8: Using a Unit Conversion Factor</h3>
Using a Unit Conversion Factor
#The mass of a competition frisbee is 125 g. Convert its mass to ounces using the unit conversion factor derived from the relationship 1 oz = 28.349 g (Table 1.6).
#<h4>Plan</h4>If we have the conversion factor, we can determine the mass in kilograms using an equation similar the one used for converting length from inches to centimeters.
#xoz=125 g×unit conversion factor
#We write the unit conversion factor in its two forms:
#1 oz28.349 gand28.349 g1 ozThe correct unit conversion factor is the ratio that cancels the units of grams and leaves ounces.
#xoz=125g×1 oz28.349g=(12528.349)oz=4.41 oz (three significant figures)
#<h4>Check Your Learning</h4>Convert a volume of 9.345 qt to liters.
#
#Answer:
#8.844 L
#<hr>
problem = 1.9 Computing Quantities from Measurement Results and Known Mathematical Relations
<h3>Example 1.9: Computing Quantities from Measurement Results and Known Mathematical Relations</h3>
Computing Quantities from Measurement Results and Known Mathematical Relations
#What is the density of common antifreeze in units of g/mL? A 4.00-qt sample of the antifreeze weighs 9.26 lb.
#<h4>Plan</h4>Since density=massvolume, we need to divide the mass in grams by the volume in milliliters. In general: the number of units of B = the number of units of A × unit conversion factor. The necessary conversion factors are given in Table 1.6: 1 lb = 453.59 g; 1 L = 1.0567 qt; 1 L = 1,000 mL. We can convert mass from pounds to grams in one step:
#9.26lb×453.59 g1lb=4.20×103g
#We need to use two steps to convert volume from quarts to milliliters.
#
#
#Convert quarts to liters.
#4.00qt×1 L1.0567qt=3.78 L
#
#Convert liters to milliliters.
#3.78L×1000 mL1L=3.78×103mL
#
#Then,
#density=4.20×103g3.78×103mL=1.11 g/mLAlternatively, the calculation could be set up in a way that uses three unit conversion factors sequentially as follows:
#9.26lb4.00qt×453.59 g1lb×1.0567qt1L×1L1000 mL=1.11 g/mL
#<h4>Check Your Learning</h4>What is the volume in liters of 1.000 oz, given that 1 L = 1.0567 qt and 1 qt = 32 oz (exactly)?
#
#Answer:
#2.956×10−2L
#
#<hr>
problem = 1.10 Computing Quantities from Measurement Results and Known Mathematical Relations
<h3>Example 1.10: Computing Quantities from Measurement Results and Known Mathematical Relations</h3>
Computing Quantities from Measurement Results and Known Mathematical Relations
#While being driven from Philadelphia to Atlanta, a distance of about 1250 km, a 2014 Lamborghini Aventador Roadster uses 213 L gasoline.
#(a) What (average) fuel economy, in miles per gallon, did the Roadster get during this trip?
#(b) If gasoline costs $3.80 per gallon, what was the fuel cost for this trip?
#<h4>Plan</h4>(a) We first convert distance from kilometers to miles:
#1250 km×0.62137 mi1 km=777 mi
#and then convert volume from liters to gallons:
#213L×1.0567qt1L×1 gal4qt=56.3 gal
#Then,
#
#(average) mileage=777 mi56.3 gal=13.8 miles/gallon=13.8 mpg
#Alternatively, the calculation could be set up in a way that uses all the conversion factors sequentially, as follows:
#1250km213L×0.62137 mi1km×1L1.0567qt×4qt1 gal=13.8 mpg
#(b) Using the previously calculated volume in gallons, we find:
#56.3 gal×$3.801 gal=$214
#<h4>Check Your Learning</h4>A Toyota Prius Hybrid uses 59.7 L gasoline to drive from San Francisco to Seattle, a distance of 1300 km (two significant digits).
#(a) What (average) fuel economy, in miles per gallon, did the Prius get during this trip?
#(b) If gasoline costs $3.90 per gallon, what was the fuel cost for this trip?
#
#Answer:
#(a) 51 mpg; (b) $62
#<hr>
problem = 1.11 Conversion from Celsius
<h3>Example 1.11: Conversion from Celsius</h3>
Conversion from Celsius
#Normal body temperature has been commonly accepted as 37.0 °C (although it varies depending on time of day and method of measurement, as well as among individuals). What is this temperature on the kelvin scale and on the Fahrenheit scale?
#<h4>Plan</h4>
#K=°C+273.15=37.0+273.2=310.2 K
#°F=95°C+32.0=(95×37.0)+32.0=66.6+32.0=98.6 °F
#<h4>Check Your Learning</h4>Convert 80.92 °C to K and °F.
#
#Answer:
#354.07 K, 177.7 °F
#<hr>
problem = 1.12 Conversion from Fahrenheit
<h3>Example 1.12: Conversion from Fahrenheit</h3>
Conversion from Fahrenheit
#Baking a ready-made pizza calls for an oven temperature of 450 °F. If you are in Europe, and your oven thermometer uses the Celsius scale, what is the setting? What is the kelvin temperature?
#<h4>Plan</h4>
#°C=59(°F−32)=59(450−32)=59×418=232 °C⟶set oven to 230 °C(two significant figures)
#K=°C+273.15=230+273=503 K⟶5.0×102K(two significant figures)
#<h4>Check Your Learning</h4>Convert 50 °F to °C and K.
#
#Answer:
#10 °C, 280 K
#<hr>
problem = 2.1 Testing Dalton’s Atomic Theory
<h3>Example 2.1: Testing Dalton’s Atomic Theory</h3>
Testing Dalton’s Atomic Theory
#In the following drawing, the green spheres represent atoms of a certain element. The purple spheres represent atoms of another element. If the spheres touch, they are part of a single unit of a compound. Does the following chemical change represented by these symbols violate any of the ideas of Dalton’s atomic theory? If so, which one?
#
#
#
#<h4>Plan</h4>The starting materials consist of two green spheres and two purple spheres. The products consist of only one green sphere and one purple sphere. This violates Dalton’s postulate that atoms are neither created nor destroyed during a chemical change, but are merely redistributed. (In this case, atoms appear to have been destroyed.)
#<h4>Check Your Learning</h4>In the following drawing, the green spheres represent atoms of a certain element. The purple spheres represent atoms of another element. If the spheres touch, they are part of a single unit of a compound. Does the following chemical change represented by these symbols violate any of the ideas of Dalton’s atomic theory? If so, which one?
#
#
#
#
#Answer:
#The starting materials consist of four green spheres and two purple spheres. The products consist of four green spheres and two purple spheres. This does not violate any of Dalton’s postulates: Atoms are neither created nor destroyed, but are redistributed in small, whole-number ratios.
#<hr>
problem = *2.2 Laws of Definite and Multiple Proportions
<h3>Example 2.2: Laws of Definite and Multiple Proportions</h3>
Laws of Definite and Multiple Proportions
#A sample of compound A (a clear, colorless gas) is analyzed and found to contain 4.27 g carbon and 5.69 g oxygen. A sample of compound B (also a clear, colorless gas) is analyzed and found to contain 5.19 g carbon and 13.84 g oxygen. Are these data an example of the law of definite proportions, the law of multiple proportions, or neither? What do these data tell you about substances A and B?
m[C]A = 4.27 g
m[O]A = 5.69 g
m[C]B = 5.19 g
m[O]B = 13.84 g
#<h4>Plan</h4>1) Calculate the mass ratios of compounds A and B. 2) See if the ratios are related
In compound A, the mass ratio of carbon to oxygen is:
r_A = m[C]A  / m[O]A
In compound B, the mass ratio of carbon to oxygen is:
r_B = m[C]B / m[O]B
#The ratio of these ratios is:
r_AB = r_A / r_B
#This supports the law of multiple proportions. This means that A and B are different compounds, with A having one-half as much carbon per amount of oxygen (or twice as much oxygen per amount of carbon) as B. A possible pair of compounds that would fit this relationship would be A = CO2 and B = CO.
#<h4>Check Your Learning</h4>A sample of compound X (a clear, colorless, combustible liquid with a noticeable odor) is analyzed and found to contain 14.13 g carbon and 2.96 g hydrogen. A sample of compound Y (a clear, colorless, combustible liquid with a noticeable odor that is slightly different from X’s odor) is analyzed and found to contain 19.91 g carbon and 3.34 g hydrogen. Are these data an example of the law of definite proportions, the law of multiple proportions, or neither? What do these data tell you about substances X and Y?
#
#Answer:
#In compound X, the mass ratio of carbon to hydrogen is 14.13 g C: 2.96 g H. In compound Y, the mass ratio of carbon to oxygen is 19.91 g C: 3.34 g H. The ratio of these ratios is 14.13 g / 2.96 g / (19.91 g / 3.34 g) = 4.77 / 5.96 = 0.800 = 4/5. This small, whole-number ratio supports the law of multiple proportions. This means that X and Y are different compounds.
#<hr>

problem = 2.3 Composition of an Atom
<h3>Example 2.3: Composition of an Atom</h3>
Composition of an Atom
#Iodine is an essential trace element in our diet; it is needed to produce thyroid hormone. Insufficient iodine in the diet can lead to the development of a goiter, an enlargement of the thyroid gland (Figure 2.12).
#
#
#
#
#(a) Insufficient iodine in the diet can cause an enlargement of the thyroid gland called a goiter. (b) The addition of small amounts of iodine to salt, which prevents the formation of goiters, has helped eliminate this concern in the US where salt consumption is high. (credit a: modification of work by “Almazi”/Wikimedia Commons; credit b: modification of work by Mike Mozart)
#
#The addition of small amounts of iodine to table salt (iodized salt) has essentially eliminated this health concern in the United States, but as much as 40% of the world’s population is still at risk of iodine deficiency. The iodine atoms are added as anions, and each has a 1− charge and a mass number of 127. Determine the numbers of protons, neutrons, and electrons in one of these iodine anions.
#SolutionThe atomic number of iodine (53) tells us that a neutral iodine atom contains 53 protons in its nucleus and 53 electrons outside its nucleus. Because the sum of the numbers of protons and neutrons equals the mass number, 127, the number of neutrons is 74 (127 − 53 = 74). Since the iodine is added as a 1− anion, the number of electrons is 54 [53 – (1–) = 54].Check Your LearningAn ion of platinum has a mass number of 195 and contains 74 electrons. How many protons and neutrons does it contain, and what is its charge?
#Answer:
#78 protons; 117 neutrons; charge is 4+
#<hr>
problem = 2.4 Calculation of Average Atomic Mass
<h3>Example 2.4: Calculation of Average Atomic Mass</h3>
Calculation of Average Atomic Mass
#A meteorite found in central Indiana contains traces of the noble gas neon picked up from the solar wind during the meteorite’s trip through the solar system. Analysis of a sample of the gas showed that it consisted of 91.84% 20Ne (mass 19.9924 amu), 0.47% 21Ne (mass 20.9940 amu), and 7.69% 22Ne (mass 21.9914 amu). What is the average mass of the neon in the solar wind?
#<h4>Plan</h4>average mass=(0.9184×19.9924 amu)+(0.0047×20.9940 amu)+(0.0769×21.9914 amu)=(18.36+0.099+1.69)amu=20.15 amu
#
#The average mass of a neon atom in the solar wind is 20.15 amu. (The average mass of a terrestrial neon atom is 20.1796 amu. This result demonstrates that we may find slight differences in the natural abundance of isotopes, depending on their origin.)
#<h4>Check Your Learning</h4>A sample of magnesium is found to contain 78.70% of 24Mg atoms (mass 23.98 amu), 10.13% of 25Mg atoms (mass 24.99 amu), and 11.17% of 26Mg atoms (mass 25.98 amu). Calculate the average mass of a Mg atom.
#
#Answer:
#24.31 amu
#<hr>
problem = 2.5 Calculation of Percent Abundance
<h3>Example 2.5: Calculation of Percent Abundance</h3>
Calculation of Percent Abundance
#Naturally occurring chlorine consists of 35Cl (mass 34.96885 amu) and 37Cl (mass 36.96590 amu), with an average mass of 35.453 amu. What is the percent composition of Cl in terms of these two isotopes?
#<h4>Plan</h4>The average mass of chlorine is the fraction that is 35Cl times the mass of 35Cl plus the fraction that is 37Cl times the mass of 37Cl.
#average mass=(fraction of35Cl×mass of35Cl)+(fraction of37Cl×mass of37Cl)If we let x represent the fraction that is 35Cl, then the fraction that is 37Cl is represented by 1.00 − x.
#(The fraction that is 35Cl + the fraction that is 37Cl must add up to 1, so the fraction of 37Cl must equal 1.00 − the fraction of 35Cl.)
#Substituting this into the average mass equation, we have:
#35.453 amu=(x×34.96885 amu)+[(1.00−x)×36.96590 amu]35.453=34.96885x+36.96590−36.96590x1.99705x=1.513x=1.5131.99705=0.7576
#
#So solving yields: x = 0.7576, which means that 1.00 − 0.7576 = 0.2424. Therefore, chlorine consists of 75.76% 35Cl and 24.24% 37Cl.
#<h4>Check Your Learning</h4>Naturally occurring copper consists of 63Cu (mass 62.9296 amu) and 65Cu (mass 64.9278 amu), with an average mass of 63.546 amu. What is the percent composition of Cu in terms of these two isotopes?
#
#Answer:
#69.15% Cu-63 and 30.85% Cu-65
#<hr>
problem = 2.6 Empirical and Molecular Formulas
<h3>Example 2.6: Empirical and Molecular Formulas</h3>
Empirical and Molecular Formulas
#Molecules of glucose (blood sugar) contain 6 carbon atoms, 12 hydrogen atoms, and 6 oxygen atoms. What are the molecular and empirical formulas of glucose?<h4>Plan</h4>The molecular formula is C6H12O6 because one molecule actually contains 6 C, 12 H, and 6 O atoms. The simplest whole-number ratio of C to H to O atoms in glucose is 1:2:1, so the empirical formula is CH2O.<h4>Check Your Learning</h4>A molecule of metaldehyde (a pesticide used for snails and slugs) contains 8 carbon atoms, 16 hydrogen atoms, and 4 oxygen atoms. What are the molecular and empirical formulas of metaldehyde?
#Answer:
#Molecular formula, C8H16O4; empirical formula, C2H4O
#<hr>
problem = 2.7 Naming Groups of Elements
<h3>Example 2.7: Naming Groups of Elements</h3>

#Atoms of each of the following elements are essential for life. Give the group name for the following elements:
#(a) chlorine
#(b) calcium
#(c) sodium
#(d) sulfur
#<h4>Plan</h4>The family names are as follows:
#(a) halogen
#(b) alkaline earth metal
#(c) alkali metal
#(d) chalcogen
#<h4>Check Your Learning</h4>Give the group name for each of the following elements:
#(a) krypton
#(b) selenium
#(c) barium
#(d) lithium
#
#Answer:
#(a) noble gas; (b) chalcogen; (c) alkaline earth metal; (d) alkali metal
#<hr>
problem = 2.8 Composition of Ions
<h3>Example 2.8: Composition of Ions</h3>

#An ion found in some compounds used as antiperspirants contains 13 protons and 10 electrons. What is its symbol?<h4>Plan</h4>Because the number of protons remains unchanged when an atom forms an ion, the atomic number of the element must be 13. Knowing this lets us use the periodic table to identify the element as Al (aluminum). The Al atom has lost three electrons and thus has three more positive charges (13) than it has electrons (10). This is the aluminum cation, Al3+.<h4>Check Your Learning</h4>Give the symbol and name for the ion with 34 protons and 36 electrons.
#Answer:
#Se2−, the selenide ion<hr>
problem = 2.9 Formation of Ions
<h3>Example 2.9: Formation of Ions</h3>

#Magnesium and nitrogen react to form an ionic compound. Predict which forms an anion, which forms a cation, and the charges of each ion. Write the symbol for each ion and name them.<h4>Plan</h4>Magnesium’s position in the periodic table (group 2) tells us that it is a metal. Metals form positive ions (cations). A magnesium atom must lose two electrons to have the same number electrons as an atom of the previous noble gas, neon. Thus, a magnesium atom will form a cation with two fewer electrons than protons and a charge of 2+. The symbol for the ion is Mg2+, and it is called a magnesium ion.
#Nitrogen’s position in the periodic table (group 15) reveals that it is a nonmetal. Nonmetals form negative ions (anions). A nitrogen atom must gain three electrons to have the same number of electrons as an atom of the following noble gas, neon. Thus, a nitrogen atom will form an anion with three more electrons than protons and a charge of 3−. The symbol for the ion is N3−, and it is called a nitride ion.<h4>Check Your Learning</h4>Aluminum and carbon react to form an ionic compound. Predict which forms an anion, which forms a cation, and the charges of each ion. Write the symbol for each ion and name them.
#
#Answer:
#Al will form a cation with a charge of 3+: Al3+, an aluminum ion. Carbon will form an anion with a charge of 4−: C4−, a carbide ion.
#<hr>
problem = 2.10 Predicting the Formula of an Ionic Compound
<h3>Example 2.10: Predicting the Formula of an Ionic Compound</h3>

#The gemstone sapphire (Figure 2.31) is mostly a compound of aluminum and oxygen that contains aluminum cations, Al3+, and oxygen anions, O2−. What is the formula of this compound?
#
#
#
#Although pure aluminum oxide is colorless, trace amounts of iron and titanium give blue sapphire its characteristic color. (credit: modification of work by Stanislav Doronenko)
#<h4>Plan</h4>Because the ionic compound must be electrically neutral, it must have the same number of positive and negative charges. Two aluminum ions, each with a charge of 3+, would give us six positive charges, and three oxide ions, each with a charge of 2−, would give us six negative charges. The formula would be Al2O3.<h4>Check Your Learning</h4>Predict the formula of the ionic compound formed between the sodium cation, Na+, and the sulfide anion, S2−.
#Answer:
#Na2S
#<hr>
problem = 2.11 Predicting the Formula of a Compound with a Polyatomic Anion
<h3>Example 2.11: Predicting the Formula of a Compound with a Polyatomic Anion</h3>

#Baking powder contains calcium dihydrogen phosphate, an ionic compound composed of the ions Ca2+ and H2PO4−. What is the formula of this compound?Solution
#The positive and negative charges must balance, and this ionic compound must be electrically neutral. Thus, we must have two negative charges to balance the 2+ charge of the calcium ion. This requires a ratio of one Ca2+ ion to two H2PO4− ions. We designate this by enclosing the formula for the dihydrogen phosphate ion in parentheses and adding a subscript 2. The formula is Ca(H2PO4)2.<h4>Check Your Learning</h4>Predict the formula of the ionic compound formed between the lithium ion and the peroxide ion, O22− (Hint: Use the periodic table to predict the sign and the charge on the lithium ion.)
#Answer:
#Li2O2
#<hr>

problem = *2.12: Predicting the Type of Bonding in Compounds
<h3>Example 2.12: Predicting the Type of Bonding in Compounds</h3>

#Predict whether the following compounds are ionic or molecular:
#(a) KI, the compound used as a source of iodine in table salt
#(b) H2O2, the bleach and disinfectant hydrogen peroxide
#(c) CHCl3, the anesthetic chloroform
#(d) Li2CO3, a source of lithium in antidepressants<h4>Plan</h4>(a) Potassium (group 1) is a metal, and iodine (group 17) is a nonmetal; KI is predicted to be ionic.
#(b) Hydrogen (group 1) is a nonmetal, and oxygen (group 16) is a nonmetal; H2O2 is predicted to be molecular.
#(c) Carbon (group 14) is a nonmetal, hydrogen (group 1) is a nonmetal, and chlorine (group 17) is a nonmetal; CHCl3 is predicted to be molecular.
#(d) Lithium (group 1) is a metal, and carbonate is a polyatomic ion; Li2CO3 is predicted to be ionic.
<h4>Check Your Learning</h4>
#Using the periodic table, predict whether the following compounds are ionic or covalent:
#(a) SO2
#(b) CaF2
#(c) N2H4
#(d) Al2(SO4)3
#Answer:
#(a) molecular; (b) ionic; (c) molecular; (d) ionic
#<hr>

problem = 2.13 Naming Ionic Compounds
<h3>Example 2.13: Naming Ionic Compounds</h3>

#Name the following ionic compounds, which contain a metal that can have more than one ionic charge:
#(a) Fe2S3
#(b) CuSe
#(c) GaN
#(d) CrCl3
#(e) Ti2(SO4)3
#SolutionThe anions in these compounds have a fixed negative charge (S2−, Se2− , N3−, Cl−, and SO42−), and the compounds must be neutral. Because the total number of positive charges in each compound must equal the total number of negative charges, the positive ions must be Fe3+, Cu2+, Ga3+, Cr3+, and Ti3+. These charges are used in the names of the metal ions:(a) iron(III) sulfide
#(b) copper(II) selenide
#(c) gallium(III) nitride
#(d) chromium(III) chloride
#(e) titanium(III) sulfate<h4>Check Your Learning</h4>Write the formulas of the following ionic compounds:
#(a) chromium(III) phosphide
#(b) mercury(II) sulfide
#(c) manganese(II) phosphate
#(d) copper(I) oxide
#(e) chromium(VI) fluoride
#Answer:
#(a) CrP; (b) HgS; (c) Mn3(PO4)2; (d) Cu2O; (e) CrF6
#<hr>
problem = 2.14 Naming Covalent Compounds
<h3>Example 2.14: Naming Covalent Compounds</h3>

#Name the following covalent compounds:
#(a) SF6
#(b) N2O3
#(c) Cl2O7
#(d) P4O6<h4>Plan</h4>Because these compounds consist solely of nonmetals, we use prefixes to designate the number of atoms of each element:
#(a) sulfur hexafluoride
#(b) dinitrogen trioxide
#(c) dichlorine heptoxide
#(d) tetraphosphorus hexoxide<h4>Check Your Learning</h4>Write the formulas for the following compounds:
#(a) phosphorus pentachloride
#(b) dinitrogen monoxide
#(c) iodine heptafluoride
#(d) carbon tetrachloride
#Answer:
#(a) PCl5; (b) N2O; (c) IF7; (d) CCl4
#<hr>

problem = *4.4: Writing Equations for Acid-Base Reactions
<h3>Example 4.4: Writing Equations for Acid-Base Reactions</h3>

#Write balanced chemical equations for the acid-base reactions described here:
#(a) the weak acid hydrogen hypochlorite reacts with water
#(b) a solution of barium hydroxide is neutralized with a solution of nitric acid
<h4>Plan</h4>(a) The two reactants are provided, HOCl and H2O. Since the substance is reported to be an acid, its reaction with water will involve the transfer of H+ from HOCl to H2O to generate hydronium ions, H3O+ and hypochlorite ions, OCl-.
!HOCl(aq) + H2O(l) <=> OCl- (aq) + H3O+(aq)
#A double-arrow is appropriate in this equation because it indicates the HOCl is a weak acid that has not reacted completely.
#(b) The two reactants are provided, Ba(OH)2 and HNO3. Since this is a neutralization reaction, the two products will be water and a salt composed of the cation of the ionic hydroxide (Ba^2+) and the anion generated when the acid transfers its hydrogen ion (NO3- ).
!Ba(OH)2(aq) + 2 HNO3(aq) -> Ba(NO3)2(aq) + 2H2O(l)
<h4>Check Your Learning</h4>
#Write the net ionic equation representing the neutralization of any strong acid with an ionic hydroxide. (Hint: Consider the ions produced when a strong acid is dissolved in water.)
#
#Answer
!H3O+(aq) + OH- (aq) -> 2H2O(l)
<hr>

problem = 4.10: Relating Masses of Reactants and Products
<h3>Example 4.10: Relating Masses of Reactants and Products</h3>

#What mass of sodium hydroxide, NaOH, would be required to produce 16 g of the antacid milk of magnesia ( Mg(OH)2, magnesium hydroxide) by the following reaction?
!MgCl2(aq) + 2NaOH(aq) -> Mg(OH)2(s) + 2NaCl(aq)
m[Mg(OH)2] = 16 g

<h4>Plan</h4>The approach used previously in Example 4.8 and Example 4.9 is likewise used here; that is, we must derive an appropriate stoichiometric factor from the balanced chemical equation and use it to relate the amounts of the two substances of interest.
@ n[NaOH] / 2 = n[Mg(OH)2]/1
In this case, however, masses (not molar amounts) are provided and requested, so additional steps of the sort learned in the previous chapter are required. The calculations required are outlined in this flowchart:
#{"ico/Ex410.JPG" width ="400"}
M[Mg(OH)2] = 58.3 g/mol
n[Mg(OH)2] = m[Mg(OH)2] / M[Mg(OH)2]
n[NaOH] = n[Mg(OH)2] / 1 * 2
M[NaOH] = 40.0 g/mol
m[NaOH] = n[NaOH] * M[NaOH]
<h4>Check Your Learning</h4>What mass of gallium oxide, Ga2O3, can be prepared from 29.0 g of gallium metal? The equation for the reaction is
!4Ga + 3O2 -> 2Ga2O3
#
#Answer:
#39.0 g
#<hr>

problem = *5.1: Measuring Heat
<h3>Example 5.1: Measuring Heat</h3>
Measuring Heat
#A flask containing 8.0e2 g of water is heated, and the temperature of the water increases from 21 °C to 85 °C. How much heat did the water absorb?
ΔT = (85 - 21) K
m[H2O] = 8.0e2 g
#<h4>Plan</h4>To answer this question, consider these factors:
#the specific heat of the substance being heated (in this case, water)
#the amount of substance being heated (in this case, 800 g)
#the magnitude of the temperature change (in this case, from 21 °C to 85 °C).
#The specific heat of water is 4.184 J/(g K), so to heat 1 g of water by 1 K requires 4.184 J. We note that since 4.184 J is required to heat 1 g of water by 1 K, we will need 800 times as much to heat 800 g of water by 1 K. Finally, we observe that since 4.184 J are required to heat 1 g of water by 1 K, we will need 64 times as much to heat it by 64 K (that is, from 21 °C to 85 °C).This can be summarized using the equation:
@q = c_p[H2O]* m[H2O] * ΔT
c_p[H2O] = 4.184 J/(g K)
q = c_p[H2O] * m[H2O] * ΔT
Because the temperature increased, the water absorbed heat and q is positive.
<h3>Check Your Learning</h3>
How much heat, in joules, must be added to a 5.00e2-g iron skillet to increase its temperature from 25 °C to 250 °C? The specific heat of iron is 0.451 J/(g K).
#Answer:
#q = 5.05e4 J

problem = *5.11: Evaluating an Enthalpy of Formation
<h3>Example 5.11: Evaluating an Enthalpy of Formation</h3>

#Ozone, O3(g), forms from oxygen, O2(g), by an endothermic process. Ultraviolet radiation is the source of the energy that drives this reaction in the upper atmosphere. Assuming that both the reactants and products of the reaction are in their standard states, determine the standard enthalpy of formation, ΔHf° of ozone from the following information:
!3O2(g) -> 2O3(g)
@ΔH°_298 = +286 kJ/mol

ΔH°_298 = 286 kJ/mol

<h3>Plan</h3>
ΔHf° is the enthalpy change for the formation of one mole of a substance in its standard state from the elements in their standard states. Thus, ΔHf° for O3(g) is the enthalpy change for the reaction:
!3/2 O2(g) -> O3(g)
The two chemical equations are the same, except that twice as much reacts and is produced in the first equation compared to the second.
ΔHf°[O3] = ΔH°_298 / 2

<h4>Check Your Learning</h4>
#Hydrogen gas, H2, reacts explosively with gaseous chlorine, Cl2, to form hydrogen chloride, HCl(g). What is the enthalpy change for the reaction of 1 mole of H2(g) with 1 mole of Cl2(g) if both the reactants and products are at standard state conditions? The standard enthalpy of formation of HCl(g) is −92.3 kJ/mol.
#Answer:
#For the reaction
!H2(g) + Cl2(g)-> 2HCl(g)
@ΔH_298 = -184.6 kJ
#<hr>

problem = studygroup
#{"ico/ava1.JPG" width ="32"} ! Check out <a href= "https://opentextbc.ca/chemistry/chapter/5-2-calorimetry/#CNX_Chem_05_02_Calorim" target="_blank">this figure from the textbook</a>
#{"ico/ava2.JPG" width ="32"} Which section do you think is most relevant?
#! <ol><li> <a href= "ico/summary.html#3.4" target="_blank">Section 3.4: Other Units for Solution Concentrations</a></li><li> <a href= "ico/summary.html#5.2" target="_blank">Section 5.2: Calorimetry</a></li><li> <a href= "ico/summary.html#5.3" target="_blank">Section 5.3: Enthalpy</a> </li><li> <a href= "ico/summary.html#6.1" target="_blank">Section 6.1: Electromagnetic Energy</a> </ol>
#{"ico/avo1.JPG" width ="32"} ! Kapow! How about a little break?
#{"ico/avo2.JPG" width ="32"} This is backwards from the typical problem. Usually, we look up enthalpies of formation, and try to figure out the reaction enthalpy.
#{"ico/avo3.JPG" width = "32"} Which step is next? 1) Collect 2) Plan and predict 3) Calculate 4) Check answer

problem = *6.4: Calculating the Energy of an Electron in a Bohr Orbit
<h3>Example 6.4: Calculating the Energy of an Electron in a Bohr Orbit</h3>

#Early researchers were very excited when they were able to predict the energy of an electron at a particular distance from the nucleus in a hydrogen atom. If a spark promotes the electron in a hydrogen atom into an orbit with n = 3, what is the calculated energy, in joules, of the electron?
n = 3
<h4>Plan</h4>The energy of the electron is given by this equation:
@E_elec = - (k Z^2 / n^2)
#The atomic number, Z, of hydrogen is 1; k = 2.179 × 10–18 J; and the electron is characterized by an n value of 3.
Z_H = 1
k = 2.179e-18 J
E_elec_3 = - (k Z_H^2 / n^2)

<h4>Check Your Learning</h4>
The electron in Figure 6.15 is promoted even further to an orbit with n = 6. What is its new energy?
#Answer:
@E_elec_6 = -6.053e-20 J
<hr>

problem = 7.9: Using Bond Energies to Calculate Approximate Enthalpy Changes
<h3>Example 7.9: Using Bond Energies to Calculate Approximate Enthalpy Changes</h3>

#Methanol, CH3OH, may be an excellent alternative fuel. The high-temperature reaction of steam and carbon produces a mixture of the gases carbon monoxide, CO, and hydrogen, H2, from which methanol can be produced. Using the bond energies in Table 7.4, calculate the approximate enthalpy change, ΔH, for the reaction here:
!CO(g) + 2H2(g) -> CH3OH(g)
<h4>Plan</h4>
First, we need to write the Lewis structures of the reactants and the products.
#{"ico/Ex79a.JPG" width ="400"}
From this, we see that ΔH for this reaction involves the energy required to break a C–O triple bond and two H–H single bonds, as well as the energy produced by the formation of three C–H single bonds, a C–O single bond, and an O–H single bond. We can express this as follows:
@ΔH_approx=sum(D_bonds_broken) - sum(D_bonds_formed)
@_ =sum(D[C#O], 2(D[H−H])) - sum(3(D[C−H]), D[C−O], D[O-H])
#Using the bond energy values in Table 7.4, we obtain:
D[C#O] = 1080 kJ/mol
D[H−H] = 436 kJ/mol
D[C−H] = 415 kJ/mol
D[C−O] = 350 kJ/mol
D[O-H] = 464 kJ/mol
ΔH_approx = sum(D[C#O], 2(D[H−H])) - sum(3(D[C−H]), D[C−O], D[O-H])
#We can compare this value to the value calculated based on ΔHf° data from Appendix G:
@ΔH_exact = ΔHf°[CH3OH(g)] - ΔHf°[CO(g)]
@ _ = -201.0 kJ/mol -(-110.52 kJ/mol) = -90.5 kJ/mol
#Note that there is a fairly significant gap between the values calculated using the two different methods. This occurs because D values are the average of different bond strengths; therefore, they often give only rough agreement with other data.
<h4>Check Your Learning</h4>
Ethyl alcohol, CH3CH2OH, was one of the first organic chemicals deliberately synthesized by humans. It has many uses in industry, and it is the alcohol contained in alcoholic beverages. It can be obtained by the fermentation of sugar or synthesized by the hydration of ethylene in the following reaction:
#{"ico/Ex79b.JPG" width ="400"}
Using the bond energies in Table 7.4, calculate an approximate enthalpy change, ΔH, for this reaction.
#
#Answer:
ΔH = -35 kJ

problem = 8.1: Counting σ and π Bonds
<h3>Example 8.1: Counting σ and π Bonds</h3>
#{"ico/Ex81a.JPG" width ="200"}
#Butadiene, C6H6, is used to make synthetic rubber. Identify the number of σ and π bonds contained in this molecule.
<h4>Plan</h4>There are six σ C–H bonds and one σ C–C bond, for a total of seven from the single bonds. There are two double bonds that each have a π bond in addition to the σ bond. This gives a total nine σ and two π bonds overall.
<h4>Check Your Learning</h4>Identify each illustration as depicting a σ or π bond:
#{"ico/Ex81b.JPG" width ="400"}
#(a) side-by-side overlap of a 4p and a 2p orbital
#(b) end-to-end overlap of a 4p and 4p orbital
#(c) end-to-end overlap of a 4p and a 2p orbital

#Answer:
#(a) is a π bond with a node along the axis connecting the nuclei while (b) and (c) are σ bonds that overlap along the axis.
#<hr>

problem = 9.10: Using the Combined Gas Law
<h3>Example 9.10: Using the Combined Gas Law</h3>
#{"ico/Ex910.JPG" width ="200"}
#<em>Figure 9.</em>: Scuba divers use compressed air to breathe while underwater. (credit: modification of work by Mark Goodchild)

#When filled with air, a typical scuba tank with a volume of 13.2 L has a pressure of 153 atm (Figure 9.16). If the water temperature is 27 °C, how many liters of air will such a tank provide to a diver’s lungs at a depth of approximately 70 feet in the ocean where the pressure is 3.13 atm?

#Letting 1 represent the air in the scuba tank and 2 represent the air in the lungs, and noting that body temperature (the temperature the air will be in the lungs) is 37 °C, we have:
P1 = 153 atm
V1 = 13.2 L
T1 = CtoKscale(27)
P2 = 3.13 atm
V2 = ?
T2 = CtoKscale(37)
#
#
#
#
<h4>Plan</h4>
The amount of gas does not change, just the pressure, temperature, and volume. We can use the combined gas law:
@P1 V1 / T1 = P2 V2 / T2
#Solving for V2 :
V2 = P1 V1 T2 / (P2 T1)

(Note: Be advised that this particular example is one in which the assumption of ideal gas behavior is not very reasonable, since it involves gases at relatively high pressures and low temperatures. Despite this limitation, the calculated volume can be viewed as a good “ballpark” estimate.)

<h4>Check Your Learning</h4>
A sample of ammonia is found to occupy 0.250 L under laboratory conditions of 27 °C and 0.850 atm. Find the volume of this sample at 0 °C and 1.00 atm.
#
#Answer:
#V = 0.193 L<hr>

problem = 10.6: A Boiling Point at Reduced Pressure
<h3>Example 10.6: A Boiling Point at Reduced Pressure</h3>

#A typical atmospheric pressure in Leadville, Colorado (elevation 10,200 feet) is 68 kPa. Use the graph in Figure 10.25 to determine the boiling point of water at this elevation.

<figure><img src="ico/Ex106.JPG"; width ="400"><figcaption>Figure 10.24 The boiling points of liquids are the temperatures at which their equilibrium vapor pressures equal the pressure of the surrounding atmosphere. Normal boiling points are those corresponding to a pressure of 1 atm (101.3 kPa.)</figcaption></figure>

<h4>Plan</h4>The graph of the vapor pressure of water versus temperature in Figure 10.25 indicates that the vapor pressure of water is 68 kPa at about 90 °C. Thus, at about 90 °C, the vapor pressure of water will equal the atmospheric pressure in Leadville, and water will boil.
<h4>Check Your Learning</h4>The boiling point of ethyl ether was measured to be 10 °C at a base camp on the slopes of Mount Everest. Use Figure 10.25 to determine the approximate atmospheric pressure at the camp.
#
#Answer:
#Approximately 40 kPa (0.4 atm)
#<hr>

problem = 11.7: Calculation of the Freezing Point of a Solution
<h3>Example 11.7: Calculation of the Freezing Point of a Solution</h3>
What is the freezing point of the 0.33 mol/kg solution of a nonvolatile nonelectrolyte solute in benzene described in Example 11.3?
n_solute = 0.33 mol
m_solvent = 1 kg

<h4>Plan</h4>
#Use the equation relating freezing point depression to solute molality to solve this problem in two steps.
#
#
#
#
#Calculate the change in freezing point.
@ΔT_f = K_f n_solute / m_solvent
K_f_benzene = 5.12 K kg/mol
ΔT_f = K_f_benzene n_solute / m_solvent
#Subtract the freezing point change observed from the pure solvent’s freezing point.
F_p_solution = CtoKscale(5.5) - ΔT_f
#
#<h4>Check Your Learning</h4>
What is the freezing point of a 1.85 mol/kg solution of a nonvolatile nonelectrolyte solute in nitrobenzene?
#Answer:
#-9.3 °C<hr>

problem = 12.1: Expressions for Relative Reaction Rates
<h3>Example 12.1: Expressions for Relative Reaction Rates</h3>

#The first step in the production of nitric acid is the combustion of ammonia:
!4NH3(g) + 5O2(g) -> 4NO(g) + 6H2O(g)
#Write the equations that relate the rates of consumption of the reactants and the rates of formation of the products.<h4>Plan</h4>Considering the stoichiometry of this homogeneous reaction, the rates for the consumption of reactants and formation of products are:
@rate[->] = -1/4 (Δc[NH3]/Δt)= -1/5 (Δc[O2]/Δt) =1/4 (Δc[NO]/Δt) = 1/6 (Δc[H2O]/Δt)
<h4>Check Your Learning</h4>
The rate of formation of Br2 is 6.0 × 10-6 mol/L/s in a reaction described by the following net ionic equation:
!5Br- + BrO3- + 6H+ -> 3Br2 + 3H2O
#Write the equations that relate the rates of consumption of the reactants and the rates of formation of the products.
#
#Answer:
@-1/5 (Δc[Br-]/Δt) = -(Δc[BrO3-]/Δt) =-1/6(Δc[H+]/Δt)=1/3 (Δc[Br2] / Δt)=1/3 (Δc[H2O] / Δt)

<hr>'''

examples = example.split('problem = ')
from collections import OrderedDict


exdict = OrderedDict()
exhtml = []
for ex in examples:
    if "\n" not in ex:
        continue
    head2, prob = ex.split("\n", 1)
    exhtml.append('<a href="/example%s">Example %s</a><br>' % (head2, head2))
    exhtml.append("<pre>%s</pre>" % prob)
    exdict[head2] = prob

exhtml = "".join(exhtml)

