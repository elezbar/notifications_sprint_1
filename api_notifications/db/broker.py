from services.broker.abscract_broker import AbstractBroker

priority_brokers: dict[str, AbstractBroker] | None = None


def get_brokers():
    if not priority_brokers:
        raise Exception('priority_brokers not initialized yet.')
    return priority_brokers
