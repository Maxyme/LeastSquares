class LockItem:

    def __init__(self, Item, MaxRecursion, Used):
        self.Item = Item
        self.MaxRecursion = MaxRecursion
        self.Used = Used # used is true or false, depending if the locked item was used in an iteration.
