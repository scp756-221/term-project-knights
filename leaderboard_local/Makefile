# Makefile for standalone Music service (l1)

VER=v0.25
HOST_DIR=$(HWD)/leaderboard

# this is needed to switch M1 Mac to x86 for compatibility with x86 instances/students
ARCH=--platform x86_64

build-l1:
	docker image build $(ARCH) -f Dockerfile --build-arg EXERARG=$(VER) --build-arg ASSIGN=$(ASSIGN) -t leaderboard:$(VER) .

run-l1:
	docker container run $(ARCH) -it --rm -p 30001:30001 -v $(HOST_DIR):/data --name l1 leaderboard:$(VER)

# Run the container in detached mode and retain its logs---mostly used for testing
run-l1-detached:
	docker container run $(ARCH) -d  --rm -p 30001:30001 -v $(HOST_DIR):/data --name l1 leaderboard:$(VER)

# Run with different port and volume mappings to demonstrate container mappings
# HOWEVER, if the client is running from another container connecting to this over the bridge
# network, it will use port 30001.  The host port mapping (20000) only is visible to clients
# running in the host OS, while containers use the container mapping (30001).
run-l1-odd:
	docker container run $(ARCH) -it --rm -p 20000:30001 -v $(HOST_DIR)/odd:/data --name l1-odd leaderboard:$(VER)

# Build an l1 image with one copy of a file of random bytes
build-l1-1-file:
	docker image build $(ARCH) -f l1-1-file-Dockerfile --build-arg EXERARG=$(VER) --build-arg ASSIGN=$(ASSIGN) -t l1-1-file:$(VER) .

# Build an l1 image with two copies of a file of random bytes
build-l1-2-files:
	docker image build $(ARCH) -f l1-2-files-Dockerfile --build-arg EXERARG=$(VER) --build-arg ASSIGN=$(ASSIGN) -t l1-2-files:$(VER) .

# Build an entirely self-contained image of l1, including the music entries
build-l1-self:
	docker image build $(ARCH) -f self-Dockerfile --build-arg EXERARG=$(VER) --build-arg ASSIGN=$(ASSIGN) -t l1-self-contained:$(VER) .
