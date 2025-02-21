
import os
import sys
from jinja2 import Template
from python_terraform import Terraform, IsFlagged, TerraformCommandError
from jinja2Temp import TF_DIR, TF_FILE, terraform_template

class TerraformDeployer:
    def __init__(self):
        self.tf_dir = TF_DIR
        self.tf_file = TF_FILE
        self.tf = Terraform(working_dir=self.tf_dir)

    def render_template(self, variables):
        """Render the Jinja2 template with variables and write the Terraform file."""
        try:
            os.makedirs(self.tf_dir, exist_ok=True)
            template = Template(terraform_template)
            rendered = template.render(**variables)
            with open(self.tf_file, "w") as f:
                f.write(rendered)
            print(f"Terraform configuration written to {self.tf_file}")
        except Exception as e:
            print("Error rendering template:", e)
            sys.exit(1)

    def deploy(self):
        """Execute terraform init, plan, and apply."""
        try:
            print("Initializing Terraform...")
            return_code, stdout, stderr = self.tf.init(capture_output=True)
            if return_code != 0:
                raise TerraformCommandError("init", return_code, stdout, stderr)

            print("Planning Terraform deployment...")
            return_code, plan_stdout, _ = self.tf.plan(no_color=IsFlagged, capture_output=True)
            if return_code != 0:
                raise TerraformCommandError("plan", return_code, plan_stdout, "")

            print("Applying Terraform deployment...")
            return_code, apply_stdout, _ = self.tf.apply(skip_plan=True, capture_output=True)
            if return_code != 0:
                raise TerraformCommandError("apply", return_code, apply_stdout, "")
            print("Terraform applied successfully.")
        except TerraformCommandError as tce:
            print(f"Terraform command '{tce.cmd}' failed with error:")
            print(tce)
            sys.exit(1)

    def get_outputs(self):
        """Retrieve Terraform outputs."""
        try:
            outputs = self.tf.output()
            print("Terraform Outputs:", outputs)
            return outputs
        except Exception as e:
            print("Error retrieving Terraform outputs:", e)
            sys.exit(1)

