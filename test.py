import os

# Iterate for each dict object in os.walk()
for root, dirs, files in os.walk("/home/csanta/lili-asr/dataset/test/"):
        print(files)