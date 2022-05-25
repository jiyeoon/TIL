"""
class Person:
    def __init__(self):
        self.name = name
    
    def get_friends(self): -> List[Person]
        ...
"""

def solution(person, k): # top k
    friends_set = {} # dictionary
    my_friends = set(person.get_friends())
    
    # O(N^2)
    for my_friend in person.get_friends(): # O(N)
        for friend in my_friend.get_friends(): # O(N)
            if friend not in my_friends:
                if friend in friends_set.keys():
                    friends_set[friend] += 1
                else:
                    friends_set[friend] = 1
    
    result = [[count, friend] for friend, count in friends_set.items()]
    result.sort(key=lambda x : -x[0])
    
    return [res[0] for res in result[:k]]
