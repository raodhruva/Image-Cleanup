# Image-Cleanup
Modified Iterative-DFS algorithm for cleaning up imperfect scanned images pixel by pixel

Created to remove imperfections from scanned images. Imperfections for the purpose of this program are defined as blemishes or light hue pixels that are usually at the fringes of images. These imperfections will be removed by converting these pixels to white.

An DFS algorithm is used to traverse through all the pixels. An iterative DFS has been implemented instead of a recursive DFS as the recursion depth is too much otherwise.
The idea is that whenever there is a pixel with a light hue (a potentially problematic pixel) the iterator creates an island of such neighbouring potentially problematic pixels. All such islands are stored.

The final step is to perfom a check on the islands to make sure we dont actually remove pixels that we care about. This is done by choosing a random subset of pixels from each island and stepping in each direction on the island until a pixel of different nature is reached. The pixel of different nature can be one of 2 types, a dark pixel or a white pixel.
If the pixel is a white pixel we are probably at the edge of the scanned image. The island is probably an imperfection and is safe to be removed. This can be done if the test pixel encounteres a white pixel in any direction.
The other case is when the test pixel encounters a black pixel in every direction. In this case, we probably accidently created an island for removal that we shouldnt have. This is because if an island is enclosed by dark pixels on every side it was probably on purpose.
