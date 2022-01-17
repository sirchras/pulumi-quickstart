import pulumi
from pulumi_aws import s3

# create resources
bucket = s3.Bucket(
  'my-bucket',
  website=s3.BucketWebsiteArgs(
    index_document='index.html'
  )
)

bucket_object = s3.BucketObject(
  'index.html',
  acl='public-read',
  content_type='text/html',
  bucket=bucket.id,
  source=pulumi.FileAsset('index.html')
)

# exports
pulumi.export('bucket_name', bucket.id)
pulumi.export('bucket_endpoint', pulumi.Output.concat('http://', bucket.website_endpoint))
