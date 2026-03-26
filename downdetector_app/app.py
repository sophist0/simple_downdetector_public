#!/usr/bin/env python3

import aws_cdk as cdk

from downdetector_app.detector_stack import DetectorStack

app = cdk.App()
DetectorStack(app, "DetectorStack")

app.synth()
