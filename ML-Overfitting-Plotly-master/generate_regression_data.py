import numpy as np
from sympy import Symbol, sympify

def compute_reg_functions(number_of_functions=12):
    final_funcs = []
    for i in range(1, number_of_functions):
        func_string = ''
        coefs = np.random.uniform(-1,1, size=i)
        for order, coef in enumerate(coefs):
            sign = ' + ' if coef >= 0 else ' - '
            if order == 0:
                func_string += f'{coef}'
            elif order == 1:
                func_string += sign + f'{abs(coef):.3f}*x1'
            else:
                func_string += sign + f'{abs(coef):.3f}*x1**{order}'

        final_funcs.append(func_string)

    return final_funcs


reg_functions = compute_reg_functions(number_of_functions=12)

def symbolize(s):
    """
    Converts a a string (equation) to a SymPy symbol object
    """
    # s1 = s.replace('.', '*')
    # s2 = s1.replace('^', '**')
    s3 = sympify(s)

    return s3


def eval_multinomial(s, vals=None, symbolic_eval=False):
    """
    Evaluates polynomial at vals.
    vals can be simple list, dictionary, or tuple of values.
    vals can also contain symbols instead of real values provided those symbols have been declared before using SymPy
    """
    sym_s = symbolize(s)
    sym_set = sym_s.atoms(Symbol)
    sym_lst = []
    for s in sym_set:
        sym_lst.append(str(s))
    sym_lst.sort()
    if symbolic_eval == False and len(sym_set) != len(vals):
        print("Length of the input values did not match number of variables and symbolic evaluation is not selected")
        return None
    else:
        if type(vals) == list:
            sub = list(zip(sym_lst, vals))
        elif type(vals) == dict:
            l = list(vals.keys())
            l.sort()
            lst = []
            for i in l:
                lst.append(vals[i])
            sub = list(zip(sym_lst, lst))
        elif type(vals) == tuple:
            sub = list(zip(sym_lst, list(vals)))
        result = sym_s.subs(sub)

    return result


def gen_regression_symbolic(m=None, n_samples=100, n_features=2, noise=0.0, noise_dist='normal'):
    """
    Generates regression sample based on a symbolic expression. Calculates the output of the symbolic expression
    at randomly generated (drawn from a Gaussian distribution) points
    m: The symbolic expression. Needs x1, x2, etc as variables and regular python arithmetic symbols to be used.
    n_samples: Number of samples to be generated
    n_features: Number of variables. This is automatically inferred from the symbolic expression. So this is ignored
                in case a symbolic expression is supplied. However if no symbolic expression is supplied then a
                default simple polynomial can be invoked to generate regression samples with n_features.
    noise: Magnitude of Gaussian noise to be introduced (added to the output).
    noise_dist: Type of the probability distribution of the noise signal.
    Currently supports: Normal, Uniform, t, Beta, Gamma, Poission, Laplace

    Returns a numpy ndarray with dimension (n_samples,n_features+1). Last column is the response vector.
    """

    if m == None:
        m = ''
        for i in range(1, n_features + 1):
            c = 'x' + str(i)
            c += np.random.choice(['+', '-'], p=[0.5, 0.5])
            m += c
        m = m[:-1]

    sym_m = sympify(m)

    n_features = len(sym_m.atoms(Symbol))
    evals = []
    lst_features = []

    # for i in range(n_features):
    lst_features.append(np.random.uniform(-2, 2, size=n_samples))

    lst_features = np.array(lst_features)
    lst_features = lst_features.T
    n_features = 1 if n_features == 0 else n_features
    lst_features = lst_features.reshape(n_samples, n_features)

    if sym_m.is_Integer or sym_m.is_Float:
        evals = [sym_m] * n_samples

    else:
        for i in range(n_samples):
            evals.append(eval_multinomial(m, vals=list(lst_features[i])))

    evals = np.array(evals)
    evals = evals.astype(np.float64)
    # evals = evals.reshape(n_samples, 1)

    if noise_dist == 'normal':
        noise_sample = np.random.normal(loc=0, scale=noise, size=n_samples)
    elif noise_dist == 'uniform':
        noise_sample = noise * np.random.uniform(low=0, high=1.0, size=n_samples)
    elif noise_dist == 'beta':
        noise_sample = noise * np.random.beta(a=0.5, b=1.0, size=n_samples)
    elif noise_dist == 'Gamma':
        noise_sample = noise * np.random.gamma(shape=1.0, scale=1.0, size=n_samples)
    elif noise_dist == 'laplace':
        noise_sample = noise * np.random.laplace(loc=0.0, scale=1.0, size=n_samples)

    # noise_sample = noise_sample.reshape(n_samples, 1)

    evals = evals + noise_sample

    # x = np.hstack((lst_features, evals))

    return lst_features, evals