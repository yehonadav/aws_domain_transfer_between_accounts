import boto3
from time import time
from secret import (
    domain,
    from_aws_access_key_id,
    from_aws_secret_access_key,
    to_aws_access_key_id,
    to_aws_secret_access_key,
)


class ZoneService:
    def __init__(self, access_key: str, secret_key: str, domain_name: str):
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name="us-east-1",
        )

        self.client = session.client('route53')
        self.zone_name = domain_name + '.'
        self.hosted_zone = None
        self.records = None

    def get_hosted_zone_of_domain(self):
        list_hosted_zones_response = self.client.list_hosted_zones()
        print("list_hosted_zones_response", list_hosted_zones_response)

        for hosted_zone in list_hosted_zones_response['HostedZones']:
            if hosted_zone['Name'] == self.zone_name:
                self.hosted_zone = hosted_zone
                return

        raise Exception(f"hosted zone '{self.zone_name}' not found in list_hosted_zones_response")

    def get_hosted_zone_records(self):
        list_resource_record_sets_response = self.client.list_resource_record_sets(HostedZoneId=self.hosted_zone['Id'])
        print("list_resource_record_sets_response", list_resource_record_sets_response)

        if len(list_resource_record_sets_response['ResourceRecordSets']) == 0:
            raise Exception(f"hosted zone '{self.zone_name}' has 0 records")

        self.records = list_resource_record_sets_response['ResourceRecordSets']

    def create_hosted_zone(self):
        create_hosted_zone_response = self.client.create_hosted_zone(
            Name=self.zone_name,
            CallerReference=f"{time()}",
        )
        print("create_hosted_zone_response", create_hosted_zone_response)

    def create_records(self, records):
        records_to_create = []
        for record in records:
            for existing_record in self.records:
                if record['Name'] == existing_record['Name']:
                    print(f"record already exist: {record}")
                    continue
                records_to_create.append(record)

        change_resource_record_sets_response = self.client.change_resource_record_sets(
            HostedZoneId=self.hosted_zone['Id'],
            ChangeBatch={
                'Comment': 'string',
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': record
                    }
                    for record in records_to_create
                ]
            }
        )
        print("change_resource_record_sets_response", change_resource_record_sets_response)
        return change_resource_record_sets_response


def copy_aws_hosted_zone_records_to_different_account(
        from_access_key: str,
        from_secret_key: str,
        to_access_key: str,
        to_secret_key: str,
        domain_name: str,
):
    """
    This functionality is not working as desired.
    I keep getting errors like this:
    botocore.errorfactory.InvalidChangeBatch: An error occurred (InvalidChangeBatch) when calling the ChangeResourceRecordSets operation: [The request contains an invalid set of changes for a resource record set 'CNAME xxx._domainkey.xxx.xxx.', The request contains an invalid set of changes for a resource record set 'CNAME xxx._domainkey.xxx.xxx.', The request contains an invalid set of changes for a resource record set 'CNAME xxx._domainkey.xxx.xxx.', The request contains an invalid set of changes for a resource record set 'A xxx.xxx.xxx.', The request contains an invalid set of changes for a resource record set 'CNAME autodiscover.xxx.xxx.', The request contains an invalid set of changes for a resource record set 'CNAME www.xxx.xxx.']
    If anyone knows how to make it work please send me a pull request =)
    :param from_access_key:
    :param from_secret_key:
    :param to_access_key:
    :param to_secret_key:
    :param domain_name:
    :return:
    """
    from_zone = ZoneService(from_access_key, from_secret_key, domain_name)
    from_zone.get_hosted_zone_of_domain()
    from_zone.get_hosted_zone_records()

    to_zone = ZoneService(to_access_key, to_secret_key, domain_name)
    # to_zone.create_hosted_zone()
    to_zone.get_hosted_zone_of_domain()
    to_zone.get_hosted_zone_records()
    to_zone.create_records(from_zone.records)


# copy_aws_hosted_zone_records_to_different_account(
#     from_aws_access_key_id,
#     from_aws_secret_access_key,
#     to_aws_access_key_id,
#     to_aws_secret_access_key,
#     domain
# )
