class CPU:
    def __init__(self, name, fr):
        self.name = name
        self.freq = fr

class Memory:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume

class MotherBoard:
    def __init__(self, name, cpu, *mem_slots):
        self.name = name
        self.cpu = cpu
        self.total_mem_slots = 4
        self.mem_slots = list(mem_slots)

    def get_config(self):
        parts = []
        for mem in self.mem_slots:
            parts.append(f"{mem.name} - {mem.volume}gb")
        memory_str = '; '.join(parts)

        return [
            f"Материнская плата: {self.name}",
            f"Центральный процессор: {self.cpu.name}, {self.cpu.freq}GHz",
            f"Слотов памяти: {self.total_mem_slots}",
            f"Память: {memory_str}",]

cpu = CPU('Intel i7-11700kf', 4400)
mem1 = Memory('Kingston', 16)
mem2 = Memory('Kingston', 16)

mb = MotherBoard('GIGABYRE', cpu, mem1, mem2)

for line in mb.get_config():
    print(line)