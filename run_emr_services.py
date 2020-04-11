import sys
from services.data_deletion.clean_deleted_data_from_db import DataDeletion

services = {
    "clean_database": DataDeletion().clean_deleted_data,
}


def run_mrm_services(arguments):
    all_services = list(services.keys())
    try:
        if not arguments:
            arguments = list(services.keys())
        for argument in arguments:
            services[argument]()
    except KeyError as wrong_key:
        print(
            wrong_key,
            "is not a valid service. Use one of these",
            all_services
        )


if __name__ == "__main__":
    arguments = sys.argv[1:]
    run_emr_services(arguments)
