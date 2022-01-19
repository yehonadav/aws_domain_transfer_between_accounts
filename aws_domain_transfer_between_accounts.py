import boto3


def send_transfer_request(from_access_key: str, from_secret_key: str, domain_name: str, to_account_id: str) -> dict:
    session = boto3.Session(
        aws_access_key_id=from_access_key,
        aws_secret_access_key=from_secret_key,
        region_name="us-east-1",
    )

    client = session.client('route53domains')

    return client.transfer_domain_to_another_aws_account(
        DomainName=domain_name,
        AccountId=to_account_id,
    )


def accept_transfer_request(access_key: str, secret_key: str, domain_name: str, send_transfer_response: dict) -> dict:
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="us-east-1",
    )

    client = session.client('route53domains')

    return client.accept_domain_transfer_from_another_aws_account(
        DomainName=domain_name,
        Password=send_transfer_response['Password']
    )


def transfer_domain_between_2_aws_accounts(
        from_aws_access_key_id,
        from_aws_secret_access_key,
        domain,
        to_account,
        to_aws_access_key_id,
        to_aws_secret_access_key
):
    send_response = send_transfer_request(from_aws_access_key_id, from_aws_secret_access_key, domain, to_account)
    print(send_response)
    accept_response = accept_transfer_request(to_aws_access_key_id, to_aws_secret_access_key, domain, send_response)
    print(accept_response)
