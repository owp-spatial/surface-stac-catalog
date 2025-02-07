class S3Bucket:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.prefixes = []  

    def get_prefixes(self):
        return self.prefixes
    def get_relative_prefixes(self):
        rel_prefixes = []
        for prefix in self.prefixes:
            dir_names = prefix.replace(self.bucket_name, "").replace("s3://", "").split("/")
            rel_prefixes.append("/".join([i for i in dir_names if i]))
        # return [i.replace(self.bucket_name, "").replace("s3://", "").split("/") for i in self.prefixes]
        return rel_prefixes

    def add_prefix(self, *prefix_parts):
        """Add a new prefix to the bucket."""
        prefix = self._build_s3_path(*prefix_parts)
        if prefix not in self.prefixes:
            self.prefixes.append(prefix)

    def remove_prefix(self, *prefix_parts):
        """Remove a prefix from the bucket."""
        prefix = self._build_s3_path(*prefix_parts)
        if prefix in self.prefixes:
            self.prefixes.remove(prefix)

    def _build_s3_path(self, *parts) -> str:
        """Build the S3 path based on the prefix parts."""
        base_path = f"s3://{self.bucket_name}"
        return f"{base_path}/{'/'.join(parts)}" if parts else base_path

    def get_uri(self, *prefix_parts) -> str:
        """Generate the URI for a given prefix."""
        return self._build_s3_path(*prefix_parts)

    def __repr__(self):
        return f"S3Bucket(bucket_name='{self.bucket_name}', prefixes={self.prefixes})"

# s3_bucket = S3Bucket(OWP_SPATIAL_S3_BUCKET_NAME)
# s3_bucket.add_prefix("surface", "nws-ehydro")
# s3_bucket.add_prefix("surface", "nws-nos-surveys")
# s3_bucket.add_prefix("surface", "nws-topobathy")

# s3_bucket.get_prefixes()
# s3_bucket.get_relative_prefixes()

# s3_bucket.get_uri("surface", "nws-ehydro", "catalog.json")