
def runSimulation(PetriNet, verbose: int = 1,  defTimeUnit: str = sec):
    # loop through all transitions and check if firing is enabled
    checkEnabled()
    # generate random delay based on distribution type for all ENABLED Timed Transitions
    generateDelay()

    # make a list of enabled transitions, randomize their order and process them one by one (update, with checkEnabled() after every event)
    processEvents()

    # increase global timer to reach the next firing
    increaseGlobalTimer()
