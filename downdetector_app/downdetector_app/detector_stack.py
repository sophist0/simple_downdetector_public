
from constructs import Construct
from aws_cdk import RemovalPolicy
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_events as events,
    aws_events_targets as targets,
    Duration
)
from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion

import aws_cdk.aws_cloudwatch as cloudwatch
import aws_cdk.aws_logs as logs

from aws_cdk.aws_sns import Topic
from aws_cdk.aws_sns_subscriptions import EmailSubscription
from aws_cdk.aws_cloudwatch_actions import SnsAction

class DetectorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        helper_layer = PythonLayerVersion(
            self,
            'HelperLayer',
            entry='lambda_layer',
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_12],
            description='A layer for Python libraries',
            removal_policy=RemovalPolicy.DESTROY
        )

        lambda_function = lambda_.Function(
            self,
            "MyFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda_code"),
            layers=[helper_layer]
        )

        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.rate(Duration.minutes(60)),
        )

        rule.add_target(targets.LambdaFunction(lambda_function))

        ### Monitoring ###

        lambda_error_metric = lambda_function.metric("Errors")
        lambda_error_alarm = cloudwatch.Alarm(self, "LambdaErrorAlarm",
            metric=lambda_error_metric,
            threshold=0.5,
            evaluation_periods=1,
            datapoints_to_alarm=1
        )

        lambda_log_group = lambda_function.log_group
        generic_endpoint_failed_filter = logs.MetricFilter(self, "GenericEndpointCheckFailed",
            log_group=lambda_log_group,
            filter_pattern=logs.FilterPattern.all_terms("End points check failed!"),
            metric_namespace="EndpointCheckFailed",
            metric_name="ErrorCount",
            metric_value="1",
        )
        generic_endpoint_alarm = cloudwatch.Alarm(self, "GenericEndpointAlarm",
            metric=generic_endpoint_failed_filter.metric(),
            threshold=0.5,
            evaluation_periods=1,
            datapoints_to_alarm=1
        )

        failed_lambda_topic = Topic(self, "AlarmFailedLambdaTopic",
            display_name="Failed Lambda Alarm Notification"
        )
        failed_endpoint_check_topic = Topic(self, "AlarmFailedEndpointCheckTopic",
            display_name="Failed Endpoint Check Alarm Notification"
        )

        email_address = "AWS_ACCOUNT_EMAIL"
        failed_lambda_topic.add_subscription(
            EmailSubscription(email_address)
        )
        failed_endpoint_check_topic.add_subscription(
            EmailSubscription(email_address)
        )

        lambda_error_alarm.add_alarm_action(SnsAction(failed_lambda_topic))
        generic_endpoint_alarm.add_alarm_action(SnsAction(failed_endpoint_check_topic))
