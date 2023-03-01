import random
import simpy

RANDOM_SEED = 42 #numero arbitrario
NUM_PROCESSES = 10
INTERVAL = 10
MEMORY_SIZE = 100
CPU_SPEED = 3 #instrucciones por unidad de tiempo
random.seed(RANDOM_SEED)

class Process:
    def __init__(self, env, id, memory_request):
        self.env = env
        self.id = id
        self.memory_request = memory_request
        self.instructions_left = random.randint(1, 10)
        self.action = env.process(self.run())

    def run(self):
        print(f'Tiempo {env.now}: Proceso {self.id} llega y pide {self.memory_request} de memoria') #New
        with memory.get(self.memory_request) as req:
            yield req
            print(f'Tiempo {env.now}: Proceso {self.id} se le da {self.memory_request} de memoria y entra READY') #New
            while self.instructions_left > 0:
                with cpu.request() as req:
                    yield req
                    print(f'Tiempo {env.now}: Proceso {self.id} está listo para el CPU, tiene {self.instructions_left} instrucciones')#READY
                    instructions_to_execute = min(self.instructions_left, CPU_SPEED) #Running
                    self.instructions_left -= instructions_to_execute
                    yield env.timeout(instructions_to_execute / CPU_SPEED)
                    if self.instructions_left <= 0: #si ya no quedan instrucciones
                        print(f"Proceso {self.id} terminado en tiempo {env.now}") #Terminated
                        memory.put(self.memory_request) # Devolver la memoria utilizada
                        return
                    else:
                        espera = random.randint(1, 2)
                        if espera == 1: #Waiting
                            print(f"Proceso {self.id} en Waiting en tiempo {env.now}")
                            print(f'El proceso {self.id} está esperando por I/O')
                            yield env.timeout(1)
                            print(f'El proceso {self.id} ha completado una operación de I/O y regresa a ready')
                            # El proceso regresa al estado ready después de las operaciones de I/O
                            estado_anterior = "READY"
                            tiempo_cambio_estado = env.now
                            print(f"{self.id} está en estado {estado_anterior} en el tiempo {tiempo_cambio_estado}")
                            
                        elif  espera == 2: #Ready
                            print(f"Proceso {self.id} regresó a Ready desde Running en tiempo {env.now}") # Ir a la cola de Ready
    


def generate_processes(env, num_processes, interval): #Genera los procesos
    for i in range(num_processes):
        memory_request = random.randint(1, 10)
        p = Process(env, i, memory_request)
        yield env.timeout(random.expovariate(1.0 / interval)) #Distribución exponencial con intervalo de 10, simula la llegada de procesos


env = simpy.Environment()
cpu = simpy.Resource(env, capacity=1)
memory = simpy.Container(env, capacity=MEMORY_SIZE, init=MEMORY_SIZE)
env.process(generate_processes(env, NUM_PROCESSES, INTERVAL))
env.run() #Corre la simulación






        