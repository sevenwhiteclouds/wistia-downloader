import requests

if __name__ == "__main__":
  file = input("Enter file name: ")

  with open(file, "r", encoding="utf-8") as file_open:
    lines = file_open.readlines()
