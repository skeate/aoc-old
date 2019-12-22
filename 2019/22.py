from input22 import v

v = v.strip().split('\n')

ccount = 10007

cards = [*range(ccount)]

cuts = 0
dealouts = 1
forward = True

def shuffle(cards, pattern):
    global cuts, dealouts, forward, abscuts, modcuts
    for c in pattern:
        if c == 'deal into new stack':
            cards = cards[::-1]
            cuts = -cuts - 1
            forward = not forward
        elif c[:3] == 'cut':
            n = int(c[4:])
            cuts -= n
            cards = cards[n:] + cards[:n]
        elif c[5:9] == 'with':
            n = int(c[20:])
            dealouts *= n
            cuts *= n
            new_cards = [-1] * ccount
            t = 0
            for card in cards:
                new_cards[t] = card
                t = (t + n) % ccount
            cards = new_cards
    return cards

def nshuffle(n, c):
    for x in range(n):
        c = shuffle(c, v)
    return c

x = shuffle(cards, v)
print(x.index(2019))


nccount = 119315717514047
times  = 101741582076661

# goal: (index * step ** times + shift * (step**(times-1) + step**(times-2) + ... + 1))
# mod ccount

# sum of geometric series is (1 - step ** (times- 1)) / (1-step)

shift = cuts % ccount
step = ((dealouts % ccount) - ccount) if forward else (ccount - (dealouts % ccount))

def poly(r, n, m):
    if n == 0:
        return 1
    if n % 2 == 0:
        return (1 + (r + r*r) * poly(r*r % m, (n-2)/2, m)) % m
    return ((1+r) * poly(r*r % m, (n-1) / 2, m)) % m

def pos_after_shuffles(val, ccount, shuffles):
    step = ((dealouts % ccount) - ccount) if forward else (ccount - (dealouts % ccount))
    shift = cuts % ccount
    p = pow(step, shuffles, ccount)
    goal = (p * val + shift * poly(step, shuffles-1, ccount)) % ccount
    return goal

def euclid(a,b):
    s = 0
    olds = 1
    r = b
    oldr = a

    while r != 0:
        q = oldr // r
        oldr, r = r, oldr - q * r
        olds, s = s, olds - q * s
    return olds

def at_index_after_shuffles(idx, ccount, shuffles):
    zero = pos_after_shuffles(0, ccount, shuffles)
    step = ((dealouts % ccount) - ccount) if forward else (ccount - (dealouts % ccount))
    p = pow(step, shuffles, ccount)
    p_times_val = (idx - zero) % ccount
    s = euclid(p, ccount)
    return (p_times_val * s) % ccount

print(at_index_after_shuffles(2020, nccount, times))
