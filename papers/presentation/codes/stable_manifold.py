def stable_manifold_shadow_1D(starting_state,lambda_s,dimensionalization,sim_time,step,system,eps=1e-6):
    ci = starting_state + eps * mult_coef_by_coef(lambda_s,dimensionalization)
    return rk4.simulate_trajectory(ci,sim_time,step,system,inverse_time=True)

def stable_manifold_sampling(lambda_s,dimensionalization,sim_time,step,system,reference_orbit,sampling,eps=1e-6):
    manifold = []
    for i in range(sampling):
        state_i = reference_orbit[i*len(reference_orbit)//sampling]
        print(i*len(reference_orbit)//sampling, state_i)
        manifold.append(stable_manifold_shadow_1D(state_i,lambda_s,dimensionalization,sim_time,step,system,eps))
    return manifold