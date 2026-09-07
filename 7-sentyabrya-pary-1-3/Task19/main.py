class CPU:
    def __init__(self, name, fr):
        self.name = name
        self.fr = fr

class Memory:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume

class MotherBoard:
    total_mem_slots = 4

    def __init__(self, name, cpu, *mem_slots):
        self.name = name
        self.cpu = cpu
        self.mem_slots = list(mem_slots[:self.total_mem_slots])

    def get_config(self):
        mem_info = []
        for mem in self.mem_slots:
            mem_info.append(f"{mem.name} - {mem.volume}")
        mem_str = "; ".join(mem_info)
        return [
            f"Материнская плата: {self.name}",
            f"Центральный процессор: {self.cpu.name}, {self.cpu.fr}",
            f"Слотов памяти: {self.total_mem_slots}",
            f"Память: {mem_str}"
        ]

cpu = CPU("Intel Core i7", "4.4 GHz")
mem1 = Memory("Kingston", "16 GB")
mem2 = Memory("Samsung", "16 GB")

mb = MotherBoard("GIGABYTE B560", cpu, mem1, mem2)

for line in mb.get_config():
    print(line)