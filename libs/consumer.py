class ConsumerInterface:
    def stop(self):
        raise NotImplementedError("SubClass must implement method.")

    async def start(self):
        raise NotImplementedError("SubClass must implement method.")
