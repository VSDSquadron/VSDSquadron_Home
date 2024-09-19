# Define variables for root path and source folders
ROOT_PATH := /home/yatharth/project_VSD/PCB/

#define Main folders

MAIN_FOLDERS := squadron_CH32\
                  squadron_GF180 \
                  squadron_MPW \
                  squadron_lattice \
                  squadron_sifive

# Define phony targets
.PHONY: all copy push push_main pull pull_main update_submodules update_submodules_main

all: copy push

copy:
	./update_linux.sh

push:
	git add .
	git commit -m "Updated production folders"
	git push
	@echo "Changes pushed successfully."

push_main:
	$(foreach folder, $(MAIN_FOLDERS), \
		cd $(ROOT_PATH)$(folder); \
		git add .; \
		git commit -m "Updated $(folder)"; \
		git push; \
		cd $(ROOT_PATH); \
	)
	@echo "Main folders pushed successfully."

pull: 
	git pull
	@echo "Changes pulled successfully."

pull_main:
	$(foreach folder, $(MAIN_FOLDERS), \
		cd $(ROOT_PATH)$(folder); \
		git pull; \
		cd $(ROOT_PATH); \
	)
	@echo "Main folders pulled successfully."

update_submodules_main:
	$(foreach folder, $(MAIN_FOLDERS), \
		cd $(ROOT_PATH)$(folder); \
		git submodule update --remote; \
		cd $(ROOT_PATH); \
	)
	@echo "Submodules in main folders updated successfully."

image:
	./update_image.sh
