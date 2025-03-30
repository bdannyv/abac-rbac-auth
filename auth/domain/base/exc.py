class AggregateHasNoEventHandler(Exception):
    def __init__(self, aggregate, event):
        super().__init__(f"{aggregate} has no handler to process: {event}")
