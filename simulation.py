import random
import math
import matplotlib.pyplot as plt
import numpy as np

class Simulation:
    def __init__(self, lambd_max, mu1, mu2, max_customers):
        self.lambd_max = lambd_max
        self.mu1 = mu1
        self.mu2 = mu2
        self.max_customers = max_customers

    def lambd(self, t):
        lambd0 = 1.0
        period = 24.0
        return lambd0 * (1 + 0.5 * math.sin(2 * math.pi * t / period))

    def next_arrival_time(self, cur_t):
        t = cur_t
        while True:
            u = random.expovariate(self.lambd_max)
            t += u
            if random.random() <= self.lambd(t) / self.lambd_max:
                return t

    def simulate_2_queue(self):
        cur_t = 0.0
        ta = self.next_arrival_time(cur_t)
        t1 = float('inf')
        t2 = float('inf')
        
        busy1 = False
        busy2 = False
        q1 = []  
        q2 = [] 
        
        customers = {}
        nxt_customer_id = 1
        departures = 0  
        
        cur1 = None
        cur2 = None
        
        while departures < self.max_customers:
            nxt_e_t = min(ta, t1, t2)
            cur_t = nxt_e_t
            
            if nxt_e_t == ta:
                cust_id = nxt_customer_id
                nxt_customer_id += 1
                customers[cust_id] = {
                    'arrival_server1': cur_t,
                    'start_service_server1': None,
                    'departure_server1': None,
                    'arrival_server2': None,
                    'start_service_server2': None,
                    'departure_server2': None,
                }
                if not busy1:
                    busy1 = True
                    cur1 = cust_id
                    customers[cust_id]['start_service_server1'] = cur_t
                    s1 = random.expovariate(self.mu1)
                    t1 = cur_t + s1
                else:
                    q1.append(cust_id)
                ta = self.next_arrival_time(cur_t)
            
            elif nxt_e_t == t1:
                cust_id = cur1
                customers[cust_id]['departure_server1'] = cur_t
                customers[cust_id]['arrival_server2'] = cur_t
                
                if q1:
                    next_cust = q1.pop(0)
                    cur1 = next_cust
                    customers[next_cust]['start_service_server1'] = cur_t
                    s1 = random.expovariate(self.mu1)
                    t1 = cur_t + s1
                else:
                    busy1 = False
                    cur1 = None
                    t1 = float('inf')
                
                if not busy2:
                    busy2 = True
                    cur2 = cust_id
                    customers[cust_id]['start_service_server2'] = cur_t
                    s2 = random.expovariate(self.mu2)
                    t2 = cur_t + s2
                else:
                    q2.append(cust_id)
            
            elif nxt_e_t == t2:
                cust_id = cur2
                customers[cust_id]['departure_server2'] = cur_t
                departures += 1
                
                if q2:
                    next_cust = q2.pop(0)
                    cur2 = next_cust
                    customers[next_cust]['start_service_server2'] = cur_t
                    s2 = random.expovariate(self.mu2)
                    t2 = cur_t + s2
                else:
                    busy2 = False
                    cur2 = None
                    t2 = float('inf')
        
        return customers

    def total_time_in_system(self, customers):
        times_in_system = []
        for cust_id, data in customers.items():
            if data['departure_server2'] is not None:
                time_total = data['departure_server2'] - data['arrival_server1']
                times_in_system.append(time_total)
        return times_in_system
    
    def total_time_in_server1(self, customers):
        times_in_server1 = []
        for cust_id, data in customers.items():
            if data['departure_server1'] is not None:
                time_server1 = data['departure_server1'] - data['arrival_server1']
                times_in_server1.append(time_server1)
        return times_in_server1
    
    def total_time_in_server2(self, customers):
        times_in_server2 = []
        for cust_id, data in customers.items():
            if data['departure_server2'] is not None and data['arrival_server2'] is not None:
                time_server2 = data['departure_server2'] - data['arrival_server2']
                times_in_server2.append(time_server2)
        return times_in_server2

def main():
    lambd_max = 1.5
    mu1 = 1.2
    mu2 = 1.5
    max_customers = 50000

    sim = Simulation(lambd_max, mu1, mu2, max_customers)
    customers = sim.simulate_2_queue()

    times_in_system = sim.total_time_in_system(customers)
    avg_time = sum(times_in_system) / len(times_in_system)
    print(f"Average time in system: {avg_time}")

if __name__ == "__main__":
    main()
