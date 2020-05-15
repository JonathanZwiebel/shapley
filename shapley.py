# Very basic shapley implementation

import math

# vote_shares = {'a': 4, 'b': 3, 'c': 2, 'd':1}

# vote_shares = {'likud':36, 'blue and white triple':33, 'joint list': 15, 'shas': 9, 'united torah': 7, 'labor meretz gesher': 7, 'yisrael': 7, 'yamina':7}

vote_shares = {'conservative': 365, 'labour': 202, 'scottish': 47, 'liberal': 11, 'unionist': 8, 'cymru': 4, 'social democratic': 2, 'alliance': 1, 'green': 1, 'independent': 1, 'sinn fein': 7, 'speaker': 1}

total_vote_share = sum([vote_shares[x] for x in vote_shares])
n = len(vote_shares)
voters = list(vote_shares.keys())


# TODO: Precompute into a table
# TODO: Don't double compute values
set_weight_values = {}
for s in range(n):
    set_weight_values[s] = math.factorial(s) * math.factorial(n - s - 1) / math.factorial(n)

def score_coalition(coalition, vote_shares):
    set_vote_share = sum([vote_shares[x] for x in coalition])
    
    if set_vote_share > total_vote_share / 2:
        return 1
    if set_vote_share == total_vote_share / 2:
        return 0
    return 0

def score_coalition_by_total(coalition_vote_share):
    if coalition_vote_share > total_vote_share / 2:
        return 1
    if coalition_vote_share == total_vote_share / 2:
        return 0
    return 0

# TODO: Instead of storing key names use a bitstring
# Coalitions are represented as frozenset of keys
coalitions = {}
def add_to_coalitions(remaining, current_voters, current_vote_share):
    if len(remaining) == 0:
        coalitions[frozenset(current_voters)] = score_coalition_by_total(current_vote_share)
    else:
        # Exclude
        add_to_coalitions(remaining[1:].copy(), current_voters.copy(), current_vote_share)
        
        # Include
        current_voters.append(remaining[0])
        add_to_coalitions(remaining[1:].copy(), current_voters.copy(), current_vote_share + vote_shares[remaining[0]])
add_to_coalitions(voters, [], 0)

final_scores = {key:0 for key in voters}
for voter in voters:
    for coalition in coalitions:
        if voter not in coalition:
            score_before = coalitions[coalition]

            c = list(coalition)
            c.append(voter)
            score_after = coalitions[frozenset(c)]
            
            final_scores[voter] += (score_after - score_before) * set_weight_values[len(coalition)]

for voter in voters:
    print(voter + "\n" + str(vote_shares[voter]) + "\t" + str(final_scores[voter] * total_vote_share) + "\t" + str(final_scores[voter]) + "\n")