# a = ["Pulemetttka", "Акбар♾", None, 810654979, 810654979]
# a2 = ["Kvinchis", "Islom", None, 5151629187, 5151629187]
# a3 = ["ROM_AND_RIP", "失われたメロディの夜明け", None, 170621337, 170621337]
# a4 = ["JoJoGG27", " ", None, 745759616, 745759616]
# a5 = ["BuTCoiN_666", "アニメちゃん", None, 5554477944, 5554477944]

a = [76,83,55,-36,-8,40,-60,-72,27,-32,37,1,77,24,-46,-26,20,-89,-35,-99,58,-7]


def maxSatisfaction(satisfaction):
    total = 0
    satisfaction_total = 0

    for s in sorted(satisfaction, reverse=True):
        satisfaction_total += s
        if satisfaction_total <= 0:
            return total
        total += satisfaction_total
    return total



print(maxSatisfaction(a))
