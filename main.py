from broker.Server import Server
from subscriber.SubEntity import SubEntity
from utils.on_messages import insert_new_device

main_server = Server()
sub = SubEntity("cliente1", "localhost", "1883", "test", "1234")
sub.connect_and_subscribe_to_topic("NuevosDispositivos", insert_new_device)



