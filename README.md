This is an arithmetic compressor I built from scratch. I was inspired after watching [this](https://www.youtube.com/user/jakobfoerster) lecture series on information theory out of the University of Cambridge.


Right now, the compressor and decompressor are together, back-to-back, for simplicity. Seperating them would make a more water-tight case that this compression, in fact, works.


Problem: For some reason, this compressor is not compressing down to the theoretical limit (within 2 bits of the entropy). I'm using the concepts I saw in the lecture. The compressor maps my message to a range inside 0 and 1, converts that to a binary range, and then converts that to a string. The decompressor turns that string into a binary range, then turns that range into the original message.


With two charachters, with p rates of (0.10,0.90), the entropy is around 0.47. However, I'm getting rates closer to 0.62. Any ideas on why I'm not getting optimal compression are welcome!


Thanks! Your math enthusiast,


Ben Tupper