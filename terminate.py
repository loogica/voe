import boto.ec2

from decouple import config

key_name = config('KEY_NAME')
aws_access_key = config("AWS_ACCESS_KEY")
aws_secret_key = config("AWS_SECRET_KEY")
region = config('REGION')
instance_size = config('INSTANCE_SIZE')
sec_group = config('DEFAULT_SECURITY_GROUP')

def terminate_all(region):
    conn = boto.ec2.connect_to_region(region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key)

    instances = [i for r in conn.get_all_reservations() for i in r.instances]
    hosts = [instance.public_dns_name for instance in instances]

    print(hosts)

    for instance in instances:
        conn.terminate_instances(instance_ids=[instance.id])

if __name__ == "__main__":
    terminate_all(region)
