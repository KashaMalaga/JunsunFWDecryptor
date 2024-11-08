import os
import mmap
import hashlib

def mmap_file(file_path, access=mmap.ACCESS_READ):
    """Opens a file and maps it to memory."""
    try:
        with open(file_path, "r+b") as f:
            st = os.stat(file_path)
            addr = mmap.mmap(f.fileno(), st.st_size, access=access)
            return addr
    except Exception as e:
        print(f"Error mapping file: {e}")
        return None


def munmap_file(addr):
    """Unmaps a file from memory."""
    try:
        addr.close()
    except Exception as e:
        print(f"Error unmapping file: {e}")


def calculate_hash(file_path):
    """Calculates the MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def main():
    """Repacks extracted partitions into a ForFan .bin firmware file."""
    print(
        "KshMlg .upd Junsun Repacker with Fixed with Order and Flags"
    )
    output_file = "8667.bin"
    input_dir = "out"
    partition_names = [
        "super.img", "recovery.img", "md1img.img", "logo.bin", "spmfw.img",
        "scp.img", "scp.img",  # Duplicate scp.img
        "sspm.img", "sspm.img",  # Duplicate sspm.img
        "lk.img", "lk.img",  # Duplicate lk.img
        "boot.img", "dtbo.img", "tee.img", "tee.img"  # Duplicate tee.img
    ]

    with open(output_file, "wb") as outfile:
        # Write initial total size (placeholder, will be updated later)
        outfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00")

        # Write partition table (placeholder, will be updated later)
        outfile.seek(0x908)
        for _ in range(15):
            outfile.write(b"\x00" * 0x48)

        current_offset = 0x908
        partition_table = []
        for i, partition_name in enumerate(partition_names):
            partition_path = os.path.join(input_dir, partition_name)
            if os.path.exists(partition_path):
                partition_size = os.path.getsize(partition_path)

                # Write partition data
                outfile.seek(current_offset)  # Set the correct offset before writing
                with open(partition_path, "rb") as infile:
                    outfile.write(infile.read())
            else:
                partition_size = 0  # If the partition file doesn't exist, set size to 0

            # Prepare partition table entry
            partition_table.append({
                "file_name":
                partition_name.encode('utf-8'),
                "name":
                partition_name.split('.')[0].encode('utf-8'),
                "size":
                partition_size,
                "flags":
                0x01000000 if partition_name == "super.img" else 0x00000000,
                "offset":
                current_offset
            })

            current_offset += partition_size  # Update offset for the next partition

        # Update total size
        total_size = current_offset
        outfile.seek(0)
        outfile.write(total_size.to_bytes(8, byteorder='big'))

        # Write partition table
        outfile.seek(0x908)
        for i, entry in enumerate(partition_table):
            base = 0x08 + (i * 0x48)
            outfile.seek(base)
            outfile.write(entry["file_name"].ljust(0x30, b"\x00"))
            outfile.write(entry["name"].ljust(0x10, b"\x00"))
            outfile.write(entry["size"].to_bytes(4, byteorder='big'))
            outfile.write(entry["flags"].to_bytes(4, byteorder='big'))

    # Calculate and print hash
    md5_hash = calculate_hash(output_file)
    print(f"Generated hash for {output_file}: {md5_hash}")

    # Save hash to .upd file
    upd_file = output_file.replace(".bin", ".upd")
    with open(upd_file, "w") as f:
        f.write(md5_hash)


if __name__ == "__main__":
    main()