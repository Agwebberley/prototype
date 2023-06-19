
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        import boto3
        
        # Step 1: Create EC2 instance with AMI id: ami-01adb54d6fdc66a39
        # Step 2: Create Postgre Database in RDS and link it to the EC2 instance
        # Step 3: Create Elastic IP and link it to the EC2 instance
        # Step 4: Create the SNS Topics and SQS Queues
        # Step 5: Create the IAM Role and attach the policy
        # Step 6: Add Postgre Credentials to settings.py & Elastic IP as allowed host
        # Step 7: Run the following commands:
        # python manage.py makemigrations
        # python manage.py migrate



        # Step 1: Create EC2 instance with AMI id: ami-01adb54d6fdc66a39
        ec2 = boto3.client('ec2', region_name='us-west-2')
        ec2_instance = ec2.ServiceResource.create_instances(
            ImageId='ami-01adb54d6fdc66a39',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='ec2-keypair',
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

        
        

            
            



