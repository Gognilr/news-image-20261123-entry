// "The World Today" — Monday 23 November 2026 front page (news-image-20261123).
//
// The entry is the pre-built 1024x1024 front page in entry.png. This program
// (Node 22+, no dependencies) validates it against the competition's limits —
// PNG/JPEG magic bytes, at most 1 MiB, at most 1024x1024 — then copies it to
// $MAKEFUN_OUTPUT_DIR/entry.png (default ./out), which is what the scorer
// reads. It draws nothing: the page is composed by compose.py at build time
// from the day's verified stories and a generated hero photograph.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = fileURLToPath(new URL(".", import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "./out";
const src = join(repoDir, "entry.png");

// Read and validate the image before copying it out.
const bytes = readFileSync(src);
const isPng = bytes.length >= 8 &&
  bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e && bytes[3] === 0x47 &&
  bytes[4] === 0x0d && bytes[5] === 0x0a && bytes[6] === 0x1a && bytes[7] === 0x0a;
const isJpeg = bytes.length >= 3 &&
  bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff;
if (!isPng && !isJpeg) {
  throw new Error("entry.png is neither a PNG nor a JPEG (bad magic bytes)");
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
if (isPng) {
  // PNG IHDR: width and height are big-endian uint32 at offsets 16 and 20.
  // Those reads need at least 24 bytes; a shorter file is a truncated PNG,
  // not a validation pass — fail cleanly instead of a raw RangeError.
  if (bytes.length < 24) {
    throw new Error("entry.png is truncated (PNG shorter than the 24-byte IHDR)");
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width > 1024 || height > 1024) {
    throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
  }
} else if (isJpeg) {
  // JPEG dimensions live in the first Start-of-Frame segment (SOF0/SOF2
  // and the other SOF markers): after the 2-byte length field comes 1 byte
  // of precision, then height and width as big-endian uint16.
  const { width, height } = jpegDimensions(bytes);
  if (width > 1024 || height > 1024) {
    throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
  }
}

// Walk JPEG markers from just past SOI (FF D8) until the first SOF segment,
// returning its width and height. Throws a clear validation error on a
// malformed or truncated file instead of a raw RangeError.
function jpegDimensions(bytes: Buffer): { width: number; height: number } {
  let i = 2; // skip SOI
  while (i + 1 < bytes.length) {
    if (bytes[i] !== 0xff) {
      throw new Error("entry.png is not a valid JPEG (bad marker)");
    }
    let marker = bytes[i + 1];
    while (marker === 0xff && i + 2 < bytes.length) {
      i += 1;
      marker = bytes[i + 1];
    }
    if (marker === 0xd9) { // EOI: the image ended with no SOF segment
      throw new Error("entry.png is a JPEG with no Start-of-Frame segment");
    }
    // Standalone markers (TEM, RSTn, SOI) carry no length field.
    if (marker === 0x01 || (marker >= 0xd0 && marker <= 0xd8)) {
      i += 2;
      continue;
    }
    if (i + 3 >= bytes.length || bytes.readUInt16BE(i + 2) < 2 ||
        i + 2 + bytes.readUInt16BE(i + 2) > bytes.length) {
      throw new Error("entry.png is a truncated JPEG");
    }
    const segLen = bytes.readUInt16BE(i + 2);
    // SOF markers are 0xC0-0xCF except DHT (0xC4), JPG (0xC8), DAC (0xCC).
    const isSof = marker >= 0xc0 && marker <= 0xcf &&
      marker !== 0xc4 && marker !== 0xc8 && marker !== 0xcc;
    if (isSof) {
      if (segLen < 8) {
        throw new Error("entry.png is a truncated JPEG");
      }
      const height = bytes.readUInt16BE(i + 5);
      const width = bytes.readUInt16BE(i + 7);
      return { width, height };
    }
    if (marker === 0xda) { // SOS: scan data follows, so no SOF comes after
      throw new Error("entry.png is a JPEG with no Start-of-Frame segment");
    }
    i += 2 + segLen;
  }
  throw new Error("entry.png is a truncated JPEG");
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));

// Confirm the copy landed byte-identical to the source: a matching size
// alone would not catch a truncated or corrupted copy.
const copied = readFileSync(join(outDir, "entry.png"));
if (!copied.equals(bytes)) {
  throw new Error("copied entry.png is not byte-identical to the source");
}

console.log(`entry.png (${bytes.length} bytes) written to ${join(outDir, "entry.png")}`);
