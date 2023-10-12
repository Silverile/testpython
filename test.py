def test():
    bob = ['Bob Smith', 42, 30000, 'software']
    sue = ['Sue Johnes', 46, 40000, 'hardware']

    people = [bob, sue]
    for person in people:
        print(person)
    print(people[1][0])
    for person in people:
        print(person[0].split()[-1])
        person[2] *= 1.20
    for person in people:
        print(person[2])

    pays = [person[2] for person in people]
    print(pays)

    pays = map((lambda x: x[2]), people)
    print(list(pays))

    people.append(['Tom', 50, 0, None])
    print(len(people))
    print(people[-1][0])

    bob2 = {'name': {'first': 'Bob', 'last': 'Smith'},
            'age': 42,
            'job': ['software', 'writing'],
            'pay': (40000, 50000)
            }

    print(bob2['name'])
    print(bob2['name']['last'])
    print(bob2['pay'][0])


test()
