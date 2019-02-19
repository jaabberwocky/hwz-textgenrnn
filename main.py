from textgenerator import HWZScrapper
import time

tic = time.time()
t = HWZScrapper()
t.scrapeForum("https://forums.hardwarezone.com.sg/eat-drink-man-woman-16/")
toc = time.time()
print("Total time taken: %.2fs " % toc-tic)