from ordercast_country.models import Country


class CountryRepository:
    @staticmethod
    def get_country_data():
        """ Get country data """
        return Country.objects.all()


