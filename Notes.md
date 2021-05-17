# About Images

* All digital images are also known as raster image. 
* Raster images are images that consists of pixels.

## Types of images

Three types of image :-

* Logical(Binary) - Has 1 byte per pixel where each byte stores either 0(Black) or 255(White).
* Grayscale - Has 1 byte per pixel. Each pixel can store either 0(Black), 1-254(Grey or its shade) or 255(White).
* RGB - Has 3 bytes per pixel. Each byte has RGB value i.e. Red, Green and Blue. We can make any color using any of these 3.

## Unlocking PNG Format :-

# Structure

* File Header: A PNG file starts with an 8-byte signature. The first eight bytes of a PNG file always contain the following (decimal) values `137 80 78 71 13 10 26 10`. This signature indicates that the remainder of the file contains a single PNG image, consisting of a series of chunks beginning with an IHDR chunk and ending with an IEND chunk. These 8 bits are represent the following info -

| Values (hex) | Purpose |
|------------|-------|
| `89` | Has the high bit set to detect transmission systems that do not support 8-bit data and to reduce the chance that a text file is mistakenly interpreted as a PNG, or vice versa. |
|`50 4E 47`| In ASCII, the letters PNG, allowing a person to identify the format easily if it is viewed in a text editor.|
|`0D 0A`|A DOS-style line ending (CRLF) to detect DOS-Unix line ending conversion of the data.|
|`1A`|A byte that stops display of the file under DOS when the command type has been used—the end-of-file character.|
|`0A`|A Unix-style line ending (LF) to detect Unix-DOS line ending conversion|

* Chunks: After the header, comes a series of chunks, each of which conveys certain information about the image. A chunk consists of four parts -

	* length (4 bytes, big-endian)

	* chunk type/name (4 bytes)

	* chunk data (length bytes)

	* CRC (cyclic redundancy code/checksum; 4 bytes). The CRC can be used to check for corruption of the data. It is calculated on the preceding bytes in the chunk, including the chunk type field and the chunk data fields, but not including the length field.

*  Critical Chunks: A decoder must be able to interpret critical chunks to read and render a PNG file.

	* IHDR must be the first chunk; it contains (in this order) the image's - 
		* width (4 bytes)
		* height (4 bytes)
		* bit depth (1 byte, values 1, 2, 4, 8, or 16). Bit depth is defined as the number of bits per sample or per palette index (not per pixel).
		* color type (1 byte, values 0, 2, 3, 4, or 6)
		* compression method (1 byte, value 0)
		* filter method (1 byte, value 0)
		* and interlace method (1 byte, values 0 "no interlace" or 1 "Adam7 interlace") (13 data bytes total).

	* PLTE contains the palette: a list of colors.

	* IDAT contains the image, which may be split among multiple IDAT chunks. Such splitting increases filesize slightly, but makes it possible to generate a PNG in a streaming manner. The IDAT chunk `contains the actual image data`, which is the output stream of the compression algorithm.

	* IEND marks the image end; the data field of the IEND chunk has 0 bytes/is empty.

	* The PLTE chunk is essential for color type 3 (indexed color). It is optional for color types 2 and 6 (truecolor and truecolor with alpha) and it must not appear for color types 0 and 4 (grayscale and grayscale with alpha).

<centre><b>Note that all integer fields in the PNG file format are stored in big endian order, that is, most significant byte first.</b><centre>
## Filters
There are various filter algorithms that can be applied before compression. The purpose of these filters is to prepare the image data for optimum compression.
PNG filter method 0 defines five basic filter types:
   Type    Name
   
   0       None
   1       Sub
   2       Up
   3       Average
   4       Paeth
(Note that filter method 0 in IHDR specifies exactly this set of five filter types. If the set of filter types is ever extended, a different filter method number will be assigned to the extended set, so that decoders need not decompress the data to discover that it contains unsupported filter types.)
The encoder can choose which of these filter algorithms to apply on a scanline-by-scanline basis. In the image data sent to the compression step, each scanline is preceded by a filter type byte that specifies the filter algorithm used for that scanline.
* `Filtering algorithms are applied to bytes, not to pixels, regardless of the bit depth or color type of the image`
* `PNG imposes no restriction on which filter types can be applied to an image. However, the filters are not equally effective on all types of data.`

|Type|Name|Filter Function|Reconstruction Function|
|----|----|-------------|--------------------|
|0|None|Filt(x) = Orig(x)|Recon(x) = Filt(x)|
|1|Sub|Filt(x) = Orig(x) - Orig(a)|Recon(x) = Filt(x) + Recon(a)|
|2|Up|Filt(x) = Orig(x) - Orig(b)|Recon(x) = Filt(x) + Recon(b)|
|3|Average|Filt(x) = Orig(x) - floor((Orig(a) + Orig(b)) / 2)|Recon(x) = Filt(x) + floor((Recon(a) + Recon(b)) / 2)|
|4|Path|Filt(x) = Orig(x) - PaethPredictor(Orig(a), Orig(b), Orig(c))|Recon(x) = Filt(x) + PaethPredictor(Recon(a), Recon(b), Recon(c))|

