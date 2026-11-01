TARGET=src/volt.py
TEST=src/test.volt

build: $(TARGET) $(TEST)
	@python3 $(TARGET) $(TEST) out.asm

launch:
	@echo launching $(TARGET)

package: $(TARGET)
# 	python3 -m nuitka --onefile --follow-imports $(TARGET)
	@echo building $(TARGET)

clean:
	rm -rf *.build *.dist *.onefile-build