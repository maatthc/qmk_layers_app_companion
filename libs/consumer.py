class ConsumerInterface:
    def stop(self):
        raise NotImplementedError("SubClass must implement method.")

    def run(self):
        raise NotImplementedError("SubClass must implement method.")
