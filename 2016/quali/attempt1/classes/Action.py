from enum import Enum
from abc import ABC, abstractmethod

class ActionType(Enum):
  LOAD = 1
  DELIVER = 2
  UNLOAD = 3
  WAIT = 4

class Action(ABC):
  def __init__(self, O, drone, action):
    self.action = action
    self.drone = drone
    self.O = O

  @abstractmethod
  def toString(self):
    pass

  @abstractmethod
  def getDuration(self, x=0, y=0):
    pass

  def __repr__(self):
      return str(self)
  def __str__(self):
      return "A(%s)" % (self.toString())

class WaitAction(Action):
  def __init__(self, O, drone, time):
    super(WaitAction, self).__init__(O, drone, ActionType.WAIT)
    self.time = time

  def toString(self):
    return str(self.drone.No) + ' W ' + str(self.time)

  def getDuration(self, x=0, y=0):
    return self.time

class DeliverAction(Action):
  def __init__(self, O, drone, order, product, quantity):
    super(DeliverAction, self).__init__(O, drone, ActionType.DELIVER)
    self.order = order
    self.product = product
    self.quantity = quantity

  def toString(self):
    return str(self.drone.No) + ' D ' + str(self.order.No) + ' ' + str(self.product.No) + ' ' + str(self.quantity)

  def getDuration(self, x=0, y=0):
    return math.ceil(((self.order.x-x)**2+(self.order.y-y)**2)**(.5)) + 1

class UnloadAction(Action):
  def __init__(self, O, drone, warehouse, product, quantity):
    super(UnloadAction, self).__init__(O, drone, ActionType.UNLOAD)
    self.warehouse = warehouse
    self.product = product
    self.quantity = quantity

  def toString(self):
    return str(self.drone.No) + ' U ' + str(self.warehouse.No) + ' ' + str(self.product.No) + ' ' + str(self.quantity)

  def getDuration(self, x=0, y=0):
    return math.ceil(((self.warehouse.x-x)**2+(self.warehouse.y-y)**2)**(.5)) + 1

class LoadAction(Action):
  def __init__(self, O, drone, warehouse, product, quantity):
    super(LoadAction, self).__init__(O, drone, ActionType.LOAD)
    self.warehouse = warehouse
    self.product = product
    self.quantity = quantity

  def toString(self):
    return str(self.drone.No) + ' L ' + str(self.warehouse.No) + ' ' + str(self.product.No) + ' ' + str(self.quantity)

  def getDuration(self, x=0, y=0):
    return math.ceil(((self.warehouse.x-x)**2+(self.warehouse.y-y)**2)**(.5)) + 1
