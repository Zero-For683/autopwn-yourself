with open("yourfile.asm") as f:
    print("\n".join(
        line.split("#")[0].strip().strip('"') 
        for line in f if line.strip()
    ))