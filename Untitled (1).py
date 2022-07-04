%region ap-southeast-2

%profile default

%iam_role arn:aws:iam::*******:role/glueServiceRole

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

glueContext = GlueContext(SparkContext.getOrCreate())

test_dynamicframe = glueContext.create_dynamic_frame.from_options(
    's3',
    {'paths': ['s3://bt-test-bck/input']},
    'csv',
    {'withHeader': True})
print("Count:",test_dynamicframe.count())
test_dynamicframe.printSchema()

%stop_session


