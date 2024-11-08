import os
import mmap

def mmap_file(file_path):
  """Opens a file and maps it to memory."""
  try:
    with open(file_path, "r+b") as f:  # Open in binary read-write mode
      st = os.stat(file_path)
      addr = mmap.mmap(f.fileno(), st.st_size, access=mmap.ACCESS_READ)
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

def write_to_file(buf, len, file_path):
  """Writes data to a file."""
  try:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
      f.write(buf)
  except Exception as e:
    print(f"Error writing to file: {e}")

def main():
  """Extracts partitions from a KshMlg .upd firmware file."""
  print("KshMlg .upd Junsun extractor with Fixed with Offsets")
  file_path = "8667.bin"  # Replace with your firmware file path and name in case its another radio type
  print("Replace with your firmware file path and name, right now using: "+file_path)
  addr = mmap_file(file_path)
  if addr is None:
    return 1

  total_size = int.from_bytes(addr[:8], byteorder='big')
  print(f"Total size: {total_size} bytes")
  print("\nPartitions:")

  current_offset = 0x908
  for i in range(15):
    base = 0x08 + (i * 0x48)
    file_name = addr[base:base+0x30].decode('utf-8').rstrip('\x00')
    name = addr[base+0x30:base+0x40].decode('utf-8').rstrip('\x00')
    size = int.from_bytes(addr[base+0x40:base+0x44], byteorder='big')
    flags = int.from_bytes(addr[base+0x44:base+0x48], byteorder='big')
    print(f"{name}: {file_name} ({size} bytes), flags: 0x{flags:08X}, offset: 0x{current_offset:X}")

    # Even if size is 0, create an empty file
    out_file_path = os.path.join("out", file_name)
    write_to_file(addr[current_offset:current_offset+size], size, out_file_path)

    current_offset += size  # Update the offset correctly

  munmap_file(addr)
  return 0

if __name__ == "__main__":
  main()
