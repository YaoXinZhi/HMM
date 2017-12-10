
# -*- coding :utf-8 -*-
# /usr/bin/python
# file HMM


class HMM():
    
    def __init__(self,alphabet = [],states = [],states_p = {},trans_p = {},emit_p = {}):
        self.alphabet = alphabet
        self.states = states
        self.states_p = states_p
        self.trans_p = trans_p
        self.emit_p = emit_p
        
    def print_datable(self,V):
        s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
        for y in V[0]:
            s += "%.5s: " % y
            s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
            s += "\n"
        print(s)        
        
    def viterbi(self):
        '''The day after the state will depend on the state 
        of the day before and the current observable state'''
        V = [{}]
        path = {}
        
        # Initializze base cases (t == 0)
        V = [{y:(self.states_p[y] * self.emit_p[y][self.alphabet[0]]) for y in self.states}]
        path = {y:[y] for y in self.states}
        
        # Run Viterbi for t >0
        for t in range(1,len(self.alphabet)):
            V.append({})
            newpath = {}
            for y in self.states:
                (prob , state) = max((V[t-1][y0] * self.trans_p[y0][y] * self.emit_p[y][self.alphabet[t]],y0) for y0 in states)
                V[t][y] = prob
                newpath[y] = path[state] + [y]
            path = newpath
        self.print_datable(V)
        (prob,state) = max((V[t][y] , y ) for y in self.states)
        print ('The maximum possible path:  '+str(path[state]))
        print ('Probability:  '+str(prob))
        print ()        
    
    def forword(self):
        
        V_p = [{}]
        V_e = [{}]
        
        # Initializze base cases (t == 0)
        V_p = [{y:self.states_p[y] for y in self.states}]
        V_e = [{y:(V_p[0][y] * self.emit_p[y][self.alphabet[0]]) for y in self.states}]
        
        # Run forword algorithm for t > 0
        for t in range(1,len(self.alphabet)):
            V_p.append({})
            V_e.append({})
            for y in self.states:
                V_p[t][y] = sum((V_p[t-1][y0] * self.trans_p[y0][y]) for y0 in self.states)
                V_e[t][y] = V_p[t][y] * self.emit_p[y][self.alphabet[t]]
        print ('Emission probability matrix: ')
        self.print_datable(V_e)
        print ('Trans probability matrix: ')
        self.print_datable(V_p)
        print ()
        prob_s = max((V_p[t][y]) for y in self.states)
        prob_a = max((V_e[t][y]) for y in self.states)
        print ('The maximum possible last state:  ' + y )
        print ('The maximum transfer probability:   ' + str(prob_s))
        print ('Maximum probability of emisson:  ' + str(prob_a))
        print ()
        
        
    def Backward(self):
        V_p = [{}]
        V_e = [{}]
        
        for i in range(len(self.alphabet)-1):
            V_p.append({})
            V_e.append({})
        
            
        # Initializze base cases (t == 0)
 
        V_p[len(self.alphabet)-1] = {y:1 for y in self.states}
        V_e[len(self.alphabet)-1] = {y:1 * self.emit_p[y][self.alphabet[-1]] for y in self.states}  
        # Run Backword algorithm for t > 0
        for t in reversed(range(len(self.alphabet)-1)):
            for y in self.states:
                V_p[t][y] = sum((V_p[t+1][y0] * self.trans_p[y0][y])for y0 in self.states)
                V_e[t][y] = (V_p[t][y] * self.emit_p[y][self.alphabet[t]])
        print ('Emission probability matrix: ')
        self.print_datable(V_e)
        print ('Trans probability matrix: ')
        self.print_datable(V_p)
        prob_s = max((V_p[t][y]) for y in self.states)
        prob_a = max((V_e[t][y]) for y in self.states)
        print ('The maximum possible last state:  ' + y )
        print ('The maximum transfer probability:   ' + str(prob_s))
        print ('Maximum probability of emisson:  ' + str(prob_a))
        print ()  
        

        
        
        
if __name__ == '__main__':
    states = ['Healthy','Fever']    #Hidden
    observations = ['normal','cold','dizzy']    #visble
    states_probability = {'Healthy':0.6,'Fever':0.4}
    transition_probability = {'Healthy':{'Healthy':0.7,'Fever':0.3},'Fever':{'Healthy':0.4,'Fever':0.6}}
    emission_probability = {'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}}
    
    ill_hmm = HMM(alphabet=observations,states=states,states_p=states_probability,trans_p=transition_probability,emit_p=emission_probability)
    
    print ('Viterbi algorithm results:')
    ill_hmm.viterbi()
    
    print ('///////////////////////////////')
    print ()
    
    print ('Forward algorithm results:')
    ill_hmm.forword()
    
    print ('////////////////////////////////')
    print ()
    
    print ('Backwork algorithm results:')
    ill_hmm.Backward()
    
