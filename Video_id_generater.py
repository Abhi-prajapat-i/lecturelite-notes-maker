from urllib.parse import urlparse,parse_qs

def get_id(url):
    parsed_url = urlparse(url)

    if parsed_url.hostname in ["youtu.be", "www.youtu.be"]:
        return parsed_url.path.strip("/").split("/")[0]

    if parsed_url.hostname in ["youtube.com", "www.youtube.com", "m.youtube.com"]:
        return parse_qs(parsed_url.query).get("v",[None])[0]
    return None


if __name__ == "__main__":
    print(get_id("https://youtu.be/J5_-l7WIO_w"))