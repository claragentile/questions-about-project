import numpy as np
 
#generate a 2d array in which each row is a pattern
def generate_patterns(num_patterns, pattern_size): #M,N
    patterns = np.random.choice([-1,1], (num_patterns,pattern_size)) 
    return patterns 

#perturb some element in a given pattern
def perturb_pattern(pattern, num_perturb):
    i = 0
    while i <= num_perturb:
        position = np.random.randint(0,np.size(pattern)-1)
        print('position : ',position)
        print('pattern', pattern)
        if pattern[position] == 1:
            pattern[position]=-1
        else :
            pattern[position]=1
        i+=1
    print('pattern',pattern)
    return pattern

def pattern_match(memorized_patterns, pattern):
    for i in range(np.size(memorized_patterns, 0)):
        if (pattern == memorized_patterns[i]).all():
            return i 
 
def hebbian_weights(patterns):
    weights_matrix= (1/np.shape(patterns)[0])*(np.matmul(np.transpose(patterns),patterns))-np.identity(np.shape(patterns)[1])
    return weights_matrix
 

def update(state, weights):
    #state is a pattern
    #weights_size = np.size(weights,1)
    weights_size = np.shape(weights)[0]
    new_state = np.zeros(weights_size) #new_state = np.zeros((1,weights_size))
    #new_state = np.dot(weights, state)#.T change rien si on fait .T
    new_state = np.dot(weights, np.dot(weights, state))
    #print('state de update: ', state)
    #print('new_state de update :', new_state)
    #print('weights de update', weights)
    for i in range(np.size(state)):
        if new_state[i] >= 0:
            new_state[i] = 1
        if new_state[i] < 0:
            new_state[i] = -1
    #print('new_state :', new_state)
    return new_state
 

def update_async(state, weights):
    new_state= state.copy()
    position = np.random.randint(0,np.size(state)-1)
    w_row= weights[position]
    #new_state[position]= np.dot(w_row, state)
    return update(new_state[position], w_row)
 
def dynamics(state, weights, max_iter):
    #new_state = state.copy() #il faut enlever ca sinon ca marche pas
    perturbed_state = perturb_pattern(state, 200)
    new_state = update(perturbed_state,weights)
    new_state_first = new_state.copy()
    #print('state : ', state)
    #print('new_state : ', new_state)
    states_list = new_state
    for i in range(max_iter):
        #new_state = update(state, weights)
        if (new_state != new_state_first).any() :
            states_list = np.vstack([states_list,new_state])
        print('states_liste : ',states_list)
        if (new_state == state).all() :
            break
        
        perturbed_state = new_state
        new_state = update(perturbed_state, weights)
        #states_list = np.append(states_list,state)
        #states_list = np.vstack([states_list,state])
    #print('states_list : ',states_list)
    return states_list
 
def dynamics_async(state, weights, max_iter, convergence_num_iter):
    new_state = state.copy()
    states_list = new_state
    iter=0
 
    for i in range(max_iter):
 
        new_state = update_async(state, weights)
        
        if (new_state == state).all() :
            iter+=1
            if iter==convergence_num_iter:
                iter=0
                break
 
        state = new_state
        states_list = np.append(states_list,state)
 
    return states_list
"""""
def storkey_weights(patterns):
    num_patterns = np.size(patterns, 0) #M
    length_patterns = np.size(patterns, 1) #N
    h_matrix= np.zeros((num_patterns,num_patterns)) #pas sure de la taille
    weights_matrix = np.zeros((num_patterns,num_patterns))
    
    for mu in range(num_patterns):
        for i in range(length_patterns):
            for j in range(length_patterns):
                sum_h=0
                for k in range(length_patterns):
                    if (k!=i and k!=j and i!=j):
                        #je ne sais pas comment faire apparaitre l'indice mu-1 des weights_matrix
                        #idee alternative --> faire une variable sum_h à la place de h_matrix: 
                                               # si on fait un sum_h += weights_matrix[i][k]*patterns[mu][k]
                                               # le += pourrait peut etre permettre de faire la somme avec le weight_matrix d'indice mu-1
                        sum_h += weights_matrix[i][k]*patterns[mu][k]          
                        #h_matrix[i][j]=weights_matrix[i][k]*patterns[mu][k]
                        weights_matrix[i][j]+= (1/length_patterns) * ((
                                                            (patterns[mu][i] * patterns[mu][j]) -
                                                             ( patterns[mu][i] * sum_h) -
                                                             ( patterns[mu][j] * sum_h)    ))
    return weights_matrix
"""
#def storkey_weights(patterns):
def storkey_weights(patterns):
     N = np.size(patterns[0])
     M = np.shape(patterns)[0]
     W = np.zeros((N,N))
     W_previous = np.zeros((N,N))
     # maybe don't need the mu and you can do with when you do the steps
     H = np.zeros((N,N))
     for mu in range(M):
         for i in range(N):
             for j in range(N):
                 for k in range(N):
                     if k != i and k != j:
                         H[i][j] += W_previous[i][k]*patterns[mu][k]
                 W[i][j] = W_previous[i][j] + (1/N)*(patterns[mu][i]*patterns[mu][j] - patterns[mu][i]*H[j][i] - patterns[mu][j]*H[i][j])
         W_previous = W.copy()
     return W