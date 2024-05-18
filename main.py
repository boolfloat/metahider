import crypto

class FM:
  red = '\x1b[31m'
  green = '\x1b[32m'
  blue = '\x1b[34m'
  reset = '\x1b[0m'


print(f"{FM.blue}${FM.reset} {FM.red}Metahider{FM.reset} by strainxx/boolfloat")

def inject_meta(s_name="sample.mp3"):
  with open(s_name, "rb") as f:
    idver = f.read(3)
    maj_ver = f.read(1)
    min_ver = f.read(1)
    flags = f.read(1)
    size = f.read(4)
    i_size = int.from_bytes(size)
    id3_data=f.read(i_size)
    print("\t-- Meta tag:", idver.decode())
    print("\t-- Version:", "0x"+maj_ver.hex(), "0x"+min_ver.hex()) # 0x04 0x00 indicates a 2.4.0 tag
    print("\t-- Size:", i_size)
    print("--DATA--\n"+id3_data.decode(errors="ignore"),"\n--DATA END--")

    mp3 = f.read()
    
    if not "ID3" in idver.decode():
      print(f"{FM.red}Critical exception{FM.reset}:\n\tnot ID3vX metadata!")
      raise NotImplementedError
    with open("generated.mp3", "wb") as out:
      out.write(idver)
      out.write(maj_ver)
      out.write(min_ver)
      out.write(flags)

      with open(input(f"({FM.blue}mp3/Inject{FM.reset}) {FM.red}${FM.reset} Enter inject file name: "), "rb") as r_in:
        inj_data = crypto.magic+crypto.xor_encrypt_decrypt(r_in.read(),crypto.zlib.crc32(mp3).to_bytes(4))
        inj_len = len(inj_data)

      out.write(int.to_bytes(i_size+inj_len, 4))
      out.write(id3_data)
      out.write(inj_data)
      out.write(mp3)
  # print(f.read(344064))

def decode_meta(s_name="generated.mp3"):
  with open(s_name, "rb") as f:
    idver = f.read(3)
    maj_ver = f.read(1)
    min_ver = f.read(1)
    flags = f.read(1)
    size = f.read(4)
    i_size = int.from_bytes(size)
    id3_data=f.read(i_size)
    print("\t-- Meta tag:", idver.decode())
    print("\t-- Version:", "0x"+maj_ver.hex(), "0x"+min_ver.hex()) # 0x04 0x00 indicates a 2.4.0 tag
    print("\t-- Size:", i_size)
    header_data = id3_data.decode(errors="ignore")
    # print("--DATA--\n"+header_data,"\n--DATA END--")

    mp3 = f.read()
    
    if not "ID3" in idver.decode():
      print(f"{FM.red}Critical exception{FM.reset}:\n\tnot ID3vX metadata!")
      raise NotImplementedError
    
    encrypted = id3_data.split(crypto.magic, 1)[1]
    # print("Encrypted data:", encrypted)
    with open(input(f"({FM.blue}mp3/Decode{FM.reset}) {FM.red}${FM.reset} Enter output name: "), "wb") as out:
      print("Decrypting...")
      out.write(crypto.xor_encrypt_decrypt(encrypted, crypto.zlib.crc32(mp3).to_bytes(4)))


if __name__=="__main__":
  print("\n1 - Inject file to audio metadata\n2 - Decode file from audio metadata\n")
  choice = input(f"{FM.red}${FM.reset} Enter choice: ")
  if choice == "1":
    inject_meta(input(f"({FM.blue}mp3/Inject{FM.reset}) {FM.red}${FM.reset} Enter mp3 name: "))
  if choice == "2":
    decode_meta(input(f"({FM.blue}mp3/Decode{FM.reset}) {FM.red}${FM.reset} Enter mp3 name: "))