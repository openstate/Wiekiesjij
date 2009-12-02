def f1():
    l = ['a', 'b', 'd']
    s = 'a b c d e f g'
    range = '18-35-99'
    list = 'male/female/undefined'

    #print ''.join(s.split())
    print ', '.join(l)

    print l[1]

    print s == ''

    total_score = 0
    question_weight = 4
    question_theme = 'asd'
    themes = ['asd', 'bsd', 'csd']

    total_score += question_weight * ((2.0 if (question_theme in themes) else 1.0) if (question_theme != '') else 1.0)

    print total_score

    range_split = range.split('-', 1)
    print range_split
    print len(range_split)

    list_split = list.split('/')
    print list_split
    print len(list_split)

    tuple = ('a tuple', 'b tuple', 'c tuple')
    list = ['a list', 'b list', 'c list']
    dict = {'a dict key': 'a dict value', 'b dict key': 'b dict value', 'c dict key': 'c dict value'}

    print 'tuple: '
    print type(tuple)
    for i in tuple:
        print i

    print 'list: '
    print type(list)
    for i in list:
        print i

    print 'dict: '
    print type(dict)
    for i in dict:
        print i


#f1()

def f2():
    tagDataMap = {"title"   : (  3,  33, 'stripnulls'),
                  "artist"  : ( 33,  63, 'stripnulls'),
                  "album"   : ( 63,  93, 'stripnulls'),
                  "year"    : ( 93,  97, 'stripnulls'),
                  "comment" : ( 97, 126, 'stripnulls'),
                  "genre"   : (127, 128, 'ord')}

    for tag, (start, end, parseFunc) in tagDataMap.items():
        print tag, start, end, parseFunc

    for tag, data in tagDataMap.items():
        print tag, data

#f2()

def f3():
    dict = {"title"   : {1: '1. Lorem ipsum dolor sit amet', 2: '2. Dolor sit amet'},
          "artist"  : {},
          "album"   : {},
          "year"    : {},
          "comment" : {},
          "genre"   : {}}

    question_id = 1

    for item in dict:
        answer = dict[item][question_id] if (question_id in dict[item]) else False
        #print item
        #print dict[item]
        #print answer

        print not answer

    print 'END---------------'
    print not ''
    print not None
    print not 'fdfds'
#f3()


def sortfunc(x,y):
    return cmp(x[1],y[1])


def f4():
    dict={'one': '1', 'three': '3', 'four': '4', 'two': '2', 'nine': '9', 'z': 'z', 'a': 'a', 'b': 'b'}

    print 'Before: ', dict
    print 'After: ', sorted(dict.items(), lambda x, y: cmp(x[1], y[1]))
    print 'Final: ', 

f4()