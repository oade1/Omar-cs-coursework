import pygame

class DataSystemManager:
    def __init__(self, game):
        game.setDataSystemManager(self) 

        self.data = {
            'PlayerData': None,
            'EnemyData': []




        } # example, this should be done reguraly, enemydata should be numbered and named according to the enemy type
          # nvm, enemy data is not a list that contains all of the enemy data objects to be saved



    def saveAllData(self):
        self.savePlayerData()
        self.saveEnemiesData()

    def savePlayerData(self):
        pass

    def saveEnemiesData(self):
        enemyDatas = self.data['EnemyData']

        if len(enemyDatas) > 0: #there is at least one object of the enemy data
            for enemyData in enemyDatas:
                for varName, varValue in enemyData.data.items():
                    print(varName, varValue)

    def loadAllData(self):
        self.loadPlayerData()
        self.loadEnemiesData()

    def loadPlayerData(self):
        pass

    def loadEnemiesData(self):
        pass                



    def addEnemyData(self, enemyData):
        if type(enemyData) is not EnemyData:
            return
        self.data['EnemyData'].append(enemyData)
    

class PlayerData:
    def __init__(self):
        self.data = {}

    def setData(self, key, value):
        self.data[key] = value
    
class EnemyData:
    def __init__(self):
        self.data = {}

    def setData(self, key, value):
        self.data[key] = value

    