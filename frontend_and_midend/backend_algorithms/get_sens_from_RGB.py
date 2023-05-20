from scipy.optimize import fsolve
import numpy as np

# def equations(variables):
#     x, y, z = variables
    
#     eq1 = 50 + np.log10((x * 226 + y * 191 + z * 210) / (x * 229 + y * 228 + z * 229))
#     eq2 = 75 + np.log10((x * 216 + y * 150 + z * 188) / (x * 229 + y * 228 + z * 229))
#     eq3 = 95 + np.log10((x * 206 + y * 125 + z * 167) / (x * 229 + y * 228 + z * 229))
    
#     return [eq1, eq2, eq3]

# # Solve the equations
# x, y, z = fsolve(equations, (1, 1, 1))

# print(f"x = {x:.3f}")
# print(f"y = {y:.3f}")
# print(f"z = {z:.3f}")

x,y,z = .5,.5,.5
def check_pred(x,y,z):
    eq1 = 50 + np.log10((x * 226 + y * 191 + z * 210) / (x * 229 + y * 228 + z * 229))
    eq2 = 75 + np.log10((x * 216 + y * 150 + z * 188) / (x * 229 + y * 228 + z * 229))
    eq3 = 95 + np.log10((x * 206 + y * 125 + z * 167) / (x * 229 + y * 228 + z * 229))
    
    print(eq1, eq2, eq3)

check_pred(x = x,y = y,z = z)