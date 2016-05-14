class Battery(object):
    """
    A battery. Start with a simple linear model - to be replaced with non linear models
    
    Attributes:
        Name: String
        capacity: KWh
        powerIn: KW
        powerOut:KW
        Dissipation Rate: % charge /HH lost  - replace with a method - default = 0
        charge: Current charge in KWh - default = 50%
        importEff: Efficiency of importing power in decimal - default 0.925
        exportEff: Efficiency of importing power in decimal - default = importEff
        
    """
    def __init__(self,name,capacity,powerIn, powerOut = None, DissipationRate = None, charge = None, importEff = None, exportEff = None):
        self.name = name
        self.capacity = capacity
        self.powerIn = powerIn
        if powerOut is None:
            powerOut = powerIn
        self.powerOut = powerOut
        if DissipationRate is None:
            DissipationRate = 0
        self.DissipationRate = DissipationRate
        if charge is None:
            charge = capacity/2 #to make for easier initialisation
        self.charge = charge
        if importEff is None:
            importEff = 0.925
        if exportEff is None:
            exportEff = importEff
        self.importEff = importEff
        self.exportEff = exportEff
        self.loss = 0
        self.totalCharges =0
        self.totalDischarges = 0
        self.availableDischarge = self.charge*self.importEff
        self.availableCharge = (self.capacity-self.charge)/self.exportEff
        
    def load(self, load):
        """Expose the battery to a load - charge or discharge as appropriate"""
        if type(load) <> float:
            raise TypeError
        if load <0:
            self.discharge(-load)
        if load>0:
            self.chargeUp(load)
        return self.charge
    
    def chargeUp(self, importAmount):
        """ Charge the battery by the amount exposed to the battery from the outside"""
        chargeAmount = importAmount*self.importEff
        if importAmount <0:
            raise ValueError('Trying to discharge by negative amount')
        if chargeAmount+self.charge > self.capacity:
            raise RuntimeError('Battery can''t store that much, can only store'+str(self.capacity-self.charge))
        self.charge += chargeAmount
        self.totals(importAmount = importAmount, chargeAmount  = chargeAmount)
        return self.charge
        
    def discharge(self, exportAmount):
        """ Discharge the battery by the amount required from the battery by the outside"""
        dischargeAmount = exportAmount/self.exportEff
        if exportAmount <0:
            raise ValueError('Trying to discharge by negative amount')
        if self.charge-dischargeAmount <0:
            raise RuntimeError('Battery discharge that much, can only discharge'+str(self.charge/self.exportEff))
        self.charge -= dischargeAmount
        self.totals(exportAmount = exportAmount, dischargeAmount  = dischargeAmount)
        return self.charge
        
    def totals(self, importAmount = 0,exportAmount = 0,chargeAmount = 0,dischargeAmount = 0):
        """Keeps track of losses in the battery"""
        loss = importAmount-exportAmount-chargeAmount+dischargeAmount
        self.loss += loss  
        self.totalCharges +=chargeAmount
        self.totalDischarges += dischargeAmount
        return self.loss  
    
        
def chargeController(Battery,charge):
    """this should become a class, that is created when battery is created"""
    if charge <0:
        if Battery.availableDischarge<-charge:    ##  should this be in battery object?
            print 'discharge of ' + str(-charge) + ' cannot be met, outputting max discharge of'
            charge = -Battery.availableDischarge
            print str(-charge) + ' KWh'
    elif charge >0:
        if Battery.availableCharge<charge:    ##  should this be in battery object?
            print 'charge of ' + str(charge) + ' cannot be met, outputting max discharge of'
            charge = Battery.availableCharge
            print charge + ' KWh'
    return charge

 
def randomChargeTest(Battery, length = 1000, mx = 500):
    import random as rd
    for i in range(length):
        jump = rd.random()* mx * rd.choice([-1,1])
        print 'load of ' + str(jump)
        charge = chargeController(Battery,jump)
        Battery.load(charge)
        print 'battery level of ' + str(Battery.charge)

            
def printResults():
    print ' battery charged by ' +str(test.totalCharges)
    print ' battery discharged by ' +str( test.totalDischarges)
    print ' battery lost ' +str( test.loss)
        
test = Battery('test battery', 2000, 500)

randomChargeTest(test)

printResults()