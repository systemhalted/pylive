Example 1
=========
print "I love python"

Example 2
=========
for x in range(1,100):
    print x

Example 3
=========
print sum(xrange(1,100))


Example 4
=========
"""
This 
is 
multiline comment in python
"""

Example 5
=========
#Single line comment in python

Example 6
=========
print 256789 * 2345667

Example 7
=========
class Person(object):
    def __init__(self):
        self._first_name = ""

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        self._first_name = first_name

    @first_name.deleter
    def first_name(self):
        del self._first_name

p = Person()
p.first_name = "Guido"
print p.first_name

Example 8
=========
indian_test_team = set(['Gambhir', 'Sehwag', 'Dravid', 'Tendulkar', 'Laxman',\
                      'Dhoni', 'Ashwin', 'Praveen', 'Zaheer', 'Umesh', 'Kolhi'])
indian_odi_team = set(["Gambhir", "Tendulkar", "Sehwag", "Kolhi", "Raina",\
                     "Dhoni", "Jadeja","Irfan", "Umesh", "Ashwin", "Praveen"])
#lets find players who are not in indian test team
print indian_test_team - indian_odi_team

Example 9
==========
divide_by_2_or_3 = [ x for x in xrange(25) if x % 2 or x % 3]
