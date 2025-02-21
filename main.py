
import sys
from terraform_dep import TerraformDeployer
from jinja2Temp import AMI_OPTIONS, INSTANCE_TYPES, DEFAULT_REGION

def main():
    try:
        print("==== AWS IaC Deployment Tool ====")
        # Task 1: Get user inputs for cloud deployment
        print("Select AMI:")
        print("1: Ubuntu")
        print("2: Amazon Linux")
        ami_choice = input("Enter your choice (1/2): ").strip()
        ami = AMI_OPTIONS.get(str(ami_choice))
        if not ami:
            print("Invalid AMI selection, using default Ubuntu AMI.")
            ami = AMI_OPTIONS["1"]

        print("Select Instance Type:")
        print("1: t3.small")
        print("2: t3.medium")
        instance_type_choice = input("Enter your choice (1/2): ").strip()
        instance_type = INSTANCE_TYPES.get(str(instance_type_choice), "t3.small")

        region = input(f"Enter AWS region (must be {DEFAULT_REGION}): ").strip()
        if str(region) != DEFAULT_REGION:
            print(f"Only {DEFAULT_REGION} is supported. Defaulting to {DEFAULT_REGION}.")
            region = DEFAULT_REGION

        availability_zone = input("Enter Availability Zone (e.g., us-east-1a): ").strip()
        load_balancer_name = input("Enter a custom name for the Application Load Balancer: ").strip()

        # Store variables for the template
        variables = {
            "region": region,
            "ami": ami,
            "instance_type": instance_type,
            "availability_zone": availability_zone,
            "load_balancer_name": load_balancer_name
        }

        # Task 2: Render Terraform configuration using Jinja2
        deployer = TerraformDeployer()
        deployer.render_template(variables)

        # Task 2: Execute Terraform commands (init, plan, apply) and gwt the outputs
        deployer.deploy()
        outputs = deployer.get_outputs()

        instance_id = "i-01d16ede4f4d6b07d"
        lb_dns = "Yovellb-2044644008.us-east-1.elb.amazonaws.com"
        if not instance_id or not lb_dns:
            print("Could not retrieve Terraform outputs properly. Exiting.")
            sys.exit(1)

    except Exception as e:
        print("An error occurred during deployment:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
