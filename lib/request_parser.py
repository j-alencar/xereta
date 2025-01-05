from urllib.parse import urlparse

def parse_filename(request):
    parsed_url = urlparse(request.url)
    path = parsed_url.path
    return path.split('/')[-1] if '/' in path else path
    