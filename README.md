# Nexus3 upload artifact V1

This action uploads files using post to [Sonatype Nexus3 repository manager](https://www.sonatype.com/products/sonatype-nexus-repository) RAW and APT repositories

# Usage

```yaml
- uses: astertom/nexus-upload-artifact@v1
  env:
      NEXUS_HOST_URL: <Nexus3 RM URL>
      NEXUS_USER: <Nexus3 RM User>
      NEXUS_TOKEN: <Nexus3 RM User Password>
  with:
      pattern: <Pattern for searching files>
      repositories: <Comma separated list of Nexus3 RM repositories names>
      directory: <Subdirectory for search in GITHUB_WORSPACE (without leading slash)> Optional
      timeout: <Timeout for single file upload> Optional
```

# Example RAW repositories

```yaml
- uses: astertom/nexus-upload-artifact@v1
  env:
      NEXUS_HOST_URL: http://localhost:8081
      NEXUS_USER: ${{ secrects.NEXUS_USER }}
      NEXUS_TOKEN: ${{ secrets.NEXUS_PASSWORD }}
  with:
      pattern: "*.log"
      repositories: "rawrepo1, rawrepo2"
```

# Example APT repository

```yaml
- uses: astertom/nexus-upload-artifact@v1
  env:
      NEXUS_HOST_URL: http://localhost:8081
      NEXUS_USER: ${{ secrects.NEXUS_USER }}
      NEXUS_TOKEN: ${{ secrets.NEXUS_PASSWORD }}
  with:
      pattern: "*.deb"
      repositories: aptrepo1
```
