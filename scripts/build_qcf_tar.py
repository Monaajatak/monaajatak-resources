"""Builds a byte-reproducible ustar archive of the 604 QCF v4 page fonts.

Usage: python3 build_qcf_tar.py <fonts_dir> <out.tar>

Every header field that could vary between machines (mtime, owner, mode,
order) is fixed, so the same font files always produce the same sha256.
"""
import io
import os
import re
import sys
import tarfile

NAME = re.compile(r"^QCF4(\d{3})_X-Regular\.woff$")


def main(src: str, out: str) -> None:
    names = sorted(n for n in os.listdir(src) if NAME.match(n))
    pages = sorted(int(NAME.match(n).group(1)) for n in names)
    if pages != list(range(1, 605)):
        sys.exit(f"expected pages 1..604, found {len(pages)} files")

    with tarfile.open(out, "w", format=tarfile.USTAR_FORMAT) as tar:
        for name in names:
            with open(os.path.join(src, name), "rb") as f:
                data = f.read()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mtime = 0
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tar.addfile(info, io.BytesIO(data))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
