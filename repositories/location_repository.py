from typing import Dict, List
from models.schemas import LocationItem, AddressItem


class LocationRepository:
    
    DEV_LOCATIONS_DATA = {
        "items": [
            {"location_name": "Bay Village Garden", "linear_feet": 84.8},
            {"location_name": "Bay Village Neighborhood Park", "linear_feet": 422.1},
            {"location_name": "Clarendon Street Playlot", "linear_feet": 781.9},
            {"location_name": "Elliot Norton Park", "linear_feet": 1406.6},
            {"location_name": "Lincoln Square", "linear_feet": 918.1},
            {"location_name": "Myrtle Street Playground", "linear_feet": 160.3},
            {"location_name": "Phillips Street Play Area", "linear_feet": 55.4},
            {"location_name": "Statler Park", "linear_feet": 1672.0},
            {"location_name": "Tai Tung Park", "linear_feet": 88.4},
            {"location_name": "Union Street Park", "linear_feet": 1673.8},
        ]
    }
    
    DEV_ADDRESSES_DATA = {
        "items": [
            {"location_name": "Bay Village Garden", "full_address": "32 Melrose St, Boston, MA 02116, USA"},
            {"location_name": "Bay Village Neighborhood Park", "full_address": "2 Melrose St, Boston, MA 02116, USA"},
            {"location_name": "Clarendon Street Playlot", "full_address": "260 Clarendon St, Boston, MA 02116, USA"},
            {"location_name": "Elliot Norton Park", "full_address": "295 Tremont St, Boston, MA 02116, USA"},
            {"location_name": "Lincoln Square", "full_address": "2 Columbus Ave, Boston, MA 02116, USA"},
            {"location_name": "Myrtle Street Playground", "full_address": "50 Myrtle St, Boston, MA 02114, USA"},
            {"location_name": "Phillips Street Play Area", "full_address": "21 Phillips St, Boston, MA 02114, USA"},
            {"location_name": "Statler Park", "full_address": "243 Stuart St, Boston, MA 02116, USA"},
            {"location_name": "Tai Tung Park", "full_address": "110 Tyler St, Boston, MA 02111, USA"},
            {"location_name": "Union Street Park", "full_address": "98 Union St, Boston, MA 02129, USA"},
        ]
    }
    
    def get_dev_locations(self) -> List[LocationItem]:
        return [LocationItem(**item) for item in self.DEV_LOCATIONS_DATA["items"]]
    
    def get_dev_addresses(self) -> List[AddressItem]:
        return [AddressItem(**item) for item in self.DEV_ADDRESSES_DATA["items"]]
    
    def get_dev_address_dict(self) -> Dict[str, str]:
        return {
            item["location_name"]: item["full_address"]
            for item in self.DEV_ADDRESSES_DATA["items"]
        }
