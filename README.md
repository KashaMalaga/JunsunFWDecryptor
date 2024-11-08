# JunsunFWDecryptor
 This tools allow us to unpack/pack the whole fw from Junsun radios

Usage: Paste the 8667.upd and 8667.bin in the same path as the python code.
Execution sample log below, but at the end an out folder would be created with a super.img unpacked.

KshMlg .upd Junsun extractor with Fixed with Offsets
Replace with your firmware file path and name, right now using: 8667.bin
Total size: 8676807237638815744 bytes

Partitions:
super: super.img (4168590055 bytes), flags: 0x01000000, offset: 0x908
recovery: recovery.img (2 bytes), flags: 0x00000000, offset: 0xF877ABEF
md1img: md1img.img (0 bytes), flags: 0x00000000, offset: 0xF877ABF1
logo: logo.bin (0 bytes), flags: 0x00000000, offset: 0xF877ABF1
spmfw: spmfw.img (2428502016 bytes), flags: 0x00000000, offset: 0xF877ABF1
scp1: scp.img (3763865600 bytes), flags: 0x00000000, offset: 0x18937ABF1
scp2: scp.img (3763865600 bytes), flags: 0x00000000, offset: 0x2698FB3F1
sspm_1: sspm.img (2427520768 bytes), flags: 0x00000000, offset: 0x349E7BBF1
sspm_2: sspm.img (2427520768 bytes), flags: 0x00000000, offset: 0x3DA98C2F1
lk: lk.img (2148144896 bytes), flags: 0x00000000, offset: 0x46B49C9F1
lk2: lk.img (2148144896 bytes), flags: 0x00000000, offset: 0x4EB53E0F1
boot: boot.img (2 bytes), flags: 0x00000000, offset: 0x56B5DF7F1
dtbo: dtbo.img (32768 bytes), flags: 0x00000000, offset: 0x56B5DF7F3
tee1: tee.img (1895039232 bytes), flags: 0x00000000, offset: 0x56B5E77F3
tee2: tee.img (1895039232 bytes), flags: 0x00000000, offset: 0x5DC5278F3

Next steps, conversion from img to raw partition and later extract the raw one with this commands.
brew install simg2img
simg2img super.img super.raw
http://newandroidbook.com/tools/imjtool
xattr -d com.apple.quarantine imjtool
chmod 777 imjtool
./imjtool super.raw extract

Log:
MMapped: 0x300000000, imgMeta 0x300001000
liblp dynamic partition (super.img) - Blocksize 0x1000, 2 slots
LP MD Header @0x3000, version 10.0, with 3 logical partitions @0x0 on block device of 4096 GB, at partition super, first sector: 0x800
Partitions @0x3080 in 2 groups:
        Group 0: default
        Group 1: main
                Name: product (read-only, Unknown, @0x100000 spanning 1 extents of 235 MB) - extracted
                Name: system (read-only, Unknown, @0xed00000 spanning 1 extents of 2 GB) - extracted
                Name: vendor (read-only, Unknown, @0x92f00000 spanning 1 extents of 1 GB) - extracted


Repacker usage:
Execute with an existing out folder containing all the images, will generate a new .bin file and also his own .upd hash to be flash into the radio