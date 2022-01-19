from aws_domain_transfer_between_accounts import transfer_domain_between_2_aws_accounts
from secret import (
    domain,
    from_aws_access_key_id,
    from_aws_secret_access_key,
    to_aws_access_key_id,
    to_aws_secret_access_key,
    to_account,
)


if __name__ == "__main__":
    transfer_domain_between_2_aws_accounts(
        from_aws_access_key_id,
        from_aws_secret_access_key,
        domain,
        to_account,
        to_aws_access_key_id,
        to_aws_secret_access_key,
    )
