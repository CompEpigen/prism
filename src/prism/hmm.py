def is_methylated(base):
    return base == 1

class HMMModel:
    def __init__(self, basePattern, e_m=0.010, e_d=0.001, e_b=0.01, p=0.960, q=0.96):
        self.e = self._emission_probabilities(basePattern, e_m, e_d, e_b)  # Emission probabilities.
        self.e_m, self.e_d, self.e_b = e_m, e_d, e_b
        self.init = [0.5, 0.5]  # Initial probabilities.
        self.p = p  # Processivity.
        self.q = q  # Recruitment efficiency.

    def _emission_probabilities(self, basePattern, e_m, e_d, e_b):
        emission = []
        for base in basePattern:
            if is_methylated(base):
                # [[e_dm(u), e_dm(m)], [e_am(u), e_am(m)]]
                emission.append([[1-e_d, e_d], [e_m, 1-e_m]])
            else:
                # [[e_du(u), e_du(m)], [e_au(u), e_au(m)]]
                emission.append([[1-e_b, e_b], [1-e_m, e_m]])

        return emission

    def proba(self, seq):
        prev = self.init
        p, q = self.p, self.q
        for i in range(len(seq)):
            curr = [self.e[i][0][seq[i]] * (prev[0] * (1 - q) + prev[1] * (1 - p)), self.e[i][1][seq[i]] * (prev[0] * q + prev[1] * p)]
            prev = curr

        s = sum(curr)

        prev = self.init
        for i in range(len(seq)-1, -1, -1):
            curr = [self.e[i][0][seq[i]] * (prev[0] * (1 - q) + prev[1] * (1 - p)), self.e[i][1][seq[i]] * (prev[0] * q + prev[1] * p)]
            prev = curr

        return (s + sum(curr)) / 2