class ParkingSpace:
    def __init__(self, id):
        self.id = id
        self.occupied = False

    def occupy(self):
        self.occupied = True

    def free(self):
        self.occupied = False

# Lista de plazas de garaje, inicialmente todas libres (False = libre, True = ocupada)
NUM_PLAZAS = 48
plazas = [False] * NUM_PLAZAS