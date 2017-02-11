Here is an arithmetic compressor/decompressor and a symbolic compressor/decompressor. I built both from scratch. I was inspired after watching [this](https://www.youtube.com/user/jakobfoerster) lecture series on information theory out of the University of Cambridge.


Right now, the compressors and decompressors are together, back-to-back, for simplicity. Seperating them would make a more water-tight case that this compression, in fact, works.


Problem: For some reason, the arithmetic compressor is not compressing down to the theoretical limit (within 2 bits of the entropy). I'm using the concepts I saw in the lecture. The compressor maps my message to a range inside 0 and 1, converts that to a binary range, and then converts that to a string. The decompressor turns that string into a binary range, then turns that range into the original message.


With two charachters, with p rates of (0.10,0.90), the entropy is around 0.47. However, I'm getting rates closer to 0.62. Any ideas on why I'm not getting optimal compression are welcome!

The symbolic compressor is, admittedly, not the ideal kind of compression, since it does not compress down to the theoretical limit of the entropy (or the Shannon Information Content). Still, ironically, it compresses better than my arithmetic compressor. Since it's a much simpler idea that I invented before hearing any outside input, I believe the code is cleaner. 


Thanks! Your math enthusiast,


Ben Tupper