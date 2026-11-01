PROCESSOR=python3

SCRIPT=src/volt.py
SOURCE=src/test.volt
OUTPUT=out/out

build: $(SCRIPT)
# 	$(PROCESSOR) -m nuitka --onefile --follow-imports $(SCRIPT)
	@echo building $(SCRIPT) 

assemble: $(SCRIPT) $(SOURCE)
	@echo compiling
	$(PROCESSOR) $(SCRIPT) $(SOURCE) $(OUTPUT).asm

compile: assemble
	nasm -felf64 $(OUTPUT).asm
	ld -o $(OUTPUT) $(OUTPUT).o

clean:
	rm -rf *.build *.dist *.onefile-build