from src.sha256 import calculate_sha256


if __name__ == '__main__':
    message = b'new kossher'
    print(calculate_sha256(message))
