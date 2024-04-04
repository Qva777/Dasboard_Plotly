from ordercast_client.models import Client


class ClientRepository:
    @staticmethod
    def get_client_data():
        """ Get client data """
        return Client.objects.all()
