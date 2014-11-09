import subprocess
import sys

import boto.ec2

from decouple import config

from my_aws import (connection, run_instance, ComputeInstance)

key_name = config('KEY_NAME')
aws_access_key = config("AWS_ACCESS_KEY")
aws_secret_key = config("AWS_SECRET_KEY")
region = config('REGION')
instance_size = config('INSTANCE_SIZE')
sec_group = config('DEFAULT_SECURITY_GROUP')

def setup(instance_type):
    n = 1
    if not instance_type == "master" and not instance_type == "sink":
        n = int(sys.argv[2])

    conn = connection(region, aws_access_key, aws_secret_key)
    instances = []

    for i in range(n):
        instances.append(ComputeInstance(run_instance(conn,
            key_name, instance_size, [sec_group])))

    for instance in instances:
        subprocess.call(["rm", "-f", "voe.zip"])
        subprocess.call(["zip", "-r", "voe.zip", "."])
        instance.run('sudo apt-get install -y unzip')
        instance.put('voe.zip', 'voe.zip')
        instance.run('unzip voe.zip')
        instance.run('chmod +x env_setup.sh')
        instance.run('./env_setup.sh')
        instance.run('sudo pip install -r requirements.txt')
        instance.run('sudo supervisorctl reload')

    if instance_type == "master":
        instance = instances[0]
        print("Master private: {}".format(instance.private_ip_address))
        print("Master public dns: {}".format(instance.public_dns_name))
        instance.run('sudo ln -s /home/ubuntu/env/master.conf /etc/supervisor/conf.d/master.conf')
        instance.run('sudo supervisorctl reload')
    elif instance_type == "sink":
        instance = instances[0]
        print("Master private: {}".format(instance.private_ip_address))
        print("Master public dns: {}".format(instance.public_dns_name))
        instance.run('sudo ln -s /home/ubuntu/env/sink.conf /etc/supervisor/conf.d/sink.conf')
        instance.run('sudo supervisorctl reload')
    else:
        for instance in instances:
            instance.run('mkdir data')
            instance.run('sudo chmod 777 data/')
            instance.run('sudo ln -s /home/ubuntu/env/worker.conf /etc/supervisor/conf.d/worker.conf')
            instance.run('sudo supervisorctl reload')
            print("Master private: {}".format(instance.private_ip_address))
            print("Master public dns: {}".format(instance.public_dns_name))

if __name__ == "__main__":
    setup(sys.argv[1])

