
# Simple Downdetector Setup

The following assumes a Linux development environment:

Replace the contents of `root_dir/downdetector_app/lambda_code/config.json` with the
endpoints you want to check.

In `root_dir/downdetector_app/detector_stack.py` replace AWS_ACCOUNT_EMAIL with the
email used to setup the AWS account that will run the service. In theory this should work with any email but an arbitrary email
triggers AWS's spam scanners and they deactiviate the SNS subscriptions. There are ways around this I have read, but have not tested.

Create a virtualenv and source it.
```
$ python3 -m venv .venv
```
```
$ source .venv/bin/activate
```

Install the required dependencies.
```
$ pip install -r requirements.txt
```

At this point you should be able to deploy the cdk.
```
$ cdk deploy
```

# Run Tests

In `root_dir/`
```
$ python3 -m pytest downdetector_app/lambda_code/
```