# OPERATIONS ON ITERABLES

l = [x for x in range(26)]

# map (squeres of all elements)
l_map = list(map(lambda x: x**2, l))
l_map_c = [x**2 for x in l] # as comprehension list


# filter (only odd elements)
l_filter = list(filter(lambda x: x%2 == 1, l))
l_filter_c = [x for x in l if x%2 == 1] # as comprehension list


# reduce (sum of all elements)
from functools import reduce
l_reduce = reduce(lambda x, y: x + y, l)
l_reduce_f = sum(l) # as built in function
# probably not possible as comprahension list 
# because comprahension lists generate lists not single values 
# and don't have collapsing functionality


# map, reduce, filter (sum of squeres of odd elements)
l_all = reduce(lambda z1, z2: z1 + z2, map(lambda y: y**2, filter(lambda x: x%2 == 1, l)))
l_all_c = sum(y**2 for y in [x for x in l if x%2 == 1]) # as comprahension list


print("l:\t",l)
print("map:\t", l_map)
print("filter:\t", l_filter)
print("reduce:\t", l_reduce)
print("all:\t", l_all)

l1, l2 = [l_map, l_filter, l_reduce, l_all], [l_map_c, l_filter_c, l_reduce_f, l_all_c]
print("Same for comprahensio lists" if all([x == y for x, y in zip(l1, l2)]) else "wrong translation to comprahension lists")


# REGULAR EXPRESSIONS (RegEx) RECAP

import re

'''
CHARACTERS:

.   Any character

\d  Decimal digit
\D  Non-digit

\s  White-space
\S  Non White-space

^   Starts with
$   Ends with

.|..    . or ..        

SETS:

[...]   A set of characters ...
[^..]   Anything accept ..
\w      Any alphabetical or digit or _ (same as [a-zA-Z0-9_])
\W      Non alphabetical or digit or _

*   0 or more of a previous character 
+   1 or more of a previous character
?   0 or 1 of previous character
.*  Any sequence
{n}     n of previous character
{n,m}   n to m of previous characters
{n,}    At least n of previous characters


NEGATIVE LOOKAHEAD:

(?!...) cannot be present after previous character
Ex.:
(?!.*@example\.com)     Any string that does not end with @example.com
(?!meet).*              Any string that does not start with meet
meet(?!\.).*            Any string that does start with meet but is not followed by period .

NEGATIVE LOOKBEHIND:

(?<!...) cannot be present before next character
Ex.:
.*(?<!@)example\.com.*  Any string containing example\.com that is not preceded with @


FUNCTIONS:

findall(ex, str)    return all mathes

search(ex, str)     returns match object of the first occurance or None

split(ex, str, max) same as bulit-in split (max - maximum matches)

sub(ex, str, str)   replace match with str

compile(ex)     compiles expression to RegEx pattern


METHODS ON MATCH OBJECT:

expand(str\.)   returns match with modified prefix

group(n)        returns n'th group

groups()        returns tuple of groups

groupdict()     returns dict of groups keyed by their names

start()         returns index of start of first match
end()           returns index of end of first match
span()          returns (start(), end())
'''

# EXAMPLES
print()

print("\nRemove leading zeros from IP adress")
ip = "111.002.034.234"
print(re.sub("\.[0]*", ".", ip))

print("\nCheck for a number at the end of a string")
string =  "43y5sdjhb kjcn  sdk89"
print(True if re.match(".*[0-9]$", string) else False)

print("\nCheck what number at the end of string if any")
print(string[-1] if re.match(".*[0-9]+$", string) else False) # find len of number

print("\nSearch for numbers (0-9) of length between 1 and 3 in a given string")
string = "1 la 12 tada 13 hey345eyey 3289"
print(num if (num := re.findall("[0-9]{1,3}", string)) else False)



