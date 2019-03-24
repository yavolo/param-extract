# param-extract
White box testing script to try all web paramters found in backend code.

Crafted URIs can be checked for reflection directly or sent to your local burp proxy on `127.0.0.1:8080`

## Usage:
`python3 param-extract.py <wwwroot> <website> <payload>`

## Example:
`python3 param-extract.py "/home/oliver/misc/website" "http://example.com" "<script>alert(1)</script>"`

