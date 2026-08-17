OUT_DIR=$HOME/lav/siti/spiega/a/
# Using GNU Make-specific functions here
FILES=$(patsubst %.org,$(OUT_DIR)/%.html,$(wildcard *.org))

.PHONY: all clean install-doc

all: install-doc

install-doc: $(OUT_DIR) $(FILES)

$(OUT_DIR):
        mkdir -v -p $(OUT_DIR)

%.html: %.org
        emacs $< --batch -f org-html-export-to-html--kill

$(OUT_DIR)/%.html: %.html
        install -v -m 644 -t $(OUT_DIR) $<
        rm $<

clean:
        rm *.html
