from aws_cdk import Stack
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_s3 as s3
import aws_cdk as cdk
from constructs import Construct


# Old DNS 13.54.216.29

class SssiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an S3 bucket called sssi.org.au with a redirect to https://geospatialcouncil.org.au
        sssi_bucket = s3.Bucket(
            self,
            "sssi.org.au.bucket",
            bucket_name="sssi.org.au",
            website_redirect=s3.RedirectTarget(
                host_name="geospatialcouncil.org.au",
                protocol=s3.RedirectProtocol.HTTPS,

            ),
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Set up an ACM certificate for sssi.org.au
        sssi_cert = acm.Certificate(
            self,
            "sssi.org.au.cert",
            domain_name="sssi.org.au",
            validation=acm.CertificateValidation.from_dns(),
        )

        # Set up cloudfront distribution for sssi.org.au
        cloudfront.CloudFrontWebDistribution(
            self,
            "sssi.org.au.distribution",
            origin_configs=[
                cloudfront.SourceConfiguration(
                    custom_origin_source=cloudfront.CustomOriginConfig(
                        domain_name=sssi_bucket.bucket_website_domain_name,
                        origin_protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
                    ),
                    behaviors=[
                        cloudfront.Behavior(
                            is_default_behavior=True
                        )
                    ],
                )
            ],
            viewer_certificate=cloudfront.ViewerCertificate.from_acm_certificate(
                certificate=sssi_cert,
                aliases=["sssi.org.au"],
            ),
            price_class=cloudfront.PriceClass.PRICE_CLASS_ALL,
            error_configurations=[
                cloudfront.CfnDistribution.CustomErrorResponseProperty(
                    error_code=404,
                    response_code=404,
                    response_page_path="/404.html",
                )
            ],
        )
