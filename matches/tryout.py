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
    sorted_dict = sorted(dict.items(), lambda x, y: cmp(x[1], y[1]))
    sorted_dict_reverse = sorted(dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    print 'After (normal sorting): ', sorted_dict
    print 'After (reversed sorting): ', sorted_dict_reverse
    print 'After limiting: ', sorted_dict_reverse[0:2]

    for key, value in sorted_dict_reverse:
        print 'Key: ', key
        print 'Value: ', value
        value = '123456'
    
    print sorted_dict_reverse
#f4()

def f5():
    def passCheck(b):
        b = 'new'

    def doesThisLanguageBindByValue(language):
        a = 'original'
        b = a
        b = 'new'
        if a == 'original':
            print "%s assigns by value" % (language)
        else:
            print "%s does not assigns by value" % (language)

    a = 'original'
    passCheck(a)
    if a == 'original':
        print "%s passes by value" % (language)
    else:
        print "%s does not pass by value" % (language)

    doesThisLanguageBindByValue('Python')

#f5()

def f6():
    n = 10.45
    result = round(n, 0)
    print result

    result = int(result)
    print result

#f6()


def f7():
    list = [('z', 'z'), ('b', 'b'), ('a', 'a'), ('nine', '9'), ('four', '4'), ('three', '3'), ('two', '2'), ('one', '1')]

    print list
    data = []


    for key, value in list:
        data.append(value)
        #list[key] = 123

    print data

    del data

    #print data
#f7()

def f8(*args, **kargs):
    print 'args: ', args
    print 'kargs: ', kargs

#f8(['fds', '123', lambda x: x + 1], 'fdsfsdjkfdsjkfjsk', {'fd': '7789789fdskfldsklfsdfsdl'}, method='post', type='get', func=(lambda y: 10 ** y))

def f9():
    data = ({'id': 1, 'title': 'Lorem', 'visible': True},
            {'id': 2, 'title': 'Lorem2', 'visible': True},
            {'id': 3, 'title': 'Lorem3', 'visible': False},
            {'id': 4, 'title': 'Lorem4', 'visible': True},
            {'id': 5, 'title': 'Lorem5', 'visible': False},
            {'id': 6, 'title': 'Lorem6', 'visible': True})

    raw = {}

    for row in data:
        raw[row['id']] = {}
        raw[row['id']]['title'] = (row['title'], row['visible'])

    print raw

#f9()

def f10():
    print True if None else False
    print True if '' else False

f10()
