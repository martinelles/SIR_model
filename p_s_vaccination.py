import matplotlib.pyplot as plt

class Problem():
    def __init__(self, s, i, r, v, beta, nu, rho, t_max, h):
        self.s0 = s
        self.i0 = i
        self.r0 = r
        self.v0 = v
        if isinstance(beta, int) or isinstance(beta, float):
            def aux_beta(x):
                return beta
            self.beta = aux_beta
        else:
            self.beta = beta
        if isinstance(nu, int) or isinstance(nu, float):
            def aux_nu(x):
                return nu
            self.nu = aux_nu
        else:
            self.nu = nu
        if isinstance(rho, int) or isinstance(rho, float):
            def aux_rho(x):
                return rho
            self.rho = aux_rho
        else:
            self.rho = rho
        self.t_max = t_max
        self.h = h


class Solver():
    def __init__(self, problem):
        h = problem.h
        def phi(x, y, f, s, i):
            f_1 = h * f(x,y,s,i)
            f_2 = h * f(x + h/2, y + f_1/2, s, i)
            f_3 = h * f(x + h/2, y + f_2/2, s, i)
            f_4 = h * f(x + h/2, y + f_3, s, i)
            return y + 1/6 * (f_1 + 2*f_2 + 2*f_3 + f_4)
        self.phi = phi

    def eval(self,problem):


        tot = [problem.s0+problem.i0+problem.r0]
        s = [problem.s0]
        i = [problem.i0]
        r = [problem.r0]
        v = [problem.v0]

        for t in range(1, problem.t_max+1):
            def f_s(x, y, s, i):
                return -1 * problem.beta(t) * y * i - problem.rho(t) * y

            def f_i(x, y, s, i):
                return problem.beta(t) * s * y - 1 * problem.nu(t) * y

            def f_r(x, y, s, i):
                return problem.nu(t) * i

            def f_v(x, y, s, i):
                return problem.rho(t) * s

            s_t, i_t, r_t, v_t = self.phi(t, s[t-1], f_s, s[t-1], i[t-1]), self.phi(t, i[t-1], f_i, s[t-1], i[t-1]), \
                            self.phi(t, r[t-1], f_r, s[t-1], i[t-1]), self.phi(t, v[t-1], f_v, s[t-1], i[t-1])
            s.append(s_t)
            i.append(i_t)
            r.append(r_t)
            v.append(v_t)
            tot.append(s_t + i_t + r_t + v_t)

        t = range(0, problem.t_max+1)

        plt.plot(t, s, label="S")
        plt.plot(t, i, label="I")
        plt.plot(t, r, label="R")
        plt.plot(t, v, label="V")
        plt.plot(t, tot, label="T")
        plt.legend()

        plt.show()


# Problema com lambda igual a 0.0005
problem = Problem(s=1500, i=1, r=0, v=0, beta=0.0005, nu=0.1, rho=0.1, t_max=300, h=0.5)

solver = Solver(problem)
solver.eval(problem)


# Problema com lambda igual a 0.0001
problem = Problem(s=1500, i=1, r=0, v=0, beta=0.0001, nu=0.1, rho=0.1, t_max=300, h=0.5)

solver = Solver(problem)
solver.eval(problem)

# Problema com lambda variavel de 0.0005 0 <= t <= 12 e 0.0001 12 < t
problem = Problem(s=1500, i=1, r=0, v=0, beta=lambda t: 0.0005 if t <= 12 else 0.0001, nu=0.1, rho=0.1, t_max=300, h=0.5)

solver = Solver(problem)
solver.eval(problem)