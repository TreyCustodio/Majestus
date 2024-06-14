from statemachine import StateMachine

class AbstractGameFSM(StateMachine):
    def __init__(self, obj):
        """All state machines will have an associated
           object."""
        self.obj = obj
        super().__init__()
    
    def updateState(self):
        pass
    
    def update(self, seconds=0):
        """Stub method to allow abstraction."""
        pass
    
    def __eq__(self, other):
        """Equality for ease of access. Can be used
        with other StateMachines of the same class or
        with strings which match the current_state.id"""
        
        if type(self) == type(other):
            return self.current_state.id == other.current_state.id
        else:
            return self.current_state.id == other