#!/usr/bin/env python3

import aws_cdk as cdk

from sssi.sssi_stack import SssiStack

app = cdk.App()
SssiStack(app, "SssiStack")

app.synth()
