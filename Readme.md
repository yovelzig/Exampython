# AWS IaC Deployment Tool


## How to Run

1. **User Input:**
    - the script ask the user for the requested input and then use in inside the template . with this input we create the main.tf file and then we run the terraform init, terraform plan, terraform apply.
    this command will give us the required load balancer and the required outputs.

## How to Run
    - you need to install python-terraform and boto3 run the main.py it will use the jinja2Temp and terraform_dep calsses 
      then you get from the template the main.tf file into terrform_deployment directory navigate to this directory and execute the terraform init , terraform plan , terraform apply and you will get the id and the dns name i save my on the output.txt file in my git.


2. **Installation:**
   - Install Python dependencies:
     install jinja2 python-terraform boto3


