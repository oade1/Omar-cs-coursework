class SaveSystemManager:
    def __init__(self, player):
        self.data = {
            'PlayerData': None,
            'EnemyData': None
        } # example, this should be done reguraly, enemydata should be numbered and named according to the enemy type

    def saveAllData(self):
        self.savePlayerData()
        self.saveEnemiesData()

    def savePlayerData(self):
        pass

    def saveEnemiesData(self):
        pass

    def loadAllData(self):
        self.loadPlayerData()
        self.loadEnemiesData()

    def loadPlayerData(self):
        pass

    def loadEnemiesData(self):
        pass




    def initiatePlayerData(self):
        pass


    def initiateEnemyData(self, Enemy):
        pass




class PlayerData:
    def __init__(self):
        self.position = None
        
    def setPosition(self, position): self.position = position

class EnemyData:
    def __init__(self):
        self.position = None
        self.type = None
        self.serializedNumber = None

    def setPosition(self, position): self.position = position
    def setType(self, Ntype): self.type = Ntype
    def setNumber(self, serializedNumber): self.serializedNumber = serializedNumber