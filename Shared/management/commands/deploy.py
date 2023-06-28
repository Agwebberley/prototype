
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        import boto3
        
        # Step 1: Create EC2 instance with AMI id: ami-01adb54d6fdc66a39
        # Step 2: Create Postgre Database in RDS and link it to the EC2 instance
        # Step 3: Create Elastic IP and link it to the EC2 instance
        # Step 4: Create the SNS Topics and SQS Queues
        # Step 5: Connect to the EC2 instance
        # Step 6: Add Postgre Credentials to settings.py & Elastic IP as allowed host
        # Step 7: Run the following commands:
        # python manage.py makemigrations
        # python manage.py migrate

        print("Starting deployment")
        print("This script assumes that you have already configured your AWS credentials and have the AWS CLI installed")

        # Step 1.1: Ensure that the EC2 keypair exists
        ec2_keypair_name = input("Enter the EC2 keypair name (If blank will be ec2-keypair): ")
        if ec2_keypair_name == "":
            ec2_keypair_name = "ec2-keypair"
        
        ec2 = boto3.client('ec2', region_name='us-west-2')
        ec2_keypairs = ec2.describe_key_pairs()
        ec2_keypair_names = [keypair['KeyName'] for keypair in ec2_keypairs['KeyPairs']]
        if ec2_keypair_name not in ec2_keypair_names:
            # Step 1.1.1: Create EC2 keypair
            ec2.create_key_pair(KeyName=ec2_keypair_name)
            print("EC2 keypair created")

            # Step 1.1.2: Save EC2 keypair file
            import os
            print(ec2_keypairs)
            ec2_keypair_file = open(f"{ec2_keypair_name}.pem", "w")
            ec2_keypair_file.write(ec2_keypairs['KeyMaterial'])
            ec2_keypair_file.close()
        else:
            print("EC2 keypair already exists, using existing keypair")
            # Check if the keypair file exists
            import os
            if not os.path.exists(f"{ec2_keypair_name}.pem"):
                print(f"EC2 keypair file {ec2_keypair_name}.pem does not exist, you will need to create one")
                print("Create the EC2 keypair in the AWS console and then run this script again")
                print("Make sure to save the keypair file in the same directory as this script")
                exit()
        # Step 1.2: Create EC2 instance with AMI id: ami-01adb54d6fdc66a39
        ec2_instance = ec2.ServiceResource.create_instances(
            ImageId='ami-01adb54d6fdc66a39',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName=ec2_keypair_name,
        )
        print("EC2 instance created")

        # Step 2: Create Postgre Database in RDS and link it to the EC2 instance
        
        # Database input variables
        db_instance_identifier = input("Enter the database instance identifier (If blank will be postgres): ")
        db_username = input("Enter the database username (If blank will be postgres): ")
        db_password = input("Enter the database password (If blank will be auto generated): ")
        db_region = input("Enter the database region (If blank will be us-west-2d): ")
        db_max_storage = input("Enter the database max storage (If blank will be 20GB): ")

        # If the user did not enter a database instance identifier, set it to postgres
        if db_instance_identifier == "":
            db_instance_identifier = "postgres"

        # If the user did not enter a username, set it to postgres
        if db_username == "":
            db_username = "postgres"
        
        # If the user did not enter a password, generate a random one
        if db_password == "":
            import secrets
            db_password = secrets.token_urlsafe(16)
            print(f"Your database password is: {db_password}")

        # If the user did not enter a region, set it to us-west-2d
        if db_region == "":
            db_region = "us-west-2d"

        # If the user did not enter a max storage, set it to 20GB
        if db_max_storage == "":
            db_max_storage = 20

        rds = boto3.client('rds', region_name='us-west-2')
        rds_response = rds.create_db_instance(
            engine='postgres',
            dbInstanceClass='db.t3.micro',
            MasterUsername=db_username,
            MasterUserPassword=db_password,
            DBInstanceIdentifier=db_instance_identifier,
            EngineVersion='15.3',
            AllocatedStorage=db_max_storage,
            EnableIAMDatabaseAuthentication=True,
        )
        print("RDS database created")

        # Step 2b: Connect the RDS database to the EC2 instance
        # Wait for the RDS database to be available
        rds_waiter = rds.get_waiter('db_instance_available')
        rds_waiter.wait(DBInstanceIdentifier=db_instance_identifier)
        rds_instance = rds.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
        rds_endpoint = rds_instance['DBInstances'][0]['Endpoint']['Address']

        # Create the security group for the EC2 instance
        ec2_security_group = ec2.create_security_group(
            Description='EC2 Security Group',
            GroupName='ec2-security-group',
        )
        ec2_security_group.authorize_ingress(
            CidrIp='0.0.0.0/0',
            IpProtocol='tcp',
            FromPort=5432,
            ToPort=5432,
        )
        print("EC2 security group created")

        # Attach the security group to the EC2 instance
        ec2_instance[0].modify_attribute(Groups=[ec2_security_group.id])
        print("EC2 security group attached to EC2 instance")

        # Add IAM role to EC2 instance that allows it to access the RDS database
        iam = boto3.client('iam', region_name='us-west-2')
        iam_response = iam.create_role(
            RoleName='ec2-role',
            AssumeRolePolicyDocument='{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Principal": {"Service": "ec2.amazonaws.com"},"Action": "sts:AssumeRole"}]}',
        )

        # Step 3: Create Elastic IP and link it to the EC2 instance
        ec2_eip = ec2.allocate_address(Domain='vpc')
        ec2_eip.associate(InstanceId=ec2_instance[0].id)
        print("Elastic IP created and attached to EC2 instance")
        print(f"Your Elastic IP is: {ec2_eip.public_ip}")

        # Step 4: Create the SNS Topics and SQS Queues
        # Step 4.1: Create the SNS Topics
        sns = boto3.client('sns', region_name='us-west-2')
        sns_topic_arns = []
        sns_topic_names = ['Log', 'Inventory', 'Items', 'Order', 'Manufacture']
        for sns_topic_name in sns_topic_names:
            sns_response = sns.create_topic(Name=sns_topic_name)
            sns_topic_arns.append(sns_response['TopicArn'])
            print(f"SNS Topic {sns_topic_name} created")
        
        # Step 4.2: Create the SQS Queues
        sqs = boto3.client('sqs', region_name='us-west-2')
        sqs_queue_urls = []
        sqs_queue_names = ['Log', 'Inventory', 'AccountsReceivable', 'Order', 'Manufacture']
        for sqs_queue_name in sqs_queue_names:
            sqs_response = sqs.create_queue(QueueName=sqs_queue_name)
            sqs_queue_urls.append(sqs_response['QueueUrl'])
            print(f"SQS Queue {sqs_queue_name} created")
        
        # Step 4.3: Subscribe the SQS Queues to the SNS Topics
        # The connections are as follows:
        # Log -> Log
        # Inventory -> Manufacture
        # Inventory -> Items
        # Items -> Inventory
        # Manufacture -> Inventory
        # Order -> Inventory
        # Order -> AccountsReceivable
        subscriptions = {"Log": ["Log"], "Inventory": ["Manufacture", "Items"], "Items": ["Inventory"], "Manufacture": ["Inventory"], "Order": ["Inventory", "AccountsReceivable"]}
        for sns_topic_arn in sns_topic_arns:
            for subscription in subscriptions[sns_topic_arn.split(":")[-1]]:
                sns.subscribe(TopicArn=sns_topic_arn, Protocol='sqs', Endpoint=sqs.get_queue_url(QueueName=subscription)['QueueUrl'])
                print(f"SQS Queue {subscription} subscribed to SNS Topic {sns_topic_arn.split(':')[-1]}")
        
        # Step 5: Connect to the EC2 instance
        from fabric import Connection, task

        # Download the key pair as key.pem
        ec2_instance[0].key_pair.download('key.pem')

        CONNECTION_PROPERTIES = {
            'user': 'ubuntu',
            'host': ec2_eip.public_ip,
            'connect_kwargs': {
                'key_filename': f'{ec2_keypair_name}.pem'
            }
        }

        def over_ssh(ctx):
            # Step 6: Add Postgre Credentials to ENV variables & Elastic IP as allowed host
            # Step 6.1: Add Postgre Credentials to ENV variables
            ctx.run('export RDS_HOSTNAME={}'.format(rds_endpoint))
            ctx.run('export RDS_PORT=5432')
            ctx.run('export RDS_USERNAME={}'.format(db_username))
            ctx.run('export RDS_PASSWORD={}'.format(db_password))
            print("Postgre credentials added to ENV variables")
            # Step 6.2: Add Elastic IP as allowed host
            ctx.run('export ALLOWED_HOSTS={}'.format(f'["http://localhost", "http://{ec2_eip.public_ip}"]'))
            os.environ['ALLOWED_HOSTS'] = f'["http://localhost", "http://{ec2_eip.public_ip}"]'
            print("Elastic IP added to allowed hosts")

            # Step 7: Run Commands
            # Step 7.1 Git Pull
            ctx.run('git clone https://github.com/Agwebberley/prototype.git')
            ctx.run('cd prototype')
            # Step 7.2: Run Django Migrations
            try:
                ctx.run('sudo python3 manage.py makemigrations')
                ctx.run('sudo python3 manage.py migrate')
                print("Django migrations completed")
            except:
                print("Django migrations failed")
                print("You will have to manually run the migrations")
            # Step 7.2: Run Django Server
            ctx.run('sudo systemctl restart gunicorn')
            ctx.run('sudo systemctl restart nginx')
            print("Django server started")
        
        with Connection(**CONNECTION_PROPERTIES) as c:
            over_ssh(c)

